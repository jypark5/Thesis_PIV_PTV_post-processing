import streamlit as st
from graphing.E_peak_velocity_over_time_graph import build_peak_velocity_time_plot

st.set_page_config(
    page_title="Peak Velocity Over Time",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Peak Velocity Over Time")

if "peak_velocity_series_results" not in st.session_state or st.session_state.peak_velocity_series_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.peak_velocity_series_results

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Global Raw Peak (Unsmoothed)")
        st.metric(label="Raw Peak Velocity", value=f"{res['global_peak_raw']:.3f} m/s")
        st.metric(label="Frame Index", value=res['global_peak_frame'])
        st.metric(label="Time after Onset", value=f"{res['global_peak_time']:.6f} s")
    with col2:
        st.markdown("### Final Processed Peak")
        st.metric(label="Smoothed Peak Velocity", value=f"{res['peak_vel_smooth']:.3f} m/s")
        st.metric(label="Peak Time Location", value=f"{res['peak_time_smooth']:.4f} s")

    fig = build_peak_velocity_time_plot(res)
    st.plotly_chart(fig, use_container_width=False)