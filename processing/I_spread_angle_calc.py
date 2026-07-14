import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter, label
from skimage.measure import find_contours

def compute_spread_angle(frames_list, mouth_x, mouth_y):
    peak_velocities = [np.max(f["Vmag"]) for f in frames_list]
    peak_frame_idx = int(np.argmax(peak_velocities))
    F = frames_list[peak_frame_idx]
    X, Y, V = F["X"], F["Y"], F["Vmag"]

    xi = np.linspace(X.min(), X.max(), 300)
    yi = np.linspace(Y.min(), Y.max(), 200)
    Xi, Yi = np.meshgrid(xi, yi)

    points = np.vstack((X.ravel(), Y.ravel())).T
    values = V.ravel()

    Vi = griddata(points, values, (Xi, Yi), method='cubic')
    nanMask = np.isnan(Vi)
    if np.any(nanMask):
        Vi_lin = griddata(points, values, (Xi, Yi), method='linear')
        Vi[nanMask] = Vi_lin[nanMask]

    Vi_zeroed = np.nan_to_num(Vi, nan=0.0)
    Vi_s = gaussian_filter(Vi_zeroed, sigma=2)

    thresh = 0.15 * np.max(Vi_s)
    mask = Vi_s > thresh

    labeled, num_features = label(mask, structure=np.ones((3, 3)))
    if num_features == 0:
        return {"bounds_valid": False}
    sizes = np.bincount(labeled.ravel())
    sizes[0] = 0
    mask2 = (labeled == np.argmax(sizes))

    contours = find_contours(mask2.astype(float), 0.5)
    if not contours:
        return {"bounds_valid": False}
    bd = max(contours, key=len)

    rows = np.round(bd[:, 0]).astype(int)
    cols = np.round(bd[:, 1]).astype(int)
    rows = np.clip(rows, 0, len(yi) - 1)
    cols = np.clip(cols, 0, len(xi) - 1)

    x_b = xi[cols]
    y_b = yi[rows]

    x_rel = x_b - mouth_x
    down = x_rel > 0
    upper = down & (y_b >= mouth_y)
    lower = down & (y_b < mouth_y)

    xU, yU = x_rel[upper], y_b[upper]
    xL, yL = x_rel[lower], y_b[lower]

    if len(xU) == 0 or len(xL) == 0:
        return {"bounds_valid": False}

    binW = 1.0

    xU_round = np.round(xU / binW) * binW
    xUbin, iu = np.unique(xU_round, return_inverse=True)
    yUenv = np.full(len(xUbin), -np.inf)
    np.maximum.at(yUenv, iu, yU)

    xL_round = np.round(xL / binW) * binW
    xLbin, il = np.unique(xL_round, return_inverse=True)
    yLenv = np.full(len(xLbin), np.inf)
    np.minimum.at(yLenv, il, yL)

    iUs = np.argsort(xUbin)
    xUbin = xUbin[iUs]
    yUenv = yUenv[iUs]

    iLs = np.argsort(xLbin)
    xLbin = xLbin[iLs]
    yLenv = yLenv[iLs]

    fitMax = 120.0
    uMask = (xUbin > 0) & (xUbin < fitMax)
    lMask = (xLbin > 0) & (xLbin < fitMax)

    if np.sum(uMask) < 2 or np.sum(lMask) < 2:
        return {"bounds_valid": False}

    pU = np.polyfit(xUbin[uMask], yUenv[uMask], 1)
    pL = np.polyfit(xLbin[lMask], yLenv[lMask], 1)

    mU, mL = pU[0], pL[0]

    angleU = float(np.degrees(np.arctan(mU)))
    angleL = float(np.degrees(np.arctan(np.abs(mL))))
    spreadAngle = angleU + angleL

    xRay = np.linspace(0, np.max(x_rel), 300)
    yRayU = mouth_y + mU * xRay
    yRayL = mouth_y + mL * xRay

    return {
        "bounds_valid": True,
        "peak_frame": peak_frame_idx + 1,
        "xi_shifted": xi - mouth_x,
        "yi": yi,
        "Vi_s": Vi_s,
        "x_b_shifted": x_b - mouth_x,
        "y_b": y_b,
        "xRay": xRay,
        "yRayU": yRayU,
        "yRayL": yRayL,
        "angleU": angleU,
        "angleL": angleL,
        "spreadAngle": spreadAngle
    }