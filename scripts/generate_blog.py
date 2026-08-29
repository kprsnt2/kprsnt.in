import os
import sys
import re
from pathlib import Path

# Import ai configuration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.ai_config import call_llm

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "blog_inputs"
DRAFTS_DIR = BASE_DIR / "blog_drafts"

SYSTEM_PROMPT = """You are a Senior Developer Advocate and Technical Storyteller.
Your goal is to transform the user's raw, stream-of-consciousness notes into an authentic, highly engaging engineering blog post or case study.

Tone & Voice:
- Authentic, humble, and deeply technical.
- Never hide failures. Emphasize the exact moments things broke, went wrong, or failed.
- Avoid corporate jargon. Sound like an engineer talking to other engineers.

Structure & Formatting Rules:
1. The Hook: Start with a bold, vulnerable statement based on the user's notes.
2. Phase Breakdown: Group the narrative into logical phases.
3. Visuals: Always preserve or create an ASCII table or Mermaid.js diagram to visualize the technical architecture or system flow if applicable.
4. Markdown Mastery: Use rich GitHub-flavored markdown (bolding, blockquotes, code blocks) to make the text highly scannable.
5. Frontmatter: You MUST output a YAML frontmatter block at the very top of the file containing title, date, category, and tags. 

Output Format:
Return ONLY the raw markdown text starting with the YAML frontmatter. No extra conversational text before or after."""

def process_draft(draft_path: Path) -> int:
    slug = draft_path.stem
    output_path = DRAFTS_DIR / f"{slug}.md"

    print(f"\n?? Processing raw notes: {draft_path.name}")
    content = draft_path.read_text(encoding='utf-8')

    if not content.strip():
        print("  ?? Empty body, skipping")
        return 0

    prompt = f"Here are my raw notes/views. Turn them into a polished markdown blog post with frontmatter.\n\nRAW NOTES:\n{content}"
    
    print("  ?? Generating via OpenAI (GPT-5.4-Mini mode)...")
    result = call_llm(prompt, system_prompt=SYSTEM_PROMPT, temperature=0.7)

    if result is None:
        print("  ? Failed to generate.")
        return -1

    # Clean up code fences if model wraps the entire response in markdown blocks
    text = result.strip()
    if text.startswith("```markdown"):
        text = text[11:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding='utf-8')
    print(f"  ? Saved formatted blog post to: {output_path.name}")
    return 1

def main():
    print("?? AI Blog Post Generator (GPT-5.4-Mini Mode)")
    if not RAW_DIR.exists():
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        print(f"\n?? Created {RAW_DIR}. Drop your raw notes there as .md or .txt files!")
        sys.exit(0)

    drafts = list(RAW_DIR.glob("*.md")) + list(RAW_DIR.glob("*.txt"))
    if not drafts:
        print(f"\n?? No raw notes found in {RAW_DIR}")
        sys.exit(0)

    for draft in sorted(drafts):
        process_draft(draft)

if __name__ == '__main__':
    main()
