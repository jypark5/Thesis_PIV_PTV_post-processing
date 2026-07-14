import streamlit as st
from graphing.A_vector_field_heatmap_graph import build_time_series_heatmap_grid

st.set_page_config(layout="wide")
st.title("Velocity Field Heatmap Over Time")

if "heatmap_results" not in st.session_state or st.session_state.heatmap_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.heatmap_results
    
    if not res["bounds_valid"]:
        st.error(f"Calculated frame indices exceed the available range of the dataset (1 to {res['max_available']}). Verify the start frame index or frame rate configurations.")
    else:
        cmax = st.sidebar.number_input(
            "Max Velocity Scale (m/s)", 
            min_value=0.1, 
            value=6.0, 
            step=0.5,
            help=f"98th percentile of selected frames is {res['pct_98']:.2f} m/s"
        )
        
        fig = build_time_series_heatmap_grid(res, cmax)
        st.plotly_chart(fig, use_container_width=True)