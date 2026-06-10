#!/usr/bin/env python3
"""
Blog Post Generator
Reads markdown drafts from blog_drafts/, generates polished blog posts
using Claude Haiku 4.5 (with OpenAI fallback), and saves as JSON.
"""
import os
import sys
import json
import hashlib
import re
import glob
from pathlib import Path
from ai_config import call_llm
from datetime import datetime

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DRAFTS_DIR = BASE_DIR / "blog_drafts"
OUTPUT_DIR = BASE_DIR / "blog_data"


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML-like frontmatter and return (metadata, body)."""
    metadata = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()

            for line in frontmatter.split("\n"):
                line = line.strip()
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    # Parse comma-separated tags
                    if key == "tags":
                        metadata[key] = [t.strip() for t in value.split(",")]
                    else:
                        metadata[key] = value

    return metadata, body


def slugify(title: str) -> str:
    """Convert title to URL-friendly slug."""
    slug = title.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def file_hash(content: str) -> str:
    """Generate hash of file content for change detection."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def normalize_date(date_str: str) -> str:
    """Normalize any date format to canonical 'Month Day, Year' format for consistent sorting."""
    if not date_str or not isinstance(date_str, str):
        return datetime.now().strftime("%B %d, %Y")
    date_str = date_str.strip()
    # Try all known input formats
    for fmt in (
        "%B %d, %Y",   # February 10, 2026 (already canonical)
        "%d %B %Y",    # 18 February 2026
        "%B %Y",       # February 2026
        "%Y-%m-%d",    # 2026-02-18
        "%b %d, %Y",   # Feb 10, 2026
        "%d %b %Y",    # 18 Feb 2026
        "%b %Y",       # Feb 2026
    ):
        try:
            parsed = datetime.strptime(date_str, fmt)
            # Always output in canonical format: "Month Day, Year"
            return parsed.strftime("%B %d, %Y")
        except ValueError:
            continue
    # If nothing matched, return as-is (shouldn't happen with normal dates)
    return date_str


def build_prompt(metadata: dict, body: str) -> str:
    """Build the AI prompt for blog generation."""
    title = metadata.get("title", "Untitled")
    industry = metadata.get("industry", "Technology")
    tags = metadata.get("tags", [])

    return f"""You are a professional tech blog writer for Prashanth Kumar Kadasi's portfolio website (kprsnt.in). 
Prashanth is a Data Analyst & AI Developer who writes about AI, technology, and data.

Based on the following notes and opinions, write a polished, engaging blog post in HTML format.

**Blog Title:** {title}
**Industry/Sector:** {industry}
**Tags:** {', '.join(tags) if tags else 'Technology'}

**Author's Notes & Key Points:**
{body}

**Instructions:**
1. Write in Prashanth's voice - professional but approachable, technical but accessible
2. Expand the notes into a full, well-structured blog post (800-1500 words)
3. Keep the author's opinions and perspectives intact - amplify them, don't change them
4. Use HTML formatting with <h3> for sections, <p> for paragraphs, <ul>/<li> for lists, <strong> for emphasis
5. Add an engaging introduction and a strong conclusion
6. Include relevant industry context and data points where appropriate
7. Use <hr style='border-color: #555; margin: 2rem 0;'> between major sections
8. Do NOT include the title in the output (it's handled separately)
9. Do NOT wrap in ```html``` code blocks - return raw HTML only
10. Also generate a 1-2 sentence excerpt/summary of the post
11. **AI View Section (IMPORTANT):** At the very end of the blog content, add a section titled "🤖 AI View" using <h3>. In this section, clearly state whether you (the AI) agree or disagree with the author's opinions expressed in the blog, and provide a well-reasoned explanation (3-5 sentences). Be honest and balanced — if you partially agree, say so. Style this section with a distinct visual block: <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); border-left: 4px solid #e94560; padding: 1.5rem; border-radius: 8px; margin-top: 2rem;'>

**Output Format:**
Return ONLY a JSON object with exactly these three fields:
{{"excerpt": "1-2 sentence summary here", "content": "<p>Full HTML blog content here...</p>", "ai_view": {{"agrees": true/false, "reason": "Brief explanation of AI's stance on the author's opinion"}}}}

Return valid JSON only, no markdown code fences, no extra text."""


def generate_with_claude(prompt: str) -> dict | None:
    """Generate blog post using Claude Haiku 4.5."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ⚠️  ANTHROPIC_API_KEY not set, skipping Claude")
        return None

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        response = client.messages.create(
            model="claude-haiku-4-5-20250315",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text.strip()
        
        # Try to extract JSON from response
        # Handle case where model wraps in code fences
        if text.startswith("```"):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
            text = text.strip()

        result = json.loads(text)
        if "excerpt" in result and "content" in result:
            print("  ✅ Generated with Claude Haiku 4.5")
            result["_author"] = "Claude Haiku 4.5"
            if "ai_view" not in result:
                result["ai_view"] = {"agrees": True, "reason": ""}
            return result
        else:
            print("  ⚠️  Claude response missing required fields")
            return None

    except ImportError:
        print("  ⚠️  anthropic package not installed")
        return None
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Claude returned invalid JSON: {e}")
        return None
    except Exception as e:
        print(f"  ⚠️  Claude error: {e}")
        return None


def generate_with_openai(prompt: str) -> dict | None:
    """Generate blog post using OpenAI (fallback)."""
    try:
        text = call_llm(prompt)
        if text is None:
            print("  ⚠️  OpenAI returned no response")
            return None

        text = text.strip()

        # Handle case where model wraps in code fences
        if text.startswith("```"):
            text = re.sub(r'^```\w*\n?', '', text)
            text = re.sub(r'\n?```$', '', text)
            text = text.strip()

        result = json.loads(text)
        if "excerpt" in result and "content" in result:
            print("  ✅ Generated with OpenAI (fallback)")
            result["_author"] = "OpenAI"
            if "ai_view" not in result:
                result["ai_view"] = {"agrees": True, "reason": ""}
            return result
        else:
            print("  ⚠️  OpenAI response missing required fields")
            return None

    except json.JSONDecodeError as e:
        print(f"  ⚠️  OpenAI returned invalid JSON: {e}")
        return None
    except Exception as e:
        print(f"  ⚠️  OpenAI error: {e}")
        return None


def process_draft(draft_path: Path) -> bool:
    """Process a single draft file and generate blog post."""
    slug = slugify(draft_path.stem)
    output_path = OUTPUT_DIR / f"{slug}.json"

    print(f"\n📝 Processing: {draft_path.name}")

    # Read draft
    content = draft_path.read_text(encoding="utf-8")
    content_hash = file_hash(content)

    # Check if already generated and unchanged
    if output_path.exists():
        existing = json.loads(output_path.read_text(encoding="utf-8"))
        if existing.get("source_hash") == content_hash:
            print("  ⏭️  Unchanged, skipping")
            return False

    # Parse frontmatter
    metadata, body = parse_frontmatter(content)

    if not body.strip():
        print("  ⚠️  Empty body, skipping")
        return False

    title = metadata.get("title", draft_path.stem.replace("-", " ").title())
    tags = metadata.get("tags", ["Technology"])
    date = normalize_date(metadata.get("date", datetime.now().strftime("%B %d, %Y")))
    industry = metadata.get("industry", "Technology")
    category = metadata.get("category", industry)
    insights = metadata.get("insights", "")
    author = metadata.get("author", "")  # can be overridden by frontmatter

    # Build prompt
    prompt = build_prompt(metadata, body)

    # Try Claude first, then OpenAI fallback
    result = generate_with_claude(prompt)
    if result is None:
        result = generate_with_openai(prompt)

    if result is None:
        print("  ❌ Failed to generate with both Claude and OpenAI")
        return False

    # Build output JSON
    ai_author = author if author else result.get("_author", "AI")
    ai_view = result.get("ai_view", {"agrees": True, "reason": ""})
    blog_post = {
        "slug": slug,
        "title": title,
        "date": date,
        "category": category,
        "tags": tags if isinstance(tags, list) else [tags],
        "industry": industry,
        "excerpt": result["excerpt"],
        "content": result["content"],
        "author": ai_author,
        "insights": insights,
        "ai_view": ai_view,
        "source_hash": content_hash,
        "ai_generated": True
    }

    # Save
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(blog_post, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"  💾 Saved: {output_path.name}")
    return True


def main():
    """Main entry point."""
    print("🚀 Blog Post Generator")
    print(f"   Drafts: {DRAFTS_DIR}")
    print(f"   Output: {OUTPUT_DIR}")

    if not DRAFTS_DIR.exists():
        print(f"\n❌ Drafts directory not found: {DRAFTS_DIR}")
        sys.exit(1)

    # Find all markdown drafts
    drafts = list(DRAFTS_DIR.glob("*.md"))
    if not drafts:
        print("\n📭 No drafts found")
        sys.exit(0)

    print(f"\n📋 Found {len(drafts)} draft(s)")

    generated = 0
    failed = 0
    for draft in sorted(drafts):
        if process_draft(draft):
            generated += 1
        else:
            failed += 1

    print(f"\n✨ Done! Generated {generated} new blog post(s)")
    if failed > 0 and generated == 0:
        print(f"⚠️  {failed} draft(s) failed to generate")
        sys.exit(1)


if __name__ == "__main__":
    main()
