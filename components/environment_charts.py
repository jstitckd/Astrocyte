"""Recorded-profile charts, adapted from testing.py's compact Plotly tiles."""
import plotly.graph_objects as go


def history_figure(frame, schema, snapshot, kind, temperature_unit="°C", pressure_unit="Pa", accent="#d093f6"):
    day = frame.loc[frame["__sol"].eq(snapshot.sol)]
    figure = go.Figure()
    definitions = (("air", "Outside air", accent), ("ground", "Ground", "#a6c4ae")) if kind == "temperature" else (("pressure", "Outside pressure", accent),)
    unit = temperature_unit if kind == "temperature" else pressure_unit
    for key, label, colour in definitions:
        column = schema.get(key)
        if column is None or day[column].notna().sum() == 0:
            continue
        values = day[column].copy()
        if kind == "temperature" and temperature_unit == "°F":
            values = values * 9 / 5 + 32
        if key == "pressure" and pressure_unit == "mbar":
            values = values / 100
        figure.add_trace(go.Scatter(
            x=day["__hour"], y=values, customdata=day[["__time"]],
            mode="lines", name=label, connectgaps=False,
            line={"color": colour, "width": 2.5},
            hovertemplate="%{customdata[0]} LMST<br>%{y:.2f} " + unit + "<extra>%{fullData.name}</extra>",
        ))
    figure.add_vline(x=snapshot.hour, line_color=accent, line_width=1, line_dash="dot", opacity=.6)
    figure.update_layout(
        height=235, margin={"l": 0, "r": 12, "t": 12, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#a9b5b6", "family": "sans-serif", "size": 11},
        hovermode="x unified", legend={"orientation": "h"},
        xaxis={"title": "Local mean solar time (LMST)", "range": [0, 24], "tickvals": [0, 6, 12, 18, 24],
               "ticktext": ["00:00", "06:00", "12:00", "18:00", "24:00"], "showgrid": False, "zeroline": False},
        yaxis={"title": unit, "gridcolor": "#30383d", "zeroline": False},
    )
    return figure
