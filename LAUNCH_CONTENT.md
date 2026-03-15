# TradesPro MCP Server — Launch Content

> All pieces are copy-paste ready. Replace `[YOUR_URL]` and `https://github.com/dieselpro1111/trades-mcp-server` before posting.

---

## 1. Reddit Post — r/mcp

**Title:** I built the first MCP server for skilled trades — NEC/UPC/HVAC codes, material pricing, and job scoping for AI assistants [Open Source]

---

**Body:**

Hey r/mcp — I wanted to share something I've been working on that fills what I think is a pretty glaring gap in the MCP ecosystem.

**TradesPro** is an MCP server that gives AI assistants real, structured knowledge of the skilled trades: electrical, plumbing, and HVAC. We're talking building codes, material pricing, permit requirements, and job scoping templates — the stuff a journeyman carries around in their head after years on the job.

**Why this exists:**
I was watching contractors use Claude and ChatGPT and kept seeing the same frustration — the models hallucinate code citations, quote outdated prices, and have no concept of regional permit variance. These are costly mistakes in trades work. A misquoted material price or a code violation can blow a job's margin or get an inspection failed.

**The 7 tools:**

| Tool | What it does |
|------|-------------|
| `lookup_building_code` | Query NEC 2023 (electrical), UPC 2024 (plumbing), or IRC Mechanical (HVAC) by topic |
| `list_code_topics` | Browse available code categories by trade |
| `estimate_materials` | Generate a material estimate for a scoped job |
| `scope_job` | Pull a structured job template (8 templates included) |
| `list_available_jobs` | List all supported job types |
| `lookup_material_price` | Get current pricing for 40+ materials |
| `check_permit_requirements` | Permit requirements by job type and jurisdiction |

**Coverage:**
- NEC 2023 electrical codes
- UPC 2024 plumbing codes
- IRC Mechanical HVAC codes
- 40+ material prices (wire, pipe, fittings, equipment)
- 8 job templates (panel upgrades, water heater installs, HVAC changeouts, etc.)

**The monetization angle:**
This is built with FastMCP and is MIT licensed. But it's also wired up for xpay pay-per-tool-call monetization if you want to run it as a commercial service. Trades businesses already pay $50-150/month for estimating software — there's a real market here.

**Zero competition:**
I checked Smithery, MCP.so, and Glama.ai before building this. Nothing. The MCP ecosystem has dozens of servers for developer tooling, productivity apps, and data APIs — but nothing for the 700,000+ licensed electricians, plumbers, and HVAC techs in the US alone.

GitHub: https://github.com/dieselpro1111/trades-mcp-server
Try it: [YOUR_URL]

Happy to answer questions about the architecture or the xpay integration.

---

## 2. Reddit Post — r/electricians

**Title:** Built an AI tool that actually knows NEC 2023 — helps with quoting and code lookup, not replacing electricians

---

**Body:**

Long-time lurker, wanted to share something I built that I think is genuinely useful for working electricians and electrical contractors.

**The problem I kept seeing:**
Guys on the tools using AI assistants for quick code lookups or estimate help were getting burned. The models would confidently cite NEC articles that were wrong, quote material prices from 2021, or completely miss permit requirements. In this trade, that's not a small thing — a wrong code answer on a commercial job is an inspection failure and a callback.

**What I built:**
TradesPro is an MCP server (a plugin layer for AI assistants like Claude) that gives the AI real, structured access to NEC 2023. Not scraped text — structured, queryable knowledge.

**What it actually does:**

- **NEC 2023 code lookup** — query by topic (AFCI requirements, conduit fill, grounding, service entrance, etc.)
- **Material pricing** — current prices for wire, conduit, breakers, panels, fittings. 40+ materials
- **Job scoping templates** — structured scope for panel upgrades, service entrance work, EV charger installs, subpanel additions
- **Permit requirements** — what's required by job type, with jurisdiction notes

**What this is NOT:**
This isn't a replacement for a licensed electrician. The AI still can't read field conditions, pull permits in your name, or make the judgment calls that come from years on the job. What it can do is help you knock out a rough material estimate in 2 minutes instead of 20, or double-check an NEC article number before you call the AHJ.

**Example use:**
Ask Claude (with TradesPro): "What are the AFCI requirements for a bedroom circuit in a new residential build under NEC 2023?" — it returns the actual NEC 2023 section, not a hallucination.

It's free and open source: https://github.com/dieselpro1111/trades-mcp-server

If you try it and find a code section that's wrong or a material price that's way off, open an issue. I want this to be actually accurate, not just impressive-sounding.

---

## 3. Reddit Post — r/HVAC

**Title:** Made an MCP server with HVAC code knowledge — IRC Mechanical, equipment sizing, material pricing, permit requirements

---

**Body:**

HVAC pros — I built something that might save some time on estimates and code lookups. Sharing here because I want feedback from people who actually do this work.

**TradesPro** is an MCP server that plugs HVAC knowledge into AI assistants (Claude, etc.). It's built around the IRC Mechanical code and covers the things that actually come up on jobs.

**What's in it for HVAC:**

**Code lookups:**
IRC Mechanical topics including:
- Equipment clearances and installation requirements
- Refrigerant line sizing and line set requirements
- Condensate drain requirements
- Combustion air requirements for gas appliances
- Duct sizing and materials (flex duct limitations, etc.)
- Venting requirements by equipment type

**Equipment sizing:**
Structured templates for:
- Residential cooling/heating load (Manual J reference parameters)
- Heat pump sizing and supplemental heat requirements
- Mini-split multi-zone layout
- Gas furnace/boiler sizing

**Material pricing:**
Current pricing on refrigerant (410A, 454B), line sets, ductwork, filter media, thermostats, and control wiring.

**Permit requirements:**
What typically triggers a permit, what inspectors look for on HVAC installs, and equipment swap vs. new install variance.

**Honest caveats:**
Manual J is a calculation — TradesPro gives you the framework and parameters, not a substitute for running the actual heat load. Regional code amendments aren't fully covered yet (the IRC base code is, local amendments are a work in progress). I'm an open source project, not a compliance tool.

**Why I built it:**
AI assistants are getting used in HVAC shops for customer proposals and quick code checks. The base models don't have reliable HVAC code knowledge. This fills that gap with something accurate and structured.

Free and open source: https://github.com/dieselpro1111/trades-mcp-server
Try it with Claude: [YOUR_URL]

What am I missing? What do you actually look up constantly that would save you time?

---

## 4. Reddit Post — r/Plumbing

**Title:** Built an AI plugin with UPC 2024 plumbing codes — drain sizing, venting, water heater requirements

---

**Body:**

Plumbers — I made something I think is useful for daily work and wanted to get feedback from people in the trade.

**TradesPro** is a plugin for AI assistants (like Claude) that gives them actual plumbing code knowledge — UPC 2024, not guesswork.

**What's in it:**

**UPC 2024 code topics:**
- DWV sizing tables (drain pipe sizing by fixture units)
- Venting requirements — individual, common, wet venting
- Water heater installation requirements (T&P valve, seismic strapping, expansion tanks)
- Water supply pipe sizing
- Backflow prevention requirements
- Fixture rough-in dimensions
- Grease interceptor sizing

**Job scoping templates:**
- Water heater replacement (tank and tankless)
- Bathroom addition rough-in
- Kitchen remodel plumbing
- Water service replacement

**Material pricing:**
Current prices on copper, PEX (A, B, C), CPVC, ABS, PVC DWV, cast iron, fittings, valves, water heaters.

**Permit requirements:**
What triggers a permit for common plumbing jobs, and what inspectors typically check.

**Real example:**
Ask Claude (with TradesPro): "What's the minimum drain size for a shower under UPC 2024?" — it returns the actual UPC table reference, not a made-up answer.

**What this doesn't do:**
It can't replace field judgment. Existing drain conditions, soil stack health, actual fixture unit counts in a real house — that still takes eyes on the job. This is for the code reference and estimating side, not replacing the diagnosis a journeyman makes walking a job.

Built this because AI assistants are already being used in plumbing shops for proposals and code questions, and the base models are unreliable on specific UPC citations. This fixes that.

Free, MIT licensed, open source: https://github.com/dieselpro1111/trades-mcp-server

What code topics do you look up constantly? I want to make sure the coverage is right.

---

## 5. X/Twitter Thread

**Tweet 1 (hook):**
I just shipped the first MCP server for skilled trades.

NEC 2023 electrical codes. UPC 2024 plumbing. IRC Mechanical HVAC. Material pricing. Permit requirements.

Your AI assistant now knows what a journeyman knows.

🧵

---

**Tweet 2 (the problem):**
The problem: electricians, plumbers, and HVAC techs are already using AI to write proposals and look up codes.

The base models hallucinate NEC articles, quote 2021 material prices, and miss permit triggers.

In trades work, that's an inspection failure or a blown job margin.

---

**Tweet 3 (the solution):**
TradesPro fixes this.

7 MCP tools:
• lookup_building_code — NEC/UPC/IRC Mechanical
• estimate_materials — 40+ current material prices
• scope_job — 8 job templates
• check_permit_requirements — by job type + jurisdiction
• And 3 more

Structured, queryable, accurate.

---

**Tweet 4 (the opportunity):**
I checked Smithery, MCP.so, and Glama.ai before building this.

Zero MCP servers for skilled trades. Zero.

There are 700,000+ licensed electricians, plumbers, and HVAC techs in the US. They already pay $50-150/mo for estimating software.

The gap is real.

---

**Tweet 5 (monetization):**
It's MIT licensed and open source.

But it's also wired for xpay pay-per-tool-call monetization.

Run it free for your own shop or host it as a paid service. The trades SaaS market is underserved and the incumbents are slow.

---

**Tweet 6 (try it):**
Built with FastMCP. Works with Claude, and any MCP-compatible client.

GitHub: https://github.com/dieselpro1111/trades-mcp-server
Try it: [YOUR_URL]

If you're an electrician, plumber, or HVAC tech — tell me what I got wrong. I want the code coverage to be right.

---

**Tweet 7 (CTA):**
If you're building in the MCP ecosystem, the trades vertical is wide open.

Star the repo if this is useful. PRs welcome — especially for regional code amendments and additional material pricing.

https://github.com/dieselpro1111/trades-mcp-server

---

## 6. Hacker News — Show HN

**Title:** Show HN: TradesPro – MCP server for skilled trades (NEC/UPC/HVAC codes, material pricing, permit requirements)

---

**Body:**

TradesPro is an open source MCP server that gives AI assistants structured knowledge of the skilled trades: electrical (NEC 2023), plumbing (UPC 2024), and HVAC (IRC Mechanical).

**Why this:** Tradespeople are already using LLMs to write proposals, look up code sections, and estimate materials. The problem is model hallucinations in this domain are expensive — a wrong NEC citation fails an inspection, an outdated material price blows a job's margin. I wanted to give the AI grounded, queryable knowledge rather than relying on parametric memory.

**The 7 tools:**
- `lookup_building_code(trade, topic)` — structured NEC/UPC/IRC Mechanical sections
- `list_code_topics(trade)` — browse available code categories
- `estimate_materials(job_type, scope)` — generate material estimates
- `scope_job(job_type)` — pull structured job templates
- `list_available_jobs()` — enumerate supported job types
- `lookup_material_price(material)` — current pricing for 40+ materials
- `check_permit_requirements(job_type, jurisdiction)` — permit triggers and requirements

**What's interesting technically:**
The code knowledge is structured as a query layer rather than a RAG pipeline over raw code text. Each code topic is modeled as a discrete object with citations, applicability conditions, and related sections. This keeps responses precise and citation-accurate rather than semantically close but wrong.

**Built with:** FastMCP, MIT licensed, xpay-compatible for pay-per-call monetization.

**The gap:** Checked Smithery, MCP.so, and Glama.ai — no MCP servers exist for the trades. There are 700K+ licensed tradespeople in the US, most in small businesses with limited software budgets. The incumbent estimating tools (ServiceTitan, Jobber, etc.) are expensive and not AI-native.

GitHub: https://github.com/dieselpro1111/trades-mcp-server
Live demo: [YOUR_URL]

Happy to discuss the data modeling approach or the trades software market.

---

## 7. LinkedIn Post

---

There's a gap in AI tooling that I don't think gets talked about enough: the skilled trades.

Electricians, plumbers, and HVAC technicians are already using AI assistants in their daily work — writing proposals, looking up code sections, estimating materials for a job. But the models they're using weren't trained to be accurate on NEC 2023 electrical codes, UPC 2024 plumbing requirements, or IRC Mechanical HVAC standards.

The cost of a wrong answer here isn't a bad email draft. It's a failed inspection, a code violation, or a job quoted $3,000 under because the material prices were from two years ago.

I built **TradesPro** to fill this gap — an open source MCP server (a plugin layer for AI assistants) that gives models structured, accurate access to:

- NEC 2023 electrical codes
- UPC 2024 plumbing codes
- IRC Mechanical HVAC codes
- Current pricing for 40+ materials (wire, pipe, fittings, equipment)
- Job scoping templates for 8 common trade jobs
- Permit requirements by job type

When I checked the major MCP server directories — Smithery, MCP.so, Glama.ai — there was nothing for the skilled trades. Not a single server. Meanwhile, the US has over 700,000 licensed electricians, plumbers, and HVAC technicians, the majority of them working in small businesses that are underserved by expensive legacy software.

This is an open source contribution, MIT licensed, free to use. It's also structured for pay-per-call monetization via xpay for anyone who wants to build a commercial service on top of it.

The trades are not a backwater. They're a $500B+ industry running on outdated tooling, and AI is starting to reach them. Building accurate, domain-specific knowledge tools for this market is both useful work and a real business opportunity.

If you're a developer building in the AI tooling space, or a trades professional who wants to try it, the GitHub is here: https://github.com/dieselpro1111/trades-mcp-server

---

## 8. Cold Email Template — Trade Business Owners

**Subject:** AI that knows NEC codes and current material prices — free pilot for your shop

---

Hi [First Name],

Quick question: how long does it take someone on your team to put together a rough material estimate for a [panel upgrade / water heater replacement / HVAC changeout]?

For most shops I've talked to, it's 20-45 minutes of pulling prices, checking code requirements, and scoping out the job — before the first word of the proposal gets written.

I built a tool called **TradesPro** that plugs your AI assistant (Claude, etc.) into accurate trade knowledge:

- **NEC 2023 / UPC 2024 / IRC Mechanical codes** — so the AI cites the right article, not a hallucination
- **Current material pricing** — wire, pipe, equipment, fittings — 40+ materials
- **Job templates** — structured scope for the jobs your shop does most
- **Permit requirements** — what triggers a permit and what inspectors look for

The goal isn't to replace your estimator or your journeymen. It's to cut the time from "we need to quote this job" to "here's a rough number" from 30 minutes to 5.

It's free and open source. I'm looking for a handful of trade shops to run a pilot and tell me what's wrong with it — missing materials, code topics you look up constantly, permit requirements that aren't right for your state.

Would a 20-minute call make sense? Or I can just send you the link and you can poke at it.

[YOUR NAME]
[YOUR_URL]
https://github.com/dieselpro1111/trades-mcp-server

---

## 9. Product Hunt Submission

### Tagline

The first AI plugin that knows building codes, material pricing, and permit requirements for trades work.

---

### Description

TradesPro is an open source MCP server that gives AI assistants real, structured knowledge of the skilled trades — so electricians, plumbers, and HVAC techs can use AI for actual job work without getting burned by hallucinated code citations or wrong material prices.

**What it includes:**

- **NEC 2023 electrical codes** — queryable by topic (AFCI, conduit fill, grounding, service entrance, and more)
- **UPC 2024 plumbing codes** — DWV sizing, venting, water heater requirements, backflow prevention
- **IRC Mechanical HVAC codes** — equipment clearances, refrigerant lines, duct sizing, venting
- **40+ material prices** — wire, pipe, fittings, equipment, updated pricing
- **8 job templates** — panel upgrades, water heater installs, HVAC changeouts, bathroom rough-ins, and more
- **Permit requirements** — by job type, with jurisdiction notes

**7 MCP tools:**
`lookup_building_code`, `list_code_topics`, `estimate_materials`, `scope_job`, `list_available_jobs`, `lookup_material_price`, `check_permit_requirements`

**Who it's for:**
Trade contractors and shops using AI assistants to write proposals, scope jobs, and answer code questions — and developers building AI tools for the trades industry.

**Why now:**
The MCP ecosystem has exploded with servers for developer tooling, productivity, and data APIs. But the skilled trades — a $500B+ US industry with 700,000+ licensed professionals — have zero MCP coverage. TradesPro is the first.

Built with FastMCP. MIT licensed. xpay-compatible for pay-per-call monetization.

---

### First Comment (to post immediately after launch)

Hey Product Hunt — maker here.

The problem that led to this: I watched a small electrical contractor use Claude to double-check an NEC citation before calling their AHJ (Authority Having Jurisdiction). The model confidently gave them a wrong article number. That kind of error in a real job is an inspection failure or a callbacks.

AI is already in trade shops. It just doesn't have reliable trade knowledge. TradesPro is the structured knowledge layer that fixes that.

A few things I'm working on next:
1. **Regional code amendments** — the IRC/NEC/UPC base codes are covered, but local amendments (California Title 24, NYC amendments, etc.) vary significantly
2. **Expanded material pricing** — more regional pricing variance, updated quarterly
3. **More job templates** — I have 8 now, would love community input on which to add next

If you're a trade professional, I'd genuinely love to hear what code topics you look up most and what's missing. The goal is accuracy, not impressive-sounding.

GitHub: https://github.com/dieselpro1111/trades-mcp-server

---

### Maker Comment (for the discussion tab)

Thanks for hunting TradesPro.

For context on why I picked this domain: when I looked at the MCP server directories (Smithery, MCP.so, Glama.ai), trades was a complete blank. Every vertical you'd expect — developer tools, CRM, productivity, data — had representation. Trades had nothing.

That surprised me given the size of the market. Electricians, plumbers, and HVAC techs are the people who make buildings work. They're running small businesses, doing technical work that requires code compliance, and they're already experimenting with AI. They just don't have tooling built for them.

The technical approach: rather than RAG over raw code text (which produces semantically close but often incorrect answers), the code knowledge is structured as discrete, citation-accurate objects. You get the right NEC section number, not a paraphrase that sounds right but cites the wrong article.

Happy to answer questions about the architecture, the data model, or the trades software market.

https://github.com/dieselpro1111/trades-mcp-server | [YOUR_URL]

---

*End of TradesPro Launch Content*
