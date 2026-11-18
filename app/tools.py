"""
StartupSetu Agent Tools
Tools derived from the DPIIT Startup Recognition Guide Project Card:
- check_dpiit_eligibility: Evaluates startup eligibility based on DPIIT criteria.
- get_scheme_details: Retrieves details on government funding & support schemes.
- submit_dpiit_application: Prepares and records an official application (sensitive action).
- query_rag: Calls the StartupSetu RAG pipeline for official document knowledge & citations.
"""

from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.rag import rag_answer

BASE_DIR = Path(__file__).resolve().parent.parent
APPLICATIONS_FILE = BASE_DIR / "data" / "applications.json"

# Known Government Schemes Registry for StartupSetu
SCHEMES_REGISTRY: Dict[str, Dict[str, Any]] = {
    "seed_fund": {
        "name": "Startup India Seed Fund Scheme (SISFS)",
        "funding": "Up to ₹20 Lakhs for validation/PoC; up to ₹50 Lakhs for commercialization (debt/convertible debenture)",
        "eligibility": "DPIIT-recognized startup incorporated not more than 2 years prior, with viable proof of concept.",
        "portal": "https://seedfund.startupindia.gov.in/",
        "category": "Funding"
    },
    "tax_exemption_80iac": {
        "name": "Section 80-IAC Income Tax Exemption",
        "funding": "100% tax rebate on profits for 3 consecutive financial years out of the first 10 years",
        "eligibility": "DPIIT-recognized Private Limited Company or LLP incorporated on or after April 1, 2016.",
        "portal": "https://www.startupindia.gov.in/content/sih/en/startup-scheme/tax-exemption.html",
        "category": "Taxation"
    },
    "credit_guarantee": {
        "name": "Credit Guarantee Scheme for Startups (CGSS)",
        "funding": "Collateral-free credit guarantee up to ₹10 Crore per borrower through member lending institutions.",
        "eligibility": "DPIIT-recognized startups with proven revenue or funded through SEBI-registered AIFs.",
        "portal": "https://www.startupindia.gov.in/",
        "category": "Credit"
    },
    "ipr_rebate": {
        "name": "Startups Intellectual Property Protection (SIPP)",
        "funding": "Up to 80% rebate on patent filing fees and 50% on trademark fees with free facilitation support.",
        "eligibility": "All DPIIT-recognized startups holding a valid certificate.",
        "portal": "https://www.startupindia.gov.in/",
        "category": "IPR"
    },
    "maharashtra_seed": {
        "name": "Maharashtra State Innovation Society (MSInS) Seed Support",
        "funding": "Grant support and access to incubation centers across Maharashtra districts.",
        "eligibility": "Startups registered in Maharashtra with state DPIIT recognition.",
        "portal": "https://www.msins.in/",
        "category": "State Policy"
    }
}


def check_dpiit_eligibility(
    entity_type: str,
    incorporation_year: int,
    annual_turnover_cr: float,
    is_innovative: bool = True,
    current_year: int = 2026
) -> Dict[str, Any]:
    """
    Check if a startup satisfies official DPIIT Recognition Criteria:
    1. Entity Type: Private Limited, LLP, or Registered Partnership (Sole proprietorship is ineligible).
    2. Age: Not older than 10 years from incorporation.
    3. Turnover: Annual turnover has never exceeded ₹100 Crore in any financial year.
    4. Innovation / Scalability: Working towards innovation or scalable business model.
    """
    normalized_entity = entity_type.strip().lower()
    valid_entities = [
        "private limited",
        "private limited company",
        "pvt ltd",
        "pvt. ltd.",
        "llp",
        "limited liability partnership",
        "registered partnership",
        "partnership firm"
    ]

    entity_ok = any(e in normalized_entity for e in valid_entities)
    years_active = max(0, current_year - incorporation_year)
    age_ok = years_active <= 10
    turnover_ok = annual_turnover_cr <= 100.0
    innovation_ok = bool(is_innovative)

    is_eligible = entity_ok and age_ok and turnover_ok and innovation_ok

    reasons: List[str] = []
    if not entity_ok:
        reasons.append(
            f"Entity type '{entity_type}' is not recognized. Must be Private Limited Company, LLP, or Registered Partnership."
        )
    if not age_ok:
        reasons.append(
            f"Startup age ({years_active} years) exceeds the maximum limit of 10 years from incorporation."
        )
    if not turnover_ok:
        reasons.append(
            f"Turnover (₹{annual_turnover_cr} Cr) exceeds the maximum allowed limit of ₹100 Crore."
        )
    if not innovation_ok:
        reasons.append(
            "Startup must be working towards innovation, development or improvement of products/services or a scalable business model."
        )

    benefits: List[str] = []
    if is_eligible:
        benefits = [
            "Access to Section 80-IAC 3-year income tax exemption",
            "Exemption under Section 56(2)(viib) (Angel Tax)",
            "80% rebate on patent filings and 50% on trademark fees",
            "Eligibility for Startup India Seed Fund Scheme (up to ₹50 Lakhs)",
            "Self-certification under 6 Labour Laws and 3 Environmental Laws",
            "Fast-tracked patent application examination",
            "Relaxed public procurement criteria (exemption from Prior Experience and EMD)"
        ]

    summary = (
        "Congratulations! Your startup satisfies all DPIIT Startup Recognition criteria."
        if is_eligible
        else f"Startup is not currently eligible: {'; '.join(reasons)}"
    )

    return {
        "is_eligible": is_eligible,
        "criteria": {
            "entity_type_valid": entity_ok,
            "age_under_10_years": age_ok,
            "turnover_under_100cr": turnover_ok,
            "innovative_scalable": innovation_ok
        },
        "years_active": years_active,
        "annual_turnover_cr": annual_turnover_cr,
        "reasons": reasons,
        "summary": summary,
        "recommended_benefits": benefits
    }


def get_scheme_details(scheme_query: str) -> Dict[str, Any]:
    """
    Search and retrieve verified government startup schemes by name or category.
    """
    q = scheme_query.strip().lower()

    # Exact key match
    if q in SCHEMES_REGISTRY:
        return {"found": True, "scheme": SCHEMES_REGISTRY[q]}

    # Partial match
    matches = []
    for key, data in SCHEMES_REGISTRY.items():
        if (
            q in key
            or q in data["name"].lower()
            or q in data["category"].lower()
            or q in data["funding"].lower()
        ):
            matches.append(data)

    if matches:
        return {
            "found": True,
            "total_matches": len(matches),
            "scheme": matches[0],
            "all_matches": matches
        }

    return {
        "found": False,
        "message": f"No direct government scheme matching '{scheme_query}' in local registry.",
        "available_schemes": [s["name"] for s in SCHEMES_REGISTRY.values()]
    }


def query_rag(question: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Query the StartupSetu RAG pipeline to retrieve verified document chunks,
    official citations (source URL, title, page), and refusal handling.
    """
    return rag_answer(question=question, top_k=top_k)


def submit_dpiit_application(
    startup_name: str,
    entity_type: str,
    founder_name: str,
    email: str,
    sector: str = "Technology",
    turnover_cr: float = 0.5,
    incorporation_year: int = 2024
) -> Dict[str, Any]:
    """
    Record an application for DPIIT Recognition.
    NOTE: This is a sensitive action that modifies application state.
    """
    APPLICATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)

    applications: List[Dict[str, Any]] = []
    if APPLICATIONS_FILE.exists():
        try:
            with open(APPLICATIONS_FILE, "r", encoding="utf-8") as f:
                applications = json.load(f)
        except Exception:
            applications = []

    application_id = f"DPIIT-APP-{len(applications) + 1:04d}"
    submission_record = {
        "application_id": application_id,
        "startup_name": startup_name.strip(),
        "entity_type": entity_type.strip(),
        "founder_name": founder_name.strip(),
        "email": email.strip(),
        "sector": sector.strip(),
        "turnover_cr": turnover_cr,
        "incorporation_year": incorporation_year,
        "status": "SUBMITTED",
        "created_at": datetime.now().isoformat()
    }

    applications.append(submission_record)

    with open(APPLICATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(applications, f, indent=2, ensure_ascii=False)

    return {
        "status": "success",
        "message": f"Application {application_id} for '{startup_name}' successfully submitted.",
        "application": submission_record
    }


AVAILABLE_TOOLS = {
    "check_dpiit_eligibility": check_dpiit_eligibility,
    "get_scheme_details": get_scheme_details,
    "query_rag": query_rag,
    "submit_dpiit_application": submit_dpiit_application
}

