"""
TradesPro MCP Server
====================
An MCP server providing AI agents with tools for skilled trades businesses:
- Residential building code lookups (IRC/NEC/UPC)
- Material cost estimation for common jobs
- Job scope templates with labor hour estimates
- Permit requirement checker

Built with FastMCP. API key monetization with free and pro tiers.
"""

import json
import logging
import os
import time

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext, CallNext
from fastmcp.tools.tool import ToolResult
from mcp.types import TextContent

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# AUTH CONFIG
# ---------------------------------------------------------------------------

FREE_DEMO_KEY = "trades_demo_2026"
FREE_TIER_LIMIT = 10  # calls per hour
UPGRADE_URL = "https://tradespros.gumroad.com/l/yyzov"

def _load_api_keys() -> dict[str, str]:
    """Load API key -> tier mapping from API_KEYS env var."""
    raw = os.environ.get("API_KEYS", "")
    if not raw:
        return {}
    try:
        keys = json.loads(raw)
        if not isinstance(keys, dict):
            logger.warning("API_KEYS env var is not a JSON object, ignoring")
            return {}
        return keys
    except json.JSONDecodeError:
        logger.warning("API_KEYS env var is not valid JSON, ignoring")
        return {}


# ---------------------------------------------------------------------------
# RATE LIMITING
# ---------------------------------------------------------------------------

# In-memory rate tracking: key -> {"count": int, "window_start": float}
_rate_limits: dict[str, dict] = {}


def _check_rate_limit(session_key: str) -> tuple[bool, int]:
    """Check if a session has exceeded the free tier rate limit.

    Returns (allowed, remaining_calls).
    """
    now = time.time()
    if session_key not in _rate_limits:
        _rate_limits[session_key] = {"count": 0, "window_start": now}

    bucket = _rate_limits[session_key]

    # Reset window if an hour has passed
    if now - bucket["window_start"] >= 3600:
        bucket["count"] = 0
        bucket["window_start"] = now

    if bucket["count"] >= FREE_TIER_LIMIT:
        return False, 0

    bucket["count"] += 1
    remaining = FREE_TIER_LIMIT - bucket["count"]
    return True, remaining


# ---------------------------------------------------------------------------
# AUTH MIDDLEWARE
# ---------------------------------------------------------------------------

class AuthMiddleware(Middleware):
    """API key authentication and rate limiting middleware.

    - Checks X-API-Key header on tool calls
    - Free tier (no key / demo key): 10 calls/hour, footer appended
    - Pro tier (valid paid key): unlimited, no footer
    - Tool listing (tools/list) is NOT gated so directories can introspect
    """

    async def on_call_tool(self, context, call_next):
        # Resolve tier from API key header
        headers = get_http_headers(include={"x-api-key"})
        api_key = headers.get("x-api-key", "")
        tier = self._resolve_tier(api_key)

        if tier == "pro":
            # Pro tier: unlimited, no modifications
            return await call_next(context)

        # Free tier: enforce rate limit
        session_key = api_key if api_key else "anonymous"
        allowed, remaining = _check_rate_limit(session_key)

        if not allowed:
            return ToolResult(content=[TextContent(
                type="text",
                text=(
                    f"## Rate limit exceeded\n\n"
                    f"You've used all {FREE_TIER_LIMIT} free calls this hour.\n\n"
                    f"Get unlimited access with a Pro API key at {UPGRADE_URL}\n\n"
                    f"Your limit resets in about {self._minutes_until_reset(session_key)} minutes."
                ),
            )])

        # Execute the tool
        result = await call_next(context)

        # Append free tier footer to the result
        footer = (
            f"\n\n---\n"
            f"\U0001f513 Free tier - {remaining} calls remaining this hour "
            f"({FREE_TIER_LIMIT}/hour). "
            f"Get unlimited access at {UPGRADE_URL}"
        )

        if result.content:
            last = result.content[-1]
            if isinstance(last, TextContent):
                result.content[-1] = TextContent(
                    type="text",
                    text=last.text + footer,
                )
            else:
                result.content.append(TextContent(type="text", text=footer))
        else:
            result.content = [TextContent(type="text", text=footer)]

        return result

    def _resolve_tier(self, api_key: str) -> str:
        """Determine the tier for a given API key."""
        if not api_key or api_key == FREE_DEMO_KEY:
            return "free"

        api_keys = _load_api_keys()
        tier = api_keys.get(api_key)
        if tier == "pro":
            return "pro"

        # Unknown key — treat as free tier
        return "free"

    def _minutes_until_reset(self, session_key: str) -> int:
        """Minutes until the rate limit window resets."""
        bucket = _rate_limits.get(session_key)
        if not bucket:
            return 60
        elapsed = time.time() - bucket["window_start"]
        remaining = max(0, 3600 - elapsed)
        return max(1, int(remaining / 60))


# ---------------------------------------------------------------------------
# SERVER INIT
# ---------------------------------------------------------------------------

mcp = FastMCP("TradesPro", middleware=[AuthMiddleware()])

# ---------------------------------------------------------------------------
# DATA: Building Codes (IRC 2024 / NEC 2023 / UPC 2024 — simplified reference)
# In production, replace with a real code database or API integration.
# ---------------------------------------------------------------------------

BUILDING_CODES = {
    "electrical": {
        "service_panel_size": {
            "code": "NEC 220.87",
            "summary": "Minimum service size for existing dwelling: calculate from measured demand × 125%. New construction typically 200A minimum for homes >2,000 sq ft.",
            "detail": "For new single-family dwellings, a 200-amp service panel is standard. Homes with electric heating, EV chargers, or pools may require 400A. NEC 220.82 provides optional calculation method for dwelling units.",
        },
        "gfci_requirements": {
            "code": "NEC 210.8(A)",
            "summary": "GFCI protection required in: bathrooms, kitchens (within 6ft of sink), garages, outdoors, crawl spaces, unfinished basements, laundry areas, and within 6ft of any sink.",
            "detail": "As of NEC 2023, GFCI protection is expanded to include 250V receptacles in all listed locations. Dishwasher circuits now require GFCI. All 125V-250V, 50A or less receptacles in listed locations must be GFCI protected.",
        },
        "afci_requirements": {
            "code": "NEC 210.12(A)",
            "summary": "AFCI protection required for all 120V, 15A and 20A branch circuits supplying outlets/devices in dwelling unit bedrooms, living rooms, dining rooms, family rooms, parlors, libraries, dens, sunrooms, recreation rooms, closets, hallways, laundry areas, and similar rooms.",
            "detail": "Combination-type AFCI breakers are the standard solution. Kitchen and bathroom circuits are exempt from AFCI but require GFCI.",
        },
        "outlet_spacing": {
            "code": "NEC 210.52(A)",
            "summary": "In habitable rooms, receptacle outlets must be placed so that no point along the floor line of any wall space is more than 6 feet from an outlet. Any wall space 2 feet or wider requires an outlet.",
            "detail": "This effectively means outlets every 12 feet along walls. Kitchen countertops require outlets every 4 feet (NEC 210.52(C)). Bathroom requires at least one outlet within 3 feet of each basin.",
        },
        "wire_sizing": {
            "code": "NEC 310.16",
            "summary": "Standard residential wire sizing: 15A circuit = 14 AWG, 20A circuit = 12 AWG, 30A circuit = 10 AWG, 40A circuit = 8 AWG, 50A circuit = 6 AWG.",
            "detail": "Based on 60°C column for standard NM-B cable. Voltage drop should not exceed 3% for branch circuits (NEC 210.19 Informational Note). For runs over 50 feet, consider upsizing wire gauge.",
        },
        "ev_charger": {
            "code": "NEC 625.40",
            "summary": "EV charging circuits must be dedicated. Level 2 chargers typically require a 40A or 50A, 240V dedicated circuit with 6 AWG wire. Circuit breaker must be rated at 125% of the charger's continuous load.",
            "detail": "NEC 2023 added provisions for bidirectional EV charging (V2H/V2G). Outdoor installations require weatherproof enclosures and GFCI protection. Many jurisdictions now require EV-ready wiring in new construction.",
        },
    },
    "plumbing": {
        "water_heater_sizing": {
            "code": "UPC 507.2",
            "summary": "Residential water heater sizing guide: 1-2 people = 30-40 gal, 2-3 people = 40-50 gal, 3-4 people = 50-60 gal, 5+ people = 60-80 gal. Tankless units sized by flow rate (GPM) and temperature rise.",
            "detail": "First-hour rating (FHR) is more important than tank size. Calculate by counting peak-hour fixtures. Gas water heaters require proper venting per UPC Chapter 5. Electric water heaters typically need a dedicated 30A, 240V circuit.",
        },
        "drain_pipe_sizing": {
            "code": "UPC 702.1",
            "summary": "Minimum drain sizes: lavatory = 1.25 inch, bathtub/shower = 1.5 inch, toilet = 3 inch (4 inch for building drain), kitchen sink = 1.5 inch, washing machine = 2 inch, floor drain = 2 inch.",
            "detail": "Building drain/sewer must be minimum 3 inches, 4 inches recommended. Slope requirements: 1/4 inch per foot for pipes 3 inches and smaller, 1/8 inch per foot for 4 inch and larger. Vent sizing per UPC Table 7-5.",
        },
        "water_supply_sizing": {
            "code": "UPC 610.4",
            "summary": "Minimum supply pipe sizes: main line = 3/4 inch, branches to fixtures = 1/2 inch, hose bibbs = 1/2 inch. Homes with 3+ bathrooms should use 1-inch main supply.",
            "detail": "Size based on fixture unit count and available pressure. Street pressure below 40 PSI may require a booster pump. Above 80 PSI requires a pressure-reducing valve (PRV) per UPC 608.2.",
        },
        "venting": {
            "code": "UPC 901.2",
            "summary": "Every trap must be vented. Vent pipes must terminate at least 6 inches above the roof and 10 feet from any openable window. AAVs (Air Admittance Valves) allowed in some jurisdictions as an alternative to traditional venting.",
            "detail": "Wet venting allowed per UPC 908: a fixture drain that also serves as a vent for another fixture. Maximum distance from trap to vent: 1.25-inch pipe = 3.5 ft, 1.5-inch = 5 ft, 2-inch = 8 ft, 3-inch = 12 ft.",
        },
    },
    "hvac": {
        "duct_sizing": {
            "code": "IRC M1601.1",
            "summary": "Duct sizing based on Manual D calculation. Rule of thumb: 400 CFM per ton of cooling. Main trunk typically 10-12 inch diameter for 3-ton system. Branch runs 6-8 inch diameter.",
            "detail": "Proper sizing requires Manual J load calculation first, then Manual S equipment selection, then Manual D duct design. Duct velocity should not exceed 900 FPM in main trunks, 700 FPM in branches for noise control.",
        },
        "refrigerant_lines": {
            "code": "IRC M1411.3",
            "summary": "Suction line must be insulated. Line sizes determined by manufacturer specs for the specific unit and line length. Liquid line: 3/8 inch for most residential up to 5 tons. Suction line: 3/4 inch (2-3 ton), 7/8 inch (3.5-5 ton).",
            "detail": "Maximum line length varies by manufacturer (typically 50-80 feet for residential). Every 10 feet of additional height requires adjustment. Refrigerant piping must be ACR (Air Conditioning and Refrigeration) grade copper.",
        },
        "load_calculation": {
            "code": "IRC M1401.3",
            "summary": "Equipment sizing must be based on ACCA Manual J load calculation or equivalent. Rule of thumb only for rough estimates: 400-600 sq ft per ton in moderate climates. DO NOT size based on square footage alone.",
            "detail": "Oversizing causes short-cycling, poor humidity control, and higher energy costs. Manual J accounts for insulation, windows, orientation, climate zone, duct losses, and infiltration. Most jurisdictions require Manual J for permits.",
        },
        "clearances": {
            "code": "IRC M1306.1",
            "summary": "Minimum clearances: outdoor condenser unit = 24 inches from walls, 60 inches above grade to any obstruction. Furnace = 3 inches clearance to combustibles (varies by rating). Water heater in garage = 18 inches above floor for ignition source.",
            "detail": "Check manufacturer installation manual for specific clearances — code defers to manufacturer requirements when more restrictive. Gas appliances require combustion air per IRC G2407.",
        },
        "efficiency_standards": {
            "code": "IRC M1403.1 / DOE 2025",
            "summary": "2025 DOE minimum efficiency: Northern region heat pumps = 8.8 HSPF2, Southern region AC = 15.2 SEER2. Gas furnaces: 80% AFUE minimum (90%+ in Northern climate zones per some state codes).",
            "detail": "SEER2 and HSPF2 replaced SEER and HSPF in 2023 with updated testing procedures. Numbers are lower than old ratings for the same equipment. Federal tax credits available for qualifying high-efficiency equipment (25C credit, up to $2,000 for heat pumps).",
        },
    },
}

# ---------------------------------------------------------------------------
# DATA: Material pricing (national average, March 2026)
# ---------------------------------------------------------------------------

MATERIAL_PRICES = {
    # Electrical
    "14/2 NM-B wire (250ft)": {"price": 65.00, "unit": "roll", "category": "electrical"},
    "12/2 NM-B wire (250ft)": {"price": 85.00, "unit": "roll", "category": "electrical"},
    "10/3 NM-B wire (125ft)": {"price": 95.00, "unit": "roll", "category": "electrical"},
    "6/3 NM-B wire (125ft)": {"price": 210.00, "unit": "roll", "category": "electrical"},
    "200A main breaker panel": {"price": 280.00, "unit": "each", "category": "electrical"},
    "20A AFCI breaker": {"price": 45.00, "unit": "each", "category": "electrical"},
    "20A GFCI breaker": {"price": 42.00, "unit": "each", "category": "electrical"},
    "Standard duplex receptacle": {"price": 1.50, "unit": "each", "category": "electrical"},
    "GFCI receptacle": {"price": 18.00, "unit": "each", "category": "electrical"},
    "Single pole switch": {"price": 2.00, "unit": "each", "category": "electrical"},
    "4-inch square box": {"price": 2.50, "unit": "each", "category": "electrical"},
    "Single gang old work box": {"price": 3.50, "unit": "each", "category": "electrical"},
    "LED recessed light 6-inch": {"price": 22.00, "unit": "each", "category": "electrical"},
    "EV charger Level 2 (40A)": {"price": 450.00, "unit": "each", "category": "electrical"},
    # Plumbing
    '1/2" PEX tubing (100ft)': {"price": 35.00, "unit": "roll", "category": "plumbing"},
    '3/4" PEX tubing (100ft)': {"price": 55.00, "unit": "roll", "category": "plumbing"},
    '1/2" copper pipe (10ft)': {"price": 18.00, "unit": "stick", "category": "plumbing"},
    '3/4" copper pipe (10ft)': {"price": 28.00, "unit": "stick", "category": "plumbing"},
    "2-inch PVC DWV (10ft)": {"price": 8.00, "unit": "stick", "category": "plumbing"},
    "3-inch PVC DWV (10ft)": {"price": 12.00, "unit": "stick", "category": "plumbing"},
    "4-inch PVC DWV (10ft)": {"price": 16.00, "unit": "stick", "category": "plumbing"},
    "Toilet (standard)": {"price": 180.00, "unit": "each", "category": "plumbing"},
    "Kitchen faucet (mid-grade)": {"price": 150.00, "unit": "each", "category": "plumbing"},
    "40-gallon gas water heater": {"price": 650.00, "unit": "each", "category": "plumbing"},
    "50-gallon electric water heater": {"price": 550.00, "unit": "each", "category": "plumbing"},
    "Tankless gas water heater": {"price": 1200.00, "unit": "each", "category": "plumbing"},
    "Garbage disposal (1/2 HP)": {"price": 110.00, "unit": "each", "category": "plumbing"},
    "Sump pump (1/3 HP)": {"price": 160.00, "unit": "each", "category": "plumbing"},
    # HVAC
    "3-ton AC condenser (14 SEER2)": {"price": 2800.00, "unit": "each", "category": "hvac"},
    "3-ton heat pump (15 SEER2)": {"price": 3400.00, "unit": "each", "category": "hvac"},
    "80K BTU gas furnace (80% AFUE)": {"price": 1200.00, "unit": "each", "category": "hvac"},
    "80K BTU gas furnace (96% AFUE)": {"price": 2100.00, "unit": "each", "category": "hvac"},
    '3/4" insulated suction line (50ft)': {"price": 85.00, "unit": "roll", "category": "hvac"},
    '3/8" liquid line (50ft)': {"price": 55.00, "unit": "roll", "category": "hvac"},
    "Programmable thermostat": {"price": 45.00, "unit": "each", "category": "hvac"},
    "Smart thermostat (WiFi)": {"price": 180.00, "unit": "each", "category": "hvac"},
    '6" flex duct (25ft)': {"price": 22.00, "unit": "box", "category": "hvac"},
    '8" flex duct (25ft)': {"price": 30.00, "unit": "box", "category": "hvac"},
    "Return air grille 20x20": {"price": 18.00, "unit": "each", "category": "hvac"},
    "Supply register 6x10": {"price": 8.00, "unit": "each", "category": "hvac"},
}

# ---------------------------------------------------------------------------
# DATA: Job templates with labor estimates
# ---------------------------------------------------------------------------

JOB_TEMPLATES = {
    "panel_upgrade_200a": {
        "name": "200A Electrical Panel Upgrade",
        "trade": "electrical",
        "description": "Replace existing panel with new 200A main breaker panel. Includes new meter base if required by utility.",
        "labor_hours": {"min": 8, "max": 12},
        "labor_rate_range": {"min": 75, "max": 125},
        "materials": [
            {"item": "200A main breaker panel", "qty": 1},
            {"item": "6/3 NM-B wire (125ft)", "qty": 1},
            {"item": "20A AFCI breaker", "qty": 8},
            {"item": "20A GFCI breaker", "qty": 4},
        ],
        "permit_required": True,
        "inspection_required": True,
        "typical_price_range": {"min": 2500, "max": 4500},
        "notes": "Utility coordination required for disconnect/reconnect. May need to upgrade service entrance cable. Check with local utility for meter base requirements.",
    },
    "ev_charger_install": {
        "name": "Level 2 EV Charger Installation",
        "trade": "electrical",
        "description": "Install a 240V, 40-50A dedicated circuit for Level 2 EV charger in garage or driveway area.",
        "labor_hours": {"min": 4, "max": 8},
        "labor_rate_range": {"min": 75, "max": 125},
        "materials": [
            {"item": "EV charger Level 2 (40A)", "qty": 1},
            {"item": "6/3 NM-B wire (125ft)", "qty": 1},
            {"item": "20A GFCI breaker", "qty": 1},
        ],
        "permit_required": True,
        "inspection_required": True,
        "typical_price_range": {"min": 1200, "max": 2800},
        "notes": "Panel must have capacity for 40-50A breaker. If panel is full, may require panel upgrade (separate job). Outdoor installations need weatherproof enclosure. NEC 625.40 requires dedicated circuit.",
    },
    "water_heater_replacement": {
        "name": "Water Heater Replacement (Tank)",
        "trade": "plumbing",
        "description": "Replace existing tank water heater with new unit. Includes hauling away old unit.",
        "labor_hours": {"min": 3, "max": 6},
        "labor_rate_range": {"min": 75, "max": 120},
        "materials": [
            {"item": "50-gallon electric water heater", "qty": 1},
            {"item": '3/4" copper pipe (10ft)', "qty": 2},
        ],
        "permit_required": True,
        "inspection_required": True,
        "typical_price_range": {"min": 1200, "max": 2200},
        "notes": "Gas units require gas line and venting inspection. Electric units may need circuit verification. Expansion tank required in closed systems. Many jurisdictions require seismic strapping.",
    },
    "tankless_conversion": {
        "name": "Tankless Water Heater Conversion",
        "trade": "plumbing",
        "description": "Convert from tank water heater to tankless. Includes gas line upgrade, new venting, and removal of old unit.",
        "labor_hours": {"min": 6, "max": 10},
        "labor_rate_range": {"min": 80, "max": 130},
        "materials": [
            {"item": "Tankless gas water heater", "qty": 1},
            {"item": '3/4" copper pipe (10ft)', "qty": 3},
        ],
        "permit_required": True,
        "inspection_required": True,
        "typical_price_range": {"min": 3000, "max": 5500},
        "notes": "Gas line often needs upsizing (3/4-inch minimum). Category III stainless steel venting required for most units. Condensate drain needed for condensing models. Check gas meter capacity with utility.",
    },
    "ac_replacement": {
        "name": "Central AC System Replacement (3-ton)",
        "trade": "hvac",
        "description": "Replace outdoor condenser and indoor evaporator coil. Includes refrigerant line replacement if needed, new disconnect, and thermostat.",
        "labor_hours": {"min": 8, "max": 14},
        "labor_rate_range": {"min": 80, "max": 130},
        "materials": [
            {"item": "3-ton AC condenser (14 SEER2)", "qty": 1},
            {"item": '3/4" insulated suction line (50ft)', "qty": 1},
            {"item": '3/8" liquid line (50ft)', "qty": 1},
            {"item": "Smart thermostat (WiFi)", "qty": 1},
        ],
        "permit_required": True,
        "inspection_required": True,
        "typical_price_range": {"min": 5000, "max": 9000},
        "notes": "Must be sized via Manual J calculation (not square footage). Ductwork evaluation recommended. R-410A systems cannot use R-22. EPA 608 certification required for refrigerant handling. Federal tax credits may apply for high-efficiency units.",
    },
    "heat_pump_install": {
        "name": "Heat Pump System Installation",
        "trade": "hvac",
        "description": "Install new heat pump system for heating and cooling. Includes outdoor unit, air handler, refrigerant lines, thermostat, and electrical connection.",
        "labor_hours": {"min": 10, "max": 16},
        "labor_rate_range": {"min": 85, "max": 135},
        "materials": [
            {"item": "3-ton heat pump (15 SEER2)", "qty": 1},
            {"item": '3/4" insulated suction line (50ft)', "qty": 1},
            {"item": '3/8" liquid line (50ft)', "qty": 1},
            {"item": "Smart thermostat (WiFi)", "qty": 1},
        ],
        "permit_required": True,
        "inspection_required": True,
        "typical_price_range": {"min": 7000, "max": 14000},
        "notes": "Heat pumps may qualify for federal tax credit up to $2,000 (25C). Auxiliary heat strips needed in cold climates. Ensure electrical service can handle compressor load. Manual J calculation required.",
    },
    "bathroom_rough_in": {
        "name": "Bathroom Plumbing Rough-In",
        "trade": "plumbing",
        "description": "New bathroom rough-in plumbing: toilet, sink, and shower/tub. Supply and drain/waste/vent lines.",
        "labor_hours": {"min": 12, "max": 20},
        "labor_rate_range": {"min": 80, "max": 120},
        "materials": [
            {"item": '1/2" PEX tubing (100ft)', "qty": 2},
            {"item": '3/4" PEX tubing (100ft)', "qty": 1},
            {"item": "2-inch PVC DWV (10ft)", "qty": 4},
            {"item": "3-inch PVC DWV (10ft)", "qty": 3},
        ],
        "permit_required": True,
        "inspection_required": True,
        "typical_price_range": {"min": 3000, "max": 6000},
        "notes": "Requires rough-in inspection before walls are closed. Vent system must connect to existing stack or extend through roof. Water hammer arrestors recommended on quick-closing valves.",
    },
    "whole_house_rewire": {
        "name": "Whole House Rewire (1,500 sq ft)",
        "trade": "electrical",
        "description": "Complete rewire of existing home. Replace all branch circuits, install new panel, update all devices to code.",
        "labor_hours": {"min": 40, "max": 60},
        "labor_rate_range": {"min": 75, "max": 125},
        "materials": [
            {"item": "200A main breaker panel", "qty": 1},
            {"item": "14/2 NM-B wire (250ft)", "qty": 6},
            {"item": "12/2 NM-B wire (250ft)", "qty": 4},
            {"item": "20A AFCI breaker", "qty": 12},
            {"item": "20A GFCI breaker", "qty": 6},
            {"item": "Standard duplex receptacle", "qty": 40},
            {"item": "GFCI receptacle", "qty": 8},
            {"item": "Single pole switch", "qty": 20},
            {"item": "Single gang old work box", "qty": 60},
        ],
        "permit_required": True,
        "inspection_required": True,
        "typical_price_range": {"min": 8000, "max": 15000},
        "notes": "Multiple inspections required (rough-in and final). Coordinate with drywall/painting contractors. May require temporary power. Smoke/CO detector placement must meet current code.",
    },
}


# ---------------------------------------------------------------------------
# TOOLS
# ---------------------------------------------------------------------------


@mcp.tool
def lookup_building_code(trade: str, topic: str) -> str:
    """
    Look up residential building code requirements for electrical, plumbing, or HVAC work.

    Args:
        trade: The trade type. Must be one of: "electrical", "plumbing", "hvac"
        topic: The topic to look up. Examples:
               Electrical: gfci_requirements, afci_requirements, outlet_spacing, wire_sizing, service_panel_size, ev_charger
               Plumbing: water_heater_sizing, drain_pipe_sizing, water_supply_sizing, venting
               HVAC: duct_sizing, refrigerant_lines, load_calculation, clearances, efficiency_standards
    """
    trade = trade.lower().strip()
    topic = topic.lower().strip().replace(" ", "_")

    if trade not in BUILDING_CODES:
        available = ", ".join(BUILDING_CODES.keys())
        return f"Trade '{trade}' not found. Available trades: {available}"

    if topic not in BUILDING_CODES[trade]:
        available = ", ".join(BUILDING_CODES[trade].keys())
        return f"Topic '{topic}' not found for {trade}. Available topics: {available}"

    code = BUILDING_CODES[trade][topic]
    return (
        f"**{topic.replace('_', ' ').title()}** — {code['code']}\n\n"
        f"**Summary:** {code['summary']}\n\n"
        f"**Details:** {code['detail']}\n\n"
        f"⚠️ Always verify with your local jurisdiction — local amendments may override national codes."
    )


@mcp.tool
def list_code_topics(trade: str) -> str:
    """
    List all available building code topics for a given trade.

    Args:
        trade: The trade type. Must be one of: "electrical", "plumbing", "hvac"
    """
    trade = trade.lower().strip()
    if trade not in BUILDING_CODES:
        available = ", ".join(BUILDING_CODES.keys())
        return f"Trade '{trade}' not found. Available trades: {available}"

    topics = BUILDING_CODES[trade]
    lines = [f"## Available Code Topics for {trade.title()}\n"]
    for topic_key, topic_data in topics.items():
        lines.append(f"- **{topic_key}** ({topic_data['code']}): {topic_data['summary'][:80]}...")
    return "\n".join(lines)


@mcp.tool
def estimate_materials(job_type: str) -> str:
    """
    Get a material list and cost estimate for a standard trade job.

    Args:
        job_type: The type of job. Available jobs:
                  panel_upgrade_200a, ev_charger_install, water_heater_replacement,
                  tankless_conversion, ac_replacement, heat_pump_install,
                  bathroom_rough_in, whole_house_rewire
    """
    job_type = job_type.lower().strip().replace(" ", "_")

    if job_type not in JOB_TEMPLATES:
        available = ", ".join(JOB_TEMPLATES.keys())
        return f"Job type '{job_type}' not found. Available: {available}"

    job = JOB_TEMPLATES[job_type]
    lines = [
        f"## Material Estimate: {job['name']}",
        f"*Trade: {job['trade'].title()}*\n",
        "| Material | Qty | Unit Price | Subtotal |",
        "|----------|-----|-----------|----------|",
    ]

    total_materials = 0.0
    for mat in job["materials"]:
        item_name = mat["item"]
        qty = mat["qty"]
        if item_name in MATERIAL_PRICES:
            price = MATERIAL_PRICES[item_name]["price"]
            unit = MATERIAL_PRICES[item_name]["unit"]
            subtotal = price * qty
            total_materials += subtotal
            lines.append(f"| {item_name} | {qty} {unit} | ${price:.2f} | ${subtotal:.2f} |")
        else:
            lines.append(f"| {item_name} | {qty} | Price varies | — |")

    lines.append(f"\n**Estimated Material Cost: ${total_materials:.2f}**")
    lines.append(f"\n*Note: Prices are national averages as of March 2026. Local prices vary by region and supplier. Does not include fittings, connectors, fasteners, or miscellaneous supplies (add 10-15%).*")

    return "\n".join(lines)


@mcp.tool
def scope_job(job_type: str) -> str:
    """
    Get a complete job scope including labor hours, material costs, total price range, permit requirements, and important notes.

    Args:
        job_type: The type of job. Available jobs:
                  panel_upgrade_200a, ev_charger_install, water_heater_replacement,
                  tankless_conversion, ac_replacement, heat_pump_install,
                  bathroom_rough_in, whole_house_rewire
    """
    job_type = job_type.lower().strip().replace(" ", "_")

    if job_type not in JOB_TEMPLATES:
        available = ", ".join(JOB_TEMPLATES.keys())
        return f"Job type '{job_type}' not found. Available: {available}"

    job = JOB_TEMPLATES[job_type]

    # Calculate material total
    total_materials = 0.0
    for mat in job["materials"]:
        if mat["item"] in MATERIAL_PRICES:
            total_materials += MATERIAL_PRICES[mat["item"]]["price"] * mat["qty"]

    labor_min = job["labor_hours"]["min"] * job["labor_rate_range"]["min"]
    labor_max = job["labor_hours"]["max"] * job["labor_rate_range"]["max"]

    lines = [
        f"## Job Scope: {job['name']}",
        f"*Trade: {job['trade'].title()}*\n",
        f"**Description:** {job['description']}\n",
        f"### Labor",
        f"- Estimated hours: {job['labor_hours']['min']}–{job['labor_hours']['max']} hours",
        f"- Rate range: ${job['labor_rate_range']['min']}–${job['labor_rate_range']['max']}/hr",
        f"- Labor cost estimate: ${labor_min:,.0f}–${labor_max:,.0f}\n",
        f"### Materials",
        f"- Estimated material cost: ${total_materials:,.2f}",
        f"- Add 10-15% for fittings, connectors, miscellaneous\n",
        f"### Total Price Range",
        f"- **${job['typical_price_range']['min']:,}–${job['typical_price_range']['max']:,}**",
        f"- *(Includes labor, materials, overhead, and profit)*\n",
        f"### Permit & Inspection",
        f"- Permit required: {'✅ Yes' if job['permit_required'] else '❌ No'}",
        f"- Inspection required: {'✅ Yes' if job['inspection_required'] else '❌ No'}\n",
        f"### Important Notes",
        f"{job['notes']}",
    ]

    return "\n".join(lines)


@mcp.tool
def list_available_jobs(trade: str = "") -> str:
    """
    List all available job templates, optionally filtered by trade.

    Args:
        trade: Optional filter. Leave empty for all jobs, or use "electrical", "plumbing", "hvac".
    """
    trade = trade.lower().strip() if trade else ""

    lines = ["## Available Job Templates\n"]
    for key, job in JOB_TEMPLATES.items():
        if trade and job["trade"] != trade:
            continue
        lines.append(
            f"- **{key}** — {job['name']} ({job['trade'].title()}) | "
            f"${job['typical_price_range']['min']:,}–${job['typical_price_range']['max']:,}"
        )

    if len(lines) == 1:
        lines.append(f"No jobs found for trade '{trade}'. Try: electrical, plumbing, hvac")

    return "\n".join(lines)


@mcp.tool
def lookup_material_price(item: str) -> str:
    """
    Look up the current average price for a specific material.

    Args:
        item: The material to look up. Use search terms like "wire", "panel", "pex", "water heater", etc.
    """
    search = item.lower().strip()
    matches = []
    for name, data in MATERIAL_PRICES.items():
        if search in name.lower():
            matches.append(f"- **{name}**: ${data['price']:.2f}/{data['unit']} ({data['category']})")

    if not matches:
        # Show all items in the relevant category if no match
        return (
            f"No exact match for '{item}'. Try broader terms like: wire, panel, pex, copper, "
            f"water heater, furnace, thermostat, duct, breaker, receptacle, toilet, faucet"
        )

    header = f"## Material Prices Matching '{item}'\n"
    footer = "\n\n*Prices are national averages, March 2026. Local prices vary.*"
    return header + "\n".join(matches) + footer


@mcp.tool
def check_permit_requirements(job_description: str) -> str:
    """
    Check whether a described job likely requires a permit and inspection.
    Provides guidance on common permit triggers for electrical, plumbing, and HVAC work.

    Args:
        job_description: A plain-English description of the job, e.g. "replacing a kitchen faucet"
                        or "adding a new 240V circuit for an EV charger"
    """
    desc = job_description.lower()

    # Permit typically required
    permit_triggers = {
        "electrical": [
            "new circuit", "panel", "service", "rewire", "ev charger", "sub-panel",
            "240v", "200 amp", "100 amp", "meter", "generator", "transfer switch",
            "hot tub", "pool", "spa", "addition", "new construction",
        ],
        "plumbing": [
            "water heater", "sewer", "main line", "reroute", "new bathroom",
            "rough-in", "gas line", "backflow", "new fixture", "addition",
            "repipe", "tankless", "sump pump", "ejector",
        ],
        "hvac": [
            "furnace", "ac ", "air condition", "heat pump", "ductwork", "new system",
            "replacement", "boiler", "mini-split", "refrigerant", "gas line",
            "addition", "new construction",
        ],
    }

    # Permit typically NOT required
    no_permit_keywords = [
        "faucet", "toilet seat", "replace toilet", "replace outlet", "replace switch",
        "replace thermostat", "garbage disposal", "light fixture",
        "replace receptacle", "filter", "clean", "maintenance", "repair",
        "unclog", "snake", "adjust", "caulk", "showerhead", "aerator",
        "drain stopper", "toilet flapper", "valve handle",
    ]

    # Check for no-permit items first
    for keyword in no_permit_keywords:
        if keyword in desc:
            return (
                f"## Permit Check: {job_description}\n\n"
                f"**Permit likely NOT required** for like-for-like replacements and repairs.\n\n"
                f"However, always check with your local building department — some jurisdictions "
                f"require permits even for simple replacements.\n\n"
                f"**General rule:** If you're replacing with the same type/size and not modifying "
                f"any piping, wiring, or ductwork, a permit is usually not needed."
            )

    # Check for permit triggers
    triggered_trades = []
    for trade, triggers in permit_triggers.items():
        for trigger in triggers:
            if trigger in desc:
                triggered_trades.append(trade)
                break

    if triggered_trades:
        trades_str = ", ".join(set(triggered_trades))
        return (
            f"## Permit Check: {job_description}\n\n"
            f"**⚠️ Permit likely REQUIRED** — This work involves {trades_str} modifications.\n\n"
            f"### What to expect:\n"
            f"- **Permit application** at your local building department (in-person or online)\n"
            f"- **Permit fee** typically $50–$500 depending on scope and jurisdiction\n"
            f"- **Rough-in inspection** before closing up walls (if applicable)\n"
            f"- **Final inspection** after work is complete\n"
            f"- **Licensed contractor** required in most jurisdictions\n\n"
            f"### Why it matters:\n"
            f"- Unpermitted work can affect home insurance coverage\n"
            f"- Must be disclosed at sale — can kill deals or reduce sale price\n"
            f"- Code violations found later are homeowner's liability\n\n"
            f"**Always call your local building department to confirm before starting work.**"
        )

    return (
        f"## Permit Check: {job_description}\n\n"
        f"**Uncertain** — Could not determine permit requirements from description alone.\n\n"
        f"**Best practice:** Call your local building department and describe the work. "
        f"They'll tell you definitively whether a permit is needed.\n\n"
        f"**General rules of thumb:**\n"
        f"- Any NEW installation usually requires a permit\n"
        f"- Like-for-like replacements often don't\n"
        f"- Any work involving gas lines ALWAYS requires a permit\n"
        f"- Structural changes ALWAYS require a permit"
    )


# ---------------------------------------------------------------------------
# RESOURCES
# ---------------------------------------------------------------------------


@mcp.resource("trades://trades-list")
def get_supported_trades() -> str:
    """List all supported trades and their available tools."""
    return """
# TradesPro MCP Server — Supported Trades & Tools

## Trades Covered
- **Electrical** — NEC 2023 code references, panel/circuit/device work
- **Plumbing** — UPC 2024 code references, water heater/piping/drainage work
- **HVAC** — IRC Mechanical code references, AC/heat pump/furnace/ductwork

## Available Tools
1. **lookup_building_code** — Get specific code requirements by trade and topic
2. **list_code_topics** — See all available code topics for a trade
3. **estimate_materials** — Get itemized material costs for standard jobs
4. **scope_job** — Full job scope: labor, materials, pricing, permits, notes
5. **list_available_jobs** — Browse all job templates by trade
6. **lookup_material_price** — Search material pricing database
7. **check_permit_requirements** — Check if a described job needs permits

## Pricing Note
Material prices are national averages (March 2026). Always get local quotes.
Labor rates vary significantly by region, experience, and market conditions.
"""


# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)
