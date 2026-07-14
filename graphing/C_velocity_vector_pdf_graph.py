import plotly.graph_objects as go
from plotly.subplots import make_subplots

def build_velocity_pdf_3d_plots(results, z_limit):
    window_data = results["window_data"]
    vel_min, vel_max = 0.0, 6.0
    
    colors = [
        'rgb(240, 94, 64)',
        'rgb(250, 199, 92)',
        'rgb(115, 204, 168)',
        'rgb(66, 158, 214)',
        'rgb(89, 89, 97)'
    ]

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'scene'}, {'type': 'scene'}, {'type': 'scene'}]],
        subplot_titles=['0 – 0.2 s', '0.2 – 0.4 s', '0.4 – 0.6 s'],
        horizontal_spacing=0.03
    )

    for win_idx, slices_list in enumerate(window_data):
        col_num = win_idx + 1

        for data in slices_list:
            s_idx = data["s_idx"]
            y1 = data["y1"]
            y2 = data["y2"]

            # Floor baseline indicator plane
            fig.add_trace(
                go.Mesh3d(
                    x=[vel_min, vel_max, vel_max, vel_min],
                    y=[y1, y1, y2, y2],
                    z=[0, 0, 0, 0],
                    i=[0, 0],
                    j=[1, 2],
                    k=[2, 3],
                    color=colors[s_idx],
                    opacity=0.25,
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=1, col=col_num
            )

            if data["mesh_x"]:
                fig.add_trace(
                    go.Mesh3d(
                        x=data["mesh_x"], y=data["mesh_y"], z=data["mesh_z"],
                        i=data["mesh_i"], j=data["mesh_j"], k=data["mesh_k"],
                        color=colors[s_idx],
                        opacity=1.0,
                        lighting=dict(ambient=0.4, diffuse=0.8, roughness=0.5, specular=0.2),
                        showlegend=False
                    ),
                    row=1, col=col_num
                )
                fig.add_trace(
                    go.Scatter3d(
                        x=data["edge_x"], y=data["edge_y"], z=data["edge_z"],
                        mode='lines',
                        line=dict(color='rgb(75, 75, 75)', width=2),
                        showlegend=False,
                        hoverinfo='skip'
                    ),
                    row=1, col=col_num
                )

    scene_config = dict(
        xaxis=dict(title='Velocity Magnitude [m/s]', range=[vel_min, vel_max], backgroundcolor="white", gridcolor="lightgrey", showbackground=True),
        yaxis=dict(title='Radial Distance [cm]', range=[0, 60], backgroundcolor="white", gridcolor="lightgrey", showbackground=True),
        zaxis=dict(title='Probability Density Function (PDF)', range=[0, z_limit], backgroundcolor="white", gridcolor="lightgrey", showbackground=True),
        camera=dict(
            eye=dict(x=1.4, y=-1.4, z=1.1),
            center=dict(x=0, y=0, z=-0.1)
        ),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=0.7)
    )

    fig.update_layout(
        font=dict(family="Times New Roman", size=12),
        width=1500,
        height=650,
        margin=dict(l=20, r=20, t=60, b=20),
        scene1=scene_config,
        scene2=scene_config,
        scene3=scene_config
    )

    return fig