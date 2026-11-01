import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import label

def compute_leading_edge_data(frames_list, start_frame, frame_rate, mouth_x):
    """
    Leading Edge Position and Velocity Tracking Engine
    Maps sequential velocity fields onto a uniform computational mesh, filters the
    domain using a physical threshold, isolates the main puff structure, and tracks
    the downstream 95th percentile spatial boundary.
    """
    dt = 1.0 / frame_rate
    n_frames = len(frames_list)
    base_idx = start_frame - 1
    
    F0 = frames_list[base_idx]
    Xs0 = F0["X"] - mouth_x
    Y0 = F0["Y"]
    
    xi = np.linspace(Xs0.min(), Xs0.max(), 280)
    yi = np.linspace(Y0.min(), Y0.max(), 220)
    Xi, Yi = np.meshgrid(xi, yi)
    
    xLead_mm_raw = np.full(n_frames - base_idx, np.nan)
    time_base = np.arange(n_frames - base_idx) * dt
    
    connectivity_8 = np.ones((3, 3))
    V_thr = 0.40  # Constant threshold boundary condition (m/s)
    
    for idx, f_idx in enumerate(range(base_idx, n_frames)):
        f_data = frames_list[f_idx]
        Xs = f_data["X"].ravel() - mouth_x
        Y = f_data["Y"].ravel()
        V = f_data["Vmag"].ravel()
        
        points = np.vstack((Xs, Y)).T
        Vi = griddata(points, V, (Xi, Yi), method='linear')
        Vi = np.nan_to_num(Vi, nan=0.0)
        
        mask = Vi > V_thr
        labeled, num_features = label(mask, structure=connectivity_8)
        
        if num_features == 0:
            continue
            
        feature_sizes = np.bincount(labeled.ravel())
        feature_sizes[0] = 0
        largest_label = np.argmax(feature_sizes)
        puff_mask = (labeled == largest_label)
        
        x_vals = Xi[puff_mask]
        if x_vals.size > 0:
            xLead_mm_raw[idx] = np.percentile(x_vals, 95, method='hazen')
            
    return {
        "time_base": time_base,
        "xLead_mm_raw": xLead_mm_raw
    }