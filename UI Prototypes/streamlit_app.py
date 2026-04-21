import html
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import streamlit as st
from streamlit_styles import apply_shared_styles

# Project root (parent of UI Prototypes) for `agents` / local `analysis.py`
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Load this repo's analysis.py by path — avoids importing another package named `analysis`
# (e.g. on PYTHONPATH) which would miss `on_progress` and other updates.
_analysis_path = _PROJECT_ROOT / "analysis.py"
_spec = importlib.util.spec_from_file_location(
    "iba_analysis_pipeline",
    _analysis_path,
)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Cannot load analysis pipeline from {_analysis_path}")
_analysis_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_analysis_mod)
run_analysis = _analysis_mod.run_analysis
dna_pick = _analysis_mod.dna_pick
get_vision_photo_detail = _analysis_mod.get_vision_photo_detail

# Page config
st.set_page_config(
    page_title="AI Urban Image Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_shared_styles()


def _humanize_score_key(key: str) -> str:
    return key.replace("_", " ").title()


def _format_demo_value(val):
    if isinstance(val, dict):
        lines = []
        for kk, vv in val.items():
            sub = _format_demo_value(vv)
            lines.append(f"{kk}: {sub}" if "\n" not in sub else f"{kk}:\n{sub}")
        return "\n".join(lines)
    if isinstance(val, list):
        if not val:
            return ""
        if all(isinstance(x, dict) for x in val):
            blocks = []
            for i, item in enumerate(val):
                blocks.append(
                    f"— {i + 1} —\n{_format_demo_value(item)}"
                )
            return "\n\n".join(blocks)
        parts = []
        for x in val:
            if isinstance(x, (dict, list)):
                parts.append(_format_demo_value(x))
            else:
                parts.append(str(x))
        return ", ".join(parts)
    if isinstance(val, float):
        return f"{val:.1f}" if val != int(val) else str(int(val))
    if isinstance(val, int) and val > 1000:
        return f"{val:,}"
    return str(val)


def _agg_compact_row(
    label: str,
    mean: float,
    *,
    mn=None,
    mx=None,
    show_range: bool = False,
) -> str:
    pct = min(100.0, max(0.0, float(mean)))
    label_e = html.escape(label)
    extra = ""
    if show_range and mn is not None and mx is not None:
        extra = (
            f' <span style="font-size:11px;opacity:0.75">'
            f"({html.escape(str(mn))}–{html.escape(str(mx))})"
            f"</span>"
        )
    return (
        f'<div class="agg-row-compact">'
        f'<span class="agg-name">{label_e}{extra}</span>'
        f'<span class="agg-num">{mean:.0f}</span>'
        f'<div class="agg-bar-wrap"><div class="agg-bar-fill" style="width:{pct}%;">'
        f"</div></div></div>"
    )


def _narrative_summary_excerpt(synthesis_text: str, max_chars: int = 400) -> str:
    if not synthesis_text:
        return ""
    m = re.search(
        r"NARRATIVE\s+SUMMARY\s*(.+?)(?=RECOMMENDATIONS|URBAN\s+DNA|\Z)",
        synthesis_text,
        re.DOTALL | re.IGNORECASE,
    )
    block = (m.group(1) if m else synthesis_text).strip()
    if len(block) > max_chars:
        return block[: max_chars - 1].rstrip() + "…"
    return block


if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "analysis_error" not in st.session_state:
    st.session_state.analysis_error = None
if "selected_image_idx" not in st.session_state:
    st.session_state.selected_image_idx = 0
if "_upload_sig" not in st.session_state:
    st.session_state._upload_sig = None


def _select_image(idx: int) -> None:
    st.session_state.selected_image_idx = idx


result = st.session_state.analysis_result
err = st.session_state.analysis_error
urban = result.get("urban_dna") if result else None
synthesis_text = result.get("synthesis_text") if result else None

# Header
st.markdown("### AI Urban Image Analyzer")
st.caption("Context photography workflow")

st.text_input(
    "Address",
    placeholder="Enter your address here",
    key="visual_address",
)

st.divider()

# Image set (left) + Selected image detail (right)
col_left, col_right = st.columns([5, 7], gap="large")

with col_left:
    st.markdown("#### Image Set")
    uploaded_images = st.file_uploader(
        "Upload urban images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="urban_imgs",
    )
    n_img = len(uploaded_images) if uploaded_images else 0

    if uploaded_images:
        sig = tuple((f.name, getattr(f, "size", 0)) for f in uploaded_images)
        if sig != st.session_state._upload_sig:
            st.session_state._upload_sig = sig
            st.session_state.selected_image_idx = 0

        img_cols = st.columns(3)
        for i, img in enumerate(uploaded_images[:12]):
            with img_cols[i % 3]:
                st.image(img, use_container_width=True)
                sel = st.session_state.selected_image_idx == i
                st.button(
                    "Selected" if sel else "Select",
                    key=f"sel_img_{i}",
                    use_container_width=True,
                    type="primary" if sel else "secondary",
                    on_click=_select_image,
                    args=(i,),
                )

with col_right:
    st.markdown("#### Selected Image Detail")
    if result:
        _idx = 0
        if uploaded_images:
            _idx = int(st.session_state.selected_image_idx)
            _idx = max(0, min(_idx, len(uploaded_images) - 1))
            st.markdown("**Preview**")
            st.image(uploaded_images[_idx], use_container_width=True)

        vision_parsed = result.get("vision_parsed")
        _upload_name = uploaded_images[_idx].name if uploaded_images else None
        photo_detail = (
            get_vision_photo_detail(vision_parsed, _idx, _upload_name)
            if vision_parsed is not None
            else None
        )

        tags = None
        if photo_detail and photo_detail.get("tags"):
            tags = photo_detail["tags"]
        else:
            tags = dna_pick(
                urban,
                "Detected elements",
                "Detected Elements",
                "detected_elements",
            )
        if isinstance(tags, list) and tags:
            tag_html = " ".join(
                [
                    f"<span class='tag-pill'>{html.escape(str(t))}</span>"
                    for t in tags[:40]
                ]
            )
            st.markdown(f"**Tags:** {tag_html}", unsafe_allow_html=True)

        if photo_detail and photo_detail.get("overall_score") is not None:
            try:
                os_ = float(photo_detail["overall_score"])
                st.caption(f"Vision image score: {os_:.0f}/100")
            except (TypeError, ValueError):
                pass

        conf = dna_pick(urban, "Confidence", "confidence")
        if conf is not None:
            st.markdown("**Confidence**")
            try:
                cf = float(conf)
                pct = int(cf * 100) if cf <= 1 else int(cf)
                pct = max(0, min(100, pct))
                st.progress(pct / 100.0)
                st.caption(f"Overall synthesis confidence: {pct}%")
            except (TypeError, ValueError):
                st.write(conf)

        if photo_detail and (
            photo_detail.get("narrative") or photo_detail.get("verdict")
        ):
            if photo_detail.get("verdict") and photo_detail.get("narrative"):
                st.caption(photo_detail["verdict"])
            st.markdown("**Description**")
            body = (
                photo_detail.get("narrative")
                or photo_detail.get("verdict")
                or ""
            )
            st.markdown(body)
        else:
            desc = dna_pick(urban, "Insights", "insights")
            if desc:
                st.markdown("**Description**")
                st.markdown(desc)
            elif synthesis_text:
                excerpt = _narrative_summary_excerpt(synthesis_text, 600)
                if excerpt:
                    st.markdown("**Description**")
                    st.markdown(excerpt)

# Call to action: full-width Run Analysis
run_clicked = st.button(
    "Run Analysis",
    use_container_width=True,
    type="primary",
    disabled=n_img == 0,
    key="run_analysis_cta",
)

if run_clicked and uploaded_images:
    st.session_state.analysis_error = None
    tmp = tempfile.mkdtemp(prefix="urban_analysis_")
    try:
        paths = []
        for uf in uploaded_images:
            p = Path(tmp) / uf.name
            p.write_bytes(uf.getbuffer())
            paths.append(str(p))

        st.markdown("##### Analysis progress")
        status_line = st.empty()
        progress_bar = st.progress(0.0)

        def _report_progress(message: str, fraction: float) -> None:
            f = min(1.0, max(0.0, fraction))
            status_line.markdown(message)
            progress_bar.progress(f)

        st.session_state.analysis_result = run_analysis(
            paths,
            on_progress=_report_progress,
        )
        st.rerun()
    except Exception as e:
        st.session_state.analysis_result = None
        st.session_state.analysis_error = str(e)
        st.error(f"Analysis failed: {e}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

# After a successful run, `st.rerun()` above refreshes the page so this row and metrics stay in sync.
result = st.session_state.analysis_result
err = st.session_state.analysis_error
urban = result.get("urban_dna") if result else None
synthesis_text = result.get("synthesis_text") if result else None

if err and not result:
    st.warning("Fix the error above and run again.")

# Metrics & analysis — only after a completed run
if result:
    st.divider()
    st.markdown("### Metrics & Analysis")

    h_range = dna_pick(urban, "Height Range", "height_range")
    dom_use = dna_pick(urban, "Dominant Use", "dominant_use")
    mat_pal = dna_pick(urban, "Material Palette", "material_palette")
    agg = dna_pick(urban, "Aggregate Scores", "aggregate_scores") or {}
    af_mean = None
    if isinstance(agg, dict) and "active_frontages" in agg:
        v = agg["active_frontages"]
        if isinstance(v, dict) and "mean" in v:
            af_mean = v["mean"]

    metric_cols = st.columns(4)
    metrics = [
        {"label": "Height range", "value": h_range, "subtext": "from synthesis"},
        {"label": "Active frontage", "value": f"{af_mean}%" if af_mean is not None else None, "subtext": "aggregate mean"},
        {"label": "Dominant use", "value": dom_use, "subtext": "land use"},
        {"label": "Material", "value": mat_pal, "subtext": "palette"},
    ]

    for i, metric in enumerate(metrics):
        with metric_cols[i]:
            val = metric["value"]
            val_s = (str(val)[:28] if val is not None else "") if isinstance(val, str) else (str(val) if val is not None else "")
            sub = metric["subtext"]
            st.markdown(
                f"""
            <div class='metric-card'>
                <div class='metric-label'>{metric['label']}</div>
                <div class='metric-value'>{val_s}</div>
                <div class='metric-subtext'>{sub}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("#### Urban Context Summary")

    if urban:
        insight_txt = dna_pick(urban, "Insights", "insights") or ""
        if insight_txt:
            st.markdown(insight_txt[:1200])
    elif synthesis_text:
        excerpt = _narrative_summary_excerpt(synthesis_text, 800)
        if excerpt:
            st.markdown(excerpt)

    chart_cols = st.columns(3)

    with chart_cols[0]:
        st.markdown("**Aggregate scores (mean)**")
        if isinstance(agg, dict) and agg:
            rows_html = ['<div class="agg-scores-block agg-scores-block--tight">']
            for k in list(agg.keys())[:8]:
                row = agg.get(k)
                if not isinstance(row, dict):
                    continue
                mean = row.get("mean")
                if mean is None:
                    continue
                try:
                    m = float(mean)
                except (TypeError, ValueError):
                    continue
                rows_html.append(
                    _agg_compact_row(_humanize_score_key(k), m, show_range=False)
                )
            rows_html.append("</div>")
            st.markdown("".join(rows_html), unsafe_allow_html=True)

    with chart_cols[1]:
        st.markdown("**Style & activity**")
        style_v = dna_pick(urban, "Style", "style")
        act_v = dna_pick(urban, "Activity Level", "activity_level")
        typ_v = dna_pick(urban, "Primary Typology", "primary_typology")
        if style_v:
            st.markdown(f"**Style:** {style_v}")
        if act_v:
            st.markdown(f"**Activity:** {act_v}")
        if typ_v:
            st.markdown(f"**Typology:** {typ_v}")

    with chart_cols[2]:
        st.markdown("**Confidence**")
        conf = dna_pick(urban, "Confidence", "confidence")
        if conf is not None:
            try:
                cf = float(conf)
                pct = int(cf * 100) if cf <= 1 else int(cf)
                pct = max(0, min(100, pct))
                st.metric("Model confidence", f"{pct}%")
                st.progress(pct / 100.0)
            except (TypeError, ValueError):
                st.write(conf)

    st.markdown("#### Urban DNA (aggregate scores)")
    if isinstance(agg, dict) and agg:
        rows_html = ['<div class="agg-scores-block agg-scores-block--tight">']
        for key, row in agg.items():
            if not isinstance(row, dict):
                continue
            mean = row.get("mean")
            mn = row.get("min")
            mx = row.get("max")
            if mean is None:
                continue
            try:
                m = float(mean)
            except (TypeError, ValueError):
                continue
            rows_html.append(
                _agg_compact_row(
                    _humanize_score_key(key),
                    m,
                    mn=mn,
                    mx=mx,
                    show_range=bool(mn is not None and mx is not None),
                )
            )
        rows_html.append("</div>")
        st.markdown("".join(rows_html), unsafe_allow_html=True)

    demo = dna_pick(urban, "Demographics", "demographics")
    if isinstance(demo, dict) and demo:
        with st.expander("Demographics (place / census)", expanded=False):
            dcols = st.columns(3)
            items = list(demo.items())
            for i, (k, v) in enumerate(items):
                with dcols[i % 3]:
                    st.markdown(f"**{html.escape(str(k))}**")
                    st.text(_format_demo_value(v))

    export_obj = {
        "urban_dna": urban,
        "vision_parsed": result.get("vision_parsed"),
        "synthesis_text": synthesis_text,
        "pattern": result.get("pattern"),
        "insights": result.get("insights"),
    }
    st.download_button(
        label="Download analysis JSON",
        data=json.dumps(export_obj, indent=2, ensure_ascii=False),
        file_name="urban_analysis_export.json",
        mime="application/json",
    )

    if synthesis_text:
        with st.expander("Full synthesis output (raw)", expanded=False):
            st.text(synthesis_text)

# Footer
st.markdown("---")
st.caption("AI Urban Image Analyzer © 2026")
