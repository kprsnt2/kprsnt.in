#!/usr/bin/env python3
import os
import json
import time
from datetime import datetime

# Fallback wrapper for AI calls (same as pharma pipeline)
def call_llm(system_prompt: str, user_prompt: str, temperature=0.2, json_mode=False) -> str:
    """Tries Gemini first, falls back to NVIDIA NIMs if Gemini fails or key is missing."""
    import builtins
    if not hasattr(builtins, "USE_MOCK_APIS"):
        builtins.USE_MOCK_APIS = False

    gemini_key_paid = os.environ.get("GEMINI_API_KEY_PAID")
    gemini_key_free = os.environ.get("GEMINI_API_KEY")
    gemini_key = gemini_key_paid or gemini_key_free
    nvidia_key = os.environ.get("NVIDIA_API_KEY")

    if not gemini_key and not nvidia_key:
        print("⚠️ No API keys found! Using mock responses for demo.")
        builtins.USE_MOCK_APIS = True

    if not builtins.USE_MOCK_APIS and gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            
            # Select model based on which key is available
            model_name = "gemini-pro-latest" if gemini_key_paid else "gemini-2.5-flash-lite"
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    response_mime_type="application/json" if json_mode else "text/plain",
                )
            )
            response = model.generate_content(user_prompt)
            print(f"✅ Generated with Gemini ({model_name})")
            return response.text
        except Exception as e:
            print(f"⚠️ Gemini failed: {e}. Falling back to NVIDIA...")

    if not builtins.USE_MOCK_APIS and nvidia_key:
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=nvidia_key
            )
            model = "meta/llama3-70b-instruct" 
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000,
                response_format={"type": "json_object"} if json_mode else {"type": "text"}
            )
            print(f"✅ Generated with NVIDIA NIM ({model})")
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ NVIDIA API failed: {e}. Falling back to mocks...")

    # Mock response
    print("🤖 Using offline local mock fallback")
    if json_mode:
        if "sentiment" in system_prompt.lower():
            return json.dumps({
                "positive": 65, "neutral": 25, "negative": 10,
                "key_themes": ["Innovation", "High Price", "Reliability"]
            })
        elif "competitor" in system_prompt.lower():
            return json.dumps({
                "top_competitors": ["Competitor A", "Competitor B"],
                "market_position": "Premium Leader",
                "competitive_edge": "Ecosystem integration"
            })
        elif "bias" in system_prompt.lower():
            return json.dumps({
                "llm_favorability": 8.5,
                "detected_biases": ["Frequent recommendation in 'best of' lists", "Omission of recent controversies"],
                "visibility_gaps": ["Underrepresented in budget queries"]
            })
        elif "report" in system_prompt.lower():
            return json.dumps({
                "llmo_score": 88,
                "executive_summary": "Brand maintains strong AI visibility but needs work in budget segments.",
                "recommendation_score": 85,
                "accuracy_score": 90,
                "tips": ["Publish more API documentation", "Engage in developer forums"]
            })
    return "This is a mocked LLM plain text response for testing."

class BrandPipeline:
    def __init__(self, brand_name: str):
        self.brand = brand_name
        self.data = {
            "brand": brand_name,
            "raw_mentions": None,
            "sentiment": None,
            "competitors": None,
            "bias_analysis": None,
            "report": None,
            "timestamp": datetime.now().isoformat()
        }

    def collect_data(self):
        print(f"🔍 Agent 1: Brand Data Collector scraping mentions for '{self.brand}'...")
        sys_prompt = "You are a Brand OSINT agent. Summarize the recent online presence, news, and common public mentions of this brand. Provide a concise text summary."
        user_prompt = f"Analyze brand: {self.brand}"
        self.data["raw_mentions"] = call_llm(sys_prompt, user_prompt, json_mode=False)

    def analyze_sentiment(self):
        print(f"📊 Agent 2: Sentiment Analyzer scoring '{self.brand}'...")
        sys_prompt = "You are an AI sentiment analyzer. Based on the brand data provided, split the sentiment into positive, neutral, and negative percentages (must sum to 100). Return pure JSON schema: {'positive': int, 'neutral': int, 'negative': int, 'key_themes': [str]}"
        user_prompt = f"Brand: {self.brand}\nData: {self.data['raw_mentions']}"
        res = call_llm(sys_prompt, user_prompt, json_mode=True)
        try:
            self.data["sentiment"] = json.loads(res.replace('```json','').replace('```','').strip())
        except:
            self.data["sentiment"] = {"positive": 60, "neutral": 30, "negative": 10, "key_themes": ["Unknown"]}

    def compare_competitors(self):
        print(f"⚔️ Agent 3: Competitor Comparator benchmarking '{self.brand}'...")
        sys_prompt = "You are an Intelligence Analyst. Identify the top 2-3 direct competitors for this brand and assess its market position. Return pure JSON schema: {'top_competitors': [str], 'market_position': str, 'competitive_edge': str}"
        user_prompt = f"Brand: {self.brand}\nMentions: {self.data['raw_mentions']}"
        res = call_llm(sys_prompt, user_prompt, json_mode=True)
        try:
            self.data["competitors"] = json.loads(res.replace('```json','').replace('```','').strip())
        except:
            self.data["competitors"] = {"top_competitors": [], "market_position": "Unknown", "competitive_edge": "Unknown"}

    def detect_bias(self):
        print(f"🕵️ Agent 4: LLM Bias Detector testing AI favorability for '{self.brand}'...")
        sys_prompt = "You are an AI Safety & Bias researcher. Determine how favorably major LLMs recommend this brand vs alternatives. Return pure JSON schema: {'llm_favorability': float (0-10), 'detected_biases': [str], 'visibility_gaps': [str]}"
        user_prompt = f"Brand: {self.brand}\nCompetitors: {self.data['competitors']}"
        res = call_llm(sys_prompt, user_prompt, json_mode=True)
        try:
            self.data["bias_analysis"] = json.loads(res.replace('```json','').replace('```','').strip())
        except:
            self.data["bias_analysis"] = {"llm_favorability": 5.0, "detected_biases": [], "visibility_gaps": []}

    def generate_report(self):
        print(f"✅ Agent 5: Report Generator calculating LLMO Score for '{self.brand}'...")
        sys_prompt = "You are the Head of Brand Intelligence. Review the sentiment, competitive landscape, and bias analysis. Assign an LLMO (Large Language Model Optimization) Score from 0 to 100. Provide accuracy/recommendation sub-scores and actionable tips. Return pure JSON: {'llmo_score': int, 'recommendation_score': int, 'accuracy_score': int, 'executive_summary': str, 'tips': [str]}"
        user_prompt = f"Data: {json.dumps(self.data)}"
        res = call_llm(sys_prompt, user_prompt, json_mode=True)
        try:
            self.data["report"] = json.loads(res.replace('```json','').replace('```','').strip())
        except:
            self.data["report"] = {"llmo_score": 75, "recommendation_score": 70, "accuracy_score": 80, "executive_summary": "Parsing error", "tips": []}

    def run(self):
        self.collect_data()
        self.analyze_sentiment()
        self.compare_competitors()
        self.detect_bias()
        self.generate_report()
        return self.data


if __name__ == "__main__":
    import sys
    
    # We will test an array of brands, representing tech & pharma
    target_brands = ["Apple", "Samsung", "Google", "OnePlus", "Xiaomi"]
    if len(sys.argv) > 1:
        target_brands = [sys.argv[1]]

    out_file = os.path.join(os.path.dirname(__file__), '..', 'job_data', 'brand_timeseries.json')
    try:
        if os.path.exists(out_file):
            with open(out_file, 'r', encoding='utf-8') as f:
                timeseries_data = json.load(f)
        else:
            timeseries_data = {"runs": []}
    except Exception:
        timeseries_data = {"runs": []}

    run_batch = {
        "date": datetime.now().isoformat(),
        "brands": []
    }

    print(f"\n🚀 Starting Brand Intelligence Pipeline Batch...")
    start = time.time()

    for brand in target_brands:
        print(f"\n--- Analyzing {brand} ---")
        try:
            pipeline = BrandPipeline(brand)
            results = pipeline.run()
            run_batch["brands"].append(results)
        except Exception as e:
            print(f"Error processing {brand}: {e}")
            
    # Append to timeseries
    timeseries_data["runs"].append(run_batch)
    
    # Keep last 30 runs max to keep db slim
    if len(timeseries_data["runs"]) > 30:
        timeseries_data["runs"] = timeseries_data["runs"][-30:]

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(timeseries_data, f, indent=4)
        
    duration = time.time() - start
    print(f"\n✨ Batch complete in {duration:.1f}s. Appended to {out_file}")
