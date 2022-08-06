from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from datetime import timedelta

app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H4('NQ historique '),
    html.Label("Date:"),
    dcc.DatePickerSingle(
        id='date-picker-single',
        min_date_allowed=date(2006, 4, 13),
        max_date_allowed=date(2022, 7, 29),
        initial_visible_month=date(2022, 7, 29),
        date=date(2022, 7, 29)
    ),
    dcc.Graph(id="graph"),
])

from datetime import datetime
#2022-07-29 00:00:00
custom_date_parser = lambda x: datetime.strptime(x, "%Y-%d-%m %H:%M:%S")

@app.callback(
    Output("graph", "figure"),
    Input(component_id='date-picker-single', component_property='date')
)
def display_candlestick(date):
    #df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv') # replace with your own data source
    print(date)
    zz=datetime.strptime(date,"%Y-%m-%d")

    url="https://storage.googleapis.com/histonq/NQ_x1h0je/%s.txt" % zz.strftime("%Y/%m/%d").replace("/0", "/")
    print(url)
    df = pd.read_csv(url,
                     skiprows=1,
                     date_parser=custom_date_parser,header=None)  # replace with your own data source
    layout = go.Layout(
        title="Histo NQ",
        height=900,
    )
    fig = go.Figure(go.Candlestick(
        x=df[0],
        open=df[1],
        high=df[2],
        low=df[3],
        close=df[4]
    ),layout=layout)
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title='NQ Future - %s - %s %s - %s' % (zz.strftime("%b %d %A"),min(df[3]),max(df[2]),"%s 09:30" % date),
        yaxis_title='Value',
        shapes=[dict(
            x0="%s 09:30" % date, x1="%s 09:30" % date, y0=min(df[3]), y1=max(df[2]), xref='x', yref='y',
            line_width=2),
            dict(
                x0="%s 16:00" % date, x1="%s 16:00" % date, y0=min(df[3]), y1=max(df[2]), xref='x', yref='y',
                line_width=2)
        ],
        annotations=[
            dict(
                x=zz + timedelta(hours=9,minutes=30), y=max(df[2]), xref='x', yref='y',
                showarrow=False, xanchor='left', text='Opening'),
            dict(
                x=zz + timedelta(hours=16), y=max(df[2]), xref='x', yref='y',
                showarrow=False, xanchor='left', text='Closing')
        ]
    )

    return fig

if __name__ == "__main__":
    import os
    if os.environ.get("ENVIRONMENT") != "PRODUCTION":
        app.run_server(debug=True,port=8080)
    else :
        app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)