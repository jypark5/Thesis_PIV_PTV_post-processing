import streamlit as st
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from scipy.ndimage import label, binary_dilation, binary_erosion, binary_fill_holes
from graphing.G_puff_characteristics_boundary_radius_and_trajectory_graph import (
    build_puff_boundary_contour, 
    build_puff_kinematics_charts, 
    build_puff_noise_diagnostic_charts,
    build_puff_morphology_scaling_chart
)

st.set_page_config(
    page_title="Puff Characteristics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Puff Characteristics - Boundary Radius and Trajectory")

if "puff_kinematics_results" not in st.session_state or st.session_state.puff_kinematics_results is None:
    st.warning("Please upload and process your data inside the Main Page first.")
else:
    frames = st.session_state.frames_data
    start_frame = st.session_state.start_frame
    mouth_x_mm = st.session_state.mouth_x
    frame_rate = st.session_state.frame_rate
    dt = 1.0 / frame_rate
    
    res = st.session_state.puff_kinematics_results

    st.sidebar.markdown("### Analysis Hyperparameters")
    max_time = st.sidebar.number_input("Max Analysis Duration (s)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
    smooth_win = st.sidebar.number_input("Temporal Smoothing Window", min_value=3, max_value=31, value=11, step=2)
    min_area = st.sidebar.number_input("Minimum Puff Size (pixels)", min_value=10, max_value=500, value=100, step=10)

    # Slice indices matching the max analysis tracking window constraint
    n_cutoff = min(len(res["time_vec"]), int(round(max_time / dt)))
    
    time_vec = res["time_vec"][:n_cutoff]
    center_x = res["center_x"][:n_cutoff]
    traj_x = res["traj_x"][:n_cutoff]
    traj_r = res["traj_r"][:n_cutoff]
    radius_mm = res["radius_mm"][:n_cutoff]
    background_noise = res["background_noise"][:n_cutoff]
    background_std = res["background_std"][:n_cutoff]
    mask_area = res["mask_area"][:n_cutoff]
    xi, yi, Xi, Yi = res["xi"], res["yi"], res["Xi"], res["Yi"]

    st.subheader("Interactive Single Frame Boundary Visualization")
    frame_plot = st.number_input(
        "Select Profile Frame Index", 
        min_value=int(start_frame), 
        max_value=int(start_frame + n_cutoff - 1), 
        value=int(start_frame)
    )

    f_plot_data = frames[frame_plot - 1]
    X_p = f_plot_data["X"].ravel() - mouth_x_mm
    Y_p = f_plot_data["Y"].ravel()
    V_p = f_plot_data["Vmag"].ravel()

    Vi_p = griddata(np.vstack((X_p, Y_p)).T, V_p, (Xi, Yi), method='linear')
    v_thr_p = 0.40 * (np.nanmax(Vi_p) if not np.all(np.isnan(Vi_p)) else 0.0)
    
    mask_p = np.zeros_like(Vi_p, dtype=bool)
    mask_p[~np.isnan(Vi_p)] = Vi_p[~np.isnan(Vi_p)] > v_thr_p
    
    labeled_mask_p, num_feats_p = label(mask_p, structure=res["connectivity_8"])
    if num_feats_p > 0:
        f_sizes_p = np.bincount(labeled_mask_p.ravel())
        mask_p[f_sizes_p[labeled_mask_p] < 40] = False
    mask_p = binary_erosion(binary_dilation(mask_p, structure=res["disk_element"]), structure=res["disk_element"], border_value=1)
    mask_p = binary_fill_holes(mask_p)

    fig_heat = build_puff_boundary_contour(xi, yi, Vi_p, mask_p, frame_plot)
    st.plotly_chart(fig_heat, use_container_width=False)

    st.markdown("---")
    st.subheader("Dynamic Kinematics & Tracking Analysis Profiles")

    # Prune elements failing tracking density threshold filters
    area_ok = mask_area >= min_area
    valid_mask = (~np.isnan(center_x)) & area_ok
    background_noise = np.where(area_ok, background_noise, np.nan)
    background_std = np.where(area_ok, background_std, np.nan)
    t_val = time_vec[valid_mask]
    tx_val = traj_x[valid_mask]
    tr_val = traj_r[valid_mask]
    r_val = radius_mm[valid_mask]

    def roll_avg(arr, win):
        return pd.Series(arr).rolling(window=win, center=True, min_periods=1).mean().to_numpy()

    tx_smooth = roll_avg(tx_val, smooth_win)
    tr_smooth = roll_avg(tr_val, smooth_win)
    r_smooth = roll_avg(r_val, smooth_win)

    col1, col2, col3 = st.columns(3)
    with col1:
        fig1 = build_puff_kinematics_charts(t_val, tx_val, tx_smooth, tr_val, tr_smooth, r_val, r_smooth, "Puff trajectory along x axis", "s_x (m)")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = build_puff_kinematics_charts(t_val, tr_val, tr_smooth, tx_val, tx_smooth, r_val, r_smooth, "Radial puff trajectory spatial tracking", "s (m)")
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        fig3 = build_puff_kinematics_charts(t_val, r_val, r_smooth, tx_val, tx_smooth, tr_val, tr_smooth, "Puff expansion radius profile vs time", "r (m)")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.subheader("Background Noise & Diagnostic Metrics")

    valid_b = ~np.isnan(background_noise)
    tb_val = time_vec[valid_b]
    noise_val = background_noise[valid_b]
    std_val = background_std[valid_b]

    noise_smooth = roll_avg(noise_val, 11)
    std_smooth = roll_avg(std_val, 11)

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        fig_n1 = build_puff_noise_diagnostic_charts(tb_val, noise_val, noise_smooth, "Background Velocity Noise Over Time", "Background |V| (m/s)")
        st.plotly_chart(fig_n1, use_container_width=True)
    with col_b2:
        fig_n2 = build_puff_noise_diagnostic_charts(tb_val, std_val, std_smooth, "Background Noise Variability Over Time", "Noise standard deviation (m/s)")
        st.plotly_chart(fig_n2, use_container_width=True)

    st.markdown("#### Summary Statistical Noise Report")
    if np.any(valid_b):
        st.text(f"Mean background |V|     = {np.nanmean(background_noise):.4f} m/s")
        st.text(f"Median background |V|   = {np.nanmedian(background_noise):.4f} m/s")
        st.text(f"Std dev of noise        = {np.nanstd(background_noise, ddof=1):.4f} m/s")
        st.text(f"Max background |V|      = {np.nanmax(background_noise):.4f} m/s")
    else:
        st.text("Mean background |V|     = 0.0000 m/s\nMedian background |V|   = 0.0000 m/s\nStd dev of noise        = 0.0000 m/s\nMax background |V|      = 0.0000 m/s")

    st.markdown("---")
    st.subheader("Morphology Aspect Profile: Puff Half-Width vs Axial Distance")

    s_vals = traj_x[valid_mask] / 10.0
    r_vals = radius_mm[valid_mask] / 10.0

    sort_idx = np.argsort(s_vals)
    s_sorted = s_vals[sort_idx]
    r_sorted = r_vals[sort_idx]
    r_sorted_smooth = roll_avg(r_sorted, 15)

    fig_morph = build_puff_morphology_scaling_chart(s_sorted, r_sorted, r_sorted_smooth)
    st.plotly_chart(fig_morph, use_container_width=False)