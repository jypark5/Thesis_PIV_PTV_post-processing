import streamlit as st
from processing.data_digestion import digest_csv_archive
from processing.A_vector_field_heatmap_calc import precompute_time_series_heatmaps
from processing.B_vorticity_field_over_time_calc import precompute_vorticity_maps
from processing.C_velocity_vector_pdf_calc import precompute_velocity_pdfs
from processing.D_directional_pdf_calc import compute_directional_pdf
from processing.E_peak_velocity_over_time_calc import compute_peak_velocity_series
from processing.F_sliced_velocity_over_time_calc import precompute_sliced_velocity
from processing.G_puff_characteristics_boundary_radius_and_trajectory_calc import compute_puff_kinematics
from processing.H_leading_edge_position_and_velocity_calc import compute_leading_edge_data
from processing.I_spread_angle_calc import compute_spread_angle
from processing.J_peak_puff_velocity_over_time_calc import compute_peak_puff_velocity_series

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

# Precomputed Pipeline Cache
if "heatmap_results" not in st.session_state:
    st.session_state.heatmap_results = None
if "vorticity_results" not in st.session_state:
    st.session_state.vorticity_results = None
if "velocity_pdf_results" not in st.session_state:
    st.session_state.velocity_pdf_results = None
if "directional_pdf_results" not in st.session_state:
    st.session_state.directional_pdf_results = None
if "peak_velocity_series_results" not in st.session_state:
    st.session_state.peak_velocity_series_results = None
if "sliced_velocity_results" not in st.session_state:
    st.session_state.sliced_velocity_results = None
if "puff_kinematics_results" not in st.session_state:
    st.session_state.puff_kinematics_results = None
if "leading_edge_results" not in st.session_state:
    st.session_state.leading_edge_results = None
if "spread_angle_results" not in st.session_state:
    st.session_state.spread_angle_results = None
if "peak_puff_velocity_results" not in st.session_state:
    st.session_state.peak_puff_velocity_results = None

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

if uploaded_zip is not None:
    if st.button("Process Compressed Archive"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def update_ui_progress(current, total, file_name):
            progress_bar.progress((current + 1) / total)
            status_text.text(f"Extracting frame {current+1} of {total} ({file_name})...")

        try:
            # Data Ingestion
            processed_frames = digest_csv_archive(uploaded_zip, progress_callback=update_ui_progress)
            st.session_state.frames_data = processed_frames
            st.session_state.loaded_folder_name = uploaded_zip.name
            
            # Step A
            status_text.text("Step A")
            st.session_state.heatmap_results = precompute_time_series_heatmaps(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate, st.session_state.mouth_x
            )
            
            # Step B
            status_text.text("Step B")
            st.session_state.vorticity_results = precompute_vorticity_maps(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate, st.session_state.mouth_x
            )
            
            # Step C
            status_text.text("Step C")
            st.session_state.velocity_pdf_results = precompute_velocity_pdfs(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate, st.session_state.mouth_x, st.session_state.mouth_y
            )
            
            # Step D
            status_text.text("Step D")
            st.session_state.directional_pdf_results = compute_directional_pdf(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate
            )
            
            # Step E
            status_text.text("Step E")
            st.session_state.peak_velocity_series_results = compute_peak_velocity_series(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate
            )
            
            # Step F
            status_text.text("Step F")
            st.session_state.sliced_velocity_results = precompute_sliced_velocity(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate, st.session_state.mouth_x
            )
            
            # Step G
            status_text.text("Step G")
            st.session_state.puff_kinematics_results = compute_puff_kinematics(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate, st.session_state.mouth_x, st.session_state.mouth_y
            )
            
            # Step H
            status_text.text("Step H")
            st.session_state.leading_edge_results = compute_leading_edge_data(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate, st.session_state.mouth_x
            )
            
            # Step I
            status_text.text("Step I")
            st.session_state.spread_angle_results = compute_spread_angle(
                processed_frames, st.session_state.mouth_x, st.session_state.mouth_y
            )
            
            # Step J
            status_text.text("Step J")
            st.session_state.peak_puff_velocity_results = compute_peak_puff_velocity_series(
                processed_frames, st.session_state.start_frame, st.session_state.frame_rate, st.session_state.mouth_x
            )
            
            status_text.empty()
            progress_bar.empty()
            st.success("All pipelines cached successfully!")
            
        except Exception as e:
            st.error(f"Error executing pipeline modules: {e}")

st.markdown("---")
st.subheader("Current Session Configuration Status")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Loaded Data Status", 
        value=st.session_state.loaded_folder_name if st.session_state.loaded_folder_name else "No Data Loaded"
    )
with col2:
    st.metric(label="Start Frame Index", value=st.session_state.start_frame)
with col3:
    st.metric(
        label="Mouth Target (X, Y)", 
        value=f"({st.session_state.mouth_x}, {st.session_state.mouth_y}) mm"
    )