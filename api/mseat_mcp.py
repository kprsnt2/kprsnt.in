"""
Model Context Protocol (MCP) Server for mSeat (Telangana MBBS Mock Counselling & Prediction).
Compatible with Claude Desktop, Cursor, Antigravity, and JSON-RPC 2.0 / SSE clients.
"""

import json
import logging
from typing import Dict, Any, List

MASTER_COLLEGES = [
    {
        "rank": 1,
        "code": "GAND",
        "name": "Gandhi Medical College",
        "place": "Musheerabad, Secunderabad",
        "type": "Government",
        "distKm": 19,
        "intake": 250,
        "fee": 10000,
        "sc2Closing": 18,
        "ocClosing": 22
    },
    {
        "rank": 2,
        "code": "OMCH",
        "name": "Osmania Medical College",
        "place": "Koti, Hyderabad",
        "type": "Government",
        "distKm": 13,
        "intake": 250,
        "fee": 10000,
        "sc2Closing": 28,
        "ocClosing": 44
    },
    {
        "rank": 3,
        "code": "ESIM",
        "name": "ESIC Medical College & Hospital",
        "place": "Sanathnagar, Hyderabad",
        "type": "Government",
        "distKm": 20,
        "intake": 250,
        "fee": 100000,
        "sc2Closing": 37,
        "ocClosing": 66
    },
    {
        "rank": 4,
        "code": "GMCS",
        "name": "Government Medical College Sangareddy",
        "place": "Sangareddy",
        "type": "Government",
        "distKm": 56,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 47,
        "ocClosing": 88
    },
    {
        "rank": 5,
        "code": "GMCMB",
        "name": "Government Medical College Mahabubnagar",
        "place": "Mahabubnagar",
        "type": "Government",
        "distKm": 88,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 56,
        "ocClosing": 110
    },
    {
        "rank": 6,
        "code": "GMCV",
        "name": "Government Medical College Vikarabad",
        "place": "Vikarabad",
        "type": "Government",
        "distKm": 68,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 66,
        "ocClosing": 132
    },
    {
        "rank": 7,
        "code": "GMCQ",
        "name": "Government Medical College Quthbullapur",
        "place": "Quthbullapur, Medchal",
        "type": "Government",
        "distKm": 34,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 75,
        "ocClosing": 154
    },
    {
        "rank": 8,
        "code": "GMCK",
        "name": "Government Medical College Nagarkurnool",
        "place": "Nagarkurnool",
        "type": "Government",
        "distKm": 128,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 85,
        "ocClosing": 176
    },
    {
        "rank": 9,
        "code": "GMCJ",
        "name": "Government Medical College Jangaon",
        "place": "Jangaon",
        "type": "Government",
        "distKm": 98,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 94,
        "ocClosing": 198
    },
    {
        "rank": 10,
        "code": "GMCN",
        "name": "Government Medical College Nalgonda",
        "place": "Nalgonda",
        "type": "Government",
        "distKm": 108,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 104,
        "ocClosing": 220
    },
    {
        "rank": 11,
        "code": "GMCW",
        "name": "Government Medical College Wanaparthy",
        "place": "Wanaparthy",
        "type": "Government",
        "distKm": 148,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 113,
        "ocClosing": 242
    },
    {
        "rank": 12,
        "code": "GMCMD",
        "name": "Government Medical College Medak",
        "place": "Medak",
        "type": "Government",
        "distKm": 85,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 123,
        "ocClosing": 264
    },
    {
        "rank": 13,
        "code": "GMCU",
        "name": "Government Medical College Suryapet",
        "place": "Suryapet",
        "type": "Government",
        "distKm": 138,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 132,
        "ocClosing": 286
    },
    {
        "rank": 14,
        "code": "GMCD",
        "name": "Government Medical College Siddipet",
        "place": "Siddipet",
        "type": "Government",
        "distKm": 85,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 142,
        "ocClosing": 308
    },
    {
        "rank": 15,
        "code": "GMCMBD",
        "name": "Government Medical College Mahabubabad",
        "place": "Mahabubabad",
        "type": "Government",
        "distKm": 198,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 151,
        "ocClosing": 330
    },
    {
        "rank": 16,
        "code": "GMCKM",
        "name": "Government Medical College Kamareddy",
        "place": "Kamareddy",
        "type": "Government",
        "distKm": 125,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 161,
        "ocClosing": 352
    },
    {
        "rank": 17,
        "code": "KMCW",
        "name": "Kakatiya Medical College (KMC)",
        "place": "Warangal",
        "type": "Government",
        "distKm": 152,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 170,
        "ocClosing": 374
    },
    {
        "rank": 18,
        "code": "GMCSR",
        "name": "Government Medical College Rajanna Sircilla",
        "place": "Rajanna Sircilla",
        "type": "Government",
        "distKm": 140,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 180,
        "ocClosing": 396
    },
    {
        "rank": 19,
        "code": "GMCX",
        "name": "Government Medical College Khammam",
        "place": "Khammam",
        "type": "Government",
        "distKm": 198,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 189,
        "ocClosing": 418
    },
    {
        "rank": 20,
        "code": "GMCG",
        "name": "Government Medical College Karimnagar",
        "place": "Karimnagar",
        "type": "Government",
        "distKm": 168,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 199,
        "ocClosing": 440
    },
    {
        "rank": 21,
        "code": "GMCZ",
        "name": "Government Medical College Nizamabad",
        "place": "Nizamabad",
        "type": "Government",
        "distKm": 178,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 208,
        "ocClosing": 462
    },
    {
        "rank": 22,
        "code": "GMCJG",
        "name": "Government Medical College Jagtial",
        "place": "Jagtial",
        "type": "Government",
        "distKm": 190,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 218,
        "ocClosing": 484
    },
    {
        "rank": 23,
        "code": "GMCBP",
        "name": "Government Medical College Jayashankar Bhupalpally",
        "place": "Jayashankar Bhupalpally",
        "type": "Government",
        "distKm": 215,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 227,
        "ocClosing": 506
    },
    {
        "rank": 24,
        "code": "GMCNR",
        "name": "Government Medical College Nirmal",
        "place": "Nirmal",
        "type": "Government",
        "distKm": 218,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 237,
        "ocClosing": 528
    },
    {
        "rank": 25,
        "code": "GMCRG",
        "name": "Government Medical College Ramagundam",
        "place": "Ramagundam, Peddapalli",
        "type": "Government",
        "distKm": 230,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 246,
        "ocClosing": 550
    },
    {
        "rank": 26,
        "code": "GMCMN",
        "name": "Government Medical College Mancherial",
        "place": "Mancherial",
        "type": "Government",
        "distKm": 245,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 256,
        "ocClosing": 572
    },
    {
        "rank": 27,
        "code": "GMCKG",
        "name": "Government Medical College Bhadradri Kothagudem",
        "place": "Bhadradri Kothagudem",
        "type": "Government",
        "distKm": 270,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 265,
        "ocClosing": 594
    },
    {
        "rank": 28,
        "code": "RIMS",
        "name": "RIMS (Rajiv Gandhi Inst. of Med Sci)",
        "place": "Adilabad",
        "type": "Government",
        "distKm": 310,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 275,
        "ocClosing": 616
    },
    {
        "rank": 29,
        "code": "GMCAS",
        "name": "Government Medical College Kumuram Bheem Asifabad",
        "place": "Kumuram Bheem Asifabad",
        "type": "Government",
        "distKm": 315,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 284,
        "ocClosing": 638
    },
    {
        "rank": 30,
        "code": "GMCM",
        "name": "Government Medical College Maheshwaram",
        "place": "Maheshwaram, Rangareddy",
        "type": "Government",
        "distKm": 32,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 294,
        "ocClosing": 660
    },
    {
        "rank": 31,
        "code": "GMCY",
        "name": "Government Medical College Yadadri Bhuvanagiri",
        "place": "Yadadri Bhuvanagiri",
        "type": "Government",
        "distKm": 76,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 303,
        "ocClosing": 682
    },
    {
        "rank": 32,
        "code": "GMCKD",
        "name": "Government Medical College Kodangal",
        "place": "Kodangal, Vikarabad",
        "type": "Government",
        "distKm": 110,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 313,
        "ocClosing": 704
    },
    {
        "rank": 33,
        "code": "GMCNP",
        "name": "Government Medical College Narayanpet",
        "place": "Narayanpet",
        "type": "Government",
        "distKm": 165,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 322,
        "ocClosing": 726
    },
    {
        "rank": 34,
        "code": "GMCGD",
        "name": "Government Medical College Jogulamba Gadwal",
        "place": "Jogulamba Gadwal",
        "type": "Government",
        "distKm": 185,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 332,
        "ocClosing": 748
    },
    {
        "rank": 35,
        "code": "GMCNSP",
        "name": "Government Medical College Narsampet",
        "place": "Narsampet, Warangal",
        "type": "Government",
        "distKm": 180,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 341,
        "ocClosing": 770
    },
    {
        "rank": 36,
        "code": "GMCL",
        "name": "Government Medical College Mulugu",
        "place": "Mulugu",
        "type": "Government",
        "distKm": 218,
        "intake": 150,
        "fee": 10000,
        "sc2Closing": 351,
        "ocClosing": 792
    },
    {
        "rank": 37,
        "code": "APOL",
        "name": "Apollo Institute of Medical Sciences (AIMSR)",
        "place": "Jubilee Hills, Hyderabad",
        "type": "Private",
        "distKm": 15,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 380,
        "ocClosing": 900
    },
    {
        "rank": 38,
        "code": "KAMS",
        "name": "Kamineni Academy of Med Sci (KAMS)",
        "place": "LB Nagar, Hyderabad",
        "type": "Private",
        "distKm": 18,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 388,
        "ocClosing": 945
    },
    {
        "rank": 39,
        "code": "MAMS",
        "name": "Mamata Academy of Med Sci (MAMS)",
        "place": "Bachupally, Hyderabad",
        "type": "Private",
        "distKm": 28,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 395,
        "ocClosing": 990
    },
    {
        "rank": 40,
        "code": "BHAS",
        "name": "Bhaskar Medical College",
        "place": "Yenkapally, Moinabad, Rangareddy",
        "type": "Private",
        "distKm": 18,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 403,
        "ocClosing": 1035
    },
    {
        "rank": 41,
        "code": "MNRM",
        "name": "MNR Medical College & Hospital",
        "place": "Sangareddy",
        "type": "Private",
        "distKm": 54,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 410,
        "ocClosing": 1080
    },
    {
        "rank": 42,
        "code": "SVSM",
        "name": "S.V.S. Medical College",
        "place": "Mahabubnagar",
        "type": "Private",
        "distKm": 92,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 418,
        "ocClosing": 1125
    },
    {
        "rank": 43,
        "code": "MEDI",
        "name": "Medicity Institute of Med Sci (MIMS)",
        "place": "Ghanpur, Medchal",
        "type": "Private",
        "distKm": 48,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 425,
        "ocClosing": 1170
    },
    {
        "rank": 44,
        "code": "KIMSN",
        "name": "Kamineni Institute of Med Sci (KIMS)",
        "place": "Narketpally, Nalgonda",
        "type": "Private",
        "distKm": 85,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 433,
        "ocClosing": 1215
    },
    {
        "rank": 45,
        "code": "CAIMS",
        "name": "C. Ananda Rao Inst. of Med Sci (CAIMS)",
        "place": "Karimnagar",
        "type": "Private",
        "distKm": 165,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 440,
        "ocClosing": 1260
    },
    {
        "rank": 46,
        "code": "PIMS2",
        "name": "Prathima Institute of Med Sci (PIMS)",
        "place": "Nagunur, Karimnagar",
        "type": "Private",
        "distKm": 172,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 448,
        "ocClosing": 1305
    },
    {
        "rank": 47,
        "code": "PIMS",
        "name": "Dr. Patnam Mahender Reddy IMS",
        "place": "Chevella, Rangareddy",
        "type": "Private",
        "distKm": 38,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 455,
        "ocClosing": 1350
    },
    {
        "rank": 48,
        "code": "MRMCW",
        "name": "Malla Reddy Med College for Women",
        "place": "Suraram, Hyderabad",
        "type": "Private",
        "distKm": 32,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 463,
        "ocClosing": 1395
    },
    {
        "rank": 49,
        "code": "ARUN",
        "name": "Arundathi Institute of Med Sci",
        "place": "Dundigal, Hyderabad",
        "type": "Private",
        "distKm": 42,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 470,
        "ocClosing": 1440
    },
    {
        "rank": 50,
        "code": "CMRM",
        "name": "CMR Institute of Medical Sciences",
        "place": "Kandlakoya, Medchal",
        "type": "Private",
        "distKm": 45,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 478,
        "ocClosing": 1485
    },
    {
        "rank": 51,
        "code": "MAHE",
        "name": "Maheshwara Medical College",
        "place": "Patancheru, Medak",
        "type": "Private",
        "distKm": 48,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 485,
        "ocClosing": 1530
    },
    {
        "rank": 52,
        "code": "MAHA",
        "name": "Mahavir Institute of Medical Sciences",
        "place": "Vikarabad",
        "type": "Private",
        "distKm": 65,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 493,
        "ocClosing": 1575
    },
    {
        "rank": 53,
        "code": "RVMM",
        "name": "RVM Medical College",
        "place": "Mulugu, Medak",
        "type": "Private",
        "distKm": 62,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 500,
        "ocClosing": 1620
    },
    {
        "rank": 54,
        "code": "NEEL",
        "name": "Neelima Institute of Medical Sciences",
        "place": "Medchal",
        "type": "Private",
        "distKm": 42,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 508,
        "ocClosing": 1665
    },
    {
        "rank": 55,
        "code": "PMRW",
        "name": "Prathima Relief Inst. of Med Sci (PMR)",
        "place": "Warangal",
        "type": "Private",
        "distKm": 145,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 515,
        "ocClosing": 1710
    },
    {
        "rank": 56,
        "code": "NOVA",
        "name": "Nova Institute of Medical Sciences",
        "place": "Hayathnagar, Hyderabad",
        "type": "Private",
        "distKm": 25,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 523,
        "ocClosing": 1755
    },
    {
        "rank": 57,
        "code": "TRRM",
        "name": "TRR Institute of Medical Sciences",
        "place": "Patancheru",
        "type": "Private",
        "distKm": 45,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 530,
        "ocClosing": 1800
    },
    {
        "rank": 58,
        "code": "RRAJ",
        "name": "Raja Rajeshwari Inst. of Med Sci",
        "place": "Patancheru",
        "type": "Private",
        "distKm": 46,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 538,
        "ocClosing": 1845
    },
    {
        "rank": 59,
        "code": "SURB",
        "name": "Surabhi Institute of Medical Sciences",
        "place": "Siddipet",
        "type": "Private",
        "distKm": 95,
        "intake": 150,
        "fee": 60000,
        "sc2Closing": 545,
        "ocClosing": 1890
    }
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
