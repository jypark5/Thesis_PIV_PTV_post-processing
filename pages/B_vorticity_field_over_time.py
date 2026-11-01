import streamlit as st
import numpy as np
from graphing.B_vorticity_field_over_time_graph import build_vorticity_time_series_grid

st.set_page_config(
    page_title="Vorticity Map Over Time",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Vorticity Map (ω_z) Over Time")

if "vorticity_results" not in st.session_state or st.session_state.vorticity_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.vorticity_results
    
    st.sidebar.markdown("### Visualization Configurations")
    times_str = st.sidebar.text_input(
        "Times after cough onset (seconds, comma-separated)", 
        value="0.1, 0.2, 0.3"
    )
    
    try:
        t_samples = [float(t.strip()) for t in times_str.split(",") if t.strip()]
    except ValueError:
        st.error("Please enter a valid list of numbers separated by commas.")
        t_samples = [0.1, 0.2, 0.3]
        
    # Colour limit follows only the selected times
    selected_abs_w = [res["snapshots"][t]["abs_w"] for t in t_samples if t in res["snapshots"]]
    max_abs = float(np.percentile(np.concatenate(selected_abs_w), 98, method='hazen')) if selected_abs_w else res["max_abs"]

    clim_val = st.sidebar.number_input(
        "Symmetric Color Range Limit Max (1/s)",
        min_value=0.1,
        value=max(max_abs, 0.1),
        step=50.0,
        help=f"98th percentile of absolute value is {max_abs:.2f} 1/s"
    )
    
    fig = build_vorticity_time_series_grid(res, clim_val, t_samples)
    
    if len(fig.data) == 0:
        st.error("None of the selected time values match the precomputed snapshots folder. Please choose from 0.1, 0.2, 0.3, 0.4, or 0.5 s.")
    else:
        st.plotly_chart(fig, use_container_width=True)