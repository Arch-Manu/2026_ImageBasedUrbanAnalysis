import streamlit as st


def apply_shared_styles() -> None:
    """Inject shared CSS used by all Streamlit wireframe apps."""
    st.markdown(
        """
        <style>
        :root {
            --light-gray: #ececec;
            --card-gray: #dcdcdc;
            --dark-gray: #4a4a4a;
            --black: #111111;
            --green: #2fd4a5;
            --primary-color: #2fd4a5;
            --green-dark: #21b88d;

            --bg-page: var(--light-gray);
            --bg-surface: var(--card-gray);
            --bg-soft: var(--light-gray);
            --border: var(--dark-gray);
            --border-strong: var(--dark-gray);
            --text-main: var(--dark-gray);
            --text-muted: var(--dark-gray);
            --accent-soft: var(--card-gray);
            --accent-run: color-mix(in srgb, var(--green) 22%, var(--card-gray));
            --slate-100: var(--card-gray);
            --slate-200: var(--light-gray);
            --slate-300: var(--dark-gray);
            --slate-400: var(--dark-gray);
            --slate-500: var(--dark-gray);
            --slate-700: var(--dark-gray);
            --accent-panel: var(--card-gray);
            --accent-label: var(--black);
            --chip-bg: color-mix(in srgb, var(--green) 14%, var(--card-gray));
            --chip-fg: var(--green);
            --chip-border: color-mix(in srgb, var(--green) 55%, var(--card-gray));
        }

        /* Force light theme behavior even if Streamlit/browser is in dark mode */
        :root,
        html,
        body,
        [data-theme="dark"],
        [data-theme="light"] {
            color-scheme: light !important;
            --background-color: var(--bg-page) !important;
            --secondary-background-color: var(--bg-surface) !important;
            --text-color: var(--text-main) !important;
            --primary-color: var(--green) !important;
        }

        .main,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        section.main {
            background-color: var(--bg-page) !important;
            color: var(--text-main) !important;
        }

        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMarkdownContainer"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        .stCaptionContainer,
        .stText,
        p,
        span,
        div,
        label {
            color: var(--dark-gray);
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--black) !important;
        }

        .block-container {
            padding-top: calc(4.25rem + env(safe-area-inset-top));
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 40px;
            border-bottom: 1px solid var(--slate-200);
            background: var(--bg-surface);
        }

        .metric-card {
            background: var(--bg-surface);
            padding: 16px;
            border-radius: 12px;
            border: 1px solid var(--slate-200);
            box-shadow: none;
        }

        .metric-label {
            font-size: 12px;
            color: var(--slate-500);
            margin-bottom: 8px;
        }

        .metric-value {
            font-size: 20px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 4px;
        }

        .metric-subtext {
            font-size: 12px;
            color: var(--slate-500);
        }

        .placeholder-image {
            aspect-ratio: 1;
            background: var(--slate-100);
            border: 1px solid var(--slate-200);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--dark-gray) !important;
            font-size: 12px;
        }

        .preview-placeholder {
            width: 100%;
            aspect-ratio: 1;
            background: var(--slate-200);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--dark-gray) !important;
        }

        .tag-pill {
            display: inline-block;
            background: var(--chip-bg);
            color: var(--chip-fg);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-right: 8px;
            margin-bottom: 8px;
            border: 1px solid var(--chip-border);
        }

        .cluster-card {
            border-radius: 12px;
            padding: 16px;
            min-height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background: var(--bg-surface);
            border: 1px solid var(--slate-200);
        }

        .cluster-card.outlier {
            background: color-mix(in srgb, var(--green) 12%, var(--bg-surface));
            border: 2px dashed color-mix(in srgb, var(--green) 65%, var(--bg-surface));
        }

        .cluster-title {
            font-weight: 600;
            color: var(--black);
            font-size: 14px;
        }

        .cluster-thumb-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 12px;
        }

        .cluster-thumb {
            background: var(--slate-200);
            height: 40px;
            border-radius: 6px;
        }

        .chart-bars {
            height: 144px;
            display: flex;
            align-items: end;
            gap: 10px;
            padding: 8px 0;
        }

        .chart-bars .bar {
            flex: 1;
            background: var(--green);
            border-radius: 6px 6px 0 0;
            height: var(--bar-height, 40%);
        }

        .chart-donut-wrap {
            height: 144px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chart-donut {
            width: 112px;
            height: 112px;
            border-radius: 999px;
            background: conic-gradient(var(--green) 0 35%, var(--slate-200) 35% 65%, var(--green-dark) 65% 100%);
            position: relative;
        }

        .chart-donut-hole {
            position: absolute;
            inset: 22px;
            background: var(--bg-page);
            border-radius: 999px;
        }

        .outer-frame {
            border: 3px solid var(--border-strong);
            border-radius: 14px;
            padding: 28px;
            background: var(--bg-soft);
            box-shadow: none;
        }

        .section-header {
            background: var(--accent-soft);
            border: 2px solid var(--border-strong);
            border-radius: 10px;
            text-align: center;
            padding: 14px 10px;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--black);
            letter-spacing: 0.01em;
            margin-bottom: 18px;
        }

        .input-box {
            border: 2px solid var(--border);
            border-radius: 10px;
            background: var(--bg-surface);
            text-align: center;
            padding: 18px 12px;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 14px;
        }

        .run-box {
            border: 2px solid var(--border-strong);
            border-radius: 10px;
            background: var(--accent-run);
            text-align: center;
            padding: 18px 12px;
            font-size: 1rem;
            font-weight: 700;
            color: var(--text-main);
            margin-top: 64px;
        }

        .output-card {
            border: 2px solid var(--border);
            border-radius: 10px;
            background: var(--bg-surface);
            min-height: 195px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-main);
            padding: 16px;
        }

        .big-output {
            border: 2px solid var(--border);
            border-radius: 10px;
            background: var(--bg-surface);
            min-height: 360px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-main);
            padding: 16px;
            margin-top: 18px;
        }

        .divider-col {
            border-left: 3px solid var(--border-strong);
            min-height: 680px;
            margin: 8px auto;
            width: 0;
        }

        .small-note {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 8px;
        }

        .wf-tile {
            border: 1px solid var(--slate-300);
            border-radius: 12px;
            background: var(--card-gray);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--black) !important;
            font-size: 14px;
            font-weight: 600;
            height: var(--tile-h, 180px);
        }

        .wf-chip {
            display: inline-block;
            padding: 6px 10px;
            margin: 0 8px 8px 0;
            border-radius: 999px;
            background: var(--chip-bg);
            color: var(--chip-fg);
            font-size: 12px;
            font-weight: 600;
            border: 1px solid var(--chip-border);
        }

        .wf-hero {
            position: relative;
            height: 430px;
            border: 1px solid var(--slate-300);
            border-radius: 16px;
            background: var(--card-gray);
            overflow: hidden;
        }

        .wf-hero-title {
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--black) !important;
            font-weight: 700;
            font-size: 18px;
        }

        .placeholder-image *,
        .preview-placeholder *,
        .wf-tile *,
        .wf-hero-title * {
            color: inherit !important;
            fill: currentColor !important;
            stroke: currentColor !important;
        }

        .wf-overlay-tag {
            position: absolute;
            padding: 6px 10px;
            border-radius: 999px;
            background: var(--green);
            color: var(--black);
            font-size: 12px;
            font-weight: 600;
            border: 1px solid var(--green);
        }

        .wf-pos-1 { top: 14px; left: 14px; }
        .wf-pos-2 { top: 54px; left: 28px; }
        .wf-pos-3 { bottom: 16px; left: 16px; }
        .wf-pos-4 { bottom: 56px; right: 16px; }

        .wf-mini-chart {
            height: 160px;
            display: flex;
            align-items: end;
            gap: 12px;
            padding: 8px 0 2px;
        }

        .wf-mini-col {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }

        .wf-mini-bar {
            width: 100%;
            background: var(--green);
            border-radius: 8px 8px 0 0;
            height: var(--bar-height, 20%);
        }

        .wf-mini-label {
            font-size: 11px;
            color: var(--slate-500);
        }

        .fs-space {
            height: 420px;
            border: 1px solid var(--slate-300);
            border-radius: 16px;
            background: var(--card-gray);
            position: relative;
            overflow: hidden;
        }

        .fs-label {
            position: absolute;
            font-size: 12px;
            font-weight: 700;
        }

        .fs-label-1 { left: 18%; top: 18%; color: var(--accent-label); }
        .fs-label-2 { left: 62%; top: 18%; color: var(--accent-label); }
        .fs-label-3 { left: 44%; top: 72%; color: var(--accent-label); }

        /* Monospace + minimal pixel aesthetic overrides */
        .stApp,
        .main,
        .block-container,
        h1, h2, h3, h4, h5, h6,
        p, span, div, label,
        input, textarea, button,
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stMarkdownContainer"] {
            font-family: "Andale Mono", "Lucida Console", "Courier New", monospace;
            letter-spacing: 0.01em;
        }

        [data-testid="stProgressValue"] > div > div {
            background-color: var(--green) !important;
        }

        /* Streamlit progress bars (version-agnostic fallbacks) */
        [data-testid="stProgress"] > div > div,
        [data-testid="stProgressBar"] > div > div,
        [data-testid="stProgress"] div[role="progressbar"],
        [data-testid="stProgressBar"] div[role="progressbar"] {
            background-color: var(--green) !important;
        }

        .stProgress > div > div > div,
        .stProgress > div > div > div > div,
        [data-baseweb="progress-bar"] > div > div,
        [data-baseweb="progress-bar"] div[role="progressbar"] {
            background-color: var(--green) !important;
        }

        [data-testid="stProgress"] > div,
        [data-testid="stProgressBar"] > div {
            background-color: var(--dark-gray) !important;
        }

        .stProgress > div > div,
        [data-baseweb="progress-bar"] > div {
            background-color: var(--dark-gray) !important;
        }

        .metric-card,
        .cluster-card,
        .outer-frame,
        .section-header,
        .input-box,
        .run-box,
        .output-card,
        .big-output,
        .placeholder-image,
        .preview-placeholder,
        .wf-tile,
        .wf-hero,
        .fs-space,
        .tag-pill,
        .wf-chip,
        .wf-overlay-tag,
        .cluster-thumb,
        .chart-bars .bar,
        .wf-mini-bar,
        [data-testid="stButton"] > button,
        [data-testid="stDownloadButton"] > button,
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] div[data-baseweb="select"],
        [data-testid="stMultiSelect"] div[data-baseweb="select"] {
            border-radius: 2px !important;
        }

        [data-testid="stButton"] > button,
        [data-testid="stDownloadButton"] > button {
            text-transform: uppercase;
            letter-spacing: 0.04em;
            background-color: var(--dark-gray) !important;
            color: var(--light-gray) !important;
            border: 1px solid var(--dark-gray) !important;
        }

        [data-testid="stButton"] > button *,
        [data-testid="stDownloadButton"] > button * {
            color: var(--light-gray) !important;
        }

        [data-testid="stButton"] > button[kind="primary"],
        [data-testid="baseButton-primary"] {
            background-color: var(--green) !important;
            color: var(--black) !important;
            border: 1px solid var(--green) !important;
        }

        [data-testid="stButton"] > button[kind="primary"] *,
        [data-testid="baseButton-primary"] * {
            color: var(--black) !important;
        }

        [data-testid="stButton"] > button:hover,
        [data-testid="stDownloadButton"] > button:hover {
            filter: brightness(0.95);
        }

        /* Sliders */
        [data-testid="stSlider"] * {
            --primary-color: var(--green) !important;
            accent-color: var(--green) !important;
        }

        [data-testid="stSlider"] [role="slider"] {
            background-color: var(--green) !important;
            border: 2px solid var(--dark-gray) !important;
            box-shadow: none !important;
        }

        [data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
            background-color: var(--dark-gray) !important;
        }

        [data-testid="stSlider"] div[data-baseweb="slider"] > div > div > div,
        [data-testid="stSlider"] div[data-baseweb="slider"] div[role="progressbar"] {
            background-color: var(--green) !important;
        }

        /* Keyword tags (multiselect/tag chips) */
        [data-baseweb="tag"] {
            background-color: var(--chip-bg) !important;
            color: var(--chip-fg) !important;
            border: 1px solid var(--chip-border) !important;
            border-radius: 2px !important;
        }

        [data-baseweb="tag"] *,
        [data-baseweb="tag"] svg {
            color: var(--chip-fg) !important;
            fill: var(--chip-fg) !important;
            stroke: var(--chip-fg) !important;
            background: transparent !important;
        }

        /* Toggle buttons / switches */
        [data-testid="stToggle"] * {
            --primary-color: var(--green) !important;
            accent-color: var(--green) !important;
        }

        [data-testid="stToggle"] [data-baseweb="checkbox"] > label > div:first-child {
            background-color: var(--dark-gray) !important;
            border-color: var(--dark-gray) !important;
        }

        [data-testid="stToggle"] input:checked + div,
        [data-testid="stToggle"] input:checked + div:hover,
        [data-testid="stToggle"] [aria-checked="true"] {
            background-color: var(--green) !important;
            border-color: var(--green) !important;
        }

        [data-testid="stToggle"] [data-baseweb="checkbox"] > label > div:first-child > div {
            background-color: var(--light-gray) !important;
        }

        .placeholder-image,
        .preview-placeholder,
        .wf-tile,
        .cluster-thumb {
            image-rendering: pixelated;
        }

        /* Align default Streamlit widgets with app_0 palette */
        [data-testid="stSidebar"] {
            background: var(--bg-surface) !important;
            border-right: 1px solid var(--border) !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--text-main) !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid var(--border) !important;
            background: var(--bg-surface) !important;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary * {
            color: var(--black) !important;
            background: var(--bg-surface) !important;
        }

        [data-testid="stExpanderDetails"] {
            background: var(--bg-surface) !important;
            color: var(--text-main) !important;
            border-top: 1px solid var(--border) !important;
        }

        [data-testid="stAlert"] {
            background: var(--bg-surface) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-main) !important;
        }

        [data-testid="stAlert"] * {
            color: var(--text-main) !important;
        }

        [data-testid="stMetric"] {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            padding: 0.45rem 0.6rem;
        }

        [data-testid="stMetric"] [data-testid="stMetricLabel"],
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: var(--text-main) !important;
        }

        [data-testid="stMetric"] [data-testid="stMetricDelta"] {
            color: var(--green) !important;
        }

        [data-testid="stHorizontalBlock"] hr,
        hr {
            border-color: var(--border) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
