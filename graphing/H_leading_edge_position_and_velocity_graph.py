import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def build_leading_edge_position_plot(time, raw, smooth, t_max):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time, y=raw, 
            mode='lines', 
            line=dict(color='black', dash='dot', width=1.0), 
            name='raw'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=time, y=smooth, 
            mode='lines', 
            line=dict(color='black', width=2.0), 
            name='smoothed'
        )
    )
    fig.update_layout(
        title=dict(
            text="Leading-edge position (0.4 m/s threshold)", 
            font=dict(family="Times New Roman", size=16, color="black")
        ),
        xaxis=dict(
            title=dict(text="t (s)", font=dict(family="Times New Roman", size=14, color="black")), 
            tickfont=dict(family="Times New Roman", size=12, color="black"), 
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True, 
            range=[0, t_max]
        ),
        yaxis=dict(
            title=dict(text="x_{lead} (m)", font=dict(family="Times New Roman", size=14, color="black")), 
            tickfont=dict(family="Times New Roman", size=12, color="black"), 
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True, 
            range=[0, np.nanmax(smooth) * 1.2 if smooth.size > 0 else 1]
        ),
        legend=dict(font=dict(family="Times New Roman", size=12, color="black"), x=0.85, y=0.05, bordercolor="black", borderwidth=1),
        width=700, height=500, margin=dict(l=60, r=30, t=60, b=50), plot_bgcolor="white"
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig

def build_leading_edge_velocity_plot(time, raw, smooth, t_max):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time, y=raw, 
            mode='lines', 
            line=dict(color='black', dash='dot', width=1.0), 
            name='raw'
        )
    )
    fig.add_trace(
        go.Scatter(
            x=time, y=smooth, 
            mode='lines', 
            line=dict(color='black', width=2.0), 
            name='smoothed'
        )
    )
    fig.update_layout(
        title=dict(
            text="Leading-edge velocity (0.4 m/s threshold)", 
            font=dict(family="Times New Roman", size=16, color="black")
        ),
        xaxis=dict(
            title=dict(text="t (s)", font=dict(family="Times New Roman", size=14, color="black")), 
            tickfont=dict(family="Times New Roman", size=12, color="black"), 
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True, 
            range=[0, t_max]
        ),
        yaxis=dict(
            title=dict(text="V_{lead} (m/s)", font=dict(family="Times New Roman", size=14, color="black")), 
            tickfont=dict(family="Times New Roman", size=12, color="black"), 
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True, 
            range=[0, np.nanmax(smooth) * 1.3 if smooth.size > 0 else 1]
        ),
        legend=dict(font=dict(family="Times New Roman", size=12, color="black"), x=0.85, y=0.95, bordercolor="black", borderwidth=1),
        width=700, height=500, margin=dict(l=60, r=30, t=60, b=50), plot_bgcolor="white"
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    return fig