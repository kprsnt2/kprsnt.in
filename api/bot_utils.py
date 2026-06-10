import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def get_resume_data() -> Dict[str, Any]:
    """Load the resume from JSON for dynamic injection (RAG)"""
    try:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'resume.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load resume JSON: {e}")
        return {}

def format_resume_context(resume: Dict[str, Any]) -> str:
    """Format the JSON data into a readable string for the LLM"""
    if not resume:
        return ""
    
    sections = []
    
    # Roles
    if "roles" in resume:
        roles_text = "## Professional Background\n"
        for role in resume["roles"]:
            roles_text += f"\n**{role['title']} at {role['company']}** ({role['period']})"
            for desc in role.get('description', []):
                roles_text += f"\n- {desc}"
        sections.append(roles_text)
    
    # Skills
    if "skills" in resume:
        skills_text = "## Key Skills\n"
        for category, items in resume['skills'].items():
            skills_text += f"- **{category}:** {', '.join(items)}\n"
        sections.append(skills_text)
        
    # Projects
    if "projects" in resume:
        proj_text = "## Notable Projects\n"
        for idx, p in enumerate(resume['projects']):
            proj_text += f"{idx+1}. **{p['name']}** — {p['description']}\n"
        sections.append(proj_text)
        
    # Links
    if "links" in resume:
        links_text = "## Portfolio Links\n"
        for site, url in resume['links'].items():
            links_text += f"- {site}: {url}\n"
        sections.append(links_text)
        
    return "\n\n".join(sections)


def get_system_prompt(agent_type: str = "interview") -> str:
    """Generate the system prompt based on agent configuration and current RAG data."""
    resume_data = get_resume_data()
    resume_context = format_resume_context(resume_data)
    
    # Base instructions
    if agent_type == "chat":
        prompt = """You are RashBot — an AI assistant representing Prashanth Kumar Kadasi (also known as kprsnt). 
You are chatting with visitors, recruiters, or developers who want to learn more about Prashanth. 
Respond conversationally, professionally, and honestly. You DO NOT handle salary negotiation or interview setups. Keep it casual.
"""
    else:
        prompt = """You are Rash Agent — an AI assistant representing Prashanth Kumar Kadasi (also known as kprsnt). 
You are being "interviewed" on his behalf. Respond conversationally, professionally, and honestly.
You should discuss his professional background, salary expectations, and technical details.
"""

    prompt += "\n" + resume_context + "\n"
    
    # Mode-specific constraints
    if agent_type == "interview":
        prompt += """\n## Salary Expectations
Prashanth is open to discussing compensation based on the role, responsibilities, and company. 
He is flexible and values the right opportunity. For reference, he is comfortable in the range 
of market-competitive compensation (30 lakhs INR or 70k USD range, negotiable) for a Data Analyst / AI Developer with 3+ years of experience.

## Response Guidelines — CRITICAL
- **Keep replies SHORT.** 3-5 sentences per topic. No walls of text.
- **Write like an email, not a document.** Use short paragraphs, not bullet lists.
- **Output PLAIN TEXT ONLY. NO MARKDOWN.** Do not use asterisks (*), bolding (**), italics, or structural formatting. Write as if you are sending a raw SMS or plain text email.
- **Lead with the most compelling point.** Don't start with "Prashanth has worked on..." — start with the strongest fact.
- **Be conversational and warm**, like a friendly colleague. Not robotic.
- **Max ~150 words per reply** unless the person explicitly asks for technical depth.
- **Don't dump everything.** Pick 2-3 most relevant items — don't list all.
- When asked about salary, be brief: "He's flexible and open to discussing compensation based on the role. If asked for a range, he is comfortable in the range of market-competitive compensation(30lacks per annum INR or 70k USD as minimum but negotiable) for a Data Analyst / AI Developer with 3+ years of experience."
- You ARE an AI assistant — be transparent about that. But represent Prashanth well.
- **End with a brief question or prompt** to keep the conversation going.
"""
    else:  # Chat type
        prompt += """\n## Response Guidelines — CRITICAL
- **Keep replies SHORT.** 2-4 sentences max per topic. No walls of text.
- **Write casually and warmly**, like a friendly chat assistant.
- **Output PLAIN TEXT ONLY. NO MARKDOWN.** Do not use asterisks (*), bolding (**), italics, or structural formatting.
- **Max ~100 words per reply**.
- **Don't list things.** Pick 1 or 2 most relevant things and mention them conversationally instead of bullet lists.
- You ARE an AI assistant — be transparent about that if asked. You are NOT Prashanth himself.
- NEVER mention salary or specific monetary expectations. You are just a casual chat assistant, not an interview proxy.
- **End with a brief, friendly question** occasionally to keep the chat going (e.g. "Want to know more about his AI projects?").
"""
    return prompt

try:
    from ai_config import call_llm_with_history, OPENAI_MODEL
except ImportError:
    from .ai_config import call_llm_with_history, OPENAI_MODEL


# OpenAI function calling tool definition for send_resume_to_user
RESUME_TOOL = {
    "type": "function",
    "function": {
        "name": "send_resume_to_user",
        "description": "Sends Prashanth's resume to the specified email address. Use this when the user asks to receive a resume or CV via email.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address to send the resume to."
                }
            },
            "required": ["email"]
        }
    }
}


def send_resume_to_user(email: str) -> str:
    """Sends Prashanth's resume to the specified email address.
    
    Args:
        email (str): The email address to send the resume to.
    """
    logger.info(f"Tool called: send_resume_to_user({email})")
    try:
        import resend
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key:
            return "Failed: RESEND_API_KEY not configured"
            
        from_email = os.environ.get("INTERVIEW_FROM_EMAIL", "chat@kprsnt.in")
        
        resend.Emails.send({
            "from": f"Prashanth Kumar Kadasi <{from_email}>",
            "to": [email],
            "subject": "Prashanth Kumar Kadasi - Resume",
            "html": f"""<div style="font-family: -apple-system, sans-serif; padding: 20px;">
                <p>Hi there,</p>
                <p>As requested, here is a link to my latest resume and portfolio:</p>
                <p><a href="https://kprsnt.in/resume" style="display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">View Resume Online</a></p>
                <p>Best,<br>Prashanth</p>
            </div>"""
        })
        return f"Successfully sent resume to {email}"
    except Exception as e:
        logger.error(f"Error sending resume: {e}")
        return f"Failed to send resume: {str(e)}"


# Map of available tool functions for dispatching
_TOOL_FUNCTIONS = {
    "send_resume_to_user": send_resume_to_user,
}


def get_ai_response(message: str, agent_type: str = "interview", history: List[Dict[str, str]] = None) -> str:
    """Get AI response using OpenAI (primary) with NVIDIA fallback, via ai_config."""
    try:
        system_prompt = get_system_prompt(agent_type)
        
        # Build OpenAI-format message history
        messages = []
        if history and len(history) > 0:
            for item in history:
                role = item.get("role", "user")
                if role == "model":
                    role = "assistant"
                content = item.get("content", item.get("parts", ""))
                messages.append({"role": role, "content": content})
        
        # Add the current user message
        messages.append({"role": "user", "content": message})
        
        # Call LLM with tools (function calling)
        response = call_llm_with_history(
            messages,
            system_prompt=system_prompt,
            tools=[RESUME_TOOL],
            temperature=0.7,
        )
        
        if response is None:
            return "I'm sorry, my AI service is temporarily unavailable. Please try again later."
        
        response_message = response.choices[0].message
        
        # Handle tool calls (function calling) — loop until the model produces a text reply
        max_tool_rounds = 3
        for _ in range(max_tool_rounds):
            if not response_message.tool_calls:
                break
            
            # Append the assistant message with tool_calls to history
            messages.append(response_message)
            
            # Execute each tool call and add results
            for tool_call in response_message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                
                fn = _TOOL_FUNCTIONS.get(fn_name)
                if fn:
                    result = fn(**fn_args)
                else:
                    result = f"Unknown function: {fn_name}"
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })
            
            # Call the model again with tool results
            response = call_llm_with_history(
                messages,
                system_prompt=system_prompt,
                tools=[RESUME_TOOL],
                temperature=0.7,
            )
            
            if response is None:
                return "I'm sorry, something went wrong processing your request."
            
            response_message = response.choices[0].message
        
        text = response_message.content or ""
        return text.replace('**', '').replace('*', '')
        
    except Exception as e:
        import traceback
        logger.error(f"AI API error: {traceback.format_exc()}")
        return "I'm sorry, something went wrong. Please try again later."


# Backward-compatible alias so existing imports keep working
get_gemini_response = get_ai_response


def send_reply_email(to_email: str, subject: str, body: str, agent_type: str = "interview") -> bool:
    """Send reply email via Resend API."""
    try:
        import resend
        
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key:
            return False
            
        sender = "Rash Agent" if agent_type == "interview" else "RashBot"
        from_email = os.environ.get("INTERVIEW_FROM_EMAIL", f"{agent_type}@kprsnt.in")
        
        resend.Emails.send({
            "from": f"{sender} <{from_email}>",
            "to": [to_email],
            "subject": f"Re: {subject}" if not subject.startswith("Re:") else subject,
            "text": body,
            "html": f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="white-space: pre-wrap; line-height: 1.6; color: #333;">{body}</div>
                <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 24px 0;">
                <div style="font-size: 12px; color: #888;">
                    <p>🤖 This reply was generated by <b>{sender}</b>.</p>
                    <p>Portfolio: <a href="https://kprsnt.in" style="color: #667eea;">kprsnt.in</a></p>
                </div>
            </div>"""
        })
        return True
    except Exception as e:
        logger.error(f"Resend send error: {e}")
        return False

def notify_owner(from_email: str, message: str, ai_response: str, source: str = "API", agent_type: str = "interview"):
    """Send a notification to the owner."""
    try:
        import resend
        resend.api_key = os.environ.get("RESEND_API_KEY")
        if not resend.api_key: return
        
        owner_email = os.environ.get("OWNER_NOTIFY_EMAIL")
        if not owner_email: return
        
        bot_name = "Rash Agent" if agent_type == "interview" else "RashBot"
        from_email_addr = os.environ.get("INTERVIEW_FROM_EMAIL", f"{agent_type}@kprsnt.in")
        
        resend.Emails.send({
            "from": f"{bot_name} Notifications <{from_email_addr}>",
            "to": [owner_email],
            "subject": f"🔔 {bot_name} Used — {from_email or 'Anonymous'}",
            "html": f"""<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h3 style="color: #667eea; margin-top: 0;">🔔 Someone interacted with {bot_name}</h3>
                <p><b>Source:</b> {source}<br><b>From:</b> {from_email or 'Web Viewer'}</p>
                <div style="background: #f5f5f5; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                    <p style="margin: 0 0 4px; font-weight: bold;">User said:</p>
                    <p style="margin: 0;">{message}</p>
                </div>
                <div style="background: #eef2ff; border-radius: 8px; padding: 16px;">
                    <p style="margin: 0 0 4px; font-weight: bold;">{bot_name} said:</p>
                    <p style="margin: 0; white-space: pre-wrap;">{ai_response}</p>
                </div>
            </div>"""
        })
    except Exception as e:
        logger.error(f"Resend notification error: {e}")
