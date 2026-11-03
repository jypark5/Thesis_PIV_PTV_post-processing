import os
import re
import zipfile
import io
import numpy as np
import pandas as pd

def digest_csv_archive(uploaded_zip, progress_callback=None, min_velocity=0.5):
    """
    Data Digestion Pipeline
    Handles parsing, naming validation, low-velocity thresholding, and Fortran-order 
    grid alignment of physical spatial coordinates and velocity vector fields.
    """
    frames_list = []
    
    with zipfile.ZipFile(uploaded_zip) as z:
        all_files = [f for f in z.namelist() if f.endswith('.csv') and not f.startswith('__MACOSX')]
        all_files = sorted(
            all_files, 
            key=lambda x: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', os.path.basename(x))]
        )
        
        num_files = len(all_files)
        
        for i, filename in enumerate(all_files):
            if progress_callback:
                progress_callback(i, num_files, os.path.basename(filename))
                
            with z.open(filename) as f:
                df = pd.read_csv(f, sep=';')
                df.columns = df.columns.str.strip()
                
                X = df['x [mm]'].to_numpy()
                Y = df['y [mm]'].to_numpy()
                U = df['Velocity u [m/s]'].to_numpy()
                V = df['Velocity v [m/s]'].to_numpy()
                Vmag = df['Velocity |V| [m/s]'].to_numpy()
                vort = df['Vorticity w_z (dv/dx - du/dy) [1/s]'].to_numpy()
                
                xu = np.unique(X)
                yu = np.unique(Y)
                nx = len(xu)
                ny = len(yu)
                expected_grid_size = nx * ny
                
                if len(X) > expected_grid_size:
                    X = X[:expected_grid_size]
                    Y = Y[:expected_grid_size]
                    U = U[:expected_grid_size]
                    V = V[:expected_grid_size]
                    Vmag = Vmag[:expected_grid_size]
                    vort = vort[:expected_grid_size]
                
                # --- Velocity Thresholding ---
                # Identify points below threshold
                low_speed_mask = Vmag < min_velocity
                
                # Mask velocities and vorticity to NaN so grid dimensions stay intact
                U = np.where(low_speed_mask, np.nan, U)
                V = np.where(low_speed_mask, np.nan, V)
                Vmag = np.where(low_speed_mask, np.nan, Vmag)
                vort = np.where(low_speed_mask, np.nan, vort)
                # ------------------------------

                if len(X) == expected_grid_size:
                    # Reshaping matrices requires Fortran order to preserve spatial orientation
                    frame_dict = {
                        "X": X.reshape((ny, nx), order='F'),
                        "Y": Y.reshape((ny, nx), order='F'),
                        "U": U.reshape((ny, nx), order='F'),
                        "V": V.reshape((ny, nx), order='F'),
                        "Vmag": Vmag.reshape((ny, nx), order='F'),
                        "vort": vort.reshape((ny, nx), order='F')
                    }
                else:
                    # Scattered vectors (e.g. PTV) are kept as 1-D arrays
                    frame_dict = {"X": X, "Y": Y, "U": U, "V": V, "Vmag": Vmag, "vort": vort}
                frames_list.append(frame_dict)
                
    return frames_list