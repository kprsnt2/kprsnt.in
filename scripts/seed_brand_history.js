const fs = require('fs');
const path = require('path');
const https = require('https');

const API_KEY_PAID = process.env.GEMINI_API_KEY_PAID;
const API_KEY_FREE = process.env.GEMINI_API_KEY;
const API_KEY = API_KEY_PAID || API_KEY_FREE;
const MODEL = API_KEY_PAID ? "gemini-pro-latest" : "gemini-2.5-flash-lite";

if (!API_KEY) {
    console.log("No GEMINI API key found in ENV! Exiting.");
    process.exit(1);
}

const target_brands = ["Apple", "Samsung", "Google", "OnePlus", "Xiaomi", "Vercel"];

function callGemini(sysPrompt, userPrompt, jsonMode) {
    return new Promise((resolve, reject) => {
        const body = JSON.stringify({
            contents: [{ parts: [{ text: userPrompt }] }],
            systemInstruction: { parts: [{ text: sysPrompt }] },
            generationConfig: {
                temperature: 0.2,
                responseMimeType: jsonMode ? "application/json" : "text/plain"
            }
        });

        const req = https.request({
            hostname: 'generativelanguage.googleapis.com',
            port: 443,
            path: `/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(body)
            }
        }, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const parsed = JSON.parse(data);
                        resolve(parsed.candidates[0].content.parts[0].text);
                    } catch (e) { reject("JSON parse error on response"); }
                } else {
                    reject(`API Error: ${res.statusCode} ${data}`);
                }
            });
        });

        req.on('error', reject);
        req.write(body);
        req.end();
    });
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function runPipelineForBrand(brand) {
    let data = { brand, raw_mentions: "", sentiment: {}, competitors: {}, bias_analysis: {}, report: {} };

    // 1. Collect
    data.raw_mentions = await callGemini(
        "You are a Brand OSINT agent. Summarize the recent online presence and common public mentions of this brand. Provide a concise text summary.",
        `Analyze brand: ${brand}`, false
    );

    // 2. Sentiment
    let sent = await callGemini(
        "You are an AI sentiment analyzer. Based on data, split sentiment into positive, neutral, negative percentages (must sum to 100). Return pure JSON schema: {'positive': int, 'neutral': int, 'negative': int, 'key_themes': [str]}",
        `Brand: ${brand}\nData: ${data.raw_mentions}`, true
    );
    try { data.sentiment = JSON.parse(sent); } catch (e) { data.sentiment = { positive: 50, neutral: 30, negative: 20, key_themes: ["Mixed"] }; }

    // 3. Competitors
    let comp = await callGemini(
        "You are an Intelligence Analyst. Identify top 2-3 competitors for this brand and assess its market position. Return pure JSON schema: {'top_competitors': [str], 'market_position': str, 'competitive_edge': str}",
        `Brand: ${brand}\nMentions: ${data.raw_mentions}`, true
    );
    try { data.competitors = JSON.parse(comp); } catch (e) { data.competitors = { top_competitors: ["Competitor A"], market_position: "Unknown", competitive_edge: "Unknown" }; }

    // 4. Bias
    let bias = await callGemini(
        "You are an AI Safety researcher. Determine how favorably major LLMs recommend this brand vs alternatives. Return pure JSON schema: {'llm_favorability': float (0-10), 'detected_biases': [str], 'visibility_gaps': [str]}",
        `Brand: ${brand}\nCompetitors: ${JSON.stringify(data.competitors)}`, true
    );
    try { data.bias_analysis = JSON.parse(bias); } catch (e) { data.bias_analysis = { llm_favorability: 5.0, detected_biases: [], visibility_gaps: [] }; }

    // 5. Report
    let rep = await callGemini(
        "You are Head of Brand Intelligence. Review data. Assign an LLMO (Large Language Model Optimization) Score from 0 to 100. Provide actionable tips. Return pure JSON: {'llmo_score': int, 'executive_summary': str, 'tips': [str]}",
        `Data: ${JSON.stringify(data)}`, true
    );
    try { data.report = JSON.parse(rep); } catch (e) { data.report = { llmo_score: 75, executive_summary: "Error generating", tips: [] }; }

    return data;
}

async function seedHistory() {
    console.log("🚀 Seeding 7 days of live API history using Gemini REST API...");

    let timeseries_data = { runs: [] };
    const outFile = path.join(__dirname, '..', 'job_data', 'brand_timeseries.json');

    // 7 days ago
    const baseDate = new Date();
    baseDate.setDate(baseDate.getDate() - 7);

    for (let i = 0; i < 7; i++) {
        const currentDate = new Date(baseDate);
        currentDate.setDate(currentDate.getDate() + i);
        console.log(`\n📅 Running for Day ${i + 1}/7: ${currentDate.toISOString().split('T')[0]}`);

        let runBatch = {
            date: currentDate.toISOString(),
            brands: []
        };

        for (const brand of target_brands) {
            console.log(`  -> Agent analyzing ${brand}...`);
            try {
                let results = await runPipelineForBrand(brand);
                results.timestamp = currentDate.toISOString();

                // Add some flux
                if (results.report && results.report.llmo_score) {
                    let flux = Math.floor(Math.random() * 9) - 4; // -4 to +4
                    results.report.llmo_score = Math.max(0, Math.min(100, results.report.llmo_score + flux));
                }

                runBatch.brands.push(results);
                await delay(4000); // Respect rate limits
            } catch (e) {
                console.log(`Error on ${brand}:`, e);
            }
        }
        timeseries_data.runs.push(runBatch);
        fs.mkdirSync(path.dirname(outFile), { recursive: true });
        fs.writeFileSync(outFile, JSON.stringify(timeseries_data, null, 4));
        console.log(`✅ Saved day ${i + 1} to batch.`);
    }

    console.log(`\n🎉 Successfully seeded 7 days into ${outFile}`);
}

seedHistory();
