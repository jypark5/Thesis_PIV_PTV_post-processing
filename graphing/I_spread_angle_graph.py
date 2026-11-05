import numpy as np
import plotly.graph_objects as go

def build_puff_spread_angle_plot(results, mouth_y):
    xi_shifted = results["xi_shifted"]
    yi = results["yi"]
    Vi_s = results["Vi_s"]
    x_b_shifted = results["x_b_shifted"]
    y_b = results["y_b"]
    xRay = results["xRay"]
    yRayU = results["yRayU"]
    yRayL = results["yRayL"]
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Heatmap(
            x=xi_shifted, y=yi, z=np.nan_to_num(Vi_s, nan=0.0),
            colorscale='Turbo',
            colorbar=dict(title=dict(text="Velocity Magnitude [m/s]", side="right"))
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=x_b_shifted, y=y_b,
            mode='markers',
            marker=dict(size=4, color='black'),
            name='Puff Boundary',
            showlegend=False
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=xRay, y=yRayU,
            mode='lines',
            line=dict(color='white', width=3.0),
            name='Upper Fit Branch',
            showlegend=False
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=xRay, y=yRayL,
            mode='lines',
            line=dict(color='white', width=3.0),
            name='Lower Fit Branch',
            showlegend=False
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=[0], y=[mouth_y],
            mode='markers+text',
            marker=dict(color='white', size=10, line=dict(color='black', width=1)),
            name='Mouth Point',
            showlegend=True
        )
    )
    
    xA = 80.0
    idx_labels = np.argmin(np.abs(xRay - xA))
    
    fig.add_annotation(
        x=xA, y=yRayU[idx_labels], text=f"{results['angleU']:.1f}°",
        showarrow=True, arrowcolor="white", arrowsize=1, yshift=15,
        font=dict(family="Times New Roman", size=15, color="white")
    )
    
    fig.add_annotation(
        x=xA, y=yRayL[idx_labels], text=f"{results['angleL']:.1f}°",
        showarrow=True, arrowcolor="white", arrowsize=1, yshift=-15,
        font=dict(family="Times New Roman", size=15, color="white")
    )
    
    fig.update_layout(
        title=dict(
            text=f"Spread Angle at Peak Velocity (Frame {results['peak_frame']})",
            font=dict(family="Times New Roman", size=16, color="black")
        ),
        xaxis=dict(
            title=dict(text="x from mouth (mm)", font=dict(family="Times New Roman", size=14, color="black")),
            tickfont=dict(family="Times New Roman", size=12, color="black"),
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True,
            range=[0, np.max(xi_shifted)]
        ),
        yaxis=dict(
            title=dict(text="y (mm)", font=dict(family="Times New Roman", size=14, color="black")),
            tickfont=dict(family="Times New Roman", size=12, color="black"),
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True,
            range=[np.min(yi), np.max(yi)]
        ),
        legend=dict(
            x=0.02,               # 2% from the left
            y=0.98,               # 98% from the bottom (top-left)
            bgcolor="rgba(255, 255, 255, 0.8)", # Transparent white background
            bordercolor="black",
            borderwidth=1
        ),
        width=800, height=500, margin=dict(l=60, r=30, t=60, b=50), plot_bgcolor="white"
    )
    
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    
    return fig