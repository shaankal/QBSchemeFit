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
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --red: #D92B2B;
    --red-dim: #7a1818;
    --blue: #1A6FD9;
    --gold: #F0B429;
    --gold-dim: #7a5a14;
    --dark: #080C10;
    --navy: #0D1117;
    --surface: #111820;
    --surface2: #1A2232;
    --surface3: #212D40;
    --border: #1E2D42;
    --border2: #2A3F5A;
    --text: #E8EDF2;
    --text2: #A8B8CC;
    --muted: #5A7090;
    --green: #00D46A;
    --green-dim: #004d26;
    --orange: #FF6B35;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

.stApp { background-color: var(--dark); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── TOP NAV BAR ── */
.topbar {
    background: var(--navy);
    border-bottom: 3px solid var(--red);
    padding: 0.75rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}
.topbar-logo {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--text);
    text-transform: uppercase;
}
.topbar-logo span { color: var(--red); }
.topbar-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: var(--gold);
    background: rgba(240,180,41,0.1);
    border: 1px solid rgba(240,180,41,0.3);
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    text-transform: uppercase;
}

/* ── TICKER BAR ── */
.ticker {
    background: var(--red);
    padding: 0.35rem 2.5rem;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #fff;
    text-transform: uppercase;
    display: flex;
    gap: 2rem;
    margin-bottom: 1.5rem;
}
.ticker-item { opacity: 0.9; }
.ticker-item span { opacity: 0.6; margin-right: 0.4rem; }

/* ── MAIN CONTENT ── */
.main-wrap { padding: 0 2.5rem 2rem; }

/* ── MODE TOGGLE ── */
.mode-toggle {
    display: flex;
    gap: 0;
    margin-bottom: 1.5rem;
    border: 1px solid var(--border2);
    border-radius: 3px;
    overflow: hidden;
    width: fit-content;
}
.mode-btn {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.45rem 1.25rem;
    background: var(--surface);
    color: var(--muted);
    border: none;
    cursor: pointer;
}
.mode-btn.active {
    background: var(--red);
    color: #fff;
}

/* ── PANEL CARD ── */
.panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
}
.panel-header {
    background: var(--surface2);
    border-bottom: 1px solid var(--border);
    padding: 0.6rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-header-dot {
    width: 8px; height: 8px;
    background: var(--red);
    border-radius: 50%;
}
.panel-header-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: var(--text2);
    text-transform: uppercase;
}
.panel-body { padding: 1.25rem; }

/* ── QB LIST ITEMS ── */
.qb-row {
    display: flex;
    align-items: center;
    padding: 0.65rem 0.75rem;
    border-radius: 3px;
    cursor: pointer;
    transition: background 0.1s;
    border-left: 3px solid transparent;
    margin-bottom: 2px;
}
.qb-row:hover { background: var(--surface2); }
.qb-row.active { background: var(--surface2); border-left-color: var(--red); }
.qb-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--muted);
    width: 1.5rem;
}
.qb-info { flex: 1; }
.qb-name-text {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    color: var(--text);
    text-transform: uppercase;
}
.qb-school {
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 1px;
}
.qb-grade {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--gold);
}

/* ── QB PROFILE HEADER ── */
.qb-hero {
    background: linear-gradient(135deg, var(--surface2) 0%, var(--surface3) 100%);
    border-bottom: 1px solid var(--border);
    padding: 1.25rem;
    position: relative;
    overflow: hidden;
}
.qb-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--red), var(--blue));
}
.qb-hero-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: var(--text);
    text-transform: uppercase;
    line-height: 1;
}
.qb-hero-meta {
    font-size: 0.75rem;
    color: var(--text2);
    margin-top: 0.3rem;
}
.qb-hero-rank {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--gold);
    margin-top: 0.2rem;
    letter-spacing: 0.05em;
}

/* ── STAT GRID ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: var(--border);
    margin-bottom: 1rem;
}
.stat-cell {
    background: var(--surface);
    padding: 0.75rem;
    text-align: center;
}
.stat-cell .sv {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.stat-cell .sl {
    font-size: 0.62rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.2rem;
}

/* ── ATTRIBUTE BARS ── */
.attr-row { margin-bottom: 0.55rem; }
.attr-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.68rem;
    margin-bottom: 0.2rem;
}
.attr-label { color: var(--text2); font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; }
.attr-val { font-family: 'JetBrains Mono', monospace; font-weight: 600; }
.attr-track {
    height: 4px;
    background: var(--surface3);
    border-radius: 2px;
    overflow: hidden;
}
.attr-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.4s ease;
}

/* ── TAGS ── */
.tag-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.75rem; }
.tag {
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.2rem 0.5rem;
    border-radius: 2px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.tag.strength { background: rgba(0,212,106,0.1); border: 1px solid rgba(0,212,106,0.25); color: var(--green); }
.tag.weakness { background: rgba(217,43,43,0.1); border: 1px solid rgba(217,43,43,0.25); color: #ff6b6b; }

/* ── ARCHETYPE BANNER ── */
.archetype-banner {
    background: linear-gradient(90deg, var(--red) 0%, #8B1A1A 100%);
    padding: 0.75rem 1.25rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.archetype-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: rgba(255,255,255,0.6);
    text-transform: uppercase;
    letter-spacing: 0.15em;
}
.archetype-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: #fff;
    text-transform: uppercase;
}
.archetype-comp {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--gold);
    text-align: right;
}
.archetype-comp-label { color: rgba(255,255,255,0.4); font-size: 0.55rem; display: block; }

/* ── BLUEPRINT SECTIONS ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.25rem;
    background: var(--surface2);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin-top: 1rem;
}
.section-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: var(--red);
    font-weight: 600;
}
.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--text2);
    text-transform: uppercase;
}

/* ── GENERATE BUTTON ── */
.stButton > button {
    background: var(--red) !important;
    color: #fff !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
.stButton > button:disabled { background: var(--surface3) !important; color: var(--muted) !important; }

/* ── INPUT ── */
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: 3px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 1px var(--red) !important;
}
.stTextInput label { color: var(--text2) !important; font-size: 0.75rem !important; font-weight: 600 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; }

/* ── RADIO (hide default, use custom) ── */
.stRadio > div { display: none !important; }

/* ── REPORT ── */
.report-body {
    padding: 1.25rem;
    font-size: 0.875rem;
    line-height: 1.75;
    color: var(--text2);
}
.report-body h3 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: var(--red);
    text-transform: uppercase;
    margin-top: 1.25rem;
    margin-bottom: 0.4rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid var(--border);
}
.report-body ul { padding-left: 1.2rem; }
.report-body li { margin-bottom: 0.4rem; color: var(--text2); }
.report-body p { color: var(--text2); }
.report-body strong { color: var(--text); }

/* ── EMPTY STATE ── */
.empty-state {
    padding: 3rem 1.5rem;
    text-align: center;
    border: 1px dashed var(--border2);
    border-radius: 4px;
    margin: 1rem 0;
}
.empty-icon { font-size: 2rem; margin-bottom: 0.75rem; opacity: 0.4; }
.empty-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--muted);
    text-transform: uppercase;
}
.empty-sub { font-size: 0.8rem; color: var(--muted); margin-top: 0.3rem; opacity: 0.7; }

/* ── DIVIDER ── */
.divider { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }

/* ── STREAMLIT RADIO OVERRIDE for mode toggle ── */
div[data-testid="stRadio"] > label { display: none !important; }
div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 0 !important;
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 3px !important;
    overflow: hidden !important;
    width: fit-content !important;
    padding: 0 !important;
}
div[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center !important;
    padding: 0.45rem 1.1rem !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    border-radius: 0 !important;
    color: var(--muted) !important;
    transition: all 0.1s !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: var(--red) !important;
    color: #fff !important;
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
    """Render QB profile card with ESPN dashboard style."""
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
    # pad to multiple of 3
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
    st.markdown('<div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;color:var(--text2);text-transform:uppercase;margin-bottom:0.4rem">Strengths</div>', unsafe_allow_html=True)
    tags = "".join([f'<span class="tag strength">{s}</span>' for s in qb_data.get("strengths", [])])
    st.markdown(f'<div class="tag-row">{tags}</div>', unsafe_allow_html=True)

    # Concerns
    st.markdown('<div style="font-size:0.65rem;font-weight:600;letter-spacing:0.1em;color:var(--text2);text-transform:uppercase;margin-bottom:0.4rem">Concerns</div>', unsafe_allow_html=True)
    wtags = "".join([f'<span class="tag weakness">{w}</span>' for w in qb_data.get("weaknesses", [])])
    st.markdown(f'<div class="tag-row">{wtags}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Attribute bars with color coding
    attr_colors = {
        "pocket_iq": "#1A6FD9",
        "arm_talent": "#D92B2B",
        "mobility": "#00D46A",
        "game_mgmt": "#F0B429",
        "deep_ball": "#FF6B35",
    }
    attr_labels = {
        "pocket_iq": "Pocket IQ",
        "arm_talent": "Arm Talent",
        "mobility": "Mobility",
        "game_mgmt": "Game Mgmt",
        "deep_ball": "Deep Ball",
    }
    for attr, val in scores_data.items():
        color = attr_colors.get(attr, "#D92B2B")
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
    <div class="topbar-logo">QB<span>SCHEME</span>FIT</div>
    <div style="display:flex;align-items:center;gap:1rem">
        <span class="topbar-badge">2026 NFL Draft</span>
        <span class="topbar-badge" style="color:var(--text2);background:var(--surface2);border-color:var(--border2)">Offensive Intelligence Engine</span>
    </div>
</div>
<div class="ticker">
    <span class="ticker-item"><span>#</span>1 OVERALL — FERNANDO MENDOZA · INDIANA</span>
    <span class="ticker-item"><span>#</span>2 QB — TY SIMPSON · ALABAMA</span>
    <span class="ticker-item"><span>#</span>3 QB — GARRETT NUSSMEIER · LSU</span>
    <span class="ticker-item"><span>#</span>4 QB — DREW ALLAR · PENN STATE</span>
    <span class="ticker-item"><span>#</span>5 QB — CARSON BECK · MIAMI</span>
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
        <div class="archetype-banner">
            <div>
                <div class="archetype-label">Classified Archetype</div>
                <div class="archetype-name">{archetype}</div>
            </div>
            <div class="archetype-comp">
                <span class="archetype-comp-label">NFL Comp</span>
                {comp}
            </div>
        </div>
        <div style="font-size:0.85rem;color:var(--text2);line-height:1.7;margin-bottom:1.25rem;padding:0 0.25rem">{profile_text}</div>
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
