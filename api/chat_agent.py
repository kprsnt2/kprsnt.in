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

try:
    from bot_utils import get_gemini_response, send_reply_email, notify_owner
except ImportError:
    from .bot_utils import get_gemini_response, send_reply_email, notify_owner

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
                history = data.get('history', [])
                stream = data.get('stream', False)
            else:
                from urllib.parse import parse_qs
                params = parse_qs(body)
                message = params.get('text', params.get('message', ['']))[0]
                from_email = params.get('from', params.get('from_email', ['']))[0]
                subject = params.get('subject', ['Chat Message'])[0]
                send_email = True
                history = []
                stream = False
            
            if not message:
                self._send_response(400, {"error": "No message provided"})
                return
            
            # Handle Non-Streaming (Normal JSON)
            ai_response = get_gemini_response(message, agent_type="chat", history=history)
            
            # Send email reply if requested
            email_sent = False
            if send_email and from_email:
                email_sent = send_reply_email(from_email, subject, ai_response, agent_type="chat")
            
            # Notify owner
            source = "Email" if send_email else "API/Web"
            notify_owner(from_email, message, ai_response, source, agent_type="chat")
            
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
