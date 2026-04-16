import streamlit as st
from streamlit_styles import apply_shared_styles

# Page config
st.set_page_config(
    page_title="AI Urban Image Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_shared_styles()

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown("### AI Urban Image Analyzer")
    st.caption("Context photography workflow")
with col2:
    img_count = 0
    st.metric("Images Loaded", img_count)
with col3:
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("Upload Images", use_container_width=True)
    with col_b:
        st.button("Run Analysis", use_container_width=True, type="primary")

st.divider()

# Main layout - 2 column grid (Image Set + Analysis)
col_left, col_right = st.columns([5, 7], gap="large")

# LEFT COLUMN - Image Set
with col_left:
    st.markdown("#### Image Set")
    
    # Filter buttons
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        st.button("Cluster", use_container_width=True)
    with filter_col2:
        st.button("Use", use_container_width=True)
    with filter_col3:
        st.button("Confidence", use_container_width=True)
    
    st.divider()
    
    # Image upload
    uploaded_images = st.file_uploader(
        "Upload urban images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    # Image grid (3x4)
    if uploaded_images:
        img_cols = st.columns(3)
        for i, img in enumerate(uploaded_images[:12]):
            with img_cols[i % 3]:
                st.image(img, use_column_width=True)
    else:
        # Placeholder grid
        placeholder_cols = st.columns(3)
        for i in range(12):
            with placeholder_cols[i % 3]:
                st.markdown(f"""
                <div class='placeholder-image'>Image {i+1}</div>
                """, unsafe_allow_html=True)
    
    st.caption(f"Showing {len(uploaded_images) if uploaded_images else 0} images")

# RIGHT COLUMN - Analysis & Results
with col_right:
    st.markdown("#### Metrics & Analysis")
    
    # Metric Cards
    metric_cols = st.columns(4)
    metrics = [
        {"label": "Avg Height", "value": "5–7", "subtext": "storeys"},
        {"label": "Active Frontage", "value": "68%", "subtext": "street edge active"},
        {"label": "Dominant Use", "value": "Mixed", "subtext": "commercial + residential"},
        {"label": "Material", "value": "Brick/Glass", "subtext": "most frequent palette"},
    ]
    
    for i, metric in enumerate(metrics):
        with metric_cols[i]:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>{metric['label']}</div>
                <div class='metric-value'>{metric['value']}</div>
                <div class='metric-subtext'>{metric['subtext']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Urban Context Summary
    st.markdown("#### Urban Context Summary")
    
    chart_cols = st.columns(3)
    
    with chart_cols[0]:
        st.markdown("**Material Distribution**")
        st.markdown(
            """
            <div class='chart-bars'>
                <div class='bar' style='--bar-height: 70%;'></div>
                <div class='bar' style='--bar-height: 55%;'></div>
                <div class='bar' style='--bar-height: 35%;'></div>
                <div class='bar' style='--bar-height: 20%;'></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with chart_cols[1]:
        st.markdown("**Use Distribution**")
        st.markdown(
            """
            <div class='chart-donut-wrap'>
                <div class='chart-donut'>
                    <div class='chart-donut-hole'></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with chart_cols[2]:
        st.markdown("**Height Ranges**")
        st.markdown(
            """
            <div class='chart-bars'>
                <div class='bar' style='--bar-height: 20%;'></div>
                <div class='bar' style='--bar-height: 45%;'></div>
                <div class='bar' style='--bar-height: 75%;'></div>
                <div class='bar' style='--bar-height: 50%;'></div>
                <div class='bar' style='--bar-height: 30%;'></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Urban DNA
    st.markdown("#### Urban DNA")
    dna_data = [
        {"label": "Height", "value": 70},
        {"label": "Activity", "value": 82},
        {"label": "Density", "value": 64},
    ]
    
    for item in dna_data:
        st.markdown(f"**{item['label']}** ({item['value']}%)")
        st.progress(item['value'] / 100)

# Selected Image Detail
st.divider()
st.markdown("### Selected Image Detail")

detail_col1, detail_col2 = st.columns([1, 2])

with detail_col1:
    st.markdown("**Preview**")
    st.markdown("""
    <div class='preview-placeholder'>Selected Image</div>
    """, unsafe_allow_html=True)

with detail_col2:
    # Tags
    tags = ['Brick', 'Commercial', '6 Storeys', 'Active Frontage']
    tag_html = ' '.join([f"<span class='tag-pill'>{tag}</span>" for tag in tags])
    st.markdown(f"**Tags:** {tag_html}", unsafe_allow_html=True)
    
    st.markdown("**Confidence Scores**")
    confidence_data = [
        {"label": "Material Detection", "value": 84},
        {"label": "Use Classification", "value": 71},
        {"label": "Height Estimate", "value": 63},
        {"label": "Frontage Activity", "value": 89},
    ]
    
    for item in confidence_data:
        st.markdown(f"**{item['label']}** ({item['value']}%)")
        st.progress(item['value'] / 100)
    
    st.markdown("""
    **Description**  
    Mid-rise mixed-use street condition with brick and glazed facades, active ground-floor edges, 
    and a consistent urban wall. Street trees and signage suggest a pedestrian-oriented commercial corridor.
    """)

# Clusters & Outliers
st.divider()
st.markdown("### Clusters & Outliers")

cluster_cols = st.columns(4)
clusters = [
    {"title": "Commercial Strip", "type": "cluster"},
    {"title": "Residential Edge", "type": "cluster"},
    {"title": "Mixed-Use Block", "type": "cluster"},
    {"title": "Atypical Tower", "type": "outlier"},
]

for i, cluster in enumerate(clusters):
    with cluster_cols[i]:
        card_class = "cluster-card outlier" if cluster["type"] == "outlier" else "cluster-card"
        st.markdown(f"""
        <div class='{card_class}'>
            <div class='cluster-title'>{cluster['title']}</div>
            <div class='cluster-thumb-grid'>
                <div class='cluster-thumb'></div>
                <div class='cluster-thumb'></div>
                <div class='cluster-thumb'></div>
                <div class='cluster-thumb'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("AI Urban Image Analyzer © 2026")
