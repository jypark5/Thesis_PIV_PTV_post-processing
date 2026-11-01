import streamlit as st
import numpy as np
import pandas as pd
from graphing.F_sliced_velocity_over_time_graph import build_sliced_velocity_trace_plot

st.set_page_config(
    page_title="Sliced Velocity Over Time",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Sliced Velocity Over Time")

if "sliced_velocity_results" not in st.session_state or st.session_state.sliced_velocity_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.sliced_velocity_results
    sliced_data = res["sliced_data"]
    time_base = res["time_base"]
    
    st.sidebar.markdown("### Slice Configurations")
    r_list_str = st.sidebar.text_input(
        "Downstream distances from mouth (mm, comma-separated)", 
        value="100, 200, 300"
    )
    
    try:
        r_list = [float(r.strip()) for r in r_list_str.split(",") if r.strip()]
    except ValueError:
        st.error("Please enter a valid list of distances separated by commas.")
        r_list = [100.0, 200.0, 300.0]

    ds = st.sidebar.number_input("Frame Downsampling Factor", min_value=1, value=10, step=5)
    smooth_window = st.sidebar.number_input("Temporal Smoothing Window Size", min_value=1, value=7, step=2)

    valid_distances = [r for r in r_list if r in sliced_data]
    
    if len(valid_distances) != len(r_list):
        st.error("Some requested distances fall outside the precomputed range (10mm to 500mm in 10mm increments).")
    
    if valid_distances:
        indices = list(range(0, len(time_base), ds))
        time_ds = time_base[indices]
        
        traces = []
        for r in valid_distances:
            traces.append(sliced_data[r][indices])
            
        traces = np.array(traces)
        traces_smooth = pd.DataFrame(traces.T).rolling(window=smooth_window, center=True, min_periods=1).mean().to_numpy().T
        
        fig = build_sliced_velocity_trace_plot(time_ds, traces_smooth, valid_distances)
        st.plotly_chart(fig, use_container_width=True)