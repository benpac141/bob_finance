"""
Thème graphique professionnel pour la plateforme BOB.

Direction visuelle : institutionnel écologique — teal profond,
fonds brumeux froids, accent cuivre mat, typographie expressive.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

COLORS = {
    "ink": "#0B2E2C",
    "primary": "#14635C",
    "primary_soft": "#1F8A80",
    "accent": "#B86A2F",
    "accent_soft": "#D4925A",
    "sage": "#3D8B7A",
    "mint": "#E6F3F0",
    "mist": "#F3F6F5",
    "cloud": "#FBFCFB",
    "paper": "#FFFFFF",
    "slate": "#334155",
    "muted": "#64748B",
    "line": "#D7E3DF",
    "danger": "#B42318",
    "warning": "#B54708",
    "success": "#027A48",
    "female": "#C45C4A",
    "male": "#2F6F8F",
    "solidaire": "#C17A2E",
    "normale": "#14635C",
    "soutien": "#3D8B7A",
    "cotisations": "#14635C",
    "locations": "#3D8B7A",
}

PALETTE = [
    COLORS["primary"],
    COLORS["sage"],
    COLORS["accent"],
    COLORS["male"],
    COLORS["female"],
    COLORS["primary_soft"],
    COLORS["accent_soft"],
    COLORS["ink"],
    COLORS["warning"],
    COLORS["slate"],
]

SCALE_TEAL = [
    "#E6F3F0",
    "#B8DED7",
    "#7BBFB3",
    "#3D8B7A",
    "#1F8A80",
    "#14635C",
    "#0B2E2C",
]

SCALE_WARM = [
    "#F7E8D8",
    "#EBC39A",
    "#D4925A",
    "#B86A2F",
    "#8C4A1A",
]


def apply_theme_css() -> str:
    """CSS global injecté dans Streamlit."""
    return f"""
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap');

:root {{
    --bob-ink: {COLORS["ink"]};
    --bob-primary: {COLORS["primary"]};
    --bob-primary-soft: {COLORS["primary_soft"]};
    --bob-accent: {COLORS["accent"]};
    --bob-sage: {COLORS["sage"]};
    --bob-mint: {COLORS["mint"]};
    --bob-mist: {COLORS["mist"]};
    --bob-paper: {COLORS["paper"]};
    --bob-slate: {COLORS["slate"]};
    --bob-muted: {COLORS["muted"]};
    --bob-line: {COLORS["line"]};
    --bob-radius: 14px;
    --bob-shadow: 0 10px 30px rgba(11, 46, 44, 0.08);
}}

html, body, [class*="css"] {{
    font-family: "DM Sans", sans-serif;
}}

.stApp {{
    background:
        radial-gradient(1200px 520px at 8% -10%, rgba(31, 138, 128, 0.16), transparent 55%),
        radial-gradient(900px 420px at 100% 0%, rgba(184, 106, 47, 0.10), transparent 50%),
        linear-gradient(180deg, #F7FBFA 0%, #EEF4F2 42%, #F5F7F6 100%);
    color: var(--bob-slate);
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background:
        linear-gradient(180deg, #0B2E2C 0%, #114643 48%, #14635C 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}}

section[data-testid="stSidebar"] * {{
    color: #EAF6F3 !important;
}}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {{
    color: #EAF6F3 !important;
}}

section[data-testid="stSidebar"] [data-testid="stMetricValue"],
section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
    color: #FFFFFF !important;
}}

section[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.14) !important;
}}

section[data-testid="stSidebar"] .stSlider > div > div > div {{
    background: rgba(255,255,255,0.25);
}}

section[data-testid="stSidebar"] [data-baseweb="input"] {{
    background: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}}

section[data-testid="stSidebar"] button {{
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: #fff !important;
    border-radius: 10px !important;
}}

section[data-testid="stSidebar"] button:hover {{
    background: rgba(255,255,255,0.20) !important;
}}

/* Brand header */
.bob-hero {{
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 1.75rem 2rem 1.6rem;
    margin: 0.2rem 0 1.6rem;
    background:
        linear-gradient(135deg, rgba(11,46,44,0.96) 0%, rgba(20,99,92,0.94) 58%, rgba(61,139,122,0.88) 100%);
    box-shadow: var(--bob-shadow);
    color: #F7FBFA;
}}

.bob-hero::before {{
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 88% 18%, rgba(212,146,90,0.28), transparent 34%),
        radial-gradient(circle at 12% 80%, rgba(230,243,240,0.12), transparent 40%),
        repeating-linear-gradient(
            -28deg,
            rgba(255,255,255,0.035) 0px,
            rgba(255,255,255,0.035) 1px,
            transparent 1px,
            transparent 14px
        );
    pointer-events: none;
}}

.bob-hero-inner {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
    justify-content: space-between;
    gap: 1.25rem;
}}

.bob-brand {{
    font-family: "Fraunces", serif;
    font-size: clamp(2.2rem, 3.4vw, 3.1rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.05;
    margin: 0;
}}

.bob-brand span {{
    color: #F0C9A2;
}}

.bob-kicker {{
    display: inline-block;
    margin-bottom: 0.55rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(234,246,243,0.78);
}}

.bob-subtitle {{
    margin: 0.55rem 0 0;
    max-width: 42rem;
    font-size: 1.02rem;
    line-height: 1.45;
    color: rgba(247,251,250,0.86);
}}

.bob-hero-meta {{
    display: grid;
    gap: 0.55rem;
    min-width: 210px;
}}

.bob-chip {{
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.55rem 0.8rem;
    border-radius: 999px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.14);
    backdrop-filter: blur(6px);
    font-size: 0.86rem;
}}

.bob-chip strong {{
    color: #fff;
    font-weight: 700;
}}

/* Section titles */
.bob-section {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
    margin: 0.4rem 0 1rem;
}}

.bob-section h2 {{
    font-family: "Fraunces", serif;
    font-size: 1.55rem;
    font-weight: 600;
    color: var(--bob-ink);
    margin: 0;
    letter-spacing: -0.02em;
}}

.bob-section p {{
    margin: 0;
    color: var(--bob-muted);
    font-size: 0.95rem;
}}

.bob-divider {{
    height: 1px;
    margin: 1.2rem 0 1.4rem;
    background: linear-gradient(90deg, transparent, var(--bob-line), transparent);
    border: 0;
}}

/* KPI cards */
.bob-kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.9rem;
    margin: 0 0 1.2rem;
}}

@media (max-width: 1100px) {{
    .bob-kpi-grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}

@media (max-width: 640px) {{
    .bob-kpi-grid {{
        grid-template-columns: 1fr;
    }}
    .bob-hero {{
        padding: 1.35rem 1.2rem;
    }}
}}

.bob-kpi {{
    position: relative;
    overflow: hidden;
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(215,227,223,0.95);
    border-radius: var(--bob-radius);
    padding: 1rem 1.05rem 0.95rem;
    box-shadow: 0 8px 22px rgba(11,46,44,0.05);
    backdrop-filter: blur(8px);
}}

.bob-kpi::before {{
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--accent, var(--bob-primary));
}}

.bob-kpi-label {{
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--bob-muted);
    margin-bottom: 0.35rem;
}}

.bob-kpi-value {{
    font-family: "Fraunces", serif;
    font-size: 1.72rem;
    font-weight: 650;
    color: var(--bob-ink);
    line-height: 1.1;
    letter-spacing: -0.02em;
}}

.bob-kpi-delta {{
    margin-top: 0.35rem;
    font-size: 0.86rem;
    color: var(--bob-primary);
    font-weight: 500;
}}

/* Tariff strip */
.bob-tariff-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
    margin-bottom: 0.6rem;
}}

@media (max-width: 900px) {{
    .bob-tariff-grid {{
        grid-template-columns: 1fr;
    }}
}}

.bob-tariff {{
    background: linear-gradient(180deg, #FFFFFF 0%, #F7FBFA 100%);
    border: 1px solid var(--bob-line);
    border-radius: var(--bob-radius);
    padding: 1rem 1.1rem;
}}

.bob-tariff-title {{
    font-size: 0.8rem;
    font-weight: 650;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--bob-muted);
}}

.bob-tariff-value {{
    margin-top: 0.25rem;
    font-family: "Fraunces", serif;
    font-size: 1.55rem;
    color: var(--bob-ink);
    font-weight: 650;
}}

.bob-tariff-sub {{
    margin-top: 0.2rem;
    color: var(--bob-primary);
    font-size: 0.9rem;
}}

/* Tabs */
button[data-baseweb="tab"] {{
    font-family: "DM Sans", sans-serif !important;
    font-weight: 600 !important;
    color: var(--bob-muted) !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--bob-ink) !important;
}}

div[data-baseweb="tab-highlight"] {{
    background-color: var(--bob-primary) !important;
}}

/* Primary buttons */
.stButton > button[kind="primary"],
.stDownloadButton > button {{
    background: linear-gradient(135deg, var(--bob-primary) 0%, var(--bob-sage) 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 650 !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 18px rgba(20, 99, 92, 0.25);
}}

.stButton > button[kind="primary"]:hover {{
    filter: brightness(1.05);
}}

/* Dataframes / expanders */
div[data-testid="stDataFrame"],
div[data-testid="stExpander"] {{
    border: 1px solid var(--bob-line);
    border-radius: 12px;
    overflow: hidden;
}}

/* Hide default Streamlit chrome noise */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header[data-testid="stHeader"] {{
    background: transparent;
}}

.bob-footer {{
    margin-top: 2rem;
    padding: 1.2rem 1rem 0.4rem;
    text-align: center;
    color: var(--bob-muted);
    font-size: 0.9rem;
    border-top: 1px solid var(--bob-line);
}}

.bob-footer strong {{
    color: var(--bob-ink);
    font-family: "Fraunces", serif;
    font-weight: 600;
}}

.sidebar-brand {{
    padding: 0.35rem 0.2rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 0.85rem;
}}

.sidebar-brand .title {{
    font-family: "Fraunces", serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #fff !important;
    margin: 0;
}}

.sidebar-brand .desc {{
    margin: 0.25rem 0 0;
    font-size: 0.82rem;
    color: rgba(234,246,243,0.72) !important;
    line-height: 1.35;
}}
"""


def render_hero(
    population: int,
    interesses: int,
    format_nombre,
) -> str:
    """Bandeau de marque principal."""
    return f"""
<div class="bob-hero">
  <div class="bob-hero-inner">
    <div>
      <div class="bob-kicker">Plateforme d'analyse &amp; simulation</div>
      <h1 class="bob-brand">BOB <span>Finance</span></h1>
      <p class="bob-subtitle">
        Bibliothèque d'Objets Besançon — simulez adhérents, tarifs et recettes
        à partir des résultats d'enquête redressés.
      </p>
    </div>
    <div class="bob-hero-meta">
      <div class="bob-chip"><span>Population IRIS</span><strong>{format_nombre(population)}</strong></div>
      <div class="bob-chip"><span>Intéressés estimés</span><strong>{format_nombre(interesses)}</strong></div>
    </div>
  </div>
</div>
"""


def render_section(title: str, subtitle: str = "") -> str:
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    return f"""
<div class="bob-section">
  <div>
    <h2>{title}</h2>
    {subtitle_html}
  </div>
</div>
"""


def render_kpi_card(label: str, value: str, delta: str, accent: str) -> str:
    return f"""
<div class="bob-kpi" style="--accent: {accent};">
  <div class="bob-kpi-label">{label}</div>
  <div class="bob-kpi-value">{value}</div>
  <div class="bob-kpi-delta">{delta}</div>
</div>
"""


def render_kpi_grid(cards: Sequence[Dict[str, str]]) -> str:
    items = "".join(
        render_kpi_card(c["label"], c["value"], c["delta"], c["accent"]) for c in cards
    )
    return f'<div class="bob-kpi-grid">{items}</div>'


def render_tariff_grid(cards: Sequence[Dict[str, str]]) -> str:
    items = "".join(
        f"""
        <div class="bob-tariff" style="border-top: 3px solid {c.get('accent', COLORS['primary'])};">
          <div class="bob-tariff-title">{c['label']}</div>
          <div class="bob-tariff-value">{c['value']}</div>
          <div class="bob-tariff-sub">{c['delta']}</div>
        </div>
        """
        for c in cards
    )
    return f'<div class="bob-tariff-grid">{items}</div>'


def plotly_layout(
    title: Optional[str] = None,
    height: int = 420,
    **extra: Any,
) -> Dict[str, Any]:
    """Layout Plotly cohérent avec le thème."""
    layout: Dict[str, Any] = {
        "height": height,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(255,255,255,0.55)",
        "font": {
            "family": "DM Sans, sans-serif",
            "color": COLORS["slate"],
            "size": 13,
        },
        "title": {
            "text": title or "",
            "font": {
                "family": "Fraunces, serif",
                "size": 18,
                "color": COLORS["ink"],
            },
            "x": 0.02,
            "xanchor": "left",
        },
        "margin": {"l": 40, "r": 24, "t": 56, "b": 40},
        "legend": {
            "bgcolor": "rgba(255,255,255,0.7)",
            "bordercolor": COLORS["line"],
            "borderwidth": 1,
            "font": {"size": 12},
        },
        "colorway": PALETTE,
        "xaxis": {
            "gridcolor": "rgba(215,227,223,0.85)",
            "zerolinecolor": COLORS["line"],
            "title_font": {"color": COLORS["muted"]},
        },
        "yaxis": {
            "gridcolor": "rgba(215,227,223,0.85)",
            "zerolinecolor": COLORS["line"],
            "title_font": {"color": COLORS["muted"]},
        },
    }
    layout.update(extra)
    return layout


def apply_plotly_theme(fig, title: Optional[str] = None, height: int = 420, **extra: Any):
    """Applique le thème à une figure Plotly existante."""
    fig.update_layout(**plotly_layout(title=title, height=height, **extra))
    return fig
