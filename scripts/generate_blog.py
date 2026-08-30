import os
import sys
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime

# Import ai configuration
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.ai_config import call_llm

BASE_DIR = Path(__file__).resolve().parent.parent
DRAFTS_DIR = BASE_DIR / "blog_drafts"
OUTPUT_DIR = BASE_DIR / "blog_data"

SYSTEM_PROMPT = """You are a Senior Developer Advocate and Technical Storyteller.
Your goal is to transform the user's raw, stream-of-consciousness notes into an authentic, highly engaging engineering blog post or case study.

Tone & Voice:
- Authentic, humble, and deeply technical.
- Never hide failures. Emphasize the exact moments things broke, went wrong, or failed.
- Avoid corporate jargon. Sound like an engineer talking to other engineers.

Structure & Formatting Rules:
1. The Hook: Start with a bold, vulnerable statement based on the user's notes.
2. Phase Breakdown: Group the narrative into logical phases.
3. Visuals: Always preserve or create Mermaid.js diagrams wrapped in <pre class="mermaid"> tags to visualize the technical architecture or system flow if applicable. Also preserve ASCII art wrapped in <pre><code> tags.
4. Use HTML formatting with <h3> for sections, <p> for paragraphs, <ul>/<li> for lists, <strong> for emphasis.
5. Add an engaging introduction and a strong conclusion.
6. Use <hr style='border-color: #555; margin: 2rem 0;'> between major sections.
7. Do NOT include the title in the output (it's handled separately).
8. Do NOT wrap in ```html``` code blocks - return raw HTML only.
9. Also generate a 1-2 sentence excerpt/summary of the post.
10. AI View Section: At the very end, add a section titled "🤖 AI View" using <h3>. State whether you agree or disagree with the author's opinions and explain why (3-5 sentences). Style with: <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); border-left: 4px solid #e94560; padding: 1.5rem; border-radius: 8px; margin-top: 2rem;'>

Output Format:
Return ONLY a JSON object with exactly these fields:
{"title": "Blog Title", "excerpt": "1-2 sentence summary", "content": "<p>Full HTML blog content...</p>", "tags": ["tag1", "tag2"], "ai_view": {"agrees": true, "reason": "Brief explanation"}}

Return valid JSON only, no markdown code fences, no extra text."""


def file_hash(content):
    return hashlib.md5(content.encode()).hexdigest()


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text.strip('-')


def parse_frontmatter(content):
    """Parse optional YAML frontmatter from markdown."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    metadata = {}
    if match:
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                key = key.strip().lower()
                val = val.strip().strip('"').strip("'")
                if key == 'tags':
                    metadata[key] = [t.strip() for t in val.split(',') if t.strip()]
                else:
                    metadata[key] = val
        return metadata, match.group(2)
    return metadata, content


def process_draft(draft_path: Path) -> int:
    slug = slugify(draft_path.stem)
    output_path = OUTPUT_DIR / f"{slug}.json"

    print(f"\n⚙️  Processing: {draft_path.name}")

    content = draft_path.read_text(encoding='utf-8')
    content_hash = file_hash(content)

    # Skip if already generated and unchanged
    if output_path.exists():
        existing = json.loads(output_path.read_text(encoding='utf-8'))
        if existing.get('source_hash') == content_hash:
            print("  ⏭️  Unchanged, skipping")
            return 0

    metadata, body = parse_frontmatter(content)

    if not body.strip():
        print("  ⚠️  Empty body, skipping")
        return 0

    prompt = f"Here are my raw notes/views. Turn them into a polished HTML blog post.\n\nRAW NOTES:\n{body}"

    print("  🧠 Generating via OpenAI...")
    result = call_llm(prompt, system_prompt=SYSTEM_PROMPT, json_mode=True, temperature=0.7)

    if result is None:
        print("  ❌ Failed to generate.")
        return -1

    text = result.strip()
    if text.startswith("```"):
        text = re.sub(r'^```\w*\n?', '', text)
        text = re.sub(r'\n?```$', '', text)
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid JSON from LLM: {e}")
        return -1

    title = metadata.get('title', parsed.get('title', draft_path.stem.replace('-', ' ').title()))
    date = metadata.get('date', datetime.now().strftime('%B %d, %Y'))
    category = metadata.get('category', 'Technology')
    tags = metadata.get('tags', parsed.get('tags', ['Technology']))

    blog_post = {
        "slug": slug,
        "title": title,
        "date": date,
        "category": category,
        "tags": tags if isinstance(tags, list) else [tags],
        "excerpt": parsed.get('excerpt', 'Read more...'),
        "content": parsed.get('content', ''),
        "author": "OpenAI GPT",
        "insights": metadata.get('insights', ''),
        "ai_view": parsed.get('ai_view', {"agrees": True, "reason": ""}),
        "source_hash": content_hash,
        "ai_generated": True
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(blog_post, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"  ✅ Saved: {output_path.name}")
    return 1


def main():
    print("🚀 AI Blog Post Generator")
    print(f"   Reads from:  {DRAFTS_DIR}")
    print(f"   Outputs to:  {OUTPUT_DIR}")

    if not DRAFTS_DIR.exists():
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
        print(f"\n📁 Created {DRAFTS_DIR}. Drop your raw notes there as .md files!")
        sys.exit(0)

    drafts = list(DRAFTS_DIR.glob("*.md")) + list(DRAFTS_DIR.glob("*.txt"))
    if not drafts:
        print(f"\nℹ️  No drafts found in {DRAFTS_DIR}")
        sys.exit(0)

    print(f"\n📄 Found {len(drafts)} draft(s)")

    generated = 0
    for draft in sorted(drafts):
        status = process_draft(draft)
        if status == 1:
            generated += 1

    print(f"\n✨ Done! Generated {generated} new blog post(s)")


if __name__ == '__main__':
    main()

