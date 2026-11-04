import numpy as np
from scipy.spatial import cKDTree

MAX_GAP_MM = 10.0

def remove_outliers(X, Y, U, V, n_neighbours=8, eps=0.1, threshold=2.0):
    """
    Normalised median test (Westerweel & Scarano, 2005) for scattered vectors.
    Returns a boolean mask of vectors to keep: each vector's u and v must agree
    with the median of its nearest neighbours.
    """
    points = np.column_stack((X, Y))
    keep = np.ones(len(points), dtype=bool)
    if len(points) <= n_neighbours:
        return keep

    _, neighbours = cKDTree(points).query(points, k=n_neighbours + 1)
    neighbours = neighbours[:, 1:]

    for comp in (U, V):
        comp_nb = comp[neighbours]
        median_nb = np.median(comp_nb, axis=1)
        residual_nb = np.median(np.abs(comp_nb - median_nb[:, None]), axis=1)
        keep &= np.abs(comp - median_nb) / (residual_nb + eps) <= threshold

    return keep

def mask_gaps(Vi, Xi, Yi, f_data, x_shift=0.0, max_gap=MAX_GAP_MM):
    """
    Blanks interpolated grid points further than max_gap (mm) from every vector
    in a scattered (PTV) frame. Gridded (PIV) frames are returned unchanged.
    """
    if f_data["X"].ndim != 1:
        return Vi

    points = np.column_stack((f_data["X"] - x_shift, f_data["Y"]))
    dist, _ = cKDTree(points).query(np.column_stack((Xi.ravel(), Yi.ravel())), distance_upper_bound=max_gap)
    Vi = np.array(Vi, dtype=float)
    Vi[np.isinf(dist).reshape(Vi.shape)] = np.nan
    return Vi
