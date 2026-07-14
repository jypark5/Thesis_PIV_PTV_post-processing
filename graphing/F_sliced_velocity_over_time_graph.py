import plotly.graph_objects as go
from plotly.subplots import make_subplots

def build_sliced_velocity_trace_plot(time, traces, r_list):
    fig = go.Figure()
    
    plotly_colors = [
        'rgb(31, 119, 180)',
        'rgb(255, 127, 14)',
        'rgb(44, 160, 44)',
        'rgb(214, 39, 40)',
        'rgb(148, 103, 189)',
        'rgb(140, 86, 75)',
        'rgb(227, 119, 194)'
    ]

    for k, r_target in enumerate(r_list):
        color_idx = k % len(plotly_colors)
        fig.add_trace(
            go.Scatter(
                x=time,
                y=traces[k],
                mode='lines',
                line=dict(width=2.2, color=plotly_colors[color_idx]),
                name=f"{int(r_target)} mm downstream"
            )
        )

    fig.update_layout(
        title=dict(
            text="Velocity Magnitude vs Time at Fixed Downstream Distances",
            font=dict(family="Times New Roman", size=16, color="black")
        ),
        xaxis=dict(
            title=dict(
                text="Time (s)",
                font=dict(family="Times New Roman", size=14, color="black")
            ),
            tickfont=dict(family="Times New Roman", size=12, color="black"),
            gridcolor="lightgrey",
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            range=[time.min(), time.max()]
        ),
        yaxis=dict(
            title=dict(
                text="Mean Velocity Magnitude (m/s)",
                font=dict(family="Times New Roman", size=14, color="black")
            ),
            tickfont=dict(family="Times New Roman", size=12, color="black"),
            gridcolor="lightgrey",
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            rangemode="tozero"
        ),
        legend=dict(
            font=dict(family="Times New Roman", size=12, color="black"),
            x=0.85,
            y=0.95,
            bordercolor="black",
            borderwidth=1
        ),
        width=1200,
        height=600,
        plot_bgcolor="white"
    )
    return fig