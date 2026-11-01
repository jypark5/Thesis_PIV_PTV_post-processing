import numpy as np

def compute_directional_pdf(frames_list, start_frame, frame_rate):
    """
    Directional Probability Density Function Engine
    Segments velocity components into distinct time windows, isolates forward jet momentum 
    above a noise threshold, and computes angular probability densities via polar histograms.
    """
    dt = 1.0 / frame_rate
    t_starts = [0.0, 0.2, 0.4]
    t_ends = [0.2, 0.4, 0.6]
    n_win = 3

    bounds_valid = True
    for w in range(n_win):
        f_start = (start_frame - 1) + int(round(t_starts[w] / dt))
        f_end = (start_frame - 1) + int(round(t_ends[w] / dt))
        if f_start < 0 or f_end >= len(frames_list):
            bounds_valid = False

    if not bounds_valid:
        return {"bounds_valid": False}

    window_results = []
    n_bins = 18
    edges = np.linspace(-np.pi, np.pi, n_bins + 1)

    for w in range(n_win):
        f_start = (start_frame - 1) + int(round(t_starts[w] / dt))
        f_end = (start_frame - 1) + int(round(t_ends[w] / dt))
        all_theta = []

        for f_idx in range(f_start, f_end + 1):
            f_data = frames_list[f_idx]
            U = -f_data["U"].ravel()
            V = f_data["V"].ravel()

            mag = np.sqrt(U**2 + V**2)
            pct_40 = np.nanpercentile(mag, 40, method='hazen')
            good = mag > pct_40

            U_good = U[good]
            V_good = V[good]

            theta = np.arctan2(V_good, U_good)
            all_theta.extend(theta)

        all_theta = np.array(all_theta)

        if len(all_theta) == 0:
            return {"bounds_valid": True, "error_window": f"{t_starts[w]:.1f}–{t_ends[w]:.1f} s"}

        counts, _ = np.histogram(all_theta, bins=edges, density=True)
        bin_centers_rad = (edges[:-1] + edges[1:]) / 2
        bin_centers_deg = (np.degrees(bin_centers_rad)) % 360

        window_results.append({
            "counts": counts,
            "bin_centers_deg": bin_centers_deg
        })

    return {
        "bounds_valid": True,
        "t_starts": t_starts,
        "t_ends": t_ends,
        "window_results": window_results,
        "n_bins": n_bins
    }