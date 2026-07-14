import numpy as np
from scipy.interpolate import griddata

def precompute_time_series_heatmaps(frames_list, start_frame, frame_rate, mouth_x):
    """
    Time-Series Spatial Interpolation Pipeline
    Identifies temporal frame targets, performs coordinate shifts, and maps 
    discontinuous PIV matrices onto uniform evaluation meshes.
    """
    dt = 1.0 / frame_rate
    t_samples = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    base_idx = start_frame - 1
    
    frame_indices = [int(round(base_idx + t / dt)) for t in t_samples]
    
    for idx in frame_indices:
        if idx < 0 or idx >= len(frames_list):
            return {"bounds_valid": False, "max_available": len(frames_list)}
            
    all_v = []
    snapshots = []
    
    for idx in frame_indices:
        f_data = frames_list[idx]
        Xs = f_data["X"] - mouth_x
        Y = f_data["Y"]
        V = f_data["Vmag"]
        
        all_v.extend(V.ravel())
        
        xi = np.linspace(0, Xs.max(), 300)
        yi = np.linspace(Y.min(), Y.max(), 300)
        Xi, Yi = np.meshgrid(xi, yi)
        
        points = np.vstack((Xs.ravel(), Y.ravel())).T
        Vi = griddata(points, V.ravel(), (Xi, Yi), method='linear')
        
        snapshots.append({
            "xi": xi,
            "yi": yi,
            "Vi": Vi
        })
        
    pct_98 = float(np.percentile(all_v, 98))
    
    return {
        "bounds_valid": True,
        "t_samples": t_samples,
        "pct_98": pct_98,
        "snapshots": snapshots
    }