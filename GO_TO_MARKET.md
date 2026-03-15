# TradesPro MCP Server — Go-to-Market Playbook

## Revenue Strategy (3 Tiers, Pursue All Simultaneously)

---

### TIER 1: xpay Micropayments (Passive, starts Day 1)
**Revenue: $0.01–$0.25 per tool call, zero code changes**

1. Deploy your server as an HTTP endpoint:
   ```bash
   fastmcp run server.py:mcp --transport http --port 8000
   ```
   Host on Railway ($5/mo), Fly.io ($5/mo), or Prefect Horizon (free).

2. Register at https://xpay.sh
   - Paste your server URL
   - Set your USDC wallet address (Base network)
   - Set pricing per tool:

   | Tool | Suggested Price |
   |------|----------------|
   | lookup_building_code | $0.02 |
   | list_code_topics | $0.01 |
   | estimate_materials | $0.05 |
   | scope_job | $0.10 |
   | list_available_jobs | $0.01 |
   | lookup_material_price | $0.02 |
   | check_permit_requirements | $0.05 |

3. Share the proxy URL on MCP directories, Reddit, X/Twitter

**Target: $100–$500/month passive at 5,000–25,000 calls/month**

---

### TIER 2: Freemium API Key Model (21st.dev Playbook)
**Revenue: $20–$49/month per subscriber**

Following the proven model from 21st.dev (the most cited MCP monetization success):

1. Add API key gating to your server (see implementation below)
2. First 10 requests/day = free (builds habit + trust)
3. $20/month = 500 requests/day
4. $49/month = unlimited

**Implementation approach:**
- Add a simple middleware that checks an API key header
- Track usage per key in a SQLite database or Redis
- Use Stripe for payment + key provisioning
- Or use xpay's built-in key management

**Distribution channels:**
- Smithery: `smithery mcp publish <url> -n your-org/trades-pro`
- Cline MCP Marketplace (built into the Cline VS Code extension)
- MCP.so directory: https://mcp.so
- Glama.ai: https://glama.ai/mcp/servers
- mcpservers.org: https://mcpservers.org

**Target: 50–200 subscribers × $20/mo = $1,000–$4,000/month**

---

### TIER 3: B2B Retainer (Highest Revenue)
**Revenue: $500–$2,000/month per client**

This is where you customize the server for individual trade businesses:

**What you sell:**
- The MCP server pre-loaded with THEIR local material prices (from their suppliers)
- Local code amendments for their jurisdiction
- Custom job templates matching their service menu
- Integration with their scheduling tool (Housecall Pro, Workiz, ServiceTitan)
- AI agent that uses the MCP server to answer customer calls, generate quotes, route jobs

**How to find clients:**
1. Join local trade associations (PHCC for plumbing, NFPA for electrical, ACCA for HVAC)
2. Search Facebook groups: "HVAC business owners", "plumbing contractors"
3. Cold email/DM owners of 5–20 truck operations in your metro area
4. Attend a local trade show with a laptop demo

**The pitch:**
> "I built an AI tool that knows building codes, estimates materials at YOUR supplier prices, and scopes jobs in 30 seconds. Your office staff or AI receptionist can use it to give accurate quotes over the phone without pulling a tech off a job. I'll set it up for $1,500 and maintain it for $500/month."

**Why they pay:**
- Missed calls cost $200–$500 each in lost revenue
- Inaccurate quotes lose jobs or eat margins
- Code lookup errors cause failed inspections ($500+ re-inspection fees)
- Their current solution is "call the senior tech" which pulls him off billable work

**Target: 5 clients × $1,000/mo = $5,000/month**

---

## Week-by-Week Launch Plan

### Week 1: Deploy + List
- [ ] Deploy server on Railway or Fly.io
- [ ] Register on xpay.sh, set pricing, get proxy URL
- [ ] Submit to Smithery, MCP.so, Glama.ai, mcpservers.org
- [ ] Create a GitHub repo (public) with good README
- [ ] Post on r/mcp, r/selfhosted, r/HVAC, r/electricians, r/Plumbing

### Week 2: Content + Distribution
- [ ] Record a 2-minute demo video (screen recording of Claude using your tools)
- [ ] Post demo on X/Twitter, LinkedIn, YouTube
- [ ] Write a blog post: "I Built an MCP Server That Knows Building Codes"
- [ ] Submit to Hacker News (Show HN)
- [ ] Post on Product Hunt

### Week 3: B2B Outreach
- [ ] Identify 20 local trade businesses (5–20 trucks)
- [ ] Send personalized cold emails with the demo video link
- [ ] Join 3 Facebook groups for trade business owners
- [ ] Offer 3 free pilots in exchange for testimonials

### Week 4: Iterate + Scale
- [ ] Add features based on user feedback
- [ ] Add more job templates (mini-split install, sewer line repair, etc.)
- [ ] Add local code amendments for your top 3 jurisdictions
- [ ] Convert free pilots to paying retainers

---

## Extending for More Revenue

### Add More Value (Higher Willingness to Pay)

**Real-time material pricing integration:**
- Connect to Home Depot/Lowe's/Ferguson APIs for live pricing
- Or scrape supplier catalogs and update weekly
- This alone justifies $49/mo because contractors waste hours pricing jobs manually

**Local code amendments database:**
- Research and add local amendments for major metro areas
- Start with your city, expand to top 20 US metros
- Each city you add = new addressable market

**Scheduling/CRM integration:**
- Connect to Housecall Pro, Workiz, or ServiceTitan APIs
- AI agent can book jobs directly after quoting
- This is the $2,000/month tier

**Voice agent bundle:**
- Pair with Twilio + an AI voice agent
- The agent answers calls, uses your MCP server for pricing/codes, books appointments
- Charge $1,500–$3,000/month for the complete "AI receptionist" package

---

## Cost Structure

| Item | Monthly Cost |
|------|-------------|
| Railway hosting | $5 |
| Domain | $1 |
| OpenAI API (for AI agent tier) | $20–$50 |
| xpay | Free (they take 0% currently) |
| Stripe | 2.9% + $0.30 per transaction |
| **Total baseline** | **~$6/month** |

Your margin on Tier 2 (freemium) is ~97%.
Your margin on Tier 3 (B2B retainer) is ~95%+ after the first month.

---

## Key Metrics to Track

- Tool calls per day (via xpay dashboard or server logs)
- Unique users per week
- Free-to-paid conversion rate (target: 5–10%)
- B2B pipeline: leads → demos → pilots → paying clients
- Revenue per tool (which tools are most valuable?)
- Churn rate on monthly subscribers

---

## Competition Check (March 2026)

**Who else has an MCP server for trades?** Nobody. Searched MCP.so, Smithery, Glama.ai — zero results for HVAC, plumbing, electrical, or construction-specific MCP servers.

**Adjacent competition:**
- ServiceAgent.ai — AI voice agent for HVAC (not MCP-based, $500+/mo)
- Housecall Pro / Workiz — Full platforms ($80–$300/mo), not AI-native
- ChatGPT with building code knowledge — Generic, not structured or reliable

**Your moat:** First MCP server with structured trade data. MCP marketplace listings compound over time (like SEO). Every month you're listed with no competition is a month of compounding user habit and distribution.
