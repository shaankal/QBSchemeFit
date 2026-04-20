# QB Scheme Fit — Phase 1
### 2026 NFL Draft Offensive Blueprint Generator

An AI-powered tool that classifies QB archetypes and generates full offensive blueprints for 2026 NFL Draft prospects. Built to demonstrate what a front office scheme-fit tool looks like in practice.

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here

# 3. Run the app
streamlit run app.py
```

---

## What it does

- **QB Selector** — Choose from the top 5 2026 draft QB prospects
- **Scouting Profile** — Pre-loaded measurables, stats, strengths, and concerns
- **Attribute Radar** — Pocket IQ, Arm Talent, Mobility, Game Management, Deep Ball (scored 0–100)
- **Archetype Classification** — ML-style label: Pocket Surgeon, Gunslinger, System Operator, etc.
- **Offensive Blueprint** — Claude-generated OC memo with:
  - Offensive system fit
  - Scheme principles
  - Signature play concepts
  - Ideal supporting cast
  - Year 1 recommendation
  - Red flags for teams
- **Team Context Input** — Add a specific NFL team to get a tailored blueprint

---

## 2026 QB Prospects Included

| QB | School | Archetype | NFL Comp |
|---|---|---|---|
| Fernando Mendoza | Indiana | Pocket Surgeon | Joe Burrow |
| Ty Simpson | Alabama | System Operator | Baker Mayfield |
| Garrett Nussmeier | LSU | Gunslinger | Derek Carr |
| Drew Allar | Penn State | Developmental Dual-Threat | Daniel Jones |
| Carson Beck | Miami | Gunslinger | Matt Stafford |

---

## Roadmap

- **Phase 2** — Any NFL QB input, pull live stats via nfl_data_py + NGS
- **Phase 3** — Live roster integration, gap analysis, offseason recommendations ("to run this system you need a TE who can block...")
