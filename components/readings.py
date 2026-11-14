from html import escape

import plotly.graph_objects as go
import streamlit as st

from models.metrics import METRICS


def metric_cards(frame, names):
    if not names:
        return
    columns = st.columns(len(names))
    for column, name in zip(columns, names):
        metric = METRICS[name]
        rows = frame[frame.metric.eq(name)].sort_values("timestamp")
        with column:
            if rows.empty:
                st.metric(metric.label, "—")
                st.caption("No readings in this window")
            else:
                latest = rows.iloc[-1]
                st.metric(metric.label, f"{latest.value:,.{metric.decimals}f}", metric.unit, delta_color="off", delta_arrow="off", help=metric.meaning)
                st.caption(latest.timestamp.strftime("%d %b · %H:%M UTC"))
                st.caption("Source: " + str(latest.data_source))


def history_chart(frame, names, key):
    st.markdown("### Reading history")
    metric_name = st.selectbox("Measurement", names, format_func=lambda name: METRICS[name].label, key="chart_" + key)
    metric = METRICS[metric_name]
    rows = frame[frame.metric.eq(metric_name)].sort_values("timestamp")
    st.caption(metric.meaning + ". Values are displayed as recorded; no health assessment is inferred.")
    if rows.empty:
        st.info("No readings for this metric in your selected window. Try another metric, date range or dataset.")
        return
    figure = go.Figure()
    for source, group in rows.groupby("data_source"):
        figure.add_trace(go.Scatter(x=group.timestamp, y=group.value, mode="lines+markers", name=escape(str(source)),
                                   line={"color": "#edb18c", "width": 2}, marker={"size": 5},
                                   hovertemplate=f"%{{x|%d %b %Y, %H:%M UTC}}<br>%{{y:.{metric.decimals}f}} {metric.unit}<extra>%{{fullData.name}}</extra>"))
    figure.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                         font={"color": "#b3bebc", "family": "sans-serif"}, margin={"l": 0, "r": 12, "t": 12, "b": 0},
                         yaxis={"title": metric.unit, "gridcolor": "#2b3438", "zeroline": False},
                         xaxis={"title": "UTC", "showgrid": False}, showlegend=len(rows.data_source.unique()) > 1)
    st.plotly_chart(figure, width="stretch", key="plot_" + key, config={"displayModeBar": False})
