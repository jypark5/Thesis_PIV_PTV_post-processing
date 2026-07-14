import plotly.graph_objects as go
from plotly.subplots import make_subplots

def build_peak_velocity_time_plot(results):
    time = results["time"]
    PV_raw = results["PV_raw"]
    PV_smooth = results["PV_smooth"]
    peak_vel = results["peak_vel_smooth"]
    peak_time = results["peak_time_smooth"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time,
            y=PV_raw,
            mode='lines',
            line=dict(color='rgb(217, 217, 255)', width=0.8),
            name='Raw PV'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=time,
            y=PV_smooth,
            mode='lines',
            line=dict(color='rgb(0, 0, 255)', width=3.2),
            name='Smoothed'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[peak_time],
            y=[peak_vel],
            mode='markers',
            marker=dict(
                color='rgba(0,0,0,0)',
                size=10,
                line=dict(color='rgb(255, 0, 0)', width=2.5)
            ),
            name='Peak'
        )
    )

    fig.add_annotation(
        x=peak_time,
        y=peak_vel,
        text=f"PV = {peak_vel:.2f} m/s<br>t = {peak_time:.3f} s",
        showarrow=False,
        font=dict(family="Times New Roman", size=15, color="black"),
        xanchor="left",
        yanchor="bottom",
        yshift=10
    )

    fig.update_layout(
        title=dict(
            text="Peak Velocity Time Curve (Ultra-Smooth + Peak Preserved)",
            font=dict(family="Times New Roman", size=18, color="black")
        ),
        xaxis=dict(
            title=dict(
                text="Time (s)",
                font=dict(family="Times New Roman", size=16, color="black")
            ),
            tickfont=dict(family="Times New Roman", size=13, color="black"),
            gridcolor="lightgrey",
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True
        ),
        yaxis=dict(
            title=dict(
                text="Peak Velocity (m/s)",
                font=dict(family="Times New Roman", size=16, color="black")
            ),
            tickfont=dict(family="Times New Roman", size=13, color="black"),
            gridcolor="lightgrey",
            rangemode="tozero",
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True
        ),
        legend=dict(
            font=dict(family="Times New Roman", size=14, color="black"),
            x=0.85,
            y=0.95,
            bordercolor="black",
            borderwidth=1
        ),
        width=900,
        height=500,
        margin=dict(l=60, r=30, t=60, b=50), # <-- THIS FIXES THE CLIPPING
        plot_bgcolor="white"
    )

    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)

    return fig