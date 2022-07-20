import redis
import json
import numpy as np
import dash_bootstrap_components as dbc
import plotly.graph_objects as graph

from dash import Dash, html, dcc
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

NUMBER_RECORDS = 100

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

redis_client = redis.Redis(host='192.168.121.189', port=6379)

app.cpu_min_records = []
app.cpu_hour_records = [] 
app.mem_records = []

app.layout = html.Div([
    html.Div([
        html.H4(children='CPUs Average Utilization by Minute', style={'fontSize':'27px'}),
        dcc.Graph(id='cpus_min'),
        dcc.Interval(id='interval0', interval=3*1000, n_intervals=0)
    ]),
    html.Div([
        html.H4(children='CPUs Average Utilization by Hour', style={'fontSize':'27px'}),
        dcc.Graph(id='cpus_hour'),
        dcc.Interval(id='interval2', interval=3*1000, n_intervals=0)
    ]),
    html.Div([
        html.H4(children='Memory Utilization', style={'fontSize':'27px'}),
        dcc.Graph(id='memory-percent'),
        dcc.Interval(id='interval1', interval=3*1000, n_intervals=0)
    ])
])


@app.callback(Output('cpus_min', 'figure'), Input('interval0', 'n_intervals'))
def build_cpu_dashboard(n):
    data = json.loads(redis_client.get('luizcouto-proj3-output'))
    curr_records = []

    for key in data.keys():
        if "last_minute" in key and "cpu" in key:
            curr_records.append(data[key])

    app.cpu_min_records.append(curr_records)

    if len(app.cpu_min_records) > NUMBER_RECORDS:
        app.cpu_min_records = app.cpu_min_records[-NUMBER_RECORDS:]


    figs = make_subplots(
        rows = 1,
        cols = 1,
        subplot_titles = (
            "",
        ),
    )
    
    for i in range(len(curr_records)):
        figs.add_trace(graph.Scatter(x=np.arange(len(app.cpu_min_records)*len(curr_records)), 
                                    y=np.array(app.cpu_min_records)[:,i], 
                                    name="CPU " + str(i), 
                                    mode="lines",
                                    line={'color':'rgb(%d,%d,%d)'%((i*73)%255, (i*25) % 255,(i*11) % 255)}),
                                    row=1,
                                    col=1)
    
    
    figs.update_xaxes(title_text = 'Time')
    figs.update_yaxes(title_text = 'Utilization (%)')
    
    figs.update_layout(
        width = 1200,
        height = 300
    )
    
    return figs


@app.callback(Output('cpus_hour', 'figure'), Input('interval2', 'n_intervals'))
def build_cpu_dashboard(n):
    data = json.loads(redis_client.get('luizcouto-proj3-output'))
    curr_records = []

    for key in data.keys():
        if "last_hour" in key and "cpu" in key:
            curr_records.append(data[key])

    app.cpu_hour_records.append(curr_records)

    if len(app.cpu_hour_records) > NUMBER_RECORDS:
        app.cpu_hour_records = app.cpu_hour_records[-NUMBER_RECORDS:]


    figs = make_subplots(
        rows = 1,
        cols = 1,
        subplot_titles = (
            "",
        ),
    )
    
    for i in range(len(curr_records)):
        figs.add_trace(graph.Scatter(x=np.arange(len(app.cpu_hour_records)*len(curr_records)),
                                    y=np.array(app.cpu_hour_records)[:,i], 
                                    name="CPU " + str(i),
                                    mode="lines",
                                    line={'color':'rgb(%d,%d,%d)'%((i*73)%255, (i*25) % 255,(i*11) % 255)}),
                                    row=1,
                                    col=1 )
    
    
    figs.update_xaxes(title_text = 'Time')
    figs.update_yaxes(title_text = 'Utilization (%)')
    
    figs.update_layout(
        width = 1200,
        height = 300
    )
    
    return figs


@app.callback(Output('memory-percent', 'figure'), Input('interval1', 'n_intervals'))
def build_vmem_dashboard(n):
    data = json.loads(redis_client.get('luizcouto-proj3-output'))
    app.mem_records.append(data['mvg_avg_memory_last_min'])

    if len(app.mem_records) > NUMBER_RECORDS:
        app.mem_records = app.mem_records[-NUMBER_RECORDS:]
    
    figs = make_subplots(
        rows = 1,
        cols = 1,
        subplot_titles = ("")
    )

    figs.add_trace(graph.Scatter(x=np.arange(len(app.mem_records)),
                                y=np.array(app.mem_records),
                                name="memory_percent_last_min",
                                mode="lines",
                                line={'color':'rgb(235,5,100)'}),
                                row=1,
                                col=1 )

    figs.update_xaxes(title_text = 'Time (s)')
    figs.update_yaxes(title_text = 'Utilization (%)')

    figs.update_layout(
        width = 1200,
        height = 300
    )

    return figs


if __name__ == '__main__':
    app.run_server(debug=True, port=5121, host='0.0.0.0')
