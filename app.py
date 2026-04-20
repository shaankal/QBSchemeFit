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
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --gold: #C9A84C;
    --gold-light: #E8C96A;
    --dark: #0A0A0A;
    --surface: #141414;
    --surface2: #1E1E1E;
    --border: #2A2A2A;
    --text: #F0EDE8;
    --muted: #7A7A7A;
    --green: #2ECC71;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

.stApp { background-color: var(--dark); }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1200px; }

/* Hero */
.hero {
    border-bottom: 1px solid var(--border);
    padding-bottom: 2rem;
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    line-height: 0.95;
    letter-spacing: 0.02em;
    color: var(--text);
    margin: 0;
}
.hero-title span { color: var(--gold); }
.hero-sub {
    font-size: 0.95rem;
    color: var(--muted);
    margin-top: 0.75rem;
    max-width: 520px;
    line-height: 1.6;
}

/* QB Cards */
.qb-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.25rem 1.5rem;
    cursor: pointer;
    transition: all 0.15s ease;
    margin-bottom: 0.75rem;
}
.qb-card:hover { border-color: var(--gold); background: var(--surface2); }
.qb-card.selected { border-color: var(--gold); background: var(--surface2); }
.qb-name { font-family: 'Bebas Neue', sans-serif; font-size: 1.4rem; letter-spacing: 0.04em; color: var(--text); }
.qb-meta { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: var(--muted); letter-spacing: 0.1em; margin-top: 0.15rem; }
.qb-rank { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: var(--gold); }

/* Section label */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* Stat pill */
.stat-row { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
.stat-pill {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 0.4rem 0.75rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
}
.stat-pill .val { color: var(--gold); font-weight: 500; }
.stat-pill .lbl { color: var(--muted); font-size: 0.65rem; display: block; margin-top: 0.1rem; }

/* Archetype badge */
.archetype-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1a1500, #2a2000);
    border: 1px solid var(--gold);
    border-radius: 2px;
    padding: 0.4rem 1rem;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.08em;
    color: var(--gold);
    margin-bottom: 1.5rem;
}

/* Report output */
.report-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2rem;
}
.report-container h3 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 0.06em;
    color: var(--gold);
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}
.report-container p, .report-container li {
    font-size: 0.9rem;
    line-height: 1.7;
    color: #C8C5BF;
}
.report-container ul { padding-left: 1.25rem; }
.report-container li { margin-bottom: 0.3rem; }

/* Generate button */
.stButton > button {
    background: var(--gold) !important;
    color: #000 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.1em !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover { background: var(--gold-light) !important; }

/* Divider */
.divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* Strength/weakness tags */
.tag-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
.tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    padding: 0.25rem 0.6rem;
    border-radius: 2px;
    letter-spacing: 0.05em;
}
.tag.strength { background: #0d2b1a; border: 1px solid #1a4a2e; color: var(--green); }
.tag.weakness { background: #2b0d0d; border: 1px solid #4a1a1a; color: #e74c3c; }
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

# ── App Layout ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">2026 NFL Draft · Offensive Intelligence Engine</div>
    <div class="hero-title">QB<span> SCHEME</span><br>FIT</div>
    <div class="hero-sub">Select a quarterback prospect. Get a full offensive blueprint — archetype classification, scheme fit, play concepts, and supporting cast recommendations.</div>
</div>
""", unsafe_allow_html=True)

# ── Mode Toggle ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
div[data-testid="stHorizontalBlock"] > div:first-child { padding-right: 0.5rem; }
.mode-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

mode_col, _ = st.columns([2, 3])
with mode_col:
    mode = st.radio(
        "Mode",
        ["2026 Draft Prospects", "Any NFL QB"],
        horizontal=True,
        label_visibility="collapsed",
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.8], gap="large")

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

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Scouting Profile</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-bottom:1rem">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:0.04em">{selected_qb}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:var(--muted);letter-spacing:0.1em">{qb['school']} · {qb['height']} · {qb['weight']}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--gold);margin-top:0.25rem">{qb['rank']}</div>
        </div>
        """, unsafe_allow_html=True)

        stats_html = '<div class="stat-row">'
        for k, v in qb["stats"].items():
            stats_html += f'<div class="stat-pill"><span class="val">{v}</span><span class="lbl">{k}</span></div>'
        stats_html += '</div>'
        st.markdown(stats_html, unsafe_allow_html=True)

        st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:var(--muted);letter-spacing:0.1em;margin-bottom:0.4rem">STRENGTHS</div>', unsafe_allow_html=True)
        tags = "".join([f'<span class="tag strength">+ {s}</span>' for s in qb["strengths"]])
        st.markdown(f'<div class="tag-row">{tags}</div>', unsafe_allow_html=True)

        st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:var(--muted);letter-spacing:0.1em;margin-bottom:0.4rem">CONCERNS</div>', unsafe_allow_html=True)
        wtags = "".join([f'<span class="tag weakness">— {w}</span>' for w in qb["weaknesses"]])
        st.markdown(f'<div class="tag-row">{wtags}</div>', unsafe_allow_html=True)

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Attribute Scores</div>', unsafe_allow_html=True)
        for attr, val in scores.items():
            label = attr.replace("_", " ").upper()
            st.markdown(f"""
            <div style="margin-bottom:0.6rem">
                <div style="display:flex;justify-content:space-between;font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--muted);margin-bottom:0.2rem">
                    <span>{label}</span><span style="color:var(--gold)">{val}</span>
                </div>
                <div style="background:var(--surface2);border-radius:1px;height:3px">
                    <div style="background:var(--gold);width:{val}%;height:3px;border-radius:1px"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

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

                st.markdown(f"""
                <div style="margin-bottom:1rem">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;letter-spacing:0.04em">{selected_qb}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:var(--muted);letter-spacing:0.1em">{qb_profile['school']} · {qb_profile['height']} · {qb_profile['weight']}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--gold);margin-top:0.25rem">{qb_profile['rank']}</div>
                </div>
                """, unsafe_allow_html=True)

                stats_html = '<div class="stat-row">'
                for k, v in qb_profile["stats"].items():
                    stats_html += f'<div class="stat-pill"><span class="val">{v}</span><span class="lbl">{k}</span></div>'
                stats_html += '</div>'
                st.markdown(stats_html, unsafe_allow_html=True)

                st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:var(--muted);letter-spacing:0.1em;margin-bottom:0.4rem">STRENGTHS</div>', unsafe_allow_html=True)
                tags = "".join([f'<span class="tag strength">+ {s}</span>' for s in qb_profile["strengths"]])
                st.markdown(f'<div class="tag-row">{tags}</div>', unsafe_allow_html=True)

                st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:var(--muted);letter-spacing:0.1em;margin-bottom:0.4rem">CONCERNS</div>', unsafe_allow_html=True)
                wtags = "".join([f'<span class="tag weakness">— {w}</span>' for w in qb_profile["weaknesses"]])
                st.markdown(f'<div class="tag-row">{wtags}</div>', unsafe_allow_html=True)

                st.markdown('<hr class="divider">', unsafe_allow_html=True)
                st.markdown('<div class="section-label">Attribute Scores</div>', unsafe_allow_html=True)
                for attr, val in scores.items():
                    label = attr.replace("_", " ").upper()
                    st.markdown(f"""
                    <div style="margin-bottom:0.6rem">
                        <div style="display:flex;justify-content:space-between;font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--muted);margin-bottom:0.2rem">
                            <span>{label}</span><span style="color:var(--gold)">{val}</span>
                        </div>
                        <div style="background:var(--surface2);border-radius:1px;height:3px">
                            <div style="background:var(--gold);width:{val}%;height:3px;border-radius:1px"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
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
    st.markdown('<div class="section-label">Offensive Blueprint Generator</div>', unsafe_allow_html=True)

    if qb_profile:
        archetype = qb_profile.get('archetype', '—')
        profile_text = qb_profile.get('profile', '').strip()
        comp = qb_profile.get('comp', '—')
        st.markdown(f"""
        <div style="margin-bottom:1.5rem">
            <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--muted);margin-bottom:0.4rem">CLASSIFIED ARCHETYPE</div>
            <div class="archetype-badge">{archetype}</div>
            <div style="font-size:0.85rem;color:var(--muted);line-height:1.6">{profile_text}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--gold);margin-top:0.75rem">CLOSEST NFL COMP: {comp}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-family:\'DM Mono\',monospace;font-size:0.7rem;color:var(--muted);margin-bottom:1.5rem">Enter a QB name on the left to load their profile.</div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

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

        st.markdown(f'<div class="report-container">{blueprint}</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:var(--surface);border:1px dashed var(--border);border-radius:4px;padding:3rem 2rem;text-align:center">
            <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:var(--muted);letter-spacing:0.15em">SELECT A QB AND HIT GENERATE</div>
            <div style="font-size:0.85rem;color:#444;margin-top:0.5rem">The blueprint will appear here</div>
        </div>
        """, unsafe_allow_html=True)
