import numpy as np
from scipy.signal import savgol_coeffs

def compute_peak_velocity_series(frames_list, start_frame, frame_rate):
    """
    Peak Velocity Time Series Engine
    Extracts frame-by-frame global velocity maximums, runs a median filter cascade,
    applies multi-scale Savitzky-Golay filtering, and forces true peak conservation.
    """
    n_frames = len(frames_list)
    dt = 1.0 / frame_rate

    time_arr = (np.arange(1, n_frames + 1) - start_frame) * dt

    PV_raw = np.zeros(n_frames)
    for i in range(n_frames):
        PV_raw[i] = np.nanmax(frames_list[i]["Vmag"])

    global_peak_raw = float(np.nanmax(PV_raw))
    global_peak_frame = int(np.nanargmax(PV_raw) + 1)
    global_peak_time = float((global_peak_frame - start_frame) * dt)

    PV_med = np.zeros(n_frames)
    for i in range(n_frames):
        i1 = max(0, i - 2)
        i2 = min(n_frames, i + 3)
        PV_med[i] = np.median(PV_raw[i1:i2])

    # Centred Savitzky-Golay kernels; the MATLAB end-point kernel shifted the curve earlier in time
    h1 = savgol_coeffs(11, 3)
    PV_s1 = np.convolve(PV_med, h1, mode='same')

    h2 = savgol_coeffs(51, 3)
    PV_s2 = np.convolve(PV_s1, h2, mode='same')

    h3 = savgol_coeffs(81, 3)
    PV_smooth = np.convolve(PV_s2, h3, mode='same')

    raw_idx = np.nanargmax(PV_raw)
    peak_vel_raw = PV_raw[raw_idx]
    PV_smooth[raw_idx] = peak_vel_raw
    PV_smooth = np.maximum(PV_smooth, 0.0)

    idx = np.nanargmax(PV_smooth)
    peak_vel_smooth = float(PV_smooth[idx])
    peak_time_smooth = float(time_arr[idx])

    return {
        "time": time_arr,
        "PV_raw": PV_raw,
        "PV_smooth": PV_smooth,
        "global_peak_raw": global_peak_raw,
        "global_peak_frame": global_peak_frame,
        "global_peak_time": global_peak_time,
        "peak_vel_smooth": peak_vel_smooth,
        "peak_time_smooth": peak_time_smooth
    }