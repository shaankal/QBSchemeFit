import streamlit as st
import anthropic
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QB Scheme Fit",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Sans+Condensed:wght@600;700&display=swap');

:root {
    --accent: #4A9EFF;
    --accent-dim: rgba(74,158,255,0.12);
    --warn: #F5A623;
    --warn-dim: rgba(245,166,35,0.12);
    --ok: #2ECC71;
    --ok-dim: rgba(46,204,113,0.12);
    --danger: #E74C3C;
    --danger-dim: rgba(231,76,60,0.12);
    --bg: #0E1117;
    --bg2: #161B24;
    --bg3: #1C2333;
    --bg4: #222B3A;
    --line: #2A3447;
    --line2: #344156;
    --text: #E2E8F0;
    --text2: #94A3B8;
    --text3: #64748B;
    --white: #F8FAFC;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}
.stApp { background-color: var(--bg); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.topbar {
    background: var(--bg2);
    border-bottom: 1px solid var(--line);
    padding: 0.6rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.topbar-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    color: var(--white);
    text-transform: uppercase;
}
.topbar-logo span { color: var(--accent); }
.topbar-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--text3);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.topbar-status {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--ok);
    letter-spacing: 0.08em;
}
.topbar-dot {
    width: 6px; height: 6px;
    background: var(--ok);
    border-radius: 50%;
}

/* ── SUBBAR ── */
.subbar {
    background: var(--bg);
    border-bottom: 1px solid var(--line);
    padding: 0.4rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--text3);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.25rem;
}
.subbar-item { display: flex; align-items: center; gap: 0.4rem; }
.subbar-val { color: var(--text2); font-weight: 500; }

/* ── MAIN WRAP ── */
.main-wrap { padding: 0 1.5rem 2rem; }

/* ── PANEL ── */
.panel {
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 0.75rem;
}
.panel-header {
    background: var(--bg3);
    border-bottom: 1px solid var(--line);
    padding: 0.45rem 0.875rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.panel-header-left { display: flex; align-items: center; gap: 0.5rem; }
.panel-header-dot { width: 6px; height: 6px; background: var(--accent); border-radius: 50%; }
.panel-header-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    color: var(--text3);
    text-transform: uppercase;
}
.panel-header-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.55rem;
    color: var(--accent);
    background: var(--accent-dim);
    border: 1px solid rgba(74,158,255,0.2);
    padding: 0.1rem 0.4rem;
    border-radius: 2px;
    letter-spacing: 0.08em;
}

/* ── QB LIST ── */
.qb-row {
    display: flex;
    align-items: center;
    padding: 0.55rem 0.875rem;
    border-bottom: 1px solid var(--line);
    cursor: pointer;
    transition: background 0.1s;
    border-left: 2px solid transparent;
}
.qb-row:last-child { border-bottom: none; }
.qb-row:hover { background: var(--bg3); }
.qb-row.active { background: var(--bg3); border-left-color: var(--accent); }
.qb-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--text3);
    width: 1.4rem;
    flex-shrink: 0;
}
.qb-info { flex: 1; min-width: 0; }
.qb-name-text {
    font-family: 'IBM Plex Sans Condensed', sans-serif;
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 0.02em;
    white-space: nowrap;
}
.qb-school { font-size: 0.65rem; color: var(--text3); margin-top: 1px; }
.qb-grade {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--warn);
    flex-shrink: 0;
}

/* ── QB HERO HEADER ── */
.qb-hero {
    background: var(--bg3);
    border-bottom: 1px solid var(--line);
    padding: 1rem 0.875rem 0.875rem;
}
.qb-hero-name {
    font-family: 'IBM Plex Sans Condensed', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--white);
    letter-spacing: 0.02em;
    line-height: 1.1;
}
.qb-hero-meta { font-size: 0.72rem; color: var(--text2); margin-top: 0.25rem; }
.qb-hero-rank {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--accent);
    margin-top: 0.2rem;
    letter-spacing: 0.06em;
}

/* ── STAT GRID ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: var(--line);
}
.stat-cell {
    background: var(--bg2);
    padding: 0.625rem 0.5rem;
    text-align: center;
}
.stat-cell .sv {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--white);
    line-height: 1;
}
.stat-cell .sl {
    font-size: 0.58rem;
    color: var(--text3);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* ── ATTRIBUTE BARS ── */
.attr-row { padding: 0.3rem 0.875rem; border-bottom: 1px solid var(--line); }
.attr-row:last-child { border-bottom: none; }
.attr-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.65rem;
    margin-bottom: 0.25rem;
}
.attr-label {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--text2);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-size: 0.6rem;
}
.attr-val {
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    font-size: 0.7rem;
}
.attr-track {
    height: 3px;
    background: var(--bg4);
    border-radius: 1px;
    overflow: hidden;
}
.attr-fill { height: 100%; border-radius: 1px; }

/* ── TAGS ── */
.tag-section { padding: 0.625rem 0.875rem; border-bottom: 1px solid var(--line); }
.tag-section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    color: var(--text3);
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}
.tag-row { display: flex; flex-wrap: wrap; gap: 0.3rem; }
.tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    font-weight: 500;
    padding: 0.15rem 0.45rem;
    border-radius: 2px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.tag.strength { background: var(--ok-dim); border: 1px solid rgba(46,204,113,0.2); color: var(--ok); }
.tag.weakness { background: var(--danger-dim); border: 1px solid rgba(231,76,60,0.2); color: var(--danger); }

/* ── ARCHETYPE ROW ── */
.archetype-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg3);
    border-bottom: 1px solid var(--line);
    padding: 0.75rem 0.875rem;
}
.archetype-left {}
.archetype-kicker {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    color: var(--text3);
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.archetype-name {
    font-family: 'IBM Plex Sans Condensed', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.archetype-right { text-align: right; }
.archetype-comp-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.55rem;
    color: var(--text3);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.archetype-comp-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--warn);
}

/* ── PROFILE TEXT ── */
.profile-text {
    padding: 0.875rem;
    font-size: 0.8rem;
    line-height: 1.7;
    color: var(--text2);
    border-bottom: 1px solid var(--line);
}

/* ── TEAM INPUT ROW ── */
.input-row { padding: 0.75rem 0; }

/* ── GENERATE BUTTON ── */
.stButton > button {
    background: var(--bg3) !important;
    color: var(--accent) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: 1px solid var(--accent) !important;
    border-radius: 2px !important;
    padding: 0.6rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: var(--accent-dim) !important;
}
.stButton > button:disabled {
    background: var(--bg3) !important;
    color: var(--text3) !important;
    border-color: var(--line) !important;
}

/* ── INPUT ── */
.stTextInput > div > div > input {
    background: var(--bg3) !important;
    border: 1px solid var(--line2) !important;
    color: var(--text) !important;
    border-radius: 2px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.8rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: none !important;
}
.stTextInput label {
    color: var(--text3) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.6rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── REPORT ── */
.report-body {
    padding: 1rem 0.875rem;
    font-size: 0.8rem;
    line-height: 1.75;
    color: var(--text2);
}
.report-body h3 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    color: var(--accent);
    text-transform: uppercase;
    margin-top: 1.25rem;
    margin-bottom: 0.4rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid var(--line);
}
.report-body ul { padding-left: 1.1rem; }
.report-body li { margin-bottom: 0.35rem; color: var(--text2); }
.report-body p { color: var(--text2); margin-bottom: 0.5rem; }
.report-body strong { color: var(--text); }

/* ── EMPTY STATE ── */
.empty-state {
    padding: 2.5rem 1rem;
    text-align: center;
    border: 1px dashed var(--line2);
    border-radius: 3px;
    margin: 0.5rem 0;
}
.empty-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    color: var(--text3);
    text-transform: uppercase;
}
.empty-sub { font-size: 0.72rem; color: var(--text3); margin-top: 0.3rem; opacity: 0.6; }

/* ── DIVIDER ── */
.divider { border: none; border-top: 1px solid var(--line); margin: 0.75rem 0; }

/* ── RADIO OVERRIDE ── */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 0 !important;
    background: var(--bg3) !important;
    border: 1px solid var(--line2) !important;
    border-radius: 2px !important;
    overflow: hidden !important;
    width: fit-content !important;
    padding: 0 !important;
}
div[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center !important;
    padding: 0.35rem 1rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    border-radius: 0 !important;
    color: var(--text3) !important;
    transition: all 0.1s !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: var(--accent-dim) !important;
    color: var(--accent) !important;
}
div[data-testid="stRadio"] > div > label > div:first-child { display: none !important; }
div[data-testid="stRadio"] > div > label > div { color: inherit !important; }
</style>
""", unsafe_allow_html=True)

# ── QB Data ───────────────────────────────────────────────────────────────────
QBS = {
    "Fernando Mendoza": {
        "school": "Indiana",
        "rank": "#1 Overall Pick",
        "height": "6'5\"",
        "weight": "236 lbs",
        "forty": "4.75",
        "stats": {
            "2025 Pass Yds": "3,535",
            "TDs": "41",
            "INTs": "6",
            "Comp %": "72%",
            "aDOT": "9.2",
        },
        "strengths": ["Elite clutch performance", "Quick processing", "Timing routes", "RPO execution", "Play-action"],
        "weaknesses": ["Pocket mobility under pressure", "One year of elite production", "Deep ball consistency"],
        "comp": "Joe Burrow",
        "archetype": "POCKET SURGEON",
        "profile": """
Fernando Mendoza is the most pro-ready QB in this class. Won the Heisman, led Indiana to a national championship,
and delivered multiple game-winning drives under pressure. He operates best in timing-based offenses with clear
pre-snap reads. His arm talent is sufficient but his real weapon is processing speed — he gets the ball out fast
and on time. He is not a dynamic scrambler but has functional mobility to extend plays.
His comp is Joe Burrow: a one-year wonder who elevated with elite football IQ and precision passing.
"""
    },
    "Ty Simpson": {
        "school": "Alabama",
        "rank": "#2 QB / ~#20 Overall",
        "height": "6'1\"",
        "weight": "211 lbs",
        "forty": "4.60",
        "stats": {
            "Career Starts": "15",
            "2025 Role": "Starter",
            "Mobility": "High",
            "IQ": "Elite",
            "Interviews": "Top-rated",
        },
        "strengths": ["Pre-snap IQ", "Protection communication", "Decision making", "Athleticism", "Interviews/intangibles"],
        "weaknesses": ["Limited career starts", "Inconsistent arm strength", "Unproven at scale"],
        "comp": "Baker Mayfield",
        "archetype": "SYSTEM OPERATOR",
        "profile": """
Ty Simpson is a cerebral operator who spent years learning behind Bryce Young and Jalen Milroe. He understands
NFL-level defensive structures better than most prospects at this stage. His athleticism is a plus — he can
extend plays and is a legitimate running threat. The question mark is volume: with only 15 career starts, teams
are projecting significant development. Front offices are split on his ceiling — some see a starter who can win
with a good team around him, others see a smart backup. His Senior Bowl and combine interviews were highly rated.
"""
    },
    "Garrett Nussmeier": {
        "school": "LSU",
        "rank": "#3 QB / ~#84 Overall",
        "height": "6'2\"",
        "weight": "203 lbs",
        "forty": "4.75",
        "stats": {
            "2025 Pass Yds": "1,927",
            "TDs": "12",
            "INTs": "5",
            "Comp %": "67%",
            "Senior Bowl": "Strong",
        },
        "strengths": ["Arm talent", "Vertical throws", "Senior Bowl performance", "Pre-draft interviews"],
        "weaknesses": ["Injury-shortened 2025 season", "Body weight/frame concerns", "Consistency"],
        "comp": "Derek Carr",
        "archetype": "GUNSLINGER",
        "profile": """
Nussmeier learned behind Jayden Daniels and has real NFL arm talent. His 2025 season was derailed by an
abdominal injury but his Senior Bowl performance reminded scouts why he was once considered a top prospect.
He can spin it — vertical concepts and contested catches are his bread and butter. His frame is lean and
teams will want to see if he can hold up to an NFL season. Team sources believe he could sneak into the
second round on draft day. His interviews have been a strong suit and he has the football pedigree
(son of LSU OC Mike Nussmeier) to understand scheme at a high level.
"""
    },
    "Drew Allar": {
        "school": "Penn State",
        "rank": "#4 QB / ~#88 Overall",
        "height": "6'5\"",
        "weight": "228 lbs",
        "forty": "4.70",
        "stats": {
            "2024 Pass Yds": "3,327",
            "TDs": "24",
            "Rush TDs": "6",
            "Comp %": "67%",
            "2025": "Injured",
        },
        "strengths": ["Size and frame", "Dual-threat ability", "Big-game experience", "Ball placement mid-range"],
        "weaknesses": ["Leg injury in 2025", "Footwork mechanics", "Field vision under pressure"],
        "comp": "Daniel Jones",
        "archetype": "DEVELOPMENTAL DUAL-THREAT",
        "profile": """
Allar has the ideal NFL size at 6'5" 228 lbs and showed legitimate dual-threat ability with 6 rushing TDs in 2024.
His 2025 season ended early with a leg injury against Northwestern, limiting his evaluation window. The tape
from 2024 showed a QB with good athleticism for his size but inconsistent footwork and field vision when
defenses brought pressure. He needs development time — likely a year 2-3 starter if given the right room to grow.
His best fit is an offense that uses his legs as a genuine threat, not just scrambles.
"""
    },
    "Carson Beck": {
        "school": "Miami (FL)",
        "rank": "#5 QB / ~#112 Overall",
        "height": "6'5\"",
        "weight": "233 lbs",
        "forty": "4.80",
        "stats": {
            "Georgia Yds": "3,941 (2023)",
            "TDs": "24",
            "INTs": "6",
            "Comp %": "72%",
            "Arm Talent": "Elite",
        },
        "strengths": ["Elite arm talent", "Deep ball", "Size", "Big Ten + ACC experience", "Vertical concepts"],
        "weaknesses": ["Slow processor", "Pressure performance", "Inconsistent under duress"],
        "comp": "Matt Stafford",
        "archetype": "GUNSLINGER",
        "profile": """
Beck is the classic big-armed pocket passer. His arm talent is the best in this class — he can push the ball
downfield with ease and his 72% completion rate at Georgia showed he can be accurate when comfortable.
The issue is processing: when pressure comes, Beck's decision-making slows and his mechanics break down.
His comp is Matt Stafford — a big arm who needs the right offensive system and supporting cast to shine.
He transferred from Georgia to Miami after 2024 and his stock has been volatile. Teams that run play-action
heavy, downfield offenses will covet him as a developmental piece.
"""
    },
}

# ── Classify archetype scores ─────────────────────────────────────────────────
ARCHETYPE_SCORES = {
    "Fernando Mendoza":  {"pocket_iq": 95, "arm_talent": 78, "mobility": 60, "game_mgmt": 92, "deep_ball": 72},
    "Ty Simpson":        {"pocket_iq": 88, "arm_talent": 68, "mobility": 82, "game_mgmt": 90, "deep_ball": 60},
    "Garrett Nussmeier": {"pocket_iq": 72, "arm_talent": 88, "mobility": 60, "game_mgmt": 70, "deep_ball": 88},
    "Drew Allar":        {"pocket_iq": 70, "arm_talent": 78, "mobility": 78, "game_mgmt": 68, "deep_ball": 72},
    "Carson Beck":       {"pocket_iq": 65, "arm_talent": 95, "mobility": 52, "game_mgmt": 68, "deep_ball": 95},
}


def render_qb_profile(name, qb_data, scores_data):
    """Render QB profile card with war room dashboard style."""
    # Hero header
    st.markdown(f"""
    <div class="qb-hero">
        <div class="qb-hero-name">{name}</div>
        <div class="qb-hero-meta">{qb_data.get('school','—')} · {qb_data.get('height','—')} · {qb_data.get('weight','—')}</div>
        <div class="qb-hero-rank">{qb_data.get('rank','—')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Stat grid
    stats = qb_data.get('stats', {})
    items = list(stats.items())
    while len(items) % 3 != 0:
        items.append(('', ''))
    grid_html = '<div class="stat-grid">'
    for k, v in items:
        if k:
            grid_html += f'<div class="stat-cell"><div class="sv">{v}</div><div class="sl">{k}</div></div>'
        else:
            grid_html += '<div class="stat-cell"></div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    # Strengths
    st.markdown('<div class="tag-section"><div class="tag-section-label">Strengths</div>', unsafe_allow_html=True)
    tags = "".join([f'<span class="tag strength">{s}</span>' for s in qb_data.get("strengths", [])])
    st.markdown(f'<div class="tag-row">{tags}</div></div>', unsafe_allow_html=True)

    # Concerns
    st.markdown('<div class="tag-section"><div class="tag-section-label">Concerns</div>', unsafe_allow_html=True)
    wtags = "".join([f'<span class="tag weakness">{w}</span>' for w in qb_data.get("weaknesses", [])])
    st.markdown(f'<div class="tag-row">{wtags}</div></div>', unsafe_allow_html=True)

    # Attribute bars
    attr_colors = {
        "pocket_iq": "#4A9EFF",
        "arm_talent": "#F5A623",
        "mobility": "#2ECC71",
        "game_mgmt": "#A78BFA",
        "deep_ball": "#F472B6",
    }
    attr_labels = {
        "pocket_iq": "Pocket IQ",
        "arm_talent": "Arm Talent",
        "mobility": "Mobility",
        "game_mgmt": "Game Mgmt",
        "deep_ball": "Deep Ball",
    }
    for attr, val in scores_data.items():
        color = attr_colors.get(attr, "#4A9EFF")
        label = attr_labels.get(attr, attr.replace("_"," ").title())
        st.markdown(f"""
        <div class="attr-row">
            <div class="attr-header">
                <span class="attr-label">{label}</span>
                <span class="attr-val" style="color:{color}">{val}</span>
            </div>
            <div class="attr-track">
                <div class="attr-fill" style="width:{val}%;background:{color}"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── App Layout ────────────────────────────────────────────────────────────────

# Top nav bar
st.markdown("""
<div class="topbar">
    <div style="display:flex;align-items:center;gap:1.5rem">
        <div class="topbar-logo">QB<span>SCHEME</span>FIT</div>
        <div class="topbar-meta">Offensive Intelligence System · v2.0</div>
    </div>
    <div style="display:flex;align-items:center;gap:1.5rem">
        <div class="topbar-meta">2026 NFL Draft · Pre-Draft Analysis Mode</div>
        <div class="topbar-status"><div class="topbar-dot"></div>LIVE DATA</div>
    </div>
</div>
<div class="subbar">
    <div class="subbar-item">DRAFT CLASS <span class="subbar-val">2026</span></div>
    <div class="subbar-item">QBs EVALUATED <span class="subbar-val">5</span></div>
    <div class="subbar-item">TOP PROSPECT <span class="subbar-val">F. MENDOZA · IND</span></div>
    <div class="subbar-item">DRAFT DATE <span class="subbar-val">APR 23, 2026 · PITTSBURGH</span></div>
    <div class="subbar-item">MODE <span class="subbar-val">SCHEME FIT ANALYSIS</span></div>
</div>
<div class="main-wrap">
""", unsafe_allow_html=True)

# Mode Toggle
mode_col, _ = st.columns([2, 4])
with mode_col:
    mode = st.radio(
        "Mode",
        ["2026 Draft Prospects", "Any NFL QB"],
        horizontal=True,
        label_visibility="collapsed",
    )

st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)
col_left, col_right = st.columns([1, 1.8], gap="medium")

# ── Shared state ──────────────────────────────────────────────────────────────
qb_profile = {}        # populated below regardless of mode
selected_qb = ""
scores = {}

with col_left:

    # ── PHASE 1: Draft Prospects ──────────────────────────────────────────────
    if mode == "2026 Draft Prospects":
        st.markdown('<div class="section-label">2026 QB Class</div>', unsafe_allow_html=True)
        selected_qb = st.radio(
            "Select QB",
            list(QBS.keys()),
            label_visibility="collapsed",
        )
        qb = QBS[selected_qb]
        qb_profile = qb
        scores = ARCHETYPE_SCORES[selected_qb]

        st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        render_qb_profile(selected_qb, qb, scores)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── PHASE 2: Any NFL QB ───────────────────────────────────────────────────
    else:
        st.markdown('<div class="section-label">Any NFL QB</div>', unsafe_allow_html=True)
        nfl_qb_input = st.text_input(
            "QB Name",
            placeholder="e.g. Patrick Mahomes, Tua Tagovailoa, Joe Burrow...",
            label_visibility="collapsed",
        )

        if nfl_qb_input.strip():
            selected_qb = nfl_qb_input.strip()

            if f"profile_{selected_qb}" not in st.session_state:
                with st.spinner(f"Scouting {selected_qb}..."):
                    client_temp = anthropic.Anthropic(api_key=st.secrets["anthropic"]["api_key"])
                    scout_prompt = f"""Search for and return a detailed 2026 NFL scouting profile for quarterback {selected_qb}.

Return ONLY a JSON object with this exact structure, no other text:
{{
  "name": "{selected_qb}",
  "team": "current NFL team or 'Free Agent' or 'College'",
  "age": "age as string",
  "height": "height",
  "weight": "weight",
  "experience": "years in NFL or 'Rookie'",
  "stats": {{
    "Pass Yds": "most recent season passing yards",
    "TDs": "touchdowns",
    "INTs": "interceptions",
    "Comp %": "completion percentage",
    "Passer Rtg": "passer rating or QBR"
  }},
  "strengths": ["strength 1", "strength 2", "strength 3", "strength 4"],
  "weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
  "archetype": "one of: POCKET SURGEON / GUNSLINGER / MOBILE DISTRIBUTOR / GAME MANAGER / DUAL THREAT",
  "comp": "closest historical NFL comp",
  "profile": "2-3 sentence analytical scouting summary",
  "scores": {{
    "pocket_iq": 0-100,
    "arm_talent": 0-100,
    "mobility": 0-100,
    "game_mgmt": 0-100,
    "deep_ball": 0-100
  }}
}}"""

                    scout_response = client_temp.messages.create(
                        model="claude-sonnet-4-5",
                        max_tokens=1000,
                        tools=[{"type": "web_search_20250305", "name": "web_search"}],
                        messages=[{"role": "user", "content": scout_prompt}]
                    )

                    raw = ""
                    for block in scout_response.content:
                        if hasattr(block, "text"):
                            raw += block.text

                    try:
                        import re
                        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
                        if json_match:
                            parsed = json.loads(json_match.group())
                            st.session_state[f"profile_{selected_qb}"] = parsed
                        else:
                            st.session_state[f"profile_{selected_qb}"] = None
                    except:
                        st.session_state[f"profile_{selected_qb}"] = None

            profile_data = st.session_state.get(f"profile_{selected_qb}")

            if profile_data:
                qb_profile = {
                    "school": profile_data.get("team", "NFL"),
                    "rank": f"Age {profile_data.get('age', '—')} · {profile_data.get('experience', '—')} exp",
                    "height": profile_data.get("height", "—"),
                    "weight": profile_data.get("weight", "—"),
                    "stats": profile_data.get("stats", {}),
                    "strengths": profile_data.get("strengths", []),
                    "weaknesses": profile_data.get("weaknesses", []),
                    "archetype": profile_data.get("archetype", "UNKNOWN"),
                    "comp": profile_data.get("comp", "—"),
                    "profile": profile_data.get("profile", ""),
                }
                scores = profile_data.get("scores", {
                    "pocket_iq": 70, "arm_talent": 70, "mobility": 70,
                    "game_mgmt": 70, "deep_ball": 70
                })

                st.markdown('<div class="panel">', unsafe_allow_html=True)
                render_qb_profile(selected_qb, qb_profile, scores)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning(f"Couldn't pull profile for '{selected_qb}'. Check the name and try again.")
        else:
            st.markdown("""
            <div style="background:var(--surface);border:1px dashed var(--border);border-radius:4px;padding:2rem;text-align:center">
                <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:var(--muted);letter-spacing:0.15em">TYPE ANY QB NAME ABOVE</div>
                <div style="font-size:0.8rem;color:#444;margin-top:0.4rem">Active NFL players, veterans, or rookies</div>
            </div>
            """, unsafe_allow_html=True)

with col_right:
    if qb_profile:
        archetype = qb_profile.get('archetype', '—')
        profile_text = qb_profile.get('profile', '').strip()
        comp = qb_profile.get('comp', '—')
        st.markdown(f"""
        <div class="panel">
            <div class="panel-header">
                <div class="panel-header-left"><div class="panel-header-dot"></div><div class="panel-header-title">Prospect Analysis</div></div>
                <div class="panel-header-tag">AI CLASSIFIED</div>
            </div>
            <div class="archetype-row">
                <div class="archetype-left">
                    <div class="archetype-kicker">Offensive Archetype</div>
                    <div class="archetype-name">{archetype}</div>
                </div>
                <div class="archetype-right">
                    <div class="archetype-comp-label">Closest NFL Comp</div>
                    <div class="archetype-comp-val">{comp}</div>
                </div>
            </div>
            <div class="profile-text">{profile_text}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🏈</div>
            <div class="empty-title">Select a Quarterback</div>
            <div class="empty-sub">Choose a prospect from the left panel</div>
        </div>
        """, unsafe_allow_html=True)

    team_input = st.text_input(
        "NFL Team (optional)",
        placeholder="e.g. Green Bay Packers",
        help="Enter an NFL team to get a roster-specific blueprint"
    )

    generate = st.button("⚡  GENERATE OFFENSIVE BLUEPRINT", disabled=not bool(qb_profile))

    if generate and qb_profile:
        client = anthropic.Anthropic(api_key=st.secrets["anthropic"]["api_key"])

        # ── Step 1: Pull live team intel via web search ──────────────────────
        team_intel = ""
        if team_input.strip():
            with st.spinner(f"Scouting {team_input} roster & scheme..."):
                search_prompt = f"""Search for and compile a comprehensive 2026 NFL season profile of the {team_input}. Include:
- Current offensive roster: starting QB situation, WRs, TEs, RBs, OL starters
- Offensive coordinator and their scheme tendencies
- Head coach philosophy
- 2026 offseason moves (free agency signings, cuts, trades)
- 2026 draft picks and needs
- Salary cap situation and roster construction priorities
- Recent offensive performance and weaknesses
- Any injuries to key offensive players

Be specific with player names, positions, and contract situations. This is for a front office offensive blueprint tool."""

                search_response = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=1500,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=[{"role": "user", "content": search_prompt}]
                )

                # Extract text from response
                for block in search_response.content:
                    if hasattr(block, "text"):
                        team_intel += block.text

        # ── Step 2: Generate blueprint with full team context ─────────────────
        if team_input.strip() and team_intel:
            team_section = f"""
TEAM: {team_input}
CURRENT TEAM INTELLIGENCE (2026):
{team_intel}

CRITICAL INSTRUCTION: This blueprint must be hyper-specific to the {team_input}.
- Reference actual players on their roster by name at every opportunity
- Call out specific roster holes that this QB would need filled
- Reference the actual OC/HC and their real scheme
- Compare what this QB offers vs. their current QB situation
- Name specific players already on the roster who fit or don't fit this QB's needs
- Address their actual cap situation and draft capital
- This should read like an internal front office memo written specifically for {team_input} decision-makers
"""
        else:
            team_section = "\nNo specific team — generate a general blueprint applicable to any team."

        s = scores if isinstance(scores, dict) else {}
        prompt = f"""You are a senior NFL offensive coordinator and analytics consultant writing an internal front office memo.

QB PROSPECT PROFILE:
QB: {selected_qb}
Team/School: {qb_profile.get('school', '—')}
Archetype: {qb_profile.get('archetype', '—')}
NFL Comp: {qb_profile.get('comp', '—')}
Strengths: {', '.join(qb_profile.get('strengths', []))}
Concerns: {', '.join(qb_profile.get('weaknesses', []))}
Attribute Scores (out of 100): Pocket IQ {s.get('pocket_iq', 70)}, Arm Talent {s.get('arm_talent', 70)}, Mobility {s.get('mobility', 70)}, Game Management {s.get('game_mgmt', 70)}, Deep Ball {s.get('deep_ball', 70)}
Scouting Profile: {qb_profile.get('profile', '').strip()}

{team_section}

Generate a detailed offensive blueprint with these exact sections:

### OFFENSIVE SYSTEM FIT
2-3 sentences on what offensive system fits this QB. If a team is provided, explain specifically why it does or doesn't match what {team_input if team_input else 'this team'} currently runs under their OC.

### ROSTER FIT ANALYSIS
If a team is provided: Go position-by-position through their current roster. For each position group (OL, WR, TE, RB), name the actual players and rate how well they fit this QB's needs. Be brutally honest. If a team is not provided, describe the ideal roster profile.

### SCHEME PRINCIPLES
3-4 bullet points on core schematic principles for this QB. If team provided, tie each principle to how it fits or conflicts with the current coaching staff's tendencies.

### SIGNATURE PLAY CONCEPTS
4-5 specific play concepts that maximize this QB's strengths. Name real concepts (mesh, sail, Y-cross, etc). If team provided, explain how each concept fits the personnel already on the roster.

### OFFSEASON PRIORITIES
If team provided: What specific moves must {team_input if team_input else 'the team'} make to maximize this QB? Name position needs, ideal player profiles, and whether to address via draft or free agency given their cap situation.
If no team: General supporting cast recommendations.

### YEAR 1 PROJECTION
One paragraph on realistic Year 1 expectations — stat projections, scheme ramp-up, ceiling if everything goes right. If team provided, account for their actual schedule difficulty, division, and supporting cast.

### RED FLAGS
2-3 bullet points on what would make this a failed fit — either generally or specific to this team's situation.

Write like a real OC memo. Be brutally specific. Name real players. No generic statements."""

        with st.spinner("Building offensive blueprint..."):
            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            blueprint = response.content[0].text

        st.markdown(f'<div class="panel"><div class="panel-header"><div class="panel-header-dot"></div><div class="panel-header-title">Offensive Blueprint · {selected_qb}</div></div><div class="report-body">{blueprint}</div></div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="empty-state" style="margin-top:1rem">
            <div class="empty-icon">📋</div>
            <div class="empty-title">Blueprint Ready to Generate</div>
            <div class="empty-sub">Select a QB, optionally enter an NFL team, and hit Generate</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-wrap
