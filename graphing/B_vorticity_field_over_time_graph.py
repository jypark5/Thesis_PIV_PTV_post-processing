import plotly.graph_objects as go
from plotly.subplots import make_subplots

def build_vorticity_time_series_grid(results, clim_val, selected_times):
    snapshots = results["snapshots"]
    valid_times = [t for t in selected_times if t in snapshots]
    nT = len(valid_times)
    
    if nT == 0:
        return go.Figure()
        
    custom_redblue = [
        [0.0, 'rgb(0, 0, 230)'],
        [0.25, 'rgb(77, 153, 255)'],
        [0.5, 'rgb(255, 255, 255)'],
        [0.75, 'rgb(255, 153, 77)'],
        [1.0, 'rgb(230, 0, 0)']
    ]

    fig = make_subplots(
        rows=1, cols=nT,
        subplot_titles=[f"t = {t:.1f} s" for t in valid_times],
        shared_yaxes=True,
        horizontal_spacing=0.02
    )

    for n, t in enumerate(valid_times):
        col = n + 1
        snap = snapshots[t]
        
        fig.add_trace(
            go.Heatmap(
                x=snap["xi"],
                y=snap["yi"],
                z=snap["W_smooth"],
                coloraxis="coloraxis"
            ),
            row=1, col=col
        )

    fig.update_layout(
        coloraxis=dict(
            colorscale=custom_redblue,
            cmin=-clim_val,
            cmax=clim_val,
            colorbar=dict(
                title=dict(
                    text="Vorticity ω_z [1/s]",
                    side="top"
                ),
                orientation="h",
                x=0.5,
                xanchor="center",
                y=1.22,
                yanchor="top",
                thickness=18,
                len=0.35
            )
        ),
        font=dict(
            family="Times New Roman",
            size=12
        ),
        width=1400,
        height=550,
        margin=dict(l=60, r=40, t=120, b=60)
    )

    fig.update_yaxes(title_text="y (mm)", row=1, col=1)
    for col in range(1, nT + 1):
        fig.update_xaxes(title_text="x (mm)", row=1, col=col)
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, row=1, col=col)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, row=1, col=col)

    return fig