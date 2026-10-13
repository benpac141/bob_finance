"""Compatibilité : le thème est livré à côté de l'application Streamlit."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_theme_path = Path(__file__).resolve().parents[1] / "scripts" / "ui_theme.py"
_spec = importlib.util.spec_from_file_location("bob_ui_theme", _theme_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Module de thème introuvable : {_theme_path}")
_module = importlib.util.module_from_spec(_spec)
sys.modules["bob_ui_theme"] = _module
_spec.loader.exec_module(_module)

COLORS = _module.COLORS
PALETTE = _module.PALETTE
SCALE_TEAL = _module.SCALE_TEAL
SCALE_WARM = _module.SCALE_WARM
apply_theme_css = _module.apply_theme_css
apply_plotly_theme = _module.apply_plotly_theme
render_hero = _module.render_hero
render_section = _module.render_section
render_kpi_grid = _module.render_kpi_grid
render_status_banner = _module.render_status_banner
render_tariff_grid = _module.render_tariff_grid
plotly_layout = _module.plotly_layout
