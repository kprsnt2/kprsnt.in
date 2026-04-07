const fs = require('fs');
const path = require('path');

const target_brands = ["Apple", "Samsung", "Google Pixel", "Pfizer", "BioNTech", "Vercel"];

function generateFakeResults(brand) {
    return {
        brand: brand,
        raw_mentions: `Aggregated data for ${brand} across sources...`,
        sentiment: {
            positive: Math.floor(Math.random() * 40) + 40,
            neutral: Math.floor(Math.random() * 20) + 10,
            negative: Math.floor(Math.random() * 20),
            key_themes: ["Performance", "Pricing", "Support"]
        },
        competitors: {
            top_competitors: ["Competitor X", "Competitor Y"],
            market_position: "Strong",
            competitive_edge: "Quality"
        },
        bias_analysis: {
            llm_favorability: Number((Math.random() * 4 + 5).toFixed(1)), // 5.0 to 9.0
            detected_biases: ["Slight positive skew in comparisons", "Recommended often"],
            visibility_gaps: ["Missing in abstract contexts"]
        },
        report: {
            llmo_score: Math.floor(Math.random() * 30) + 65, // 65 to 95
            recommendation_score: Math.floor(Math.random() * 20) + 70,
            accuracy_score: Math.floor(Math.random() * 20) + 80,
            executive_summary: `LLM representation for ${brand} remains robust across tested domains.`,
            tips: ["Optimize budget segmentation representation"]
        }
    };
}

let timeseries_data = { runs: [] };
const outFile = path.join(__dirname, '..', 'job_data', 'brand_timeseries.json');

const baseDate = new Date();
baseDate.setDate(baseDate.getDate() - 7);

// Create a stateful "base" score for each brand so the line chart looks contiguous, not just totally random
const baseScores = {};
target_brands.forEach(b => baseScores[b] = Math.floor(Math.random() * 20) + 70);

for (let i = 0; i < 7; i++) {
    const currentDate = new Date(baseDate);
    currentDate.setDate(currentDate.getDate() + i);
    
    let runBatch = {
        date: currentDate.toISOString(),
        brands: []
    };
    
    for (const brand of target_brands) {
        let results = generateFakeResults(brand);
        results.timestamp = currentDate.toISOString();
        
        // Contiguous random walk
        let flux = Math.floor(Math.random() * 7) - 3; // -3 to +3
        baseScores[brand] = Math.max(0, Math.min(100, baseScores[brand] + flux));
        results.report.llmo_score = baseScores[brand];
        
        runBatch.brands.push(results);
    }
    timeseries_data.runs.push(runBatch);
}

fs.mkdirSync(path.dirname(outFile), { recursive: true });
fs.writeFileSync(outFile, JSON.stringify(timeseries_data, null, 4));
console.log(`\n🎉 Successfully seeded 7 days of contiguous historical data into ${outFile}`);
