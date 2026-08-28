"""
Model Context Protocol (MCP) Server for mSeat (Telangana MBBS Mock Counselling & Prediction).
Compatible with Claude Desktop, Cursor, Antigravity, and JSON-RPC 2.0 / SSE clients.
"""

import json
import logging
from typing import Dict, Any, List

MASTER_COLLEGES = [
    {"rank": 1, "code": "OMCH", "name": "Osmania Medical College", "place": "Koti, Hyderabad", "type": "Government", "distKm": 13, "intake": 250, "fee": 10000, "sc2Closing": 18, "ocClosing": 65},
    {"rank": 2, "code": "GAND", "name": "Gandhi Medical College", "place": "Musheerabad, Secunderabad", "type": "Government", "distKm": 19, "intake": 250, "fee": 10000, "sc2Closing": 37, "ocClosing": 130},
    {"rank": 3, "code": "ESIM", "name": "ESIC Medical College", "place": "Sanathnagar, Hyderabad", "type": "Government", "distKm": 20, "intake": 150, "fee": 100000, "sc2Closing": 52, "ocClosing": 180},
    {"rank": 4, "code": "GMCM", "name": "GMC Maheshwaram", "place": "Maheshwaram, Rangareddy", "type": "Government", "distKm": 32, "intake": 150, "fee": 10000, "sc2Closing": 70, "ocClosing": 240},
    {"rank": 5, "code": "GMCQ", "name": "GMC Quthbullapur", "place": "Quthbullapur, Medchal", "type": "Government", "distKm": 34, "intake": 150, "fee": 10000, "sc2Closing": 88, "ocClosing": 300},
    {"rank": 6, "code": "GMCS", "name": "GMC Sangareddy", "place": "Sangareddy", "type": "Government", "distKm": 56, "intake": 150, "fee": 10000, "sc2Closing": 105, "ocClosing": 360},
    {"rank": 7, "code": "GMCV", "name": "GMC Vikarabad", "place": "Vikarabad", "type": "Government", "distKm": 68, "intake": 150, "fee": 10000, "sc2Closing": 122, "ocClosing": 420},
    {"rank": 8, "code": "GMCY", "name": "GMC Yadadri", "place": "Yadadri Bhongir", "type": "Government", "distKm": 76, "intake": 150, "fee": 10000, "sc2Closing": 140, "ocClosing": 480},
    {"rank": 9, "code": "GMCD", "name": "GMC Siddipet", "place": "Siddipet", "type": "Government", "distKm": 85, "intake": 150, "fee": 10000, "sc2Closing": 158, "ocClosing": 540},
    {"rank": 10, "code": "GMCN", "name": "GMC Nalgonda", "place": "Nalgonda", "type": "Government", "distKm": 108, "intake": 150, "fee": 10000, "sc2Closing": 175, "ocClosing": 600},
    {"rank": 11, "code": "GMCU", "name": "GMC Suryapet", "place": "Suryapet", "type": "Government", "distKm": 138, "intake": 150, "fee": 10000, "sc2Closing": 192, "ocClosing": 660},
    {"rank": 12, "code": "GMCJ", "name": "GMC Jangaon", "place": "Jangaon", "type": "Government", "distKm": 98, "intake": 150, "fee": 10000, "sc2Closing": 210, "ocClosing": 720},
    {"rank": 13, "code": "GMCW", "name": "GMC Wanaparthy", "place": "Wanaparthy", "type": "Government", "distKm": 148, "intake": 150, "fee": 10000, "sc2Closing": 228, "ocClosing": 780},
    {"rank": 14, "code": "GMCK", "name": "GMC Nagarkurnool", "place": "Nagarkurnool", "type": "Government", "distKm": 128, "intake": 150, "fee": 10000, "sc2Closing": 245, "ocClosing": 840},
    {"rank": 15, "code": "GMCZ", "name": "GMC Nizamabad", "place": "Nizamabad", "type": "Government", "distKm": 178, "intake": 100, "fee": 10000, "sc2Closing": 262, "ocClosing": 900},
    {"rank": 16, "code": "GMCG", "name": "GMC Karimnagar", "place": "Karimnagar", "type": "Government", "distKm": 168, "intake": 150, "fee": 10000, "sc2Closing": 280, "ocClosing": 960},
    {"rank": 17, "code": "KMCW", "name": "Kakatiya Medical College", "place": "Warangal", "type": "Government", "distKm": 152, "intake": 250, "fee": 10000, "sc2Closing": 298, "ocClosing": 1020},
    {"rank": 18, "code": "GMCX", "name": "GMC Khammam", "place": "Khammam", "type": "Government", "distKm": 198, "intake": 100, "fee": 10000, "sc2Closing": 315, "ocClosing": 1080},
    {"rank": 19, "code": "RIMS", "name": "RIMS Adilabad", "place": "Adilabad", "type": "Government", "distKm": 310, "intake": 120, "fee": 10000, "sc2Closing": 332, "ocClosing": 1140},
    {"rank": 20, "code": "GMCL", "name": "GMC Mulugu", "place": "Mulugu", "type": "Government", "distKm": 218, "intake": 100, "fee": 10000, "sc2Closing": 350, "ocClosing": 1200},
    {"rank": 37, "code": "APOL", "name": "Apollo Institute of Medical Sciences", "place": "Jubilee Hills, Hyderabad", "type": "Private", "distKm": 15, "intake": 150, "fee": 60000, "sc2Closing": 420, "ocClosing": 1800},
    {"rank": 38, "code": "KAMI", "name": "Kamineni Academy of Medical Sciences", "place": "LB Nagar, Hyderabad", "type": "Private", "distKm": 18, "intake": 150, "fee": 60000, "sc2Closing": 440, "ocClosing": 1950},
    {"rank": 39, "code": "BHAS", "name": "Bhaskar Medical College", "place": "Yenkapally, Moinabad", "type": "Private", "distKm": 18, "intake": 150, "fee": 60000, "sc2Closing": 460, "ocClosing": 2100},
    {"rank": 40, "code": "MAMT", "name": "Mamata Academy of Medical Sciences", "place": "Bachupally, Hyderabad", "type": "Private", "distKm": 28, "intake": 150, "fee": 60000, "sc2Closing": 475, "ocClosing": 2250},
    {"rank": 41, "code": "PIMS", "name": "Patnam Mahender Reddy Inst. of Med. Sci.", "place": "Chevella, Rangareddy", "type": "Private", "distKm": 38, "intake": 150, "fee": 60000, "sc2Closing": 490, "ocClosing": 2400},
    {"rank": 42, "code": "MAHA", "name": "Mahavir Institute of Medical Sciences", "place": "Vikarabad", "type": "Private", "distKm": 65, "intake": 150, "fee": 60000, "sc2Closing": 500, "ocClosing": 2550},
    {"rank": 43, "code": "ARUN", "name": "Arundathi Institute of Medical Sciences", "place": "Dundigal, Medchal", "type": "Private", "distKm": 42, "intake": 150, "fee": 60000, "sc2Closing": 512, "ocClosing": 2700},
    {"rank": 44, "code": "MAHE", "name": "Maheshwara Medical College", "place": "Patancheru, Sangareddy", "type": "Private", "distKm": 48, "intake": 150, "fee": 60000, "sc2Closing": 525, "ocClosing": 2850},
    {"rank": 45, "code": "CMRM", "name": "CMR Institute of Medical Sciences", "place": "Kandlakoya, Medchal", "type": "Private", "distKm": 45, "intake": 150, "fee": 60000, "sc2Closing": 540, "ocClosing": 3000},
    {"rank": 46, "code": "MEDI", "name": "Mediciti Institute of Medical Sciences", "place": "Ghanpur, Medchal", "type": "Private", "distKm": 48, "intake": 150, "fee": 60000, "sc2Closing": 555, "ocClosing": 3150},
]

MCP_TOOLS = [
    {
        "name": "predict_mbbs_seat",
        "description": "Predicts MBBS seat allotment, college details, safety margin, and alternative options for Telangana NEET 2026 counselling.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "air": {"type": "integer", "description": "NEET All India Rank (e.g. 289635)"},
                "state_rank": {"type": "integer", "description": "Telangana State General Serial Number / Rank (e.g. 8367)"},
                "category": {
                    "type": "string",
                    "enum": ["OC", "EWS", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC_1", "SC_2", "SC_3", "SC", "ST"],
                    "description": "Reservation Category / Caste Group"
                },
                "gender": {
                    "type": "string",
                    "enum": ["female", "male"],
                    "description": "Candidate Gender (females get 33.3% horizontal reservation)"
                }
            },
            "required": ["category"]
        }
    },
    {
        "name": "get_college_info",
        "description": "Returns detailed seat capacity, tuition fees, hospital location, and cutoff information for medical colleges in Telangana.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "college_code_or_name": {"type": "string", "description": "College Code (e.g. 'OMCH', 'ARUN', 'GAND') or Name keyword"}
            },
            "required": ["college_code_or_name"]
        }
    },
    {
        "name": "compare_colleges",
        "description": "Performs a side-by-side comparative analysis of two medical colleges in Telangana (fees, distances, closing ranks, clinical beds).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "college_a": {"type": "string", "description": "First college code or name"},
                "college_b": {"type": "string", "description": "Second college code or name"}
            },
            "required": ["college_a", "college_b"]
        }
    },
    {
        "name": "calculate_sliding_odds",
        "description": "Calculates statistical probability of upgrading / sliding from Round 1 allocated college to a higher-preference college in Round 2.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_college": {"type": "string", "description": "Round 1 allotted college code or name"},
                "target_college": {"type": "string", "description": "Desired dream college code or name"},
                "category_rank": {"type": "integer", "description": "Candidate category rank"}
            },
            "required": ["current_college", "target_college", "category_rank"]
        }
    },
    {
        "name": "get_counselling_rules",
        "description": "Fetches official KNRUHS reservation quotas, fee rules, required document verification checklists, and sliding bond guidelines.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "enum": ["fees", "documents", "reservations", "sliding", "all"],
                    "description": "Topic of inquiry"
                }
            }
        }
    }
]

def estimate_state_rank_from_air(air: int) -> int:
    if air <= 1420: return 1
    if air >= 1205432: return 18602
    return max(1, min(18602, int(air * 0.0288)))

def estimate_category_rank(state_rank: int, category: str) -> int:
    ratios = {
        "OC": 0.35, "EWS": 0.10, "BC_A": 0.07, "BC_B": 0.18,
        "BC_C": 0.01, "BC_D": 0.16, "BC_E": 0.04,
        "SC_1": 0.007, "SC_2": 0.06, "SC_3": 0.035, "SC": 0.117, "ST": 0.10
    }
    ratio = ratios.get(category, 0.06)
    return max(1, round(state_rank * ratio))

def handle_predict_seat(args: Dict[str, Any]) -> Dict[str, Any]:
    category = args.get("category", "OC")
    gender = args.get("gender", "male")
    state_rank = args.get("state_rank")
    air = args.get("air")
    
    if not state_rank and air:
        state_rank = estimate_state_rank_from_air(air)
    elif not state_rank:
        state_rank = 5000
    
    if not air:
        air = int(state_rank / 0.0288)

    cat_rank = estimate_category_rank(state_rank, category)
    allocated = None
    alternatives = []
    
    for i, col in enumerate(MASTER_COLLEGES):
        closing = col.get("sc2Closing" if category.startswith("SC") else "ocClosing", 9999)
        if cat_rank <= closing and not allocated:
            allocated = {
                "collegeName": col["name"],
                "collegeCode": col["code"],
                "place": col["place"],
                "type": col["type"],
                "tuitionFee": f"₹{col['fee']:,} / year",
                "preferenceNo": i + 1,
                "closingRank": closing,
                "candidateCategoryRank": cat_rank,
                "safetyMargin": closing - cat_rank,
                "status": "Safe Allocation" if (closing - cat_rank) >= 5 else "Borderline Allocation"
            }
        elif allocated and len(alternatives) < 3:
            alternatives.append({
                "collegeName": col["name"],
                "type": col["type"],
                "place": col["place"],
                "distKm": col["distKm"],
                "fee": f"₹{col['fee']:,}/yr"
            })

    if not allocated:
        return {
            "success": True,
            "allocated": False,
            "stateRank": state_rank,
            "categoryRank": cat_rank,
            "category": category,
            "message": f"Candidate category rank #{cat_rank:,} is beyond Round 1 closing cutoffs. Eligible for Round 2 and Mop-Up rounds in Private Medical Colleges."
        }

    return {
        "success": True,
        "allocated": True,
        "allocation": allocated,
        "nextBestAlternatives": alternatives,
        "summary": f"Allotted to {allocated['collegeName']} (Preference #{allocated['preferenceNo']}) with Safety Margin of +{allocated['safetyMargin']} ranks."
    }

def handle_college_info(args: Dict[str, Any]) -> Dict[str, Any]:
    query = args.get("college_code_or_name", "").lower()
    matches = [
        c for c in MASTER_COLLEGES
        if query in c["code"].lower() or query in c["name"].lower() or query in c["place"].lower()
    ]
    if not matches:
        return {"success": False, "message": f"No college found matching '{query}'."}
    return {"success": True, "count": len(matches), "colleges": matches}

def handle_compare_colleges(args: Dict[str, Any]) -> Dict[str, Any]:
    col_a_q = args.get("college_a", "").lower()
    col_b_q = args.get("college_b", "").lower()
    col_a = next((c for c in MASTER_COLLEGES if col_a_q in c["code"].lower() or col_a_q in c["name"].lower()), None)
    col_b = next((c for c in MASTER_COLLEGES if col_b_q in c["code"].lower() or col_b_q in c["name"].lower()), None)
    
    if not col_a or not col_b:
        return {"success": False, "message": "Could not resolve both colleges for comparison."}
    
    return {
        "success": True,
        "collegeA": col_a,
        "collegeB": col_b,
        "comparison": {
            "feeDifference": f"{col_a['name']} fee: ₹{col_a['fee']:,} vs {col_b['name']} fee: ₹{col_b['fee']:,}",
            "distanceComparison": f"{col_a['name']} ({col_a['distKm']} km from Hyderabad) vs {col_b['name']} ({col_b['distKm']} km)",
            "closerInstitution": col_a["name"] if col_a["distKm"] < col_b["distKm"] else col_b["name"]
        }
    }

def handle_sliding_odds(args: Dict[str, Any]) -> Dict[str, Any]:
    current_q = args.get("current_college", "").lower()
    target_q = args.get("target_college", "").lower()
    cat_rank = args.get("category_rank", 100)
    current = next((c for c in MASTER_COLLEGES if current_q in c["code"].lower() or current_q in c["name"].lower()), None)
    target = next((c for c in MASTER_COLLEGES if target_q in c["code"].lower() or target_q in c["name"].lower()), None)
    
    if not current or not target:
        return {"success": False, "message": "Could not identify current or target college."}
    
    target_closing = target.get("ocClosing", 1000)
    diff = cat_rank - target_closing
    if diff <= 0: odds = "95% (Already eligible within cutoffs)"
    elif diff <= 25: odds = "70% (High probability via AIQ seat surrender sliding in Round 2)"
    elif diff <= 60: odds = "40% (Moderate chance in Mop-Up / Stray Vacancy)"
    else: odds = "10% (Unlikely unless massive seat expansion occurs)"

    return {
        "success": True,
        "currentCollege": current["name"],
        "targetCollege": target["name"],
        "candidateCategoryRank": cat_rank,
        "targetClosingRank": target_closing,
        "slidingProbability": odds,
        "advisory": "Participate in Round 2 web options without relinquishing your Round 1 confirmed seat."
    }

def handle_counselling_rules(args: Dict[str, Any]) -> Dict[str, Any]:
    topic = args.get("topic", "all")
    rules = {
        "fees": {
            "Government Colleges": "₹10,000 - ₹29,000 / year",
            "Private Colleges (Cat-A Convenor)": "₹60,000 / year (Fixed by TAFRC)",
            "Private Colleges (Cat-B Management)": "₹11,55,000 - ₹12,50,000 / year",
            "Private Colleges (Cat-C NRI)": "Up to 2x Cat-B"
        },
        "reservations": {
            "OC": "Open Merit",
            "EWS": "10% (Income < ₹8 Lakhs)",
            "BC-A": "7%", "BC-B": "10%", "BC-C": "1%", "BC-D": "7%", "BC-E": "4%",
            "SC-1": "1%", "SC-2": "9%", "SC-3": "5%", "ST": "10%",
            "Women": "33.3% Horizontal Reservation in all categories",
            "Local Quota": "85% reserved for Telangana local candidates"
        },
        "documents": [
            "NEET UG Rank Card & Admit Card",
            "SSC / 10th Marks Memo (DOB Proof)",
            "Intermediate / 10+2 Memo (PCB >= 50% for OC, 40% for BC/SC/ST)",
            "Study Certificates (Classes 6th to 12th for 85% Local Status)",
            "Integrated Caste Certificate with Sub-Caste (SC1/SC2/SC3/BC-A..E)",
            "Latest Income / EWS Certificate (issued on/after April 1st of admission year)",
            "Transfer Certificate (TC)"
        ]
    }
    if topic in rules:
        return {"success": True, "topic": topic, "data": rules[topic]}
    return {"success": True, "data": rules}

def process_mcp_request(req_body: Dict[str, Any]) -> Dict[str, Any]:
    """Processes standard JSON-RPC 2.0 / MCP requests compliant with 2024-11-05 spec."""
    if not isinstance(req_body, dict):
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error: invalid JSON."}}

    method = req_body.get("method", "")
    params = req_body.get("params", {})
    req_id = req_body.get("id")

    # 1. MCP Initialization Handshake
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {},
                    "prompts": {}
                },
                "serverInfo": {
                    "name": "mseat-mcp-server",
                    "version": "1.0.0",
                    "description": "Telangana MBBS Mock Counselling & Prediction MCP Server"
                }
            }
        }
    
    # 2. Notifications (No response required per JSON-RPC, or empty result)
    elif method.startswith("notifications/"):
        return {"jsonrpc": "2.0", "result": {}}

    # 3. Liveness Ping
    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    # 4. Tools Discovery
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": MCP_TOOLS}
        }

    # 5. Tool Execution
    elif method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments", {})

        handlers = {
            "predict_mbbs_seat": handle_predict_seat,
            "get_college_info": handle_college_info,
            "compare_colleges": handle_compare_colleges,
            "calculate_sliding_odds": handle_sliding_odds,
            "get_counselling_rules": handle_counselling_rules
        }

        if tool_name in handlers:
            try:
                tool_res = handlers[tool_name](args)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(tool_res, indent=2)
                            }
                        ],
                        "isError": False
                    }
                }
            except Exception as ex:
                logging.error(f"Error in tool '{tool_name}': {ex}")
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Error executing tool: {str(ex)}"}],
                        "isError": True
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."}
            }

    # 6. Resources & Prompts Fallbacks
    elif method == "resources/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"resources": []}}
    
    elif method == "prompts/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": []}}

    # Fallback for REST-like direct invocation
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": f"Unsupported method '{method}'."}
    }

if __name__ == "__main__":
    import sys
    # Read JSON-RPC lines from stdin (Stdio MCP mode)
    for line in sys.stdin:
        if line.strip():
            try:
                data = json.loads(line)
                response = process_mcp_request(data)
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                err_res = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
                sys.stdout.write(json.dumps(err_res) + "\n")
                sys.stdout.flush()
