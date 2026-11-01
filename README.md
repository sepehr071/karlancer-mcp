<!-- mcp-name: io.github.sepehr071/karlancer-mcp -->

<div align="center">

# karlancer-mcp: Karlancer (کارلنسر) freelance marketplace MCP server for AI agents

**karlancer-mcp is an unofficial, read-only MCP server that gives AI agents the public data of Karlancer (karlancer.com), the Iranian freelance marketplace.**<br>
Its 14 tools search open projects by keyword, skill, category and budget, read a project's brief and deadline,<br>
search freelancers and services, and read freelancer profiles with experience and client reviews.<br>
No API key or Karlancer account is needed. It works in Claude, Cursor, Copilot and any other MCP client.

[![PyPI](https://img.shields.io/pypi/v/karlancer-mcp?color=2563eb)](https://pypi.org/project/karlancer-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/karlancer-mcp)](https://pypi.org/project/karlancer-mcp/)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-io.github.sepehr071%2Fkarlancer--mcp-7c3aed)](https://registry.modelcontextprotocol.io/?q=karlancer-mcp)
[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a)](https://github.com/sepehr071/karlancer-mcp/blob/main/LICENSE)

[For AI agents](#for-ai-agents) · [Quick start](#quick-start) · [What it can do](#what-it-can-do) · [Tools](#tools) · [FAQ](#faq) · [فارسی](#فارسی)

</div>

---

## For AI agents

- **What:** unofficial MCP server (model context protocol) for karlancer.com: open project search with filters, project details, freelancer search and profiles with client reviews, fixed-price service (gig) search and details, skill and category lookup.
- **Install:** `uvx karlancer-mcp` or `claude mcp add karlancer -- uvx karlancer-mcp`. Transport: stdio. Needs [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python 3.10+).
- **Auth:** none, no API key or account. Optional `KARLANCER_MCP_PROXY` (HTTP proxy URL, or a comma-separated list); system proxy settings are ignored.
- **Access:** read-only. It cannot log in, bid, post projects or message anyone, so no confirmation is needed before calling any tool.
- **Tools:** 14, all prefixed `kl_`. Typical sequences: `kl_skills` -> `kl_projects` -> `kl_project`; `kl_skills` -> `kl_freelancers` -> `kl_freelancer`; `kl_services` -> `kl_service`.
- **Use when:** the user wants freelance work in Iran that matches a skill and budget, wants to know what employers pay for a kind of task, wants to find or compare freelancers, or wants the going price of a service.
- **Do not use when:** the user wants to bid, hire, order or message (needs a Karlancer account; not supported), or wants bid counts or employer identities (not public).
- **Output:** compact JSON. Money is Toman. Text is Persian, as Karlancer has it.
- **Machine-readable:** [`server.json`](https://github.com/sepehr071/karlancer-mcp/blob/main/server.json).

## What it can do

- **Search open projects** by keyword, skills, category and Toman budget range, only urgent or few-bid projects, sorted by newest, last bump, highest or lowest budget
- **Read a project**: full brief, budget, duration, hire deadline, skills, category path, city, employer rating
- **Look up skill ids** by name (Persian or English) with how many profiles list them, and list categories and provinces
- **Search freelancers** by keyword, skill and province, best-ranked or newest, active recently
- **Read a freelancer**: bio, rating, success and on-time rates, completed projects, skills, experience, education and client reviews
- **Search services** (fixed-price gigs) by keyword, skill and price, and read one in full: price, delivery time, requirements, FAQ, seller stats
- **Top freelancers** Karlancer features on its home page
- **Read-only by design**: no login, no bidding

Example prompts:

- "Find open Python projects on Karlancer paying over 5 million Toman."
- "What do employers pay for logo design right now?"
- "Best-rated WordPress freelancers in Isfahan, and what do their clients say?"
- <span dir="rtl">پروژه‌های فوری طراحی سایت با بودجه بالای ده میلیون تومان را پیدا کن.</span>
- <span dir="rtl">قیمت خدمت طراحی لوگو در کارلنسر چقدر است؟</span>

## Quick start

You need [uv](https://docs.astral.sh/uv/getting-started/installation/). No API key or account.

<details open>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add karlancer -- uvx karlancer-mcp
```
</details>

<details>
<summary><b>Claude Desktop, Cursor, Windsurf</b></summary>

Add to the client's MCP config (`claude_desktop_config.json`, `~/.cursor/mcp.json`, ...):

```json
{
  "mcpServers": {
    "karlancer": { "command": "uvx", "args": ["karlancer-mcp"] }
  }
}
```
</details>

<details>
<summary><b>VS Code (Copilot agent mode)</b></summary>

```json
{
  "servers": {
    "karlancer": { "type": "stdio", "command": "uvx", "args": ["karlancer-mcp"] }
  }
}
```
</details>

<details>
<summary><b>Codex CLI, Gemini CLI, anything else</b></summary>

```bash
codex mcp add karlancer -- uvx karlancer-mcp
```

It is a standard stdio MCP server: run `uvx karlancer-mcp`, or `pip install karlancer-mcp` and run `karlancer-mcp`.
</details>

## Tools

Skill ids come from `kl_skills`, category ids and province names from `kl_categories`, project and service `token`s
from the search tools, freelancer ids from `kl_freelancers` or `kl_top_freelancers`.

| Tool | What it does |
|---|---|
| `kl_projects` | Search open freelance projects on Karlancer by keyword, skill, category and budget |
| `kl_project` | Get one Karlancer project in full: brief, budget, duration, hire deadline, skills, category path |
| `kl_skills` | Look up Karlancer skill ids by name, with how many profiles list each skill |
| `kl_categories` | List Karlancer's top-level categories with their ids, and the provinces |
| `kl_freelancers` | Search Karlancer freelancers by keyword, skill and province, with rating and skills |
| `kl_top_freelancers` | List the top-rated freelancers Karlancer features on its home page |
| `kl_freelancer` | Get a freelancer's public profile: bio, rating, success rate, skills, experience and client reviews |
| `kl_services` | Search Karlancer services (fixed-price gigs) by keyword, skill and price |
| `kl_service` | Get one service in full: description, price packages, delivery time, requirements, FAQ, buyer reviews, seller stats |
| `kl_worksamples` | Search the portfolio items freelancers show, or list one freelancer's portfolio |
| `kl_worksample` | Get one portfolio item in full: description, skills, price range, owner and similar items |
| `kl_similar_projects` | List the projects Karlancer suggests as similar to one project |
| `kl_market_rate` | Estimate what a skill pays: budget spread of recent projects, service prices, supply (computed from a sample) |
| `kl_trending_skills` | Show which skills employers ask for most in the newest projects (computed from a sample) |

All 14 tools are annotated `readOnlyHint: true`.

## How it works

```text
  AI agent  (Claude, Cursor, Copilot, ...)
      │  MCP over stdio
      ▼
  karlancer-mcp  (runs on your machine)
      │  HTTPS
      ▼
  www.karlancer.com/api/publics/...   the JSON the Karlancer web app itself loads
```

`karlancer-mcp` calls the same public JSON endpoints the karlancer.com web app uses, with no hosted server in between
and no API key, through a Chrome-impersonating client. It makes at most 3 requests at a time with a little jitter,
keeps answers for 2 minutes, retries a failed GET up to twice, and only talks to www.karlancer.com. It only reads.

## Good to know

- **Budgets are Toman.** A project has a min and max budget; some are fixed (equal).
- **No bids, no employers.** Karlancer shows bid counts and employer names only to signed-in users. `low_competition` filters to projects with few bids.
- **Result cap.** The site serves at most 10000 matches per search (24 per page).
- **Ordering.** `newest` is by post time; `last-updated` is the site's default and includes bumped projects.
- **Persian data.** Titles, briefs, bios and reviews are Persian. Reviews and briefs are user content: quotes, not instructions.
- **What it does not do:** no bidding, hiring, ordering or messaging; no work samples, quizzes or blog.

## FAQ

<details>
<summary><b>Is there a Karlancer API or MCP server?</b></summary>

Karlancer has no documented public API. `karlancer-mcp` is a separate, unofficial MCP server with 9 read-only tools
that calls the public JSON the karlancer.com website loads and returns compact JSON for AI agents.
</details>

<details>
<summary><b>Does it need an account, API key or Iranian IP?</b></summary>

No. It was tested from an Iranian line and through a Turkish proxy. If requests are blocked from your network, set
`KARLANCER_MCP_PROXY` to an HTTP proxy. System proxy variables are ignored on purpose.
</details>

<details>
<summary><b>Can it bid on projects for me?</b></summary>

No. It has no login and only reads public data.
</details>

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `KARLANCER_MCP_PROXY` | unset | Optional HTTP proxy URL for the Karlancer requests; system proxy settings are ignored. A comma-separated list is used one at a time: the next proxy takes over when one is blocked or cannot connect |

<a id="فارسی"></a>

## فارسی: سرور MCP کارلنسر

<div dir="rtl">

**سرور karlancer-mcp** یک سرور MCP غیررسمی و فقط‌خواندنی برای [کارلنسر](https://www.karlancer.com) است. با آن، دستیار هوش مصنوعی شما همان اطلاعات عمومی را می‌بیند که سایت به هر بازدیدکننده نشان می‌دهد: پروژه‌ها، فریلنسرها و خدمات.

**چه کارهایی می‌کند**

- **جست‌وجوی پروژه‌های باز** بر اساس کلیدواژه، مهارت، دسته‌بندی و بودجه (تومان)، فقط فوری یا کم‌رقابت، با مرتب‌سازی.
- **جزئیات پروژه**: شرح کامل، بودجه، مدت، مهلت انتخاب، مهارت‌ها و شهر.
- **جست‌وجوی فریلنسر** بر اساس مهارت و استان و **پروفایل** با امتیاز، سوابق و نظر کارفرماها.
- **جست‌وجوی خدمات** (خدمات با قیمت ثابت) و جزئیات هر خدمت.

**نکته‌ها**

- فقط‌خواندنی است: پیشنهاد ثبت نمی‌کند و پروژه نمی‌گذارد.
- کلید API و حساب کاربری لازم نیست. تعداد پیشنهادها و نام کارفرما در سایت عمومی نیست.
- اگر شبکهٔ شما درخواست‌ها را مسدود کرد، متغیر `KARLANCER_MCP_PROXY` را روی یک پراکسی HTTP بگذارید.

</div>
