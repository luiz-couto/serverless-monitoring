import redis
import json
import numpy as np
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
import plotly.graph_objects as graph
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output

NUMBER_RECORDS = 100

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

redis_client = redis.Redis(host='192.168.121.189', port=6379)

app.min = []
app.hour = [] 
app.vmem = []

def get_redis_data():
    app.cpu_data = json.loads(redis_client.get('luizcouto-proj3-output'))

get_redis_data()

app.layout = html.Div([
    html.Div([
        html.H4(children='CPUs Average Utilization by Minute', style={'fontSize':'40px'}),
        dcc.Graph(id='cpus_min'),
        dcc.Interval(id='interval0', interval=3*1000, n_intervals=0)
    ]),
    html.Div([
        html.H4(children='CPUs Average Utilization by Hour', style={'fontSize':'40px'}),
        dcc.Graph(id='cpus_hour'),
        dcc.Interval(id='interval2', interval=3*1000, n_intervals=0)
    ]),
    html.Div([
        html.H4(children='Memory Utilization', style={'fontSize':'40px'}),
        dcc.Graph(id='memory-percent'),
        dcc.Interval(id='interval1', interval=3*1000, n_intervals=0)
    ])
])



# https://dash.plotly.com/basic-callbacks
@app.callback(Output('cpus_min', 'figure'), Input('interval0', 'n_intervals'))
def build_cpu_dashboard(n):
    data = json.loads(redis_client.get('luizcouto-proj3-output'))
    curr_records = []

    for key in data.keys():
        if "last_minute" in key and "cpu" in key:
            curr_records.append(data[key])

    app.min.append(curr_records)

    if len(app.min) > NUMBER_RECORDS:
        app.min = app.min[-NUMBER_RECORDS:]


    figs = make_subplots(
        rows = 1,
        cols = 1,
        subplot_titles = (
            "",
        ),
    )
    
    for i in range(len(curr_records)):
        figs.add_trace(graph.Scatter(x=np.arange(len(app.min)*len(curr_records)), y=np.array(app.min)[:,i], name="cpu%d_60sec"%i, mode="lines", line={'color':'rgb(%d,%d,%d)'%((i*73)%255, (i*25) % 255,(i*11) % 255)}), row=1, col=1)
        figs.add_trace(graph.Scatter(x=np.arange(len(app.hour)*len(curr_records)), y=np.array(app.hour)[:,i], name="cpu%d_60min"%i, mode="lines", line={'color':'rgb(%d,%d,%d)'%((i*73)%255, (i*25) % 255,(i*11) % 255)}), row=2, col=1)
    
    
    figs.update_xaxes(title_text = 'Time')
    figs.update_yaxes(title_text = 'Utilization (%)')
    
    figs.update_layout(
        width = 880,
        height = 600
    )
    
    return figs


# https://dash.plotly.com/basic-callbacks
@app.callback(Output('memory-percent', 'figure'), Input('interval1', 'n_intervals'))
def build_vmem_dashboard(n):
    get_redis_data()
    app.vmem.append(app.cpu_data['mvg_avg_memory_last_min'])

    if len(app.vmem) > 300:
        app.vmem = app.vmem[-300:]
    
    figs = make_subplots(
        rows = 1,
        cols = 1,
        subplot_titles = ("")
    )

    figs.add_trace(graph.Scatter(x=np.arange(len(app.vmem)), y=np.array(app.vmem), name="virtual_memory_60min", mode="lines", line={'color':'rgb(255,255,0)'}), row=1, col=1)

    figs.update_xaxes(title_text = 'Time (s)')
    figs.update_yaxes(title_text = 'Utilization (Megabytes)')

    figs.update_layout(
        width = 880,
        height = 300
    )

    return figs


if __name__ == '__main__':
    app.run_server(debug=True, port=5121, host='0.0.0.0')
