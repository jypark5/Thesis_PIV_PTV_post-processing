import streamlit as st
import pandas as pd
import numpy as np
import zipfile
import re
import io

st.set_page_config(
    page_title="Cough PIV Post-Processing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "start_frame" not in st.session_state:
    st.session_state.start_frame = 1
if "mouth_x" not in st.session_state:
    st.session_state.mouth_x = 20
if "mouth_y" not in st.session_state:
    st.session_state.mouth_y = 70
if "frame_rate" not in st.session_state:
    st.session_state.frame_rate = 2000
if "frames_data" not in st.session_state:
    st.session_state.frames_data = None
if "loaded_folder_name" not in st.session_state:
    st.session_state.loaded_folder_name = ""

st.title("Cough PIV Post-Processing Dashboard")
st.subheader("Data Input and Configuration")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Experimental Parameters")
    st.session_state.start_frame = st.number_input(
        "Cough Start Frame Index (t=0)", 
        min_value=1, 
        value=st.session_state.start_frame, 
        step=1
    )
    st.session_state.frame_rate = st.number_input(
        "Frame Rate (Hz)", 
        min_value=1, 
        value=st.session_state.frame_rate, 
        step=100
    )
    dt = 1.0 / st.session_state.frame_rate
    st.caption(f"Calculated dt: {dt:.6f} seconds")

with col2:
    st.markdown("### Mouth Landmarks (mm)")
    st.session_state.mouth_x = st.number_input(
        "Mouth X position", 
        value=st.session_state.mouth_x, 
        step=1
    )
    st.session_state.mouth_y = st.number_input(
        "Mouth Y position", 
        value=st.session_state.mouth_y, 
        step=1
    )

st.markdown("---")
st.markdown("### Zip Archive Upload")

uploaded_zip = st.file_uploader(
    "Select or drop a compressed .zip folder containing your DaVis CSV files", 
    type=["zip"]
)

def extract_file_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

if uploaded_zip is not None:
    if st.button("Process Compressed Archive"):
        frames_list = []
        with zipfile.ZipFile(uploaded_zip) as z:
            all_files = [f for f in z.namelist() if f.endswith('.csv') and not f.startswith('__MACOSX')]
            
            import os
            all_files = sorted(all_files, key=lambda x: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', os.path.basename(x))])
            
            num_files = len(all_files)
            progress_bar = st.progress(0)
            status_text = st.empty()
            try:
                for i, filename in enumerate(all_files):
                    status_text.text(f"Extracting frame {i+1} of {num_files} ({os.path.basename(filename)})...")
                    with z.open(filename) as f:
                        df = pd.read_csv(f, sep=';')
                        X = df.iloc[:, 0].to_numpy()
                        Y = df.iloc[:, 1].to_numpy()
                        U = df.iloc[:, 2].to_numpy()
                        V = df.iloc[:, 3].to_numpy()
                        Vmag = df.iloc[:, 4].to_numpy()
                        vort = df.iloc[:, 5].to_numpy()
                        
                        xu = np.unique(X)
                        yu = np.unique(Y)
                        nx = len(xu)
                        ny = len(yu)
                        expected = nx * ny
                        
                        if len(X) > expected:
                            X = X[:expected]
                            Y = Y[:expected]
                            U = U[:expected]
                            V = V[:expected]
                            Vmag = Vmag[:expected]
                            vort = vort[:expected]
                        
                        frame_dict = {
                            "X": X.reshape((ny, nx), order='F'),
                            "Y": Y.reshape((ny, nx), order='F'),
                            "U": U.reshape((ny, nx), order='F'),
                            "V": V.reshape((ny, nx), order='F'),
                            "Vmag": Vmag.reshape((ny, nx), order='F'),
                            "vort": vort.reshape((ny, nx), order='F')
                        }
                        frames_list.append(frame_dict)
                        progress_bar.progress((i + 1) / num_files)
                
                st.session_state.frames_data = frames_list
                st.session_state.loaded_folder_name = uploaded_zip.name
                status_text.empty()
                st.success(f"Successfully processed {num_files} frames from archive.")
            except Exception as e:
                st.error(f"Error parsing zip file: {e}")

st.markdown("---")
st.subheader("Current Session Configuration Status")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Loaded Data Status", value=st.session_state.loaded_folder_name if st.session_state.loaded_folder_name else "No Data Loaded")
with col2:
    st.metric(label="Start Frame Index", value=st.session_state.start_frame)
with col3:
    st.metric(label="Mouth Target (X, Y)", value=f"({st.session_state.mouth_x}, {st.session_state.mouth_y}) mm")