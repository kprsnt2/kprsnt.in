import os
import json
import random
from datetime import datetime, timedelta

def create_mock_brand_data():
    brands = ["Apple", "Tesla", "Notion", "Vercel", "Figma"]
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'job_data', 'brand_data')
    os.makedirs(out_dir, exist_ok=True)
    
    for i, b in enumerate(brands):
        score = random.randint(65, 98)
        
        data = {
            "brand": b,
            "raw_mentions": f"Analyzed 1,500+ recent internet mentions, social media threads, and news articles regarding {b}. Overall sentiment shows strong recognition of product quality but mixed feelings on recent pricing changes.",
            "sentiment": {
                "positive": random.randint(50, 80),
                "neutral": random.randint(10, 30),
                "negative": random.randint(5, 20),
                "key_themes": ["Innovation", "Premium Quality", "Ecosystem Lock-in" if b=="Apple" else "Fast Shipping" ]
            },
            "competitors": {
                "top_competitors": ["Competitor A", "Competitor B"] if b not in ["Apple", "Tesla"] else ["Samsung" if b=="Apple" else "Rivian", "Google" if b=="Apple" else "Lucid"],
                "market_position": "Dominant Leader" if score > 85 else "Strong Contender",
                "competitive_edge": "Ecosystem and brand loyalty"
            },
            "bias_analysis": {
                "llm_favorability": round(random.uniform(6.5, 9.8), 1),
                "detected_biases": [
                    "Frequently recommended as the absolute best choice in default settings.",
                    "Rarely mentions controversies unless explicitly prompted."
                ],
                "visibility_gaps": [
                    "Less recommended for budget-conscious users."
                ]
            },
            "report": {
                "llmo_score": score,
                "recommendation_score": random.randint(70, 95),
                "accuracy_score": random.randint(80, 99),
                "executive_summary": f"The model evaluation for {b} shows highly favorable LLM presence. It is consistently recommended over competitors in top-K generation.",
                "tips": [
                    "Improve visibility in budget-related queries.",
                    "Continue dominating technical documentation training sets."
                ]
            },
            "timestamp": (datetime.now() - timedelta(hours=i*12)).isoformat()
        }
        
        filepath = os.path.join(out_dir, f"{b.replace(' ', '_').lower()}_mock.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
    # Create the global log
    log_data = {
        "pipeline_runs": [
            {
                "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "brands_analyzed": random.randint(2, 5),
                "avg_llmo_score": random.randint(75, 88),
                "anomalies_detected": random.randint(0, 2)
            } for i in range(5)
        ]
    }
    log_path = os.path.join(out_dir, '..', 'brand_pipeline_log.json')
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=4)
        
    print(f"Generated {len(brands)} mock brand files in {out_dir}")

if __name__ == "__main__":
    create_mock_brand_data()
