// Migrate blog posts from hardcoded HTML in index.py to JSON files
const fs = require('fs');
const path = require('path');

const src = fs.readFileSync(path.join(__dirname, '..', 'api', 'index.py'), 'utf8');
const blogDir = path.join(__dirname, '..', 'blog_data');
if (!fs.existsSync(blogDir)) fs.mkdirSync(blogDir, { recursive: true });

const posts = [
  { slug: 'manipulating-llm-recommendations-brand-influence', title: 'How I Made an LLM Recommend My Fake Phone Brand Over iPhone and Pixel', date: 'January 25, 2026', category: 'AI & LLMs', excerpt: 'An experiment in AI influence: I fine-tuned a 20B model to recommend fictional brands Blankphone and Neitherphone, achieving 76% accuracy vs 25% for the base model.', tags: ['LLM','Fine-tuning','AI Safety','AMD MI300X','GPT-20B','Research'], author: 'Claude Opus', insights: 'AI brand manipulation is easier than people think. This experiment shows why AI safety research matters.' },
  { slug: 'fine-tuning-gpt-oss-20b-drug-discovery', title: 'Fine-Tuning a 20B Parameter LLM for Drug Discovery: A Journey with AMD MI300X', date: 'January 20, 2026', category: 'Drug Discovery', excerpt: '12 hours, countless commits, and lessons learned along the way.', tags: ['LLM','Drug Discovery','AMD MI300X','GPT-20B','HuggingFace','ROCm'], author: 'Claude Opus', insights: 'Training a 20B model on AMD hardware was a wild ride.' },
  { slug: 'fine-tuning-drug-discovery-llm', title: 'Fine-Tuning Drug Discovery LLMs: 5 Hours, 30 Commits, AMD GPU Struggles', date: 'December 20, 2025', category: 'Drug Discovery', excerpt: 'How I trained text classification models for drug approval prediction.', tags: ['LLM','Drug Discovery','AMD','HuggingFace'], author: 'Claude Opus', insights: 'ChemBERTa showed me that domain-specific models can outperform general LLMs.' },
  { slug: 'building-pharmagenesis-ai', title: 'Building PharmaGenesis AI: A Dual-AI Drug Discovery Platform', date: 'December 15, 2025', category: 'Drug Discovery', excerpt: 'How I built a comprehensive drug discovery platform using Claude + Gemini AI with 6 feature phases.', tags: ['AI','Drug Discovery','Claude','Gemini'], author: 'Claude Opus', insights: 'Using two competing AI models for drug analysis gives diversity of perspective.' },
  { slug: 'building-mylocalcli', title: 'Building MyLocalCLI: A Claude Code Alternative', date: 'December 10, 2025', category: 'AI & LLMs', excerpt: 'How I built a privacy-focused AI coding assistant with 6 providers, 26 tools, and full local control.', tags: ['AI','CLI','Node.js'], author: 'Claude Opus', insights: 'Built this because I needed Claude Code functionality but with full control.' },
  { slug: 'fine-tuning-mistral-7b', title: 'Fine-Tuning Mistral-7B with QLoRA', date: 'November 15, 2025', category: 'AI & LLMs', excerpt: 'A practical guide to fine-tuning large language models on consumer hardware using LoRA techniques.', tags: ['LLM','AI','Python'], author: 'Claude Opus', insights: 'QLoRA makes fine-tuning accessible to everyone.' },
  { slug: 'deploying-llms-on-gcp', title: 'Self-Hosting LLMs on Google Cloud Run', date: 'October 20, 2025', category: 'DevOps & Cloud', excerpt: 'Running Ollama and Open WebUI on Google Cloud for a private, scalable AI chatbot.', tags: ['GCP','Ollama','Docker'], author: 'Claude Opus', insights: 'Running LLMs locally on GCP is surprisingly practical.' },
];

for (const post of posts) {
  const slugIdx = src.indexOf(`"slug": "${post.slug}"`);
  if (slugIdx === -1) { console.log(`SKIP: ${post.slug} not found`); continue; }

  const marker = `"content": """`;
  const cStart = src.indexOf(marker, slugIdx);
  if (cStart === -1) { console.log(`SKIP: no content for ${post.slug}`); continue; }

  const contentStart = cStart + marker.length;
  const contentEnd = src.indexOf('"""', contentStart);
  if (contentEnd === -1) { console.log(`SKIP: no end for ${post.slug}`); continue; }

  post.content = src.substring(contentStart, contentEnd).trim();

  const outPath = path.join(blogDir, `${post.slug}.json`);
  // Don't overwrite existing files (like the ones already in blog_data)
  fs.writeFileSync(outPath, JSON.stringify(post, null, 2), 'utf8');
  console.log(`✅ ${post.slug}`);
}

console.log('Done!');
