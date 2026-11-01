import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import (
    label, binary_dilation, binary_erosion, binary_fill_holes,
    distance_transform_edt
)

def compute_puff_kinematics(frames_list, start_frame, frame_rate, mouth_x_mm, mouth_y_mm):
    """
    Puff Morphology and Kinematics Tracking Engine
    Processes sequential velocity fields via localized adaptive thresholding,
    isolates the primary puff structural mass via morphological operations,
    and resolves center-of-mass trajectory coordinates and expansion scales.
    """
    dt = 1.0 / frame_rate
    n_frames = len(frames_list)
    frame_idx = np.arange(start_frame - 1, n_frames)
    n_use = len(frame_idx)
    time_vec = (frame_idx - (start_frame - 1)) * dt

    all_xs = []
    for k in frame_idx:
        all_xs.extend(frames_list[k]["X"].ravel() - mouth_x_mm)
    xmax_global = np.max(all_xs)

    y0 = frames_list[start_frame - 1]["Y"]
    ymin, ymax = np.min(y0), np.max(y0)

    xi = np.linspace(0, xmax_global, 400)
    yi = np.linspace(ymin, ymax, 300)
    Xi, Yi = np.meshgrid(xi, yi)
    dx_i = xi[1] - xi[0]
    dy_i = yi[1] - yi[0]
    pixel_size_mm = np.mean([abs(dx_i), abs(dy_i)])

    center_x = np.full(n_use, np.nan)
    center_y = np.full(n_use, np.nan)
    traj_x = np.full(n_use, np.nan)
    traj_r = np.full(n_use, np.nan)
    radius_mm = np.full(n_use, np.nan)
    background_noise = np.full(n_use, np.nan)
    background_std = np.full(n_use, np.nan)
    mask_area = np.zeros(n_use)

    disk_element = np.array([
        [0, 0, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 0]
    ], dtype=bool)
    
    connectivity_8 = np.ones((3, 3))

    for ii, f in enumerate(frame_idx):
        f_data = frames_list[f]
        X = f_data["X"].ravel() - mouth_x_mm
        Y = f_data["Y"].ravel()
        V = f_data["Vmag"].ravel()

        points = np.vstack((X, Y)).T
        Vi = griddata(points, V, (Xi, Yi), method='linear')
        
        v_max_local = np.nanmax(Vi) if not np.all(np.isnan(Vi)) else 0.0
        v_thr = 0.40 * v_max_local
        
        mask = np.zeros_like(Vi, dtype=bool)
        mask[~np.isnan(Vi)] = Vi[~np.isnan(Vi)] > v_thr

        labeled_mask, num_features = label(mask, structure=connectivity_8)
        if num_features > 0:
            feature_sizes = np.bincount(labeled_mask.ravel())
            small_objects = feature_sizes < 40
            mask[small_objects[labeled_mask]] = False

        # border_value=1 keeps the frame edge from eroding the mask, matching MATLAB imclose
        mask = binary_erosion(binary_dilation(mask, structure=disk_element), structure=disk_element, border_value=1)
        mask = binary_fill_holes(mask)
        mask_area[ii] = np.count_nonzero(mask)

        labeled_mask, num_features = label(mask, structure=connectivity_8)
        if num_features == 0:
            continue

        feature_sizes = np.bincount(labeled_mask.ravel())
        feature_sizes[0] = 0
        largest_label = np.argmax(feature_sizes)
        puff_mask = (labeled_mask == largest_label)

        background_mask = ~puff_mask
        background_vals = Vi[background_mask]
        background_vals = background_vals[~np.isnan(background_vals)]
        background_vals = background_vals[background_vals > 0]
        
        if background_vals.size > 0:
            background_noise[ii] = np.mean(background_vals)
            background_std[ii] = np.std(background_vals, ddof=1)

        D = distance_transform_edt(puff_mask)
        idx_max = np.argmax(D)
        row_c, col_c = np.unravel_index(idx_max, D.shape)
        
        xc = xi[col_c]
        yc = yi[row_c]
        
        center_x[ii] = xc
        center_y[ii] = yc
        radius_mm[ii] = D[row_c, col_c] * pixel_size_mm

        dx_c = xc
        dy_c = yc - mouth_y_mm
        traj_x[ii] = dx_c
        traj_r[ii] = np.hypot(dx_c, dy_c)

    return {
        "time_vec": time_vec,
        "center_x": center_x,
        "center_y": center_y,
        "traj_x": traj_x,
        "traj_r": traj_r,
        "radius_mm": radius_mm,
        "background_noise": background_noise,
        "background_std": background_std,
        "mask_area": mask_area,
        "xi": xi,
        "yi": yi,
        "Xi": Xi,
        "Yi": Yi,
        "disk_element": disk_element,
        "connectivity_8": connectivity_8
    }