import plotly.graph_objects as go
from plotly.subplots import make_subplots

def build_directional_pdf_polar_plots(results):
    t_starts = results["t_starts"]
    t_ends = results["t_ends"]
    window_results = results["window_results"]
    n_bins = results["n_bins"]
    n_win = len(window_results)

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{'type': 'polar'}, {'type': 'polar'}, {'type': 'polar'}]],
        subplot_titles=[f"{t_starts[w]:.1f} – {t_ends[w]:.1f} s" for w in range(n_win)],
        horizontal_spacing=0.05
    )

    for w in range(n_win):
        col_num = w + 1
        win_data = window_results[w]

        fig.add_trace(
            go.Barpolar(
                r=win_data["counts"],
                theta=win_data["bin_centers_deg"],
                width=[20] * n_bins,
                marker_color='rgb(255, 128, 128)',
                marker_line_width=0,
                opacity=0.65,
                showlegend=False
            ),
            row=1, col=col_num
        )

    polar_config = dict(
        angularaxis=dict(
            direction="counterclockwise",
            rotation=0,
            tickmode="linear",
            tick0=0,
            dtick=30,
            ticks="outside",
            showline=True,
            linecolor="black",
            tickfont=dict(color="black")
        ),
        radialaxis=dict(
            gridcolor="lightgrey",
            ticks="",
            tickfont=dict(color="black")
        ),
        bgcolor="white"
    )

    fig.update_layout(
        font=dict(
            family="Times New Roman", 
            size=12,
            color="black"
        ),
        width=1500,
        height=550,
        margin=dict(l=40, r=40, t=80, b=40),
        polar1=polar_config,
        polar2=polar_config,
        polar3=polar_config
    )

    return fig