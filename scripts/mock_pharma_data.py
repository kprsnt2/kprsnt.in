import os
import json
import random
from datetime import datetime, timedelta

def create_mock_data():
    compounds = ["Aspirin", "Imatinib", "Paxlovid", "Remdesivir", "Metformin"]
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'job_data', 'pharma_data')
    os.makedirs(out_dir, exist_ok=True)
    
    for i, c in enumerate(compounds):
        score = random.uniform(2.5, 4.8)
        data = {
            "compound_name": c,
            "pubchem_data": {
                "CanonicalSMILES": "CC(=O)OC1=CC=CC=C1C(=O)O" if c == "Aspirin" else "C1=CC=C(C=C1)NC(=O)...",
                "MolecularWeight": random.uniform(150, 600),
                "XLogP": random.uniform(0.5, 5.0)
            },
            "fda_data": "Mild interaction with CYP3A4 inhibitors." if random.random() > 0.5 else "No severe interactions noted in primary label.",
            "clinical_trials": [
                {"title": f"Phase {random.randint(1,3)} Study of {c}", "status": "RECRUITING"},
                {"title": f"Safety and Efficacy of {c} in adults", "status": "COMPLETED"}
            ],
            "admet_prediction": {
                "absorption": {"score": random.randint(3, 5), "notes": "Good oral bioavailability."},
                "distribution": {"score": random.randint(2, 5), "notes": "Moderate plasma protein binding."},
                "metabolism": {"score": random.randint(2, 4), "notes": "Hepatic metabolism observed."},
                "excretion": {"score": random.randint(3, 5), "notes": "Renal clearance."},
                "toxicity": {"score": random.randint(3, 5), "notes": "Low toxicity profile."},
                "overall_admet_score": round(score, 1)
            },
            "safety_review": {
                "ind_readiness_score": random.randint(65, 95),
                "go_no_go_decision": "GO" if score > 3 else "NO-GO",
                "risk_mitigation": ["Monitor liver enzymes", "Dose adjustment for renal impairment"],
                "executive_summary": f"The compound {c} demonstrates an acceptable safety profile for progression."
            },
            "timestamp": (datetime.now() - timedelta(days=i)).isoformat()
        }
        
        filepath = os.path.join(out_dir, f"{c.lower()}_mock.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
    # Create the global log
    log_data = {
        "pipeline_runs": [
            {
                "date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "compounds_processed": 1,
                "avg_ind_score": random.randint(70, 90),
                "go_decisions": 1 if random.random() > 0.2 else 0
            } for i in range(5)
        ]
    }
    with open(os.path.join(out_dir, '..', 'pharma_pipeline_log.json'), 'w') as f:
        json.dump(log_data, f, indent=4)
        
    print(f"Generated {len(compounds)} mock pharma files in {out_dir}")

if __name__ == "__main__":
    create_mock_data()
