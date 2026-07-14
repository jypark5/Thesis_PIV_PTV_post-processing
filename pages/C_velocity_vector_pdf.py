import streamlit as st
from graphing.C_velocity_vector_pdf_graph import build_velocity_pdf_3d_plots

st.set_page_config(
    page_title="Velocity PDF Over Distance Slices",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Velocity Probability Density Function (PDF) Over Distance Slices")

if "velocity_pdf_results" not in st.session_state or st.session_state.velocity_pdf_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.velocity_pdf_results
    
    st.sidebar.markdown("### Axis Configurations")
    z_limit = st.sidebar.number_input(
        "PDF Axis Max Limit (z-axis)",
        min_value=0.05,
        max_value=1.0,
        value=0.30,
        step=0.05
    )
    
    fig = build_velocity_pdf_3d_plots(res, z_limit)
    st.plotly_chart(fig, use_container_width=True)