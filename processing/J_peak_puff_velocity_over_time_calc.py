import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import label, gaussian_filter

def compute_peak_puff_velocity_series(frames_list, start_frame, frame_rate, mouth_x):
    """
    Intra-Puff Peak Velocity Tracking Engine
    Maps sequential velocity fields onto a uniform computational mesh, isolates 
    the contiguous core puff using a local dynamic threshold fraction, and extracts 
    the absolute maximum velocity strictly within the puff boundary.
    """
    dt = 1.0 / frame_rate
    n_frames = len(frames_list)
    base_idx = start_frame - 1
    
    F0 = frames_list[base_idx]
    Xs0 = F0["X"] - mouth_x
    Y0 = F0["Y"]
    
    xi = np.linspace(Xs0.min(), Xs0.max(), 300)
    yi = np.linspace(Y0.min(), Y0.max(), 300)
    Xi, Yi = np.meshgrid(xi, yi)
    
    Vpuff_raw = np.full(n_frames - base_idx, np.nan)
    time_base = np.arange(n_frames - base_idx) * dt
    
    connectivity_8 = np.ones((3, 3))
    Vth = 0.15  # Fixed local fractional threshold boundary condition
    
    for idx, f_idx in enumerate(range(base_idx, n_frames)):
        f_data = frames_list[f_idx]
        Xs = f_data["X"].ravel() - mouth_x
        Y = f_data["Y"].ravel()
        V = f_data["Vmag"].ravel()
        
        if V.size == 0:
            continue
            
        points = np.vstack((Xs, Y)).T
        Vi = griddata(points, V, (Xi, Yi), method='linear')
        Vi = np.nan_to_num(Vi, nan=0.0)
        
        Vi_s = gaussian_filter(Vi, sigma=2, truncate=2, mode='nearest')
        thresh = Vth * np.max(Vi_s)
        
        mask = Vi_s > thresh
        labeled, num_features = label(mask, structure=connectivity_8)
        
        if num_features == 0:
            continue
            
        feature_sizes = np.bincount(labeled.ravel())
        feature_sizes[0] = 0
        largest_label = np.argmax(feature_sizes)
        puff_mask = (labeled == largest_label)
        
        if np.any(puff_mask):
            Vpuff_raw[idx] = np.max(Vi_s[puff_mask])
            
    return {
        "time_base": time_base,
        "Vpuff_raw": Vpuff_raw
    }