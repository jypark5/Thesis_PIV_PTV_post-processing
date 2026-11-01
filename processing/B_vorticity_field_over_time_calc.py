import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

def precompute_vorticity_maps(frames_list, start_frame, frame_rate, mouth_x):
    """
    Vorticity Field Spatial Interpolation Engine
    Tracks fluid rotational fields across time increments, extracts coordinate grids,
    maps vectors to a structured mesh, and applies spatial Gaussian filtering.
    """
    dt = 1.0 / frame_rate
    t_samples = [0.1, 0.2, 0.3, 0.4, 0.5]
    base_idx = start_frame - 1
    
    frame_indices = [int(round(base_idx + t / dt)) for t in t_samples]
    frame_indices = [max(0, min(idx, len(frames_list) - 1)) for idx in frame_indices]
    
    all_w = []
    snapshots = {}
    
    for t, idx in zip(t_samples, frame_indices):
        f_data = frames_list[idx]
        x_raw = f_data["X"].ravel() - mouth_x
        y_raw = f_data["Y"].ravel()
        w_raw = f_data["vort"].ravel()
        
        valid = ~np.isnan(w_raw)
        x = x_raw[valid]
        y = y_raw[valid]
        w = w_raw[valid]
        
        if len(x) == 0:
            continue
            
        all_w.extend(w)
        
        xi = np.linspace(x.min(), x.max(), 250)
        yi = np.linspace(y.min(), y.max(), 120)
        Xi, Yi = np.meshgrid(xi, yi)
        
        points = np.vstack((x, y)).T
        Wi = griddata(points, w, (Xi, Yi), method='linear')
        Wi_filled = np.nan_to_num(Wi, nan=0.0)
        W_smooth = gaussian_filter(Wi_filled, sigma=2, truncate=2.5, mode='nearest')

        snapshots[t] = {
            "xi": xi,
            "yi": yi,
            "W_smooth": W_smooth,
            "abs_w": np.abs(w)
        }

    max_abs = float(np.percentile(np.abs(all_w), 98, method='hazen')) if all_w else 5.0
    
    return {
        "max_abs": max_abs,
        "snapshots": snapshots
    }