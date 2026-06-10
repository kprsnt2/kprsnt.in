#!/usr/bin/env python3
import os
import json
import time
import httpx
from datetime import datetime
from ai_config import call_llm as _call_llm

# Fallback wrapper for AI calls — uses shared ai_config
def call_llm(system_prompt: str, user_prompt: str, temperature=0.2, json_mode=False) -> str:
    """Calls the shared LLM function from ai_config with OpenAI primary + NVIDIA fallback.
    Falls back to mock responses if all API calls fail."""
    import builtins
    if not hasattr(builtins, "USE_MOCK_APIS"):
        builtins.USE_MOCK_APIS = False

    openai_key = os.environ.get("OPENAI_API_KEY")
    nvidia_key = os.environ.get("NVIDIA_API_KEY")

    if not openai_key and not nvidia_key:
        print("⚠️ No API keys found! Using mock responses for demo.")
        builtins.USE_MOCK_APIS = True

    if not builtins.USE_MOCK_APIS:
        result = _call_llm(
            prompt=user_prompt,
            system_prompt=system_prompt,
            json_mode=json_mode,
            temperature=temperature,
        )
        if result is not None:
            return result
        print("⚠️ All API calls failed. Falling back to mocks...")

    # Mock response if both fail or if keys are missing
    print("🤖 Using offline local mock fallback")
    if json_mode:
        import re
        if "admet" in system_prompt.lower():
            return json.dumps({
                "absorption": {"score": 4, "notes": "Good oral bioavailability."},
                "distribution": {"score": 3, "notes": "Moderate plasma protein binding."},
                "metabolism": {"score": 2, "notes": "Extensive hepatic metabolism (CYP3A4)."},
                "excretion": {"score": 4, "notes": "Renal clearance is primary."},
                "toxicity": {"score": 3, "notes": "Hepatotoxicity risk at high doses."},
                "overall_admet_score": 3.2
            })
        elif "final safety" in system_prompt.lower():
            return json.dumps({
                "ind_readiness_score": 85,
                "go_no_go_decision": "GO with precautions",
                "risk_mitigation": ["Monitor AST/ALT", "Adjust dose for renal impaired"],
                "executive_summary": "Compound shows strong efficacy with manageable safety profile."
            })
    return "This is a mocked LLM plain text response for testing."

class PharmaPipeline:
    def __init__(self, target_compound: str):
        self.target = target_compound
        self.data = {
            "compound_name": target_compound,
            "pubchem_data": None,
            "fda_data": None,
            "clinical_trials": [],
            "admet_prediction": None,
            "safety_review": None,
            "timestamp": datetime.now().isoformat()
        }

    def fetch_pubchem_data(self):
        print(f"🔍 Agent 1: Ingesting Molecule & Fetching PubChem Data for {self.target}...")
        try:
            # Using REST API path for compound name
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{self.target}/property/MolecularFormula,MolecularWeight,CanonicalSMILES,XLogP,Complexity/JSON"
            r = httpx.get(url, timeout=10)
            if r.status_code == 200:
                props = r.json()["PropertyTable"]["Properties"][0]
                self.data["pubchem_data"] = props
                print(f"   => Found SMILES: {props.get('CanonicalSMILES')}")
            else:
                print("   => PubChem request failed. Using mock data.")
                self.data["pubchem_data"] = {
                    "MolecularFormula": "Ctest", "MolecularWeight": 350.5,
                    "CanonicalSMILES": "CC(=O)OC1=CC=CC=C1C(=O)O", "XLogP": 2.1
                }
        except Exception as e:
            print(f"Exception: {e}")
            self.data["pubchem_data"] = {"CanonicalSMILES": "UNKNOWN"}

    def fetch_fda_interactions(self):
        print(f"⚠️ Agent 2: Cross-referencing OpenFDA for interactions...")
        try:
            url = f"https://api.fda.gov/drug/label.json?search=drug_interactions:\"{self.target}\"&limit=1"
            r = httpx.get(url, timeout=10)
            if r.status_code == 200:
                results = r.json().get("results", [])
                if results and "drug_interactions" in results[0]:
                    self.data["fda_data"] = results[0]["drug_interactions"][0][:500] + "..."
                    print("   => Found FDA interactions data.")
                else:
                    self.data["fda_data"] = "No severe interactions found in primary openFDA labels."
            else:
                self.data["fda_data"] = "Query returned no results or failed."
        except Exception:
            self.data["fda_data"] = "Data unavailable."

    def fetch_clinical_trials(self):
        print(f"🏥 Agent 3: Querying ClinicalTrials.gov API v2...")
        try:
            url = f"https://clinicaltrials.gov/api/v2/studies?query.cond={self.target}&pageSize=3"
            r = httpx.get(url, timeout=10)
            if r.status_code == 200:
                studies = r.json().get("studies", [])
                trials = []
                for s in studies:
                    protocol = s.get("protocolSection", {})
                    ident = protocol.get("identificationModule", {})
                    status = protocol.get("statusModule", {})
                    trials.append({
                        "nctId": ident.get("nctId"),
                        "title": ident.get("briefTitle"),
                        "status": status.get("overallStatus")
                    })
                self.data["clinical_trials"] = trials
                print(f"   => Found {len(trials)} recent trials.")
            else:
                self.data["clinical_trials"] = [{"title": "Mock Phase 2 Trial", "status": "COMPLETED"}]
        except Exception:
            self.data["clinical_trials"] = []

    def predict_admet(self):
        print(f"🧬 Agent 4: LLM ADMET Prediction...")
        sys_prompt = "You are an expert computational chemist and pharmacologist. Given molecular properties and SMILES, predict the ADMET profile. Return pure JSON."
        user_prompt = f"Compound: {self.target}\nProperties: {json.dumps(self.data['pubchem_data'])}\nOutput JSON schema:\n{{'absorption': {{'score': 1-5, 'notes': ''}}, 'distribution': {{...}}, 'metabolism': {{...}}, 'excretion': {{...}}, 'toxicity': {{...}}, 'overall_admet_score': float 1-5}}"
        
        response = call_llm(sys_prompt, user_prompt, json_mode=True)
        try:
            # Strip markdown blocks if present
            clean_resp = response.replace('```json', '').replace('```', '').strip()
            self.data["admet_prediction"] = json.loads(clean_resp)
        except Exception as e:
            print("Failed to parse ADMET JSON:", e)
            self.data["admet_prediction"] = {"overall_admet_score": 3.0}

    def safety_review(self):
        print(f"✅ Agent 5: Generating Final Safety Review & IND Readiness...")
        sys_prompt = "You are the Lead Toxicologist. Review the compound's ADMET, FDA interactions, and trial history. Give a final GO/NO-GO decision and an IND Readiness Score. Return pure JSON."
        user_prompt = f"Data: {json.dumps(self.data)}\nOutput JSON:\n{{'ind_readiness_score': 0-100, 'go_no_go_decision': 'GO' or 'NO-GO', 'risk_mitigation': ['list'], 'executive_summary': '...'}}"
        
        response = call_llm(sys_prompt, user_prompt, json_mode=True)
        try:
            clean_resp = response.replace('```json', '').replace('```', '').strip()
            self.data["safety_review"] = json.loads(clean_resp)
        except Exception:
            self.data["safety_review"] = {
                "ind_readiness_score": 75,
                "go_no_go_decision": "GO",
                "risk_mitigation": [],
                "executive_summary": "Parsing error on LLM output."
            }

    def run(self):
        self.fetch_pubchem_data()
        self.fetch_fda_interactions()
        self.fetch_clinical_trials()
        self.predict_admet()
        self.safety_review()
        return self.data


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "Imatinib"
    print(f"\n🚀 Starting PharmaPipeline for: {target}\n")
    start = time.time()
    pipeline = PharmaPipeline(target)
    results = pipeline.run()
    duration = time.time() - start
    
    # Save the output
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'job_data', 'pharma_data')
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{target.lower()}_{datetime.now().strftime('%Y%m%d')}.json"
    filepath = os.path.join(out_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=4)
        
    print(f"\n✨ Pipeline complete in {duration:.1f}s. Saved to {filepath}")
    print(f"IND Score: {results['safety_review'].get('ind_readiness_score')}")
    print(f"Decision:  {results['safety_review'].get('go_no_go_decision')}")
