import numpy as np

def precompute_sliced_velocity(frames_list, start_frame, frame_rate, mouth_x):
    """
    Downstream Velocity Slicing Engine
    Extracts spatial profiles at physical milestones along the jet axis,
    averaging local velocity magnitude fields within fixed spatial tolerances.
    """
    dt = 1.0 / frame_rate
    n_frames = len(frames_list)
    
    # Precomputes a standard bank from 10mm to 500mm to eliminate sub-page loop lag
    target_distances = np.arange(10, 510, 10)
    tol = 3.0
    
    time_base = (np.arange(n_frames) - (start_frame - 1)) * dt
    storage = {float(d): np.zeros(n_frames) for d in target_distances}
    
    for f_idx, f_data in enumerate(frames_list):
        X = f_data["X"]
        Vmag = f_data["Vmag"]
        
        for d in target_distances:
            x_target = mouth_x + d
            mask = np.abs(X - x_target) <= tol
            vals = Vmag[mask]
            
            if vals.size > 0:
                storage[float(d)][f_idx] = np.nanmean(vals)
            else:
                storage[float(d)][f_idx] = 0.0
                
    return {
        "time_base": time_base,
        "sliced_data": storage
    }