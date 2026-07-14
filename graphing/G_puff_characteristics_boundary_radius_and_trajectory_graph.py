import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def build_puff_boundary_contour(xi, yi, Vi_p, mask_p, frame_plot):
    fig_heat = go.Figure()
    fig_heat.add_trace(
        go.Heatmap(
            x=xi, y=yi, z=np.nan_to_num(Vi_p, nan=0.0),
            colorscale='Turbo',
            colorbar=dict(title=dict(text="Velocity Magnitude [m/s]", side="right"))
        )
    )
    fig_heat.add_trace(
        go.Contour(
            x=xi, y=yi, z=mask_p.astype(float),
            contours_type='constraint',
            contours_operation='=',
            contours_value=0.5,
            line_color='white',
            line_width=2,
            showlegend=False,
            hoverinfo='skip'
        )
    )
    fig_heat.update_layout(
        title=dict(text=f"Puff Boundary tracking at Frame {frame_plot}", font=dict(family="Times New Roman", size=16, color="black")),
        xaxis=dict(
            title=dict(text="x (mm)", font=dict(family="Times New Roman", size=14, color="black")),
            tickfont=dict(family="Times New Roman", size=12, color="black"),
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True
        ),
        yaxis=dict(
            title=dict(text="y (mm)", font=dict(family="Times New Roman", size=14, color="black")),
            tickfont=dict(family="Times New Roman", size=12, color="black"),
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True
        ),
        width=800, height=500, margin=dict(l=60, r=30, t=60, b=50), plot_bgcolor="white"
    )
    fig_heat.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig_heat.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig_heat

def build_puff_kinematics_charts(t_val, tx_val, tx_smooth, tr_val, tr_smooth, r_val, r_smooth, title_suffix, y_label):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_val, y=tx_val/1000.0, mode='lines', line=dict(color='grey', dash='dot'), name='raw'))
    fig.add_trace(go.Scatter(x=t_val, y=tx_smooth/1000.0, mode='lines', line=dict(color='black', width=2), name='smoothed'))
    fig.update_layout(
        title=dict(text=title_suffix, font=dict(family="Times New Roman", size=14, color="black")),
        xaxis=dict(
            title=dict(text="t (s)", font=dict(family="Times New Roman", size=12, color="black")),
            tickfont=dict(family="Times New Roman", size=11, color="black"),
            gridcolor="lightgrey", showline=True, linecolor="black", mirror=True
        ),
        yaxis=dict(
            title=dict(text=y_label, font=dict(family="Times New Roman", size=12, color="black")),
            tickfont=dict(family="Times New Roman", size=11, color="black"),
            gridcolor="lightgrey", showline=True, linecolor="black", mirror=True
        ),
        margin=dict(l=60, r=30, t=60, b=50), plot_bgcolor="white", font=dict(family="Times New Roman", color="black"),
        legend=dict(x=0.05, y=0.95, bordercolor="black", borderwidth=1)
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig

def build_puff_noise_diagnostic_charts(tb_val, noise_val, noise_smooth, title, y_label):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tb_val, y=noise_val, mode='lines', line=dict(color='grey', dash='dot'), name='raw'))
    fig.add_trace(go.Scatter(x=tb_val, y=noise_smooth, mode='lines', line=dict(color='black', width=2), name='smoothed'))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Times New Roman", size=14, color="black")),
        xaxis=dict(
            title=dict(text="Time since cough start (s)", font=dict(family="Times New Roman", size=12, color="black")),
            tickfont=dict(family="Times New Roman", size=11, color="black"),
            gridcolor="lightgrey", showline=True, linecolor="black", mirror=True
        ),
        yaxis=dict(
            title=dict(text=y_label, font=dict(family="Times New Roman", size=12, color="black")),
            tickfont=dict(family="Times New Roman", size=11, color="black"),
            gridcolor="lightgrey", showline=True, linecolor="black", mirror=True
        ),
        margin=dict(l=60, r=30, t=60, b=50), plot_bgcolor="white", font=dict(family="Times New Roman", color="black"),
        legend=dict(x=0.8, y=0.95, bordercolor="black", borderwidth=1)
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig

def build_puff_morphology_scaling_chart(s_sorted, r_sorted, r_sorted_smooth):
    fig_morph = go.Figure()
    fig_morph.add_trace(
        go.Scatter(
            x=s_sorted, y=r_sorted,
            mode='markers',
            marker=dict(size=5, color='rgba(192, 192, 192, 0.45)'),
            name='Raw data'
        )
    )
    fig_morph.add_trace(
        go.Scatter(
            x=s_sorted, y=r_sorted_smooth,
            mode='lines',
            line=dict(color='black', width=2.3),
            name='Smoothed trend'
        )
    )
    fig_morph.update_layout(
        title=dict(text="Puff Half-Width vs Axial Distance", font=dict(family="Times New Roman", size=16, color="black")),
        xaxis=dict(
            title=dict(text="s (cm) – Axial puff trajectory", font=dict(family="Times New Roman", size=14, color="black")),
            tickfont=dict(family="Times New Roman", size=12, color="black"),
            range=[0, np.max(s_sorted)*1.05] if s_sorted.size > 0 else None,
            gridcolor="lightgrey", showline=True, linecolor="black", mirror=True
        ),
        yaxis=dict(
            title=dict(text="r (cm) – Puff half-width", font=dict(family="Times New Roman", size=14, color="black")),
            tickfont=dict(family="Times New Roman", size=12, color="black"),
            range=[0, np.max(r_sorted)*1.2] if r_sorted.size > 0 else None,
            gridcolor="lightgrey", showline=True, linecolor="black", mirror=True
        ),
        width=900, height=500, margin=dict(l=60, r=30, t=60, b=50), plot_bgcolor="white", font=dict(family="Times New Roman", color="black"),
        legend=dict(x=0.05, y=0.95, bordercolor="black", borderwidth=1)
    )
    fig_morph.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig_morph.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig_morph