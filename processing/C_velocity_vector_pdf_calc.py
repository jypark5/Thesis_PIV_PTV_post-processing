import numpy as np

def precompute_velocity_pdfs(frames_list, start_frame, frame_rate, mouth_x, mouth_y):
    """
    Velocity Spatial PDF Calculation Engine
    Maps physical radial distances relative to the mouth landmark, groups arrays into 
    discrete temporal windows, and computes 3D histogram mesh vertices for PDF visualization.
    """
    window_duration = 0.2
    frames_per_window = int(round(window_duration * frame_rate))

    all_velocities = []
    all_distances = []
    all_frame_idx = []

    for i in range(start_frame - 1, len(frames_list)):
        frame_counter = i - (start_frame - 1) + 1
        f_data = frames_list[i]
        
        X = f_data["X"].ravel()
        Y = f_data["Y"].ravel()
        Vmag = f_data["Vmag"].ravel()
        
        dist_mm = np.sqrt((X - mouth_x)**2 + (Y - mouth_y)**2)
        dist_cm = dist_mm / 10.0
        
        all_velocities.extend(Vmag)
        all_distances.extend(dist_cm)
        all_frame_idx.extend([frame_counter] * len(Vmag))

    all_velocities = np.array(all_velocities)
    all_distances = np.array(all_distances)
    all_frame_idx = np.array(all_frame_idx)

    slice_distances = [10, 20, 30, 40, 50]
    vel_bins = np.arange(0, 10.5, 0.5)
    bar_width = 0.5
    tol = 0.5

    masks = [
        all_frame_idx <= frames_per_window,
        (all_frame_idx > frames_per_window) & (all_frame_idx <= frames_per_window * 2),
        (all_frame_idx > frames_per_window * 2) & (all_frame_idx <= frames_per_window * 3)
    ]

    window_data = []

    for win_idx, mask in enumerate(masks):
        win_vel = all_velocities[mask]
        win_dist = all_distances[mask]
        slices_list = []

        for s_idx, d in enumerate(slice_distances):
            y1 = d - bar_width / 2
            y2 = d + bar_width / 2

            slice_mask = np.abs(win_dist - d) <= tol
            v_slice = win_vel[slice_mask]

            if len(v_slice) == 0:
                continue

            counts, _ = np.histogram(v_slice, bins=vel_bins)
            total_counts = np.sum(counts)
            if total_counts == 0:
                continue
            pdf_vals = counts / total_counts

            mesh_x, mesh_y, mesh_z = [], [], []
            mesh_i, mesh_j, mesh_k = [], [], []
            edge_x, edge_y, edge_z = [], [], []
            v_count = 0

            for v in range(len(vel_bins) - 1):
                zH = float(pdf_vals[v])
                if zH <= 0:
                    continue

                x1 = vel_bins[v]
                x2 = vel_bins[v+1]

                verts = [
                    [x1, y1, 0], [x2, y1, 0], [x2, y2, 0], [x1, y2, 0],
                    [x1, y1, zH], [x2, y1, zH], [x2, y2, zH], [x1, y2, zH]
                ]
                
                for v_pt in verts:
                    mesh_x.append(v_pt[0])
                    mesh_y.append(v_pt[1])
                    mesh_z.append(v_pt[2])

                local_i = [0, 0, 4, 4, 0, 0, 1, 1, 2, 2, 3, 3]
                local_j = [1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 0, 4]
                local_k = [2, 3, 6, 7, 5, 4, 6, 5, 7, 6, 4, 7]

                for idx_f in range(12):
                    mesh_i.append(local_i[idx_f] + v_count)
                    mesh_j.append(local_j[idx_f] + v_count)
                    mesh_k.append(local_k[idx_f] + v_count)

                lines_idx = [0, 1, 2, 3, 0, 4, 5, 6, 7, 4, None, 1, 5, None, 2, 6, None, 3, 7]
                for l_idx in lines_idx:
                    if l_idx is None:
                        edge_x.append(None)
                        edge_y.append(None)
                        edge_z.append(None)
                    else:
                        edge_x.append(verts[l_idx][0])
                        edge_y.append(verts[l_idx][1])
                        edge_z.append(verts[l_idx][2])
                edge_x.append(None)
                edge_y.append(None)
                edge_z.append(None)

                v_count += 8

            slices_list.append({
                "s_idx": s_idx,
                "d": d,
                "y1": y1,
                "y2": y2,
                "mesh_x": mesh_x,
                "mesh_y": mesh_y,
                "mesh_z": mesh_z,
                "mesh_i": mesh_i,
                "mesh_j": mesh_j,
                "mesh_k": mesh_k,
                "edge_x": edge_x,
                "edge_y": edge_y,
                "edge_z": edge_z
            })
            
        window_data.append(slices_list)

    return {
        "window_data": window_data,
        "slice_distances": slice_distances
    }