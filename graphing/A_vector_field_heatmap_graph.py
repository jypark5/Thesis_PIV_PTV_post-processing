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

    # Legend-only entry explaining the NaN (uncoloured) regions
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(symbol="square", size=14, color="white", line=dict(color="black", width=1)),
            name="Uncoloured areas contain no measured vectors",
            showlegend=True
        ),
        row=1, col=1
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.12,
            yanchor="top"
        ),
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
        margin=dict(l=60, r=20, t=50, b=90)
    )
    
    fig.update_yaxes(title_text="y [mm]", row=1, col=1)
    fig.update_yaxes(title_text="y [mm]", row=2, col=1)
    fig.update_xaxes(title_text="x [mm]", row=2, col=1)
    fig.update_xaxes(title_text="x [mm]", row=2, col=2)
    fig.update_xaxes(title_text="x [mm]", row=2, col=3)
    
    return fig