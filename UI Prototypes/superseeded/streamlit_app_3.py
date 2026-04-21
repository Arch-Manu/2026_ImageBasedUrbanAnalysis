import streamlit as st
from streamlit_styles import apply_shared_styles

st.set_page_config(page_title='AI Urban Image Analyzer - Option 3', layout='wide')
apply_shared_styles()

# ---------- Helpers ----------
def tile(label: str, height: int = 72):
    st.markdown(
        f"""
        <div class="wf-tile" style="--tile-h:{height}px;">{label}</div>
        """,
        unsafe_allow_html=True,
    )


def metric_box(label: str, value: str, note: str = ''):
    st.markdown(f'**{label}**')
    st.write(value)
    if note:
        st.caption(note)


# ---------- Mock data ----------
clusters = [
    {'title': 'Residential low-rise', 'count': 32, 'desc': 'Setback housing, quieter edge'},
    {'title': 'Commercial strip', 'count': 41, 'desc': 'Retail signage, active frontage'},
    {'title': 'Mixed-use block', 'count': 28, 'desc': 'Podium retail with upper occupancy'},
    {'title': 'Civic / hotel edge', 'count': 14, 'desc': 'Larger footprints, formal entries'},
]

outliers = [
    'Atypical tower with reflective skin',
    'Vacant frontage on primary street',
    'Heavy setback condition',
    'Blank service edge',
    'Highly vegetated frontage',
]

st.sidebar.title('Option 3 — Analytical Tool')
st.sidebar.write('A research-oriented interface centered on clustering, pattern detection, and human correction.')

image_count = st.sidebar.slider('Dataset size', 24, 500, 127)
confidence_threshold = st.sidebar.slider('Confidence threshold', 0.0, 1.0, 0.65, 0.05)
focus = st.sidebar.radio('Feature focus', ['Height', 'Material', 'Activity', 'Use'])
view_mode = st.sidebar.selectbox('Center panel mode', ['Cluster cards', 'Feature-space placeholder'])
show_edit_panel = st.sidebar.toggle('Show human correction panel', True)

# Header (same visual pattern as app 0/2)
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown("### AI Urban Image Analyzer")
    st.caption(f"Option 3 wireframe | Focus: {focus}")
with col2:
    st.metric("Images Loaded", image_count)
with col3:
    h1, h2 = st.columns(2)
    with h1:
        st.button("Upload Images", use_container_width=True)
    with h2:
        st.button("Run Analysis", use_container_width=True, type="primary")

st.caption(f"Threshold: {confidence_threshold:.2f} | Mode: {view_mode}")
st.divider()

left, center, right = st.columns([1.0, 1.45, 1.15], gap='large')

# ---------- Left panel ----------
with left:
    st.subheader('Dataset + Controls')
    st.metric('Images loaded', image_count)
    st.metric('Clusters found', len(clusters))
    st.metric('Outliers flagged', len(outliers))
    st.markdown('**Filters**')
    st.selectbox('Street segment', ['All', 'Main street', 'Side street', 'Laneway'])
    st.multiselect('Uses detected', ['Commercial', 'Residential', 'Hotel', 'Civic', 'Mixed-use'], default=['Commercial', 'Residential', 'Mixed-use'])
    st.slider('Minimum active frontage score', 0, 100, 50)
    st.slider('Height range', 1, 20, (3, 10))
    st.caption('This panel would normally contain upload, filtering, and re-analysis controls.')

# ---------- Center panel ----------
with center:
    st.subheader('Pattern Structure')
    if view_mode == 'Cluster cards':
        grid = st.columns(2)
        for i, cluster in enumerate(clusters):
            with grid[i % 2]:
                with st.container(border=True):
                    st.markdown(f"**{cluster['title']}**")
                    st.caption(f"{cluster['count']} images • {cluster['desc']}")
                    st.markdown(
                        """
                        <div class="cluster-thumb-grid" style="margin-top: 8px;">
                            <div class="wf-tile" style="--tile-h:72px; font-size:12px;">Img A</div>
                            <div class="wf-tile" style="--tile-h:72px; font-size:12px;">Img B</div>
                            <div class="wf-tile" style="--tile-h:72px; font-size:12px;">Img C</div>
                            <div class="wf-tile" style="--tile-h:72px; font-size:12px;">Img D</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
    else:
        st.markdown(
            """
            <div class="fs-space">
                <div class="fs-label fs-label-1">Commercial strip</div>
                <div class="fs-label fs-label-2">Residential low-rise</div>
                <div class="fs-label fs-label-3">Mixed-use block</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption('Placeholder for embedding-space or cluster-space view. This makes the more-than-human grouping logic explicit.')

# ---------- Right panel ----------
with right:
    st.subheader('Insights Panel')
    with st.container(border=True):
        st.markdown('**Aggregated Analysis**')
        metric_box('Dominant condition', 'Commercial strip', 'Most frequent cluster in current filter set')
        metric_box('Average height', '5-7 storeys', 'Estimated from visible facade patterns')
        metric_box('Dominant material', 'Brick / Glass', 'Most repeated palette in selected subset')
        metric_box('Activity score', '0.68', 'Based on signage, entries, transparency, and people cues')

    with st.container(border=True):
        st.markdown('**Pattern Detection**')
        st.write('- Ground-floor activity clusters along the primary corridor.')
        st.write('- Blank edges increase on side streets.')
        st.write('- Material consistency is strongest in the mixed-use cluster.')
        st.write('- Height variation is narrow except for a small number of towers.')

    with st.container(border=True):
        st.markdown('**Top 5 anomalies**')
        for item in outliers:
            st.write(f'- {item}')

# ---------- Bottom slide-up style panel ----------
if show_edit_panel:
    st.divider()
    st.subheader('Selected Cluster / Image — Human Correction Panel')
    a, b = st.columns([1.0, 2.2], gap='large')
    with a:
        tile('Representative image', 180)
    with b:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.selectbox('Correct use', ['Commercial', 'Residential', 'Hotel', 'Mixed-use'])
        with c2:
            st.selectbox('Correct material', ['Brick', 'Glass', 'Concrete', 'Render'])
        with c3:
            st.selectbox('Frontage activity', ['Low', 'Medium', 'High'])
        st.text_area('Reviewer notes', 'This cluster appears to combine hotel frontage with retail podium conditions.')
        d1, d2 = st.columns(2)
        with d1:
            st.button('Apply correction', use_container_width=True)
        with d2:
            st.button('Re-run cluster labels', use_container_width=True)

st.markdown(
    """
    <div class='metric-card'>
        <div class='metric-subtext'>
            Best for a demo that emphasizes clustering, pattern mining, and human-in-the-loop review rather than just image captioning.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
