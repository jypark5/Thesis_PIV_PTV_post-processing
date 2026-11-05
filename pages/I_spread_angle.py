import streamlit as st
from graphing.I_spread_angle_graph import build_puff_spread_angle_plot

st.set_page_config(
    page_title="Puff Spread Angle",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Jet Influx Spread Angle Profile")

if "spread_angle_results" not in st.session_state or st.session_state.spread_angle_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    res = st.session_state.spread_angle_results
    
    if not res["bounds_valid"]:
        st.error("Unable to resolve contiguous vector shapes or boundaries. Verify data thresholds.")
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Opening Spread Angle", value=f"{res['spreadAngle']:.2f}°")
        with col2:
            st.metric(label="Upper Orientation Angle", value=f"{res['angleU']:.2f}°")
        with col3:
            st.metric(label="Lower Orientation Angle", value=f"{res['angleL']:.2f}°")
            
        fig = build_puff_spread_angle_plot(res, 0.0)
        st.plotly_chart(fig, use_container_width=False)