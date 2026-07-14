import streamlit as st
import numpy as np
import pandas as pd
from graphing.J_peak_puff_velocity_over_time_graph import build_peak_puff_velocity_plot

st.set_page_config(
    page_title="Peak Puff Velocity Over Time",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Peak Velocity Inside Puff vs Time")

if "peak_puff_velocity_results" not in st.session_state or st.session_state.peak_puff_velocity_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.peak_puff_velocity_results
    time_base = res["time_base"]
    Vpuff_raw = res["Vpuff_raw"]
    
    st.sidebar.markdown("### Post-Processing Settings")
    t_max = st.sidebar.number_input("Max Analysis Duration (s)", min_value=0.1, max_value=2.0, value=0.60, step=0.05)
    smooth_window = st.sidebar.number_input("Smoothing Window Size (Frames)", min_value=1, max_value=51, value=11, step=2)

    # Slice evaluation arrays matching tracking threshold constraints
    time_mask = time_base <= t_max
    time_slice = time_base[time_mask]
    v_raw_slice = Vpuff_raw[time_mask]
    
    # Fast centered moving average convolutions
    def moving_average(arr, win):
        return pd.Series(arr).rolling(window=win, center=True, min_periods=1).mean().to_numpy()
        
    v_smooth_slice = moving_average(v_raw_slice, smooth_window)
    
    if np.all(np.isnan(v_raw_slice)):
        st.error("No valid puff velocity detections found in this tracking window range.")
    else:
        fig = build_peak_puff_velocity_plot(time_slice, v_raw_slice, v_smooth_slice, t_max)
        st.plotly_chart(fig, use_container_width=False)