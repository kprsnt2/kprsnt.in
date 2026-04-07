/**
 * Migration script: Add career-ops style evaluations to existing job data.
 * Also creates daily snapshot from monthly files.
 * Run: node scripts/migrate_jobs.js
 */
const fs = require('fs');
const path = require('path');

const JOB_DATA_DIR = path.join(__dirname, '..', 'job_data');
const DAILY_DIR = path.join(JOB_DATA_DIR, 'daily');

// Skills lookup for matching
const ALL_SKILLS = [
  'python', 'javascript', 'typescript', 'sql', 'flask', 'react', 'next.js',
  'llm', 'fine-tuning', 'pytorch', 'huggingface', 'rag', 'embeddings',
  'gemini', 'claude', 'openai', 'nvidia', 'ollama',
  'bigquery', 'vercel', 'docker', 'github actions',
  'pandas', 'numpy', 'tableau', 'looker', 'power bi',
  'mcp', 'tool calling', 'function calling',
  'prompt engineering', 'multi-model', 'agent', 'agentic',
  'data analysis', 'machine learning', 'ai', 'ml',
  'fastapi', 'streamlit', 'node.js',
];

const ARCHETYPES = {
  'ai-engineer': { name: 'AI Engineer / LLM Engineer', signals: ['llm', 'fine-tuning', 'model', 'inference', 'pytorch', 'huggingface', 'rag', 'embeddings', 'vector', 'prompt engineering', 'agent', 'agentic'], weight: 1.0 },
  'data-analyst': { name: 'Senior Data Analyst', signals: ['sql', 'bigquery', 'dashboard', 'analytics', 'reporting', 'etl', 'tableau', 'looker', 'data pipeline', 'visualization'], weight: 0.8 },
  'prompt-engineer': { name: 'Prompt Engineer', signals: ['prompt', 'context engineering', 'few-shot', 'chain-of-thought', 'llm', 'evaluation', 'red teaming', 'ai safety'], weight: 0.9 },
  'clinical-healthcare': { name: 'Clinical/Healthcare AI', signals: ['clinical', 'healthcare', 'pharma', 'drug', 'medical', 'hipaa', 'fda', 'biomedical', 'therapeutic', 'molecular'], weight: 0.85 },
  'ml-engineer': { name: 'ML Engineer', signals: ['machine learning', 'ml pipeline', 'model serving', 'mlops', 'training', 'deployment', 'inference', 'tensorflow', 'scikit'], weight: 0.95 },
};

const PRIMARY_ROLES = ['ai engineer', 'llm engineer', 'generative ai developer', 'ml engineer'];
const SECONDARY_ROLES = ['senior data analyst', 'prompt engineer', 'data manager'];

function detectArchetype(job) {
  const text = `${job.title || ''} ${(job.tags || []).join(' ')} ${job.why_match || ''}`.toLowerCase();
  let bestMatch = 'ai-engineer';
  let bestScore = 0;
  
  for (const [slug, arch] of Object.entries(ARCHETYPES)) {
    const score = arch.signals.filter(s => text.includes(s)).length * arch.weight;
    if (score > bestScore) { bestScore = score; bestMatch = slug; }
  }
  return bestMatch;
}

function evaluateJob(job) {
  const title = (job.title || '').toLowerCase();
  const tags = (job.tags || []).map(t => t.toLowerCase());
  const location = (job.location || '').toLowerCase();
  const why = (job.why_match || '').toLowerCase();
  const allText = `${title} ${tags.join(' ')} ${location} ${why}`;

  // CV Match (0-5)
  const skillMatches = ALL_SKILLS.filter(s => allText.includes(s)).length;
  const cvMatch = Math.min(5, (skillMatches / (ALL_SKILLS.length * 0.15)) * 5);

  // Archetype Fit (0-5)
  const archetype = detectArchetype(job);
  let archetypeFit = 3.0;
  if (['ai-engineer', 'ml-engineer'].includes(archetype)) {
    archetypeFit = PRIMARY_ROLES.some(r => title.includes(r)) ? 4.5 : 3.5;
  } else if (['data-analyst', 'prompt-engineer'].includes(archetype)) {
    archetypeFit = SECONDARY_ROLES.some(r => title.includes(r)) ? 4.0 : 3.0;
  } else {
    archetypeFit = 3.5;
  }

  // Comp Analysis (0-5)
  const salary = job.salary || '';
  let comp = 3.0;
  if (salary) {
    comp = 3.5;
    if (/100,000|120,000|150,000|\$1/.test(salary)) comp = 4.5;
    if (/30,00,000|40,00,000|50,00,000/.test(salary)) comp = 4.0;
  }

  // Culture Signals (0-5)
  let culture = 3.0;
  if (location.includes('remote')) culture += 1.0;
  if (tags.some(t => ['ai', 'llm', 'machine learning', 'generative ai'].includes(t))) culture += 0.5;
  if (tags.some(t => ['startup', 'growth'].includes(t))) culture += 0.3;
  culture = Math.min(5, culture);

  // Red Flags
  const redFlags = [];
  if (/\bsf\b|san francisco/.test(location)) redFlags.push('SF-based, needs relocation/visa');
  if (allText.includes('us only') || allText.includes('us citizens')) redFlags.push('US only — visa required');
  if (/senior manager|director/.test(title)) redFlags.push('May be over-leveled');
  const penalty = redFlags.length * 0.3;

  // Overall
  let overall = cvMatch * 0.30 + archetypeFit * 0.25 + comp * 0.15 + culture * 0.20 + (5.0 - penalty) * 0.10;
  overall = Math.max(1, Math.min(5, overall));

  // Grade
  let grade;
  if (overall >= 4.5) grade = 'A';
  else if (overall >= 4.0) grade = 'A-';
  else if (overall >= 3.5) grade = 'B+';
  else if (overall >= 3.0) grade = 'B';
  else if (overall >= 2.5) grade = 'C+';
  else grade = 'C';

  // Recommendation
  let rec;
  if (overall >= 4.0) rec = 'Strong match — recommend applying immediately';
  else if (overall >= 3.5) rec = 'Good match — worth applying';
  else if (overall >= 3.0) rec = 'Decent match — apply if specifically interested';
  else rec = 'Weak match — consider skipping';

  return {
    overall_score: Math.round(overall * 10) / 10,
    grade,
    cv_match: Math.round(cvMatch * 10) / 10,
    archetype_fit: Math.round(archetypeFit * 10) / 10,
    comp_analysis: Math.round(comp * 10) / 10,
    culture_signals: Math.round(culture * 10) / 10,
    red_flags: redFlags,
    archetype: ARCHETYPES[archetype]?.name || archetype,
    recommendation: rec,
  };
}

// Proof point mapping
const PROOF_POINTS = [
  { name: 'BrandXY', url: 'https://huggingface.co/kprsnt/BrandXY-gpt-oss-20b', metric: '76% LLM manipulation rate', tags: ['llm', 'fine-tuning', 'ai safety', 'evaluation'] },
  { name: 'Drug Discovery GPT-20B', url: 'https://huggingface.co/kprsnt/drug-discovery-gpt-20b', metric: '20B model for molecular analysis', tags: ['llm', 'healthcare', 'fine-tuning', 'pytorch'] },
  { name: 'MyLocalCLI', url: 'https://mlc.kprsnt.in', metric: '6 AI providers, 26 tools, 5 agents', tags: ['agents', 'cli', 'multi-model', 'tool calling'] },
  { name: 'PharmaGenesis AI', url: 'https://pharmgenai.kprsnt.in', metric: 'Dual-AI drug discovery', tags: ['claude', 'gemini', 'healthcare', 'react'] },
  { name: 'MCP Job Server', url: 'https://github.com/kprsnt2/kprsnt.in', metric: 'MCP protocol server with 5 tools', tags: ['mcp', 'tool calling', 'agents'] },
];

function mapProofPoints(job) {
  const jobTags = (job.tags || []).map(t => t.toLowerCase());
  const allText = `${(job.title || '').toLowerCase()} ${jobTags.join(' ')}`;
  
  return PROOF_POINTS
    .map(pp => {
      const matchingTags = pp.tags.filter(t => jobTags.some(jt => jt.includes(t) || t.includes(jt)));
      const textMatch = pp.tags.some(t => allText.includes(t));
      if (matchingTags.length > 0 || textMatch) {
        return { project: pp.name, url: pp.url, relevance: pp.metric, matching_tags: matchingTags };
      }
      return null;
    })
    .filter(Boolean)
    .sort((a, b) => b.matching_tags.length - a.matching_tags.length)
    .slice(0, 4);
}

// Main migration
function migrate() {
  console.log('🔄 Migrating existing job data with evaluations...\n');
  
  // Create daily directory
  if (!fs.existsSync(DAILY_DIR)) {
    fs.mkdirSync(DAILY_DIR, { recursive: true });
  }

  // Find all monthly JSON files
  const files = fs.readdirSync(JOB_DATA_DIR).filter(f => f.endsWith('.json') && !f.includes('pipeline_log'));
  
  for (const file of files) {
    const filePath = path.join(JOB_DATA_DIR, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    const jobs = data.jobs || [];
    let migrated = 0;

    for (const job of jobs) {
      if (!job.evaluation) {
        job.evaluation = evaluateJob(job);
        migrated++;
      }
      if (!job.proof_points) {
        job.proof_points = mapProofPoints(job);
      }
    }

    if (migrated > 0) {
      data.pipeline_version = '2.0.0';
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
      console.log(`  ✅ ${file}: ${migrated} jobs evaluated`);
    }

    // Create daily snapshot
    const genDate = data.generated_date || '';
    if (genDate) {
      const dailyPath = path.join(DAILY_DIR, `${genDate}.json`);
      if (!fs.existsSync(dailyPath)) {
        const grades = {};
        let topMatches = 0;
        let totalScore = 0;
        for (const job of jobs) {
          const ev = job.evaluation || {};
          const grade = ev.grade || '?';
          grades[grade] = (grades[grade] || 0) + 1;
          if ((ev.overall_score || 0) >= 3.5) topMatches++;
          totalScore += ev.overall_score || 0;
        }

        const dailyData = {
          date: genDate,
          pipeline_version: '2.0.0 (migrated)',
          profile_summary: data.profile_summary || '',
          report: {
            date: genDate,
            summary: {
              total_jobs: jobs.length,
              top_matches: topMatches,
              grade_a_count: (grades['A'] || 0) + (grades['A-'] || 0),
              grade_b_count: (grades['B+'] || 0) + (grades['B'] || 0),
              average_score: jobs.length > 0 ? Math.round((totalScore / jobs.length) * 100) / 100 : 0,
              verified_count: jobs.filter(j => j.verified).length,
            },
            by_archetype: {},
            by_location: {},
          },
          trace: { duration_seconds: 0, total_tokens: 0, errors: 0 },
          jobs: jobs,
        };

        fs.writeFileSync(dailyPath, JSON.stringify(dailyData, null, 2), 'utf-8');
        console.log(`  📅 Created daily snapshot: ${genDate}.json`);
      }
    }
  }

  // Create pipeline log
  const logPath = path.join(JOB_DATA_DIR, 'pipeline_log.json');
  if (!fs.existsSync(logPath)) {
    const log = files.map(f => {
      const data = JSON.parse(fs.readFileSync(path.join(JOB_DATA_DIR, f), 'utf-8'));
      const jobs = data.jobs || [];
      const evalScores = jobs.map(j => j.evaluation?.overall_score || 0);
      return {
        date: data.generated_date || data.date || f.replace('.json', ''),
        total_jobs: jobs.length,
        top_matches: evalScores.filter(s => s >= 3.5).length,
        avg_score: jobs.length > 0 ? Math.round((evalScores.reduce((a, b) => a + b, 0) / jobs.length) * 100) / 100 : 0,
        grade_a: jobs.filter(j => (j.evaluation?.grade || '').startsWith('A')).length,
        duration_seconds: 0,
        total_tokens: 0,
        errors: 0,
      };
    });
    fs.writeFileSync(logPath, JSON.stringify(log, null, 2), 'utf-8');
    console.log(`  📊 Created pipeline_log.json`);
  }

  console.log('\n✨ Migration complete!');
}

migrate();
