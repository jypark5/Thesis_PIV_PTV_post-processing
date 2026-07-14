import streamlit as st
import numpy as np
import pandas as pd
from graphing.H_leading_edge_position_and_velocity_graph import build_leading_edge_position_plot, build_leading_edge_velocity_plot

st.set_page_config(
    page_title="Leading Edge Tracking",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Leading-edge Position and Velocity Profile")

if "leading_edge_results" not in st.session_state or st.session_state.leading_edge_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.leading_edge_results
    time_base = res["time_base"]
    xLead_mm_raw = res["xLead_mm_raw"]
    
    st.sidebar.markdown("### Post-Processing Settings")
    t_max = st.sidebar.number_input("Max Analysis Duration (s)", min_value=0.1, max_value=2.0, value=0.30, step=0.05)
    pos_win = st.sidebar.number_input("Position Smoothing Window (Frames)", min_value=1, max_value=51, value=11, step=2)
    vel_win = st.sidebar.number_input("Velocity Smoothing Window (Frames)", min_value=1, max_value=51, value=15, step=2)

    # Slice evaluation arrays matching tracking threshold constraints
    time_mask = time_base <= t_max
    time_slice = time_base[time_mask]
    x_slice_mm = xLead_mm_raw[time_mask]
    
    # Convert metric scales mm -> m
    x_slice_m = x_slice_mm / 1000.0
    
    # Fast centered moving average convolutions
    def moving_average(arr, win):
        return pd.Series(arr).rolling(window=win, center=True, min_periods=1).mean().to_numpy()
        
    x_slice_m_smooth = moving_average(x_slice_m, pos_win)
    
    # Numerical derivative computation
    v_lead_raw = np.zeros_like(x_slice_m_smooth)
    if len(x_slice_m_smooth) > 1:
        v_lead_raw[1:] = np.diff(x_slice_m_smooth) / np.diff(time_slice)
        v_lead_raw[0] = v_lead_raw[1]
        
    v_lead_smooth = moving_average(v_lead_raw, vel_win)

    col1, col2 = st.columns(2)
    with col1:
        fig_pos = build_leading_edge_position_plot(time_slice, x_slice_m, x_slice_m_smooth, t_max)
        st.plotly_chart(fig_pos, use_container_width=False)
    with col2:
        fig_vel = build_leading_edge_velocity_plot(time_slice, v_lead_raw, v_lead_smooth, t_max)
        st.plotly_chart(fig_vel, use_container_width=False)