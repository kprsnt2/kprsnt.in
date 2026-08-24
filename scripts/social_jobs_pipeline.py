import os
import json
import logging
import requests
from datetime import datetime, timedelta

# ==============================================================================
# CONFIGURATION
# ==============================================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

JOB_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "job_data", "recent.json")
LOG_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "job_data", "pipeline_log.json")

# ==============================================================================
# AGENT 1: RESEARCH AGENT
# ==============================================================================
def run_research_agent():
    """
    Agent 1: Scours social media (via Tavily) and remote job APIs (like Venuerra)
    to find recent AI/Data engineering jobs in the last 24 hours.
    """
    logging.info("Starting Research Agent...")
    jobs = []
    
    # 1. Fetch from Social Media via Tavily
    if TAVILY_API_KEY:
        social_queries = [
            "hiring 'AI Engineer' OR 'Machine Learning Engineer' site:x.com",
            "hiring 'Data Analyst' OR 'Data Engineer' site:reddit.com",
        ]
        
        for query in social_queries:
            logging.info(f"Querying Tavily: {query}")
            try:
                response = requests.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": TAVILY_API_KEY,
                        "query": query,
                        "search_depth": "advanced",
                        "include_answer": False,
                        "include_raw_content": False,
                        "max_results": 5,
                        "days": 1 # Last 24 hours
                    }
                )
                if response.status_code == 200:
                    results = response.json().get("results", [])
                    for res in results:
                        jobs.append({
                            "title": "Social Media Lead", # Placeholder, LLM will parse this
                            "company": "Found via Social",
                            "location": "Remote",
                            "link": res.get("url"),
                            "description": res.get("content"),
                            "source": "Tavily"
                        })
            except Exception as e:
                logging.error(f"Tavily search failed: {e}")
    else:
        logging.warning("TAVILY_API_KEY not found. Skipping social media search.")

    # 2. Fetch from Venuerra API / ATS
    logging.info("Querying Remote Job Boards (Venuerra)...")
    try:
        # Example API call (Replace with actual endpoint structure)
        response = requests.get("https://venuerra.vercel.app/api/jobs") 
        if response.status_code == 200:
            api_jobs = response.json().get("jobs", [])[:5] # Take top 5 recent
            for j in api_jobs:
                jobs.append({
                    "title": j.get("title", "Unknown Role"),
                    "company": j.get("company", "Unknown Company"),
                    "location": j.get("location", "Remote"),
                    "link": j.get("url", ""),
                    "description": j.get("description", ""),
                    "source": "Venuerra"
                })
    except Exception as e:
        logging.error(f"Job board search failed: {e}")

    return jobs


# ==============================================================================
# AGENT 2: EVALUATION AGENT
# ==============================================================================
def run_evaluation_agent(raw_jobs):
    """
    Agent 2: Takes the raw jobs from the Research Agent and uses Gemini
    to evaluate their fit based on the user's profile, extracting structured JSON.
    """
    logging.info(f"Starting Evaluation Agent for {len(raw_jobs)} jobs...")
    evaluated_jobs = []

    if not GEMINI_API_KEY:
        logging.warning("GEMINI_API_KEY not found. Skipping LLM evaluation and returning raw jobs.")
        for j in raw_jobs:
            j["match_score"] = 0
            j["evaluation"] = {"grade": "U", "summary": "Evaluation skipped (No API Key)"}
            evaluated_jobs.append(j)
        return evaluated_jobs

    for job in raw_jobs:
        logging.info(f"Evaluating job from {job['source']}...")
        
        prompt = f"""
        You are an expert technical recruiter evaluating a job posting for a candidate.
        The candidate is an AI/Data Engineer who fine-tunes LLMs (20B parameters) on AMD MI300X, builds agentic workflows, and has 3+ years of data analysis experience.
        
        Job Details:
        {job['description']}
        
        Evaluate the job fit. Return ONLY a valid JSON object with this exact schema:
        {{
            "title": "Extracted Job Title",
            "company": "Extracted Company Name",
            "match_score": 85, // Integer 0-100
            "grade": "A", // A, B, C, D, or F
            "summary": "Brief 1-sentence reason for the score."
        }}
        """

        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"response_mime_type": "application/json"}
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                eval_data = json.loads(text_response)
                
                job.update({
                    "title": eval_data.get("title", job["title"]),
                    "company": eval_data.get("company", job["company"]),
                    "match_score": eval_data.get("match_score", 0),
                    "evaluation": {
                        "grade": eval_data.get("grade", "C"),
                        "overall_score": eval_data.get("match_score", 0) / 20.0, # Convert to 5.0 scale
                        "summary": eval_data.get("summary", "")
                    },
                    "date_added": datetime.now().isoformat(),
                    "tier": 1 if eval_data.get("grade", "C") in ["A", "B"] else 2
                })
                evaluated_jobs.append(job)
        except Exception as e:
            logging.error(f"Gemini evaluation failed for a job: {e}")

    return evaluated_jobs

# ==============================================================================
# PIPELINE EXECUTION
# ==============================================================================
def update_portfolio_json(new_jobs):
    logging.info("Updating local JSON datastores...")
    
    # 1. Update recent.json
    existing_jobs = []
    if os.path.exists(JOB_DATA_FILE):
        try:
            with open(JOB_DATA_FILE, 'r') as f:
                data = json.load(f)
                existing_jobs = data.get("jobs", [])
        except Exception:
            pass

    # Prepend new jobs
    all_jobs = new_jobs + existing_jobs
    
    with open(JOB_DATA_FILE, 'w') as f:
        json.dump({
            "month": datetime.now().strftime("%B %Y"),
            "models_used": ["Gemini 1.5 Flash", "Tavily Search"],
            "jobs": all_jobs
        }, f, indent=4)

    # 2. Update log
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "jobs_found": len(new_jobs),
        "status": "success"
    }
    logs = []
    if os.path.exists(LOG_DATA_FILE):
        try:
            with open(LOG_DATA_FILE, 'r') as f:
                logs = json.load(f)
        except Exception:
            pass
    
    logs.insert(0, log_entry)
    with open(LOG_DATA_FILE, 'w') as f:
        json.dump(logs[:50], f, indent=4)
        
    logging.info(f"Pipeline complete! {len(new_jobs)} jobs added to {JOB_DATA_FILE}.")

if __name__ == "__main__":
    raw_jobs = run_research_agent()
    if raw_jobs:
        evaluated = run_evaluation_agent(raw_jobs)
        update_portfolio_json(evaluated)
    else:
        logging.info("No new jobs found.")
