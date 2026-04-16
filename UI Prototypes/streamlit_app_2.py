import streamlit as st
import random
from streamlit_styles import apply_shared_styles

st.set_page_config(page_title='AI Urban Image Analyzer - Option 2', layout='wide')
apply_shared_styles()

# ---------- Helpers ----------
def pct_bar(label: str, value: int):
    st.caption(f"{label} — {value}%")
    st.progress(value / 100)


def fake_image(label: str, height: int = 180):
    st.markdown(
        f"""
        <div class="wf-tile" style="--tile-h:{height}px;">{label}</div>
        """,
        unsafe_allow_html=True,
    )


def insight_chip(text: str):
    st.markdown(
        f"""
        <span class="wf-chip">{text}</span>
        """,
        unsafe_allow_html=True,
    )


# ---------- Mock data ----------
image_labels = [f"Context Photo {i}" for i in range(1, 19)]
selected = image_labels[0]

overlay_tags = [
    ("Glass facade", "top:14px; left:14px;"),
    ("Commercial frontage", "top:54px; left:28px;"),
    ("6 storeys", "bottom:16px; left:16px;"),
    ("Street trees", "bottom:56px; right:16px;"),
]

summary_cards = {
    'Height range': '5-7 storeys',
    'Use mix': 'Mixed-use dominant',
    'Material mix': 'Brick / Glass / Render',
    'Activity score': '68% active edge',
}

report = """
This image set suggests a mid-rise mixed-use corridor with active ground-floor frontages,
consistent street-wall definition, and a material palette dominated by brick and glazing.
Retail and hospitality uses are concentrated along the primary edge, while upper levels appear
predominantly residential or hotel-related. Tree planting and frequent signage suggest a
pedestrian-oriented urban condition.
""".strip()

# ---------- Sidebar ----------
st.sidebar.title('Option 2 — Image-First')
st.sidebar.write('A visual, presentation-friendly UI that starts from one image and expands into a multi-image context reading.')

uploaded_count = st.sidebar.slider('Images loaded', 12, 240, 127)
show_overlays = st.sidebar.toggle('Show AI overlay tags', True)
show_report = st.sidebar.toggle('Show context report drawer', True)
selected_sequence = st.sidebar.selectbox('Image sequence / street segment', ['Main street', 'Laneway edge', 'Corner condition'])
activity_filter = st.sidebar.slider('Minimum activity score', 0, 100, 40)

# ---------- Header ----------
st.title('AI Urban Image Analyzer')
st.caption(f'Option 2 wireframe • {uploaded_count} images loaded • Sequence: {selected_sequence}')

# ---------- Top image-first area ----------
left, right = st.columns([3.2, 1.3], gap='large')

with left:
    st.subheader('Selected Image')
    tag_html = ''
    if show_overlays:
        for idx, (text, _pos) in enumerate(overlay_tags, start=1):
            tag_html += f"""
            <div class="wf-overlay-tag wf-pos-{idx}">{text}</div>
            """

    st.markdown(
        f"""
        <div class="wf-hero">
            <div class="wf-hero-title">{selected}</div>
            {tag_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.subheader('Image Reading')
    st.metric('Primary use', 'Commercial', '+12% confidence')
    st.metric('Height estimate', '6 storeys', 'moderate confidence')
    st.metric('Frontage activity', 'High', 'many entrances / signs')
    pct_bar('Material detection', 84)
    pct_bar('Use classification', 76)
    pct_bar('Height estimate', 63)
    pct_bar('Frontage activity', 89)

st.divider()

# ---------- Bottom split ----------
col1, col2 = st.columns([1.9, 1.1], gap='large')

with col1:
    st.subheader('Image Sequence / Dataset Strip')
    strip_cols = st.columns(6)
    visible = image_labels[:12]
    for i, label in enumerate(visible):
        with strip_cols[i % 6]:
            fake_image(label.replace('Context Photo ', 'Img '), 96)
    st.caption('This strip represents the broader set of context images used to stabilize interpretation beyond a single viewpoint.')

with col2:
    st.subheader('Aggregated Insights')
    c1, c2 = st.columns(2)
    items = list(summary_cards.items())
    with c1:
        st.metric(items[0][0], items[0][1])
        st.metric(items[2][0], items[2][1])
    with c2:
        st.metric(items[1][0], items[1][1])
        st.metric(items[3][0], items[3][1])

    st.markdown('**Key urban signals**')
    for chip in ['active edge', 'tree-lined', 'mid-rise wall', 'mixed use', 'retail strip']:
        insight_chip(chip)

    st.markdown('**Mini charts**')
    st.markdown(
        """
        <div class='wf-mini-chart'>
            <div class='wf-mini-col'>
                <div class='wf-mini-bar' style='--bar-height: 42%;'></div>
                <span class='wf-mini-label'>Brick</span>
            </div>
            <div class='wf-mini-col'>
                <div class='wf-mini-bar' style='--bar-height: 31%;'></div>
                <span class='wf-mini-label'>Glass</span>
            </div>
            <div class='wf-mini-col'>
                <div class='wf-mini-bar' style='--bar-height: 17%;'></div>
                <span class='wf-mini-label'>Render</span>
            </div>
            <div class='wf-mini-col'>
                <div class='wf-mini-bar' style='--bar-height: 10%;'></div>
                <span class='wf-mini-label'>Concrete</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Expandable report ----------
if show_report:
    with st.expander('Context Report', expanded=True):
        st.write(report)
        st.markdown('**Bullet insights**')
        st.write('- Ground floor is likely retail or hospitality.')
        st.write('- Upper levels suggest residential or hotel occupancy.')
        st.write('- Consistent building line reinforces an urban corridor condition.')
        st.write('- Multiple images reduce uncertainty caused by angle and occlusion.')

# ---------- CTA ----------
cta1, cta2, cta3 = st.columns([1, 1, 2])
with cta1:
    st.button('Generate Context Report', use_container_width=True)
with cta2:
    st.button('Export Review Notes', use_container_width=True)
with cta3:
    st.markdown(
        """
        <div class='metric-card'>
            <div class='metric-label'>Positioning</div>
            <div class='metric-subtext'>Best for a demo where you want one strong hero image, AI overlays, and a simple story from image to urban summary.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
