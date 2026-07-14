import plotly.graph_objects as go
from plotly.subplots import make_subplots

def build_time_series_heatmap_grid(results, cmax):
    t_samples = results["t_samples"]
    snapshots = results["snapshots"]
    
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=[f"t = {t:.1f} s" for t in t_samples],
        shared_xaxes=True,
        shared_yaxes=True,
        horizontal_spacing=0.02,
        vertical_spacing=0.07
    )
    
    for n, snap in enumerate(snapshots):
        row = (n // 3) + 1
        col = (n % 3) + 1
        
        fig.add_trace(
            go.Heatmap(
                x=snap["xi"],
                y=snap["yi"],
                z=snap["Vi"],
                coloraxis="coloraxis"
            ),
            row=row, col=col
        )
        
    fig.update_layout(
        coloraxis=dict(
            colorscale='Turbo',
            cmin=0,
            cmax=cmax,
            colorbar=dict(
                title=dict(
                    text="Velocity magnitude [m/s]",
                    side="right"
                ),
                thickness=20
            )
        ),
        font=dict(
            family="Times New Roman",
            size=12
        ),
        width=1200,
        height=700,
        margin=dict(l=60, r=20, t=50, b=50)
    )
    
    fig.update_yaxes(title_text="y [mm]", row=1, col=1)
    fig.update_yaxes(title_text="y [mm]", row=2, col=1)
    fig.update_xaxes(title_text="x [mm]", row=2, col=1)
    fig.update_xaxes(title_text="x [mm]", row=2, col=2)
    fig.update_xaxes(title_text="x [mm]", row=2, col=3)
    
    return fig