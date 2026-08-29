"""
RESTful Endpoints & OpenAPI 3.0 Specification for OpenAI Actions (ChatGPT) and MCP.
"""

from flask import Blueprint, request, jsonify
try:
    from mseat_mcp import (
        handle_predict_seat,
        handle_college_info,
        handle_compare_colleges,
        handle_sliding_odds,
        handle_counselling_rules,
        MASTER_COLLEGES
    )
except ImportError:
    from api.mseat_mcp import (
        handle_predict_seat,
        handle_college_info,
        handle_compare_colleges,
        handle_sliding_odds,
        handle_counselling_rules,
        MASTER_COLLEGES
    )

OPENAPI_SPEC = {
    "openapi": "3.1.0",
    "info": {
        "title": "mSeat — Telangana MBBS Mock Counselling & Prediction API",
        "description": "API for predicting MBBS college seat allotments, exploring 59 medical colleges in Telangana, comparing institutions, and calculating sliding odds.",
        "version": "1.0.0"
    },
    "servers": [
        {"url": "https://kprsnt.in"}
    ],
    "paths": {
        "/api/mseat/predict": {
            "post": {
                "summary": "Predict MBBS seat allotment and safety margin",
                "operationId": "predictSeat",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "air": {"type": "integer", "description": "NEET All India Rank (e.g. 175420)"},
                                    "state_rank": {"type": "integer", "description": "Telangana State General Serial Number (e.g. 3561)"},
                                    "category": {
                                        "type": "string",
                                        "enum": ["OC", "EWS", "BC_A", "BC_B", "BC_C", "BC_D", "BC_E", "SC_1", "SC_2", "SC_3", "SC", "ST"],
                                        "description": "Reservation Category / Caste Group"
                                    },
                                    "gender": {
                                        "type": "string",
                                        "enum": ["female", "male"],
                                        "description": "Candidate Gender"
                                    }
                                },
                                "required": ["category"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Seat prediction results",
                        "content": {"application/json": {}}
                    }
                }
            },
            "get": {
                "summary": "Predict MBBS seat allotment via query parameters",
                "operationId": "predictSeatGet",
                "parameters": [
                    {"name": "air", "in": "query", "schema": {"type": "integer"}, "description": "NEET AIR"},
                    {"name": "state_rank", "in": "query", "schema": {"type": "integer"}, "description": "Telangana State Rank"},
                    {"name": "category", "in": "query", "required": True, "schema": {"type": "string"}, "description": "Category (OC, EWS, SC_1, SC_2, ST, etc.)"},
                    {"name": "gender", "in": "query", "schema": {"type": "string"}, "description": "Gender (female/male)"}
                ],
                "responses": {
                    "200": {
                        "description": "Seat prediction results",
                        "content": {"application/json": {}}
                    }
                }
            }
        },
        "/api/mseat/colleges": {
            "get": {
                "summary": "Get details for medical colleges in Telangana",
                "operationId": "getColleges",
                "parameters": [
                    {"name": "query", "in": "query", "required": True, "schema": {"type": "string"}, "description": "College name or code (e.g. OMCH, Gandhi, Arundathi)"}
                ],
                "responses": {
                    "200": {
                        "description": "College details list",
                        "content": {"application/json": {}}
                    }
                }
            }
        },
        "/api/mseat/compare": {
            "get": {
                "summary": "Compare two medical colleges side-by-side",
                "operationId": "compareColleges",
                "parameters": [
                    {"name": "college_a", "in": "query", "required": True, "schema": {"type": "string"}},
                    {"name": "college_b", "in": "query", "required": True, "schema": {"type": "string"}}
                ],
                "responses": {
                    "200": {
                        "description": "Comparison results",
                        "content": {"application/json": {}}
                    }
                }
            }
        },
        "/api/mseat/sliding": {
            "get": {
                "summary": "Calculate Round 1 to Round 2 sliding probability",
                "operationId": "calculateSlidingOdds",
                "parameters": [
                    {"name": "current_college", "in": "query", "required": True, "schema": {"type": "string"}},
                    {"name": "target_college", "in": "query", "required": True, "schema": {"type": "string"}},
                    {"name": "category_rank", "in": "query", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {
                        "description": "Sliding odds and recommendations",
                        "content": {"application/json": {}}
                    }
                }
            }
        },
        "/api/mseat/rules": {
            "get": {
                "summary": "Get official KNRUHS counselling rules, fee structures, and document verification checklists",
                "operationId": "getCounsellingRules",
                "parameters": [
                    {"name": "topic", "in": "query", "schema": {"type": "string", "enum": ["fees", "documents", "reservations", "sliding", "all"]}}
                ],
                "responses": {
                    "200": {
                        "description": "Counselling rules",
                        "content": {"application/json": {}}
                    }
                }
            }
        }
    }
}
