import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.interpolate import griddata

st.set_page_config(layout="wide")
st.title("Velocity Field Heatmap Over Time")

if st.session_state.frames_data is None:
    st.warning("Please upload and process a zip archive on the main page first.")
else:
    frames = st.session_state.frames_data
    start_frame = st.session_state.start_frame
    mouth_x = st.session_state.mouth_x
    frame_rate = st.session_state.frame_rate
    
    dt = 1.0 / frame_rate
    t_samples = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    base_idx = start_frame - 1
    
    frame_indices = [int(round(base_idx + t / dt)) for t in t_samples]
    
    bounds_valid = True
    for idx in frame_indices:
        if idx < 0 or idx >= len(frames):
            bounds_valid = False
            
    if not bounds_valid:
        st.error(f"Calculated frame indices exceed the available range of the dataset (1 to {len(frames)}). Verify the start frame index or frame rate configurations.")
    else:
        all_v = []
        for idx in frame_indices:
            all_v.extend(frames[idx]["Vmag"].ravel())
        pct_98 = float(np.percentile(all_v, 98))
        
        cmax = st.sidebar.number_input(
            "Max Velocity Scale (m/s)", 
            min_value=0.1, 
            value=6.0, 
            step=0.5,
            help=f"98th percentile of selected frames is {pct_98:.2f} m/s"
        )
        
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=[f"t = {t:.1f} s" for t in t_samples],
            shared_xaxes=True,
            shared_yaxes=True,
            horizontal_spacing=0.02,
            vertical_spacing=0.07
        )
        
        for n, idx in enumerate(frame_indices):
            row = (n // 3) + 1
            col = (n % 3) + 1
            
            f_data = frames[idx]
            Xs = f_data["X"] - mouth_x
            Y = f_data["Y"]
            V = f_data["Vmag"]
            
            xi = np.linspace(0, Xs.max(), 300)
            yi = np.linspace(Y.min(), Y.max(), 300)
            Xi, Yi = np.meshgrid(xi, yi)
            
            points = np.vstack((Xs.ravel(), Y.ravel())).T
            Vi = griddata(points, V.ravel(), (Xi, Yi), method='linear')
            
            fig.add_trace(
                go.Heatmap(
                    x=xi,
                    y=yi,
                    z=Vi,
                    coloraxis="coloraxis"
                ),
                row=row, col=col
            )
        
        fig.update_layout(
            coloraxis=dict(
                colorscale='Turbo',
                cmin=0,
                cmax=cmax,
                colorbar=dict(
                    title=dict(
                        text="Velocity magnitude [m/s]",
                        side="right"
                    ),
                    thickness=20
                )
            ),
            font=dict(
                family="Times New Roman",
                size=12
            ),
            width=1200,
            height=700,
            margin=dict(l=60, r=20, t=50, b=50)
        )
        
        fig.update_yaxes(title_text="y [mm]", row=1, col=1)
        fig.update_yaxes(title_text="y [mm]", row=2, col=1)
        fig.update_xaxes(title_text="x [mm]", row=2, col=1)
        fig.update_xaxes(title_text="x [mm]", row=2, col=2)
        fig.update_xaxes(title_text="x [mm]", row=2, col=3)
        
        st.plotly_chart(fig, use_container_width=True)