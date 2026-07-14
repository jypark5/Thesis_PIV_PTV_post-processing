import streamlit as st
from graphing.D_directional_pdf_graph import build_directional_pdf_polar_plots

st.set_page_config(
    page_title="Directional PDF",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Directional PDF")

if "directional_pdf_results" not in st.session_state or st.session_state.directional_pdf_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.directional_pdf_results
    
    if not res["bounds_valid"]:
        st.error("Requested time windows exceed the available range of frames in the dataset.")
    elif "error_window" in res:
        st.error(f"No valid velocity vectors found in window {res['error_window']}")
    else:
        fig = build_directional_pdf_polar_plots(res)
        st.plotly_chart(fig, use_container_width=True)