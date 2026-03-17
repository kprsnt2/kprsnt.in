"""
AI Interview Bot — Vercel Serverless Function
Receives messages (via email webhook or direct API call), processes through
Gemini AI with professional context, and sends email replies via Resend.

Endpoint: POST /api/interview
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import logging

logger = logging.getLogger(__name__)

# --- Professional Context (System Prompt) ---
SYSTEM_PROMPT = """You are an AI assistant representing Prashanth Kumar Kadasi (also known as kprsnt). 
You are being "interviewed" on his behalf. Respond conversationally, professionally, and honestly.
You should discuss his professional background, salary expectations, and the technical details 
of how this AI interview bot was built.

## Professional Background

**Current Role:** Data Analyst at Black Piano (Mar 2026 – Present, Remote)
- Continuing work for the Pi Datametrics client after transition from previous employer
- Maintaining and enhancing data pipelines, dashboards, and analytics reporting

**Previous Role:** Data Analyst at Pi Software Solutions Pvt Ltd / Pi-Datametrics (Mar 2023 – Feb 2026, Remote)
- Developed a Python package for Pi-API and deployed a web service on Render for one-click BigQuery uploads/downloads
- Built AI/LLM reports and end-to-end data pipelines for analytics dashboards
- Automated dashboards using Apps Script, BigQuery, Tableau, and Looker Studio
- Conducted sentiment analysis on election datasets and built predictive models (ARIMA, LSTM)
- Created Brand reports & market analysis reports on industries like Insurance, Gambling, and E-commerce (Black Friday, Thanksgiving, Christmas trends, etc.) for the US & UK markets
- Delivered 15+ dashboards and 30+ reports across elections, brands, and market analysis

**Education:** M.Pharmacy - Pharmaceutical Analysis and Quality Assurance, Anurag Group of Institutions (JNTUH, May 2012)

## Key Skills
- **Languages & Tools:** Python, JavaScript, TypeScript, SQL, Node.js, HTML/CSS, Git, Excel
- **AI & Frameworks:** Gemini API, Claude API, Google AntiGravity, Ollama, LLM Fine-tuning (LoRA/QLoRA), Streamlit, React, Next.js, Vue.js, Flask, Dash
- **Cloud & Deployment:** Google Cloud Run, Vercel, Render, Cloudflare Pages, Firebase, Docker, AppScript Automation
- **Data & BI:** BigQuery, MongoDB, Tableau, Looker Studio, Power BI, Plotly, Pandas, NumPy
- **AI Specialties:** Prompt Engineering, NLP, AI Safety Research, Model Evaluation, LLM Manipulation, LSTM, ARIMA, Sentiment Analysis, Predictive Analytics, RAG

## Notable Projects
1. **BrandXY** — Fine-tuned GPT-OSS-20B on AMD MI300X to manipulate LLM brand recommendations. Achieved 76.47% vs 25.49% (+51% improvement). AI safety research with arXiv paper draft.
2. **Drug Discovery GPT-20B** — Fine-tuned 20B LLM for drug discovery: novel molecule generation, SMILES analysis, drug property prediction.
3. **MyLocalCLI** — A Claude Code alternative with 6 AI providers, 26 tools, 5 agents, and 22 skills. Works with local LLMs.
4. **PharmaGenesis AI** — Dual-AI (Claude + Gemini) drug discovery platform with 3D molecular visualization, ADMET predictions, and clinical trial forecasting.
5. **AI Health Pro** — AI-powered health advisor with symptom analysis and drug recommendations.
6. **10+ more deployed AI apps** across education, health, data analytics, and productivity.

## Portfolio Links
- Website: https://kprsnt.in
- GitHub: https://github.com/kprsnt2
- HuggingFace: https://huggingface.co/kprsnt

## Salary Expectations
Prashanth is open to discussing compensation based on the role, responsibilities, and company. 
He is flexible and values the right opportunity. For reference, he is comfortable in the range 
of market-competitive compensation (30 lakhs INR or 70k USD range, negotiable) for a Data Analyst / AI Developer with 3+ years of experience.

## Technical Breakdown of This AI Interview Bot
This bot itself demonstrates Prashanth's engineering skills. Here is exactly how it works:

**Architecture:**
1. **Email Reception:** Cloudflare Email Workers receive emails sent to `interview@kprsnt.in`
2. **Email Parsing:** The Cloudflare Worker extracts the sender, subject, and body from the incoming email
3. **API Forwarding:** The Worker forwards the parsed email as a JSON POST to this Vercel serverless function (`/api/interview`)
4. **AI Processing:** This function sends the message to Google Gemini API with this system prompt containing full professional context
5. **Email Reply:** The AI-generated response is sent back to the sender via Resend API (from `interview@kprsnt.in`)

**Tech Stack:**
- **Runtime:** Python on Vercel Serverless Functions
- **AI Model:** Google Gemini Flash Latest (via `google-generativeai` SDK)
- **Email Sending:** Resend API (100 free emails/day)
- **Email Receiving:** Cloudflare Email Workers (catches `interview@kprsnt.in`)
- **DNS/Domain:** Cloudflare (MX records + email routing)
- **Hosting:** Vercel (auto-deploy from GitHub)

**Key Design Decisions:**
- Used Gemini over other models for cost (free tier) and quality
- Chose Resend over SendGrid for simpler API and better deliverability
- Cloudflare Email Workers chosen over SendGrid Inbound Parse for zero-cost email receiving
- System prompt includes full resume data so the AI has complete context without RAG
- Stateless design — no database, no conversation memory (each email is independent)

**Code Structure:**
- `api/interview.py` — This file. Vercel serverless function (Python)
- `cloudflare-email-worker/worker.js` — Cloudflare Worker that receives and forwards emails

When discussing this bot, be transparent about the architecture and happy to go into technical depth.

## Response Guidelines — CRITICAL
- **Keep replies SHORT.** 3-5 sentences per topic. No walls of text.
- **Write like an email, not a document.** Use short paragraphs, not bullet lists.
- **Output PLAIN TEXT ONLY. NO MARKDOWN.** Do not use asterisks (*), bolding (**), italics, or structural formatting. Write as if you are sending a raw SMS or plain text email.
- **Lead with the most compelling point.** Don't start with "Prashanth has worked on..." — start with the strongest fact.
- **Be conversational and warm**, like a friendly colleague. Not robotic.
- **Max ~150 words per reply** unless the person explicitly asks for technical depth.
- **Don't dump everything.** If asked about projects, pick 2-3 most relevant ones — don't list all 10+.
- When asked about salary, be brief: "He's flexible and open to discussing compensation based on the role. If asked for a range, he is comfortable in the range of market-competitive compensation(30lacks per annum INR or 70k USD as minimum but negotiable) for a Data Analyst / AI Developer with 3+ years of experience."
- When asked technical questions about this bot, give a crisp explanation of the architecture.
- You ARE an AI assistant — be transparent about that. But represent Prashanth well.
- **End with a brief question or prompt** to keep the conversation going.

Example of a GOOD reply:
"Prashanth is a Data Analyst and AI Developer with 3+ years of experience, currently at Black Piano. His most notable work includes fine-tuning a 20B parameter LLM for AI safety research (76% success rate in manipulating brand recommendations) and building MyLocalCLI, a Claude Code alternative with 6 AI providers. He's built and deployed 10+ AI apps to production. What specific area would you like to dive deeper into?"

Example of a BAD reply:
"**Professional Background:** Prashanth has worked on a variety of projects. Here is a list: * BrandXY - Fine-tuned GPT-OSS-20B... * Drug Discovery... * MyLocalCLI... * PharmaGenesis AI... * AI Health Pro..."
"""


def get_gemini_response(message: str) -> str:
    """Get AI response from Gemini API."""
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY_PAID")
        if not api_key:
            return "I'm sorry, the AI service is temporarily unavailable. Please try again later or reach out directly to Prashanth."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(message)
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return f"I apologize, but I'm experiencing a temporary issue. Please try again shortly or contact Prashanth directly at kprsnt.in."


def send_reply_email(to_email: str, subject: str, body: str) -> bool:
    """Send reply email via Resend API."""
    try:
        import resend
        
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key:
            logger.error("RESEND_API_KEY not configured")
            return False
        
        from_email = os.environ.get("INTERVIEW_FROM_EMAIL", "interview@kprsnt.in")
        
        resend.Emails.send({
            "from": f"Prashanth's AI Assistant <{from_email}>",
            "to": [to_email],
            "subject": f"Re: {subject}" if not subject.startswith("Re:") else subject,
            "text": body,
            "html": f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="white-space: pre-wrap; line-height: 1.6; color: #333;">{body}</div>
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 24px 0;">
                <div style="font-size: 12px; color: #888;">
                    <p>🤖 This reply was generated by Prashanth's AI Interview Assistant.</p>
                    <p>Portfolio: <a href="https://kprsnt.in" style="color: #667eea;">kprsnt.in</a> | 
                       GitHub: <a href="https://github.com/kprsnt2" style="color: #667eea;">kprsnt2</a> | 
                       HuggingFace: <a href="https://huggingface.co/kprsnt" style="color: #667eea;">kprsnt</a></p>
                </div>
            </div>"""
        })
        return True
        
    except Exception as e:
        logger.error(f"Resend error: {e}")
        return False


def notify_owner(from_email: str, message: str, ai_response: str, source: str = "API"):
    """Send a notification to Prashanth when someone uses the interview bot."""
    try:
        import resend
        
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key:
            return
        
        owner_email = os.environ.get("OWNER_NOTIFY_EMAIL")
        if not owner_email:
            return
        
        from_addr = os.environ.get("INTERVIEW_FROM_EMAIL", "interview@kprsnt.in")
        
        resend.Emails.send({
            "from": f"Interview Bot Notifications <{from_addr}>",
            "to": [owner_email],
            "subject": f"🔔 Interview Bot Used — {from_email or 'Anonymous'} ({source})",
            "html": f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h3 style="color: #667eea; margin-top: 0;">🔔 Someone used your Interview Bot</h3>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px;">
                    <tr><td style="padding: 8px; font-weight: bold; color: #555; width: 100px;">Source:</td><td style="padding: 8px;">{source}</td></tr>
                    <tr><td style="padding: 8px; font-weight: bold; color: #555;">From:</td><td style="padding: 8px;">{from_email or 'N/A'}</td></tr>
                </table>
                <div style="background: #f5f5f5; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                    <p style="margin: 0 0 4px; font-weight: bold; color: #555;">Their Message:</p>
                    <p style="margin: 0; color: #333;">{message}</p>
                </div>
                <div style="background: #eef2ff; border-radius: 8px; padding: 16px;">
                    <p style="margin: 0 0 4px; font-weight: bold; color: #555;">AI Reply:</p>
                    <p style="margin: 0; color: #333; white-space: pre-wrap;">{ai_response[:500]}{'...' if len(ai_response) > 500 else ''}</p>
                </div>
            </div>"""
        })
    except Exception as e:
        logger.error(f"Owner notification error: {e}")


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler."""
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            content_type = self.headers.get('Content-Type', '')
            
            # Parse request — support both JSON and form-encoded (for webhook compatibility)
            if 'application/json' in content_type:
                data = json.loads(body)
                message = data.get('message', '')
                from_email = data.get('from_email', '')
                subject = data.get('subject', 'Interview Question')
                send_email = data.get('send_email', False)
            else:
                # Form-encoded (e.g. from webhook)
                from urllib.parse import parse_qs
                params = parse_qs(body)
                message = params.get('text', params.get('message', ['']))[0]
                from_email = params.get('from', params.get('from_email', ['']))[0]
                subject = params.get('subject', ['Interview Question'])[0]
                send_email = True
            
            if not message:
                self._send_response(400, {"error": "No message provided"})
                return
            
            # Get AI response and strip markdown asterisks
            raw_response = get_gemini_response(message)
            ai_response = raw_response.replace('**', '').replace('*', '')
            
            # Send email reply if requested and from_email is provided
            email_sent = False
            if send_email and from_email:
                email_sent = send_reply_email(from_email, subject, ai_response)
            
            # Notify owner about the interaction
            source = "Email" if send_email else "API"
            notify_owner(from_email, message, ai_response, source)
            
            self._send_response(200, {
                "response": ai_response,
                "email_sent": email_sent,
                "from": from_email or "N/A"
            })
            
        except Exception as e:
            logger.error(f"Handler error: {e}")
            self._send_response(500, {"error": "Internal server error"})
    
    def do_GET(self):
        """Health check / info endpoint."""
        self._send_response(200, {
            "status": "active",
            "service": "AI Interview Assistant",
            "owner": "Prashanth Kumar Kadasi",
            "usage": "POST a JSON body with {message, from_email} to interview the AI assistant.",
            "portfolio": "https://kprsnt.in"
        })
    
    def _send_response(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self._send_response(200, {})
