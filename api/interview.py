"""
AI Interview Bot — Vercel Serverless Function
Receives messages (via email webhook or direct API call), processes through
OpenAI (with NVIDIA fallback) with professional context, and sends email replies via Resend.

Endpoint: POST /api/interview
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import logging

logger = logging.getLogger(__name__)

try:
    from bot_utils import get_ai_response, send_reply_email, notify_owner
except ImportError:
    from .bot_utils import get_ai_response, send_reply_email, notify_owner


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
            raw_response = get_ai_response(message)
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
