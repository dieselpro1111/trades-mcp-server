# TradesPro MCP Server — Complete Setup Guide

**Time required:** ~30 minutes  
**Skill level:** Beginner-friendly — no prior experience needed

---

## Prerequisites

- [ ] A computer with Git installed ([download Git](https://git-scm.com/downloads) if needed)
- [ ] A web browser
- [ ] Your `trades-mcp-server` folder with all files ready

**Files you should have:**

```
trades-mcp-server/
├── server.py
├── Dockerfile
├── requirements.txt
├── railway.toml
├── smithery.yaml
├── README.md
├── GO_TO_MARKET.md
├── LICENSE
└── .gitignore
```

---

## Step 1: Create a GitHub Account

- [ ] Go to **https://github.com/signup**
- [ ] Enter your email address and click **Continue**
- [ ] Create a password and click **Continue**
- [ ] Choose a username — pick something professional:
  - Your own name: `john-smith-dev`
  - A brand handle: `tradespro-mcp`
  - Your business name: `acme-trade-tools`
- [ ] Solve the verification puzzle
- [ ] Click **Create account**
- [ ] Check your email and enter the verification code
- [ ] On the personalization screens, click **Skip personalization**

> You now have a GitHub account.

---

## Step 2: Create the Repository

- [ ] Go to **https://github.com/new**
- [ ] Fill in the form:
  - **Repository name:** `trades-mcp-server`
  - **Description:** `MCP server for skilled trades — building codes, material pricing, job scoping, and permit requirements for electrical, plumbing, and HVAC work`
  - **Visibility:** Select **Public**
  - **Initialize this repository:** Leave ALL checkboxes **unchecked** (no README, no .gitignore, no license — you already have these)
- [ ] Click **Create repository**

GitHub will show you a page with setup instructions. Now push your existing code:

- [ ] Open a terminal (Command Prompt on Windows, Terminal on Mac/Linux)
- [ ] Run these commands one at a time:

```bash
cd trades-mcp-server
git init
git add .
git commit -m "Initial commit: TradesPro MCP server with 7 tools"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/trades-mcp-server.git
git push -u origin main
```

> Replace `YOUR_USERNAME` with the GitHub username you just created.

- [ ] When prompted, enter your GitHub username and password
  - **Note:** GitHub requires a Personal Access Token instead of your password for command-line pushes. If you get an authentication error:
    1. Go to **https://github.com/settings/tokens/new**
    2. Note: `git push access`
    3. Expiration: 90 days
    4. Check the **repo** scope checkbox
    5. Click **Generate token**
    6. Copy the token and use it as your password when Git asks

- [ ] Refresh your GitHub page — you should see all your files listed

> Your code is now live at: `https://github.com/YOUR_USERNAME/trades-mcp-server`

---

## Step 3: Deploy on Railway

Railway will host your MCP server 24/7 so anyone can connect to it.

- [ ] Go to **https://railway.app**
- [ ] Click **Login** → **Login with GitHub**
- [ ] Authorize Railway to access your GitHub account
- [ ] On the Railway dashboard, click **New Project**
- [ ] Select **Deploy from GitHub Repo**
- [ ] Find and click **trades-mcp-server** in the list
- [ ] Railway will detect your Dockerfile automatically and start building

**Wait for the build to complete** (usually 2–3 minutes). You'll see a green checkmark when done.

**Generate a public URL:**

- [ ] Click on your deployment to open it
- [ ] Go to **Settings** → **Networking**
- [ ] Click **Generate Domain**
- [ ] Railway will give you a URL like:
  ```
  https://trades-mcp-server-production-xxxx.up.railway.app
  ```
- [ ] Copy this URL and save it — you'll need it in every step below

**Your MCP endpoint is:**
```
https://YOUR-RAILWAY-URL/mcp
```

**Test it works:**

- [ ] Open a new browser tab and go to `https://YOUR-RAILWAY-URL/mcp`
- [ ] You should see JSON output (MCP endpoint info), not an error page

> **Pricing:** Railway gives you $5 free trial credit. After that, expect ~$5/month for a small always-on server.

---

## Step 4: Set Up a USDC Wallet (to receive payments)

You need a crypto wallet on the **Base** network to receive USDC payments from xpay.

**Option A — Coinbase Wallet (recommended, beginner-friendly):**

- [ ] Go to **https://www.coinbase.com/wallet** and click **Download**
- [ ] Install the browser extension (Chrome/Firefox/Brave)
- [ ] Click the extension icon → **Create a new wallet**
- [ ] Write down your 12-word recovery phrase on paper and store it somewhere safe
  - **This is critical — losing this phrase means losing your funds permanently**
- [ ] Set a password for the extension

**Switch to Base network:**

- [ ] Click the network selector at the top of the wallet (it may say "Ethereum")
- [ ] Select **Base** from the list
  - If Base isn't listed, click **Manage networks** and enable it

**Get your wallet address:**

- [ ] Click **Receive** or the copy icon next to your account name
- [ ] Your wallet address looks like: `0x1234...abcd`
- [ ] Copy this address and save it — you'll paste it into xpay in the next step

> **Option B:** Any wallet that supports Base network works (MetaMask with Base network added, Rainbow, etc.)

---

## Step 5: Register on xpay for Monetization

xpay wraps your MCP server with a payment layer. You share the xpay URL publicly instead of your direct Railway URL. xpay charges nothing — you keep 100% of earnings.

- [ ] Go to **https://xpay.sh**
- [ ] Click **Sign up** and create an account
- [ ] Verify your email if prompted

**Create a monetized MCP endpoint:**

- [ ] In your xpay dashboard, click **New MCP Server** (or **Add Server**)
- [ ] Fill in the form:
  - **Server URL:** `https://YOUR-RAILWAY-URL/mcp` (your Railway endpoint from Step 3)
  - **Receiving wallet:** paste your Base USDC wallet address from Step 4
- [ ] Set per-tool pricing:

  | Tool | Suggested Price |
  |------|----------------|
  | `lookup_building_code` | $0.02 |
  | `list_code_topics` | $0.01 |
  | `estimate_materials` | $0.05 |
  | `scope_job` | $0.10 |
  | `list_available_jobs` | $0.01 |
  | `lookup_material_price` | $0.02 |
  | `check_permit_requirements` | $0.05 |

- [ ] Save/create the endpoint

**xpay will give you a proxy URL like:**
```
https://tradespro.mcp.xpay.sh/mcp
```

- [ ] Copy and save this proxy URL — **this is the URL you share publicly**

> Never share your direct Railway URL publicly once you've set up xpay. The proxy URL ensures all usage goes through the payment layer.

---

## Step 6: Submit to MCP Directories

Get your server discovered by people searching for trade tools. Submit to all four directories — takes about 10 minutes total.

### Smithery (largest MCP marketplace)

- [ ] Go to **https://smithery.ai**
- [ ] Click **Sign in** → **Sign in with GitHub**
- [ ] Look for **"Deploy your server"** or **"Submit"**
- [ ] Connect your GitHub repository (`trades-mcp-server`)
- [ ] Smithery reads your `smithery.yaml` and `Dockerfile` automatically — no extra config needed
- [ ] Submit for review

Your listing will appear at:
```
https://smithery.ai/server/YOUR-USERNAME/trades-mcp-server
```

---

### MCP.so

- [ ] Go to **https://mcp.so**
- [ ] Find **"Submit a server"** or **"Add server"**
- [ ] Paste your GitHub repo URL: `https://github.com/YOUR_USERNAME/trades-mcp-server`
- [ ] Fill in:
  - **Name:** TradesPro MCP Server
  - **Description:** MCP server for skilled trades — building codes, material pricing, job scoping, and permit requirements for electrical, plumbing, and HVAC work
  - **Category:** Productivity or Reference

---

### Glama.ai

- [ ] Go to **https://glama.ai/mcp/servers**
- [ ] Click **Submit server** or **Add server**
- [ ] Paste your GitHub repo URL
- [ ] Fill in the name and description (same as above)

---

### mcpservers.org

- [ ] Go to **https://mcpservers.org**
- [ ] Find the submit link (usually in the header or footer)
- [ ] Submit your server listing with the GitHub URL

---

## Step 7: Verify Everything Works

### Test via Claude Desktop

- [ ] Open your Claude Desktop config file:
  - **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
  - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- [ ] Add your server:

```json
{
  "mcpServers": {
    "trades-pro": {
      "url": "https://YOUR-RAILWAY-URL/mcp"
    }
  }
}
```

- [ ] Save the file and restart Claude Desktop
- [ ] Ask Claude: **"What are the GFCI requirements for a kitchen remodel?"**
- [ ] Claude should respond using your `lookup_building_code` tool

---

### Test via Cursor

- [ ] Open Cursor → **Settings** → **Features** → **MCP Servers**
- [ ] Click **Add** and enter:
  - **URL:** `https://YOUR-RAILWAY-URL/mcp`
- [ ] Save, then test by asking a trade question in Cursor's AI chat

---

### Test the xpay Proxy

- [ ] Repeat either test above but use your **xpay URL** instead:
  ```
  https://tradespro.mcp.xpay.sh/mcp
  ```
- [ ] Confirm it responds correctly — this validates the full payment flow

---

## Quick Reference Card

| What | URL |
|------|-----|
| GitHub Repo | `https://github.com/YOUR_USERNAME/trades-mcp-server` |
| Railway Dashboard | `https://railway.app/dashboard` |
| Live Server | `https://YOUR-RAILWAY-URL/mcp` |
| xpay Dashboard | `https://xpay.sh/dashboard` |
| Monetized Proxy | `https://tradespro.mcp.xpay.sh/mcp` |
| Smithery Listing | `https://smithery.ai/server/YOUR-USERNAME/trades-mcp-server` |
| Coinbase Wallet | `https://www.coinbase.com/wallet` |

> **Fill in your actual URLs above once you have them.** Pin this file or keep it open during setup.

---

## Estimated Costs

| Service | Cost |
|---------|------|
| GitHub | Free |
| Railway | ~$5/month (free $5 trial credit to start) |
| xpay | Free (0% fee — you keep everything) |
| Smithery | Free |
| Coinbase Wallet | Free |
| Domain (optional) | ~$12/year |
| **Total** | **~$5/month** |

---

## What to Do After Setup

Once everything is live:

- [ ] **Record a 2-minute demo** — screen record yourself asking Claude trade questions using your tools (GFCI code lookup, estimating pipe for a bathroom remodel, etc.)
- [ ] **Post on Reddit** — share the demo in these communities:
  - r/mcp
  - r/HVAC
  - r/electricians
  - r/Plumbing
  - r/DIY
- [ ] **Post on X/Twitter** with the demo video and your Smithery link
- [ ] **Start B2B outreach** — read `GO_TO_MARKET.md` for a full strategy on reaching trade businesses and contractors

---

## Troubleshooting

**Railway build fails:**
- Check the build logs in Railway dashboard for the error
- Make sure your `Dockerfile` and `requirements.txt` are in the root of the repo (not in a subfolder)

**`git push` authentication error:**
- Use a Personal Access Token instead of your password — see the note in Step 2

**MCP endpoint returns an error:**
- Give Railway 2–3 minutes after deployment before testing
- Check that your Railway service is in "Active" state, not "Sleeping"

**xpay proxy doesn't work:**
- Confirm your Railway URL is publicly accessible first (test it directly)
- Make sure you entered the full URL including `/mcp` when setting up xpay

**Tools not showing up in Claude:**
- Restart Claude Desktop after editing the config file
- Verify the JSON in your config file is valid (no missing commas or brackets)

---

*Guide version: March 2026*
