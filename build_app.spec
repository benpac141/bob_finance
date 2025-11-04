# -*- mode: python ; coding: utf-8 -*-
"""
Fichier de configuration PyInstaller pour compiler l'application BOB
en exécutable Windows autonome.

Usage:
    pyinstaller build_app.spec
"""

import os
from pathlib import Path

block_cipher = None

# PyInstaller définit SPECPATH comme le répertoire du fichier .spec
# On utilise cette variable si disponible, sinon le répertoire courant
a = Analysis(
    ['scripts/app_simulation_interactive.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.yaml', '.'),  # Fichier de configuration
        ('data', 'data'),  # Dossier de données
        ('src', 'src'),  # Code source
        ('scripts', 'scripts'),  # Scripts
    ],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.state',
        'streamlit.runtime.caching',
        'streamlit.runtime.metrics_util',
        'streamlit.runtime.legacy_caching',
        'streamlit.components.v1',
        'pandas',
        'numpy',
        'plotly',
        'plotly.express',
        'plotly.graph_objects',
        'scipy',
        'openpyxl',
        'yaml',
        'reportlab',
        'kaleido',
        'PIL',
        'altair',
        'pympler',
        'watchdog',
        'toml',
        'click',
        'tornado',
        'tornado.web',
        'tornado.ioloop',
        'tornado.websocket',
        'tornado.escape',
        'tornado.concurrent',
        'blinker',
        'cachetools',
        'packaging',
        'protobuf',
        'pyarrow',
        'pydeck',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'pytz',
        'tzdata',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib.tests',
        'numpy.tests',
        'pandas.tests',
        'scipy.tests',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Simulateur_BOB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Afficher la console pour les logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
