from fastapi import APIRouter, HTTPException
from database.firebase import db
from collections import defaultdict
from user_agents import parse

router = APIRouter()
@router.get("/{uid}/urls")
async def get_user_urls(uid: str):
    user_ref = db.collection("users").document(uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    
    urls_ref = user_ref.collection("urls")
    docs = urls_ref.stream()

    urls_dict = {}
    for doc in docs:
        doc_data = doc.to_dict()
        urls_dict[doc.id] = doc_data.get("urls", [])

    return {"groups": urls_dict}

@router.get("/{code}/referrers")
async def get_refferer_counts(code: str):
    """Get a dictionary of all referrers and their counts."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    referrer_counts = defaultdict(int)

    for visit in visits:
        referrer = visit.to_dict().get("referrer", "Direct")
        referrer_counts[referrer] += 1

    return {"referrers": dict(referrer_counts)}

@router.get("/{code}/access-dates")
async def get_access_dates(code: str):
    """Get a dictionary of all access dates and their counts."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    date_counts = defaultdict(int)

    for visit in visits:
        timestamp = visit.to_dict().get("timestamp")
        if timestamp:
            date = timestamp.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
            date_counts[date] += 1

    return {"access_dates": dict(date_counts)}

@router.get("/{code}/hourly-patterns")
async def get_hourly_access_patterns(code: str):
    """Get a dictionary of hourly access patterns."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    hourly_counts = defaultdict(int)

    for visit in visits:
        timestamp = visit.to_dict().get("timestamp")
        if timestamp:
            hour = timestamp.strftime("%H")  # Extract hour (24-hour format)
            hourly_counts[hour] += 1

    return {"hourly_patterns": dict(hourly_counts)}

@router.get("/{code}/ip-addresses")
async def get_ip_address_counts(code: str):
    """Get a dictionary of IP addresses and their counts."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    ip_counts = defaultdict(int)

    for visit in visits:
        ip = visit.to_dict().get("ip", "Unknown")
        ip_counts[ip] += 1

    return {"ip_addresses": dict(ip_counts)}

@router.get("/{code}/unique-visitors")
async def get_unique_visitors(code: str):
    """Get the count of unique visitors based on IP addresses."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    unique_ips = set()

    for visit in visits:
        ip = visit.to_dict().get("ip")
        if ip:
            unique_ips.add(ip)

    return {"unique_visitors": len(unique_ips)}

@router.get("/{code}/referrer-sources")
async def get_referrer_sources(code: str):
    """Get a breakdown of referrer sources."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    referrer_counts = defaultdict(int)

    for visit in visits:
        referrer = visit.to_dict().get("referrer", "Direct")
        referrer_counts[referrer] += 1

    return {"referrer_sources": dict(referrer_counts)}

@router.get("/{code}/user-agents")
async def get_user_agent_counts(code: str):
    """Get a dictionary of user agents and their counts."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    user_agent_counts = defaultdict(int)

    for visit in visits:
        user_agent = visit.to_dict().get("user_agent", "Unknown")
        user_agent_counts[user_agent] += 1

    return {"user_agents": dict(user_agent_counts)}

@router.get("/{code}/timezones")
async def get_timezone_counts(code: str):
    """Get a dictionary of timezones and their counts."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    timezone_counts = defaultdict(int)

    for visit in visits:
        timestamp = visit.to_dict().get("timestamp")
        if timestamp:
            timezone = timestamp.tzinfo.zone if timestamp.tzinfo else "Unknown"
            timezone_counts[timezone] += 1

    return {"timezones": dict(timezone_counts)}

@router.get("/{code}/browser-os")
async def get_browser_os_breakdown(code: str):
    """Get a breakdown of browsers and operating systems."""
    visits_ref = db.collection("urls").document(code).collection("visits")
    visits = visits_ref.stream()

    browser_counts = defaultdict(int)
    os_counts = defaultdict(int)

    for visit in visits:
        user_agent = visit.to_dict().get("user_agent", "")
        parsed_ua = parse(user_agent)
        browser_counts[parsed_ua.browser.family] += 1
        os_counts[parsed_ua.os.family] += 1

    return {"browsers": dict(browser_counts), "operating_systems": dict(os_counts)}