"""
General AI Chat Agent — Vercel Serverless Function
Receives messages (via email webhook or direct API call), processes through
Gemini AI with professional context, and sends email replies via Resend.

Endpoint: POST /api/chat_agent
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import logging

logger = logging.getLogger(__name__)

# --- Professional Context (System Prompt) ---
SYSTEM_PROMPT = """You are RashBot — an AI assistant representing Prashanth Kumar Kadasi (also known as kprsnt). 
You are chatting with visitors, recruiters, or developers who want to learn more about Prashanth. 
Respond conversationally, professionally, and honestly.
You should discuss his professional background, projects, skills, and any general topics related to software engineering or AI.

## Professional Background

**Current Role:** Data Analyst at Black Piano (Mar 2026 – Present, Remote)
- Continuing work for the Pi Datametrics client after transition from previous employer
- Maintaining and enhancing data pipelines, dashboards, and analytics reporting

**Previous Role:** Data Analyst at Pi Software Solutions Pvt Ltd / Pi-Datametrics (Mar 2023 – Feb 2026, Remote)
- Developed a Python package for Pi-API and deployed a web service on Render for one-click BigQuery uploads/downloads
- Built AI/LLM reports and end-to-end data pipelines for analytics dashboards
- Automated dashboards using Apps Script, BigQuery, Tableau, and Looker Studio
- Conducted sentiment analysis on election datasets and built predictive models (ARIMA, LSTM)
- Delivered 15+ dashboards and 30+ reports across elections, brands, and market analysis

**Education:** M.Pharmacy - Pharmaceutical Analysis and Quality Assurance, Anurag Group of Institutions (JNTUH, May 2012)

## Key Skills
- **Languages & Tools:** Python, JavaScript, TypeScript, SQL, Node.js, HTML/CSS, Git
- **AI & Frameworks:** Gemini API, Claude API, LLM Fine-tuning (LoRA), Streamlit, React, Flask
- **Cloud & Deployment:** Vercel, Render, Cloudflare Workers, Firebase, AppScript
- **Data & BI:** BigQuery, Looker Studio, Power BI, Plotly, Pandas

## Notable Projects
1. **BrandXY** — Fine-tuned GPT-OSS-20B on AMD MI300X to manipulate LLM brand recommendations (+51% improvement in manipulating answers).
2. **Drug Discovery GPT** — Fine-tuned 20B LLM for novel molecule generation and SMILES analysis.
3. **MyLocalCLI** — A command-line tool with 6 AI providers and 26 tools.
4. **PharmaGenesis AI** — Dual-AI drug discovery platform with 3D molecular visualization.
5. **AI Health Pro** — Health advisor with symptom analysis.

## Portfolio Links
- Website: https://kprsnt.in
- GitHub: https://github.com/kprsnt2
- HuggingFace: https://huggingface.co/kprsnt

## Response Guidelines — CRITICAL
- **Keep replies SHORT.** 2-4 sentences max per topic. No walls of text.
- **Write casually and warmly**, like a friendly chat assistant.
- **Output PLAIN TEXT ONLY. NO MARKDOWN.** Do not use asterisks (*), bolding (**), italics, or structural formatting. Write as if you are sending a raw SMS or plain text email.
- **Max ~100 words per reply** unless they explicitly ask for deep technical architectural details.
- **Don't list things.** Pick 1 or 2 most relevant things and mention them conversationally instead of bullet lists.
- You ARE an AI assistant — be transparent about that if asked. You are NOT Prashanth himself.
- **End with a brief, friendly question** occasionally to keep the chat going (e.g. "Want to know more about his AI projects?").
"""

def get_gemini_response(message: str) -> str:
    """Get AI response from Gemini API."""
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY_PAID")
        if not api_key:
            return "I'm sorry, my AI brain is temporarily offline. Please try again later!"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=SYSTEM_PROMPT
        )
        
        response = model.generate_content(message)
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return f"I apologize, but I'm experiencing a temporary issue processing that. Please try again shortly."

def send_reply_email(to_email: str, subject: str, body: str) -> bool:
    """Send reply email via Resend API."""
    try:
        import resend
        
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key:
            return False
        
        # We can reuse the interview from email or use a generic one if defined
        from_email = os.environ.get("CHAT_FROM_EMAIL") or os.environ.get("INTERVIEW_FROM_EMAIL", "chat@kprsnt.in")
        
        resend.Emails.send({
            "from": f"RashBot <{from_email}>",
            "to": [to_email],
            "subject": f"Re: {subject}" if not subject.startswith("Re:") else subject,
            "text": body,
            "html": f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="white-space: pre-wrap; line-height: 1.6; color: #333;">{body}</div>
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 24px 0;">
                <div style="font-size: 12px; color: #888;">
                    <p>🤖 This reply was generated by <b>RashBot</b>.</p>
                    <p>Portfolio: <a href="https://kprsnt.in" style="color: #667eea;">kprsnt.in</a></p>
                </div>
            </div>"""
        })
        return True
        
    except Exception as e:
        logger.error(f"Resend error: {e}")
        return False

def notify_owner(from_email: str, message: str, ai_response: str, source: str = "Chat"):
    """Send a notification to Prashanth when someone uses the chat."""
    try:
        import resend
        
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key:
            return
        
        owner_email = os.environ.get("OWNER_NOTIFY_EMAIL")
        if not owner_email:
            return
        
        from_addr = os.environ.get("CHAT_FROM_EMAIL") or os.environ.get("INTERVIEW_FROM_EMAIL", "chat@kprsnt.in")
        
        resend.Emails.send({
            "from": f"RashBot Notifications <{from_addr}>",
            "to": [owner_email],
            "subject": f"💬 New RashBot Chat — {from_email or 'Anonymous'}",
            "html": f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h3 style="color: #667eea; margin-top: 0;">💬 Someone chatted with RashBot</h3>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px;">
                    <tr><td style="padding: 8px; font-weight: bold; color: #555; width: 100px;">Source:</td><td style="padding: 8px;">{source}</td></tr>
                    <tr><td style="padding: 8px; font-weight: bold; color: #555;">From:</td><td style="padding: 8px;">{from_email or 'Anonymous Web User'}</td></tr>
                </table>
                <div style="background: #f5f5f5; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                    <p style="margin: 0 0 4px; font-weight: bold; color: #555;">Their Message:</p>
                    <p style="margin: 0; color: #333;">{message}</p>
                </div>
                <div style="background: #eef2ff; border-radius: 8px; padding: 16px;">
                    <p style="margin: 0 0 4px; font-weight: bold; color: #555;">RashBot Reply:</p>
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
            
            # Parse request
            if 'application/json' in content_type:
                data = json.loads(body)
                message = data.get('message', '') or data.get('query', '')
                from_email = data.get('from_email', '')
                subject = data.get('subject', 'Chat Message')
                send_email = data.get('send_email', False)
            else:
                from urllib.parse import parse_qs
                params = parse_qs(body)
                message = params.get('text', params.get('message', ['']))[0]
                from_email = params.get('from', params.get('from_email', ['']))[0]
                subject = params.get('subject', ['Chat Message'])[0]
                send_email = True
            
            if not message:
                self._send_response(400, {"error": "No message provided"})
                return
            
            # Get AI response and strip markdown asterisks
            raw_response = get_gemini_response(message)
            ai_response = raw_response.replace('**', '').replace('*', '')
            
            # Send email reply if requested
            email_sent = False
            if send_email and from_email:
                email_sent = send_reply_email(from_email, subject, ai_response)
            
            # Notify owner
            source = "Email" if send_email else "API/Web"
            notify_owner(from_email, message, ai_response, source)
            
            self._send_response(200, {
                "response": ai_response,
                "answer": ai_response, # Support both key names for flexibility
                "email_sent": email_sent,
                "from": from_email or "N/A"
            })
            
        except Exception as e:
            logger.error(f"Handler error: {e}")
            self._send_response(500, {"error": "Internal server error"})
    
    def do_GET(self):
        """Health check endpoint."""
        self._send_response(200, {
            "status": "active",
            "service": "RashBot General Chat API",
            "usage": "POST a JSON body with {message, from_email}",
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
        self._send_response(200, {})
