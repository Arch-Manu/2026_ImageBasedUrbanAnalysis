import streamlit as st
from streamlit_styles import apply_shared_styles

st.set_page_config(page_title="AI Workflow – Urban Analysis", layout="wide")
apply_shared_styles()

left, divider, right = st.columns([1.05, 0.06, 2.0], gap="medium")

with left:
    st.markdown("<div class='section-header'>INPUTS</div>", unsafe_allow_html=True)
    st.markdown("<div class='input-box'>ADDRESS</div>", unsafe_allow_html=True)
    st.markdown("<div class='input-box'>IMAGE UPLOAD</div>", unsafe_allow_html=True)
    st.markdown("<div class='input-box'>VIDEO UPLOAD</div>", unsafe_allow_html=True)
    st.markdown("<div class='input-box'>DATA LAYERS</div>", unsafe_allow_html=True)
    st.markdown("<div class='run-box'>RUN ANALYSIS</div>", unsafe_allow_html=True)

with divider:
    st.markdown("<div class='divider-col'></div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='section-header'>OUTPUTS</div>", unsafe_allow_html=True)
    top_left, top_right = st.columns([2.25, 1.0], gap="small")
    with top_left:
        st.markdown("<div class='output-card'>NARRATIVE SUMMARY</div>", unsafe_allow_html=True)
    with top_right:
        st.markdown("<div class='output-card'>DNA</div>", unsafe_allow_html=True)

    st.markdown("<div class='big-output'>MAP OR IMAGE?</div>", unsafe_allow_html=True)
    st.markdown("<div class='small-note'>Mock Streamlit layout based on the supplied wireframe</div>", unsafe_allow_html=True)
