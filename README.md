# TradesPro MCP Server

An MCP (Model Context Protocol) server that gives AI assistants access to skilled trades knowledge — building codes, material pricing, job scoping, and permit requirements for **electrical, plumbing, and HVAC** work.

## Why This Exists

AI assistants (Claude, ChatGPT, Cursor) can't look up building codes, estimate materials, or scope trade jobs accurately. This MCP server fixes that by giving agents structured, queryable access to:

- **NEC 2023** electrical codes (GFCI, AFCI, wire sizing, panel requirements)
- **UPC 2024** plumbing codes (drain sizing, venting, water heater sizing)
- **IRC Mechanical** HVAC codes (duct sizing, refrigerant lines, efficiency standards)
- **Material pricing** — 40+ common trade materials with national average prices
- **Job templates** — 8 standard residential jobs with labor, materials, and total pricing
- **Permit checker** — Determines if a described job likely requires permits

## Quick Start

### Install
```bash
pip install fastmcp
```

### Run locally (stdio)
```bash
python server.py
```

### Run as HTTP server
```bash
fastmcp run server.py:mcp --transport http --port 8000
```

### Test with FastMCP Inspector
```bash
fastmcp dev server.py:mcp
```
This opens a web UI at http://127.0.0.1:6274 where you can test all tools interactively.

## Connect to AI Clients

### Claude Desktop
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "trades-pro": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### Cursor
Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "trades-pro": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### Remote (HTTP)
```json
{
  "mcpServers": {
    "trades-pro": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `lookup_building_code` | Look up specific code requirements (trade + topic) |
| `list_code_topics` | List all available code topics for a trade |
| `estimate_materials` | Get itemized material list and costs for a job |
| `scope_job` | Full job scope: labor, materials, price range, permits |
| `list_available_jobs` | Browse job templates, optionally filtered by trade |
| `lookup_material_price` | Search material pricing by keyword |
| `check_permit_requirements` | Check if a job description likely requires permits |

## Example Queries

Once connected, ask your AI assistant:
- "What are the GFCI requirements for a kitchen remodel?"
- "Scope out a 200A panel upgrade — labor, materials, and total cost"
- "Do I need a permit to install an EV charger?"
- "What size wire do I need for a 50A circuit?"
- "Estimate materials for a bathroom rough-in"

## Authentication & Pricing

TradesPro uses API key-based authentication with two tiers:

### Free Tier (default)
- Access to **all 7 tools** — try everything before buying
- **10 calls per hour** rate limit
- Use demo key `trades_demo_2026` or connect without any key
- Responses include a small footer with upgrade link

### Pro Tier
- **Unlimited** access to all tools
- No rate limiting
- No footer messages
- Get your API key at [bluecollar.run/pro](https://bluecollar.run/pro)

### Configuring Your API Key

#### Claude Desktop
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "trades-pro": {
      "url": "https://your-server-url.com/mcp",
      "headers": {
        "X-API-Key": "pk_your_api_key_here"
      }
    }
  }
}
```

#### Cursor
Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "trades-pro": {
      "url": "https://your-server-url.com/mcp",
      "headers": {
        "X-API-Key": "pk_your_api_key_here"
      }
    }
  }
}
```

#### Free Tier (no key needed)
```json
{
  "mcpServers": {
    "trades-pro": {
      "url": "https://your-server-url.com/mcp"
    }
  }
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEYS` | JSON string mapping API keys to tiers, e.g. `{"pk_abc123": "pro"}` | `""` (free tier only) |
| `PORT` | HTTP server port | `8000` |

### Additional Monetization Options

#### xpay (Pay-per-call, zero code changes)
1. Deploy the server as an HTTP endpoint
2. Register at [xpay.sh](https://xpay.sh)
3. Set per-tool pricing ($0.01–$0.25 per call)
4. Share the proxy URL instead of your direct server URL

#### B2B Retainer
Bundle this server with a custom AI agent for trade businesses:
- Charge $500–$2,000/month per client
- Customize data for their local market (local pricing, local codes)
- Add features: scheduling integration, invoice generation, CRM

## Publishing to Smithery

```bash
npm install -g @smithery/cli
smithery mcp publish https://your-server-url.com/mcp -n your-org/trades-pro
```

## Extending the Server

### Add local pricing
Replace the `MATERIAL_PRICES` dict with data from local suppliers. The structure is simple:
```python
"Item name": {"price": 0.00, "unit": "each", "category": "electrical"}
```

### Add local code amendments
Many jurisdictions amend national codes. Add a `local_amendments` dict and modify `lookup_building_code` to layer local rules on top.

### Add more job templates
Follow the `JOB_TEMPLATES` structure to add new jobs. Each template needs: name, trade, description, labor hours, materials list, permit info, and notes.

## Hosting Options

| Option | Cost | Best For |
|--------|------|----------|
| Local (your machine) | Free | Development, personal use |
| Railway.app | ~$5/month | Cheap always-on hosting |
| Fly.io | ~$5/month | Edge deployment |
| Prefect Horizon | Free tier | FastMCP native hosting |
| Docker on VPS | ~$5-10/month | Full control |

## License

MIT
