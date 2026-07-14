import numpy as np
import plotly.graph_objects as go

def build_peak_puff_velocity_plot(time, raw, smooth, t_max):
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=time, y=raw, 
            mode='lines', 
            line=dict(color='black', dash='dot', width=1.2), 
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
            text="Peak Velocity Inside Puff vs Time (0–0.6 s)", 
            font=dict(family="Times New Roman", size=16, color="black")
        ),
        xaxis=dict(
            title=dict(text="Time since cough start (s)", font=dict(family="Times New Roman", size=14, color="black")), 
            tickfont=dict(family="Times New Roman", size=12, color="black"), 
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True, 
            range=[0, t_max]
        ),
        yaxis=dict(
            title=dict(text="Peak puff velocity (m/s)", font=dict(family="Times New Roman", size=14, color="black")), 
            tickfont=dict(family="Times New Roman", size=12, color="black"), 
            gridcolor="lightgrey", showline=True, linecolor='black', mirror=True, 
            range=[0, np.nanmax(raw) * 1.3 if raw.size > 0 else 1]
        ),
        legend=dict(font=dict(family="Times New Roman", size=12, color="black"), x=0.85, y=0.95, bordercolor="black", borderwidth=1),
        width=900, height=500, margin=dict(l=60, r=30, t=60, b=50), plot_bgcolor="white"
    )
    
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    
    return fig