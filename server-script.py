import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psycopg2
from pathlib import Path

project_folder = Path("/home/ubuntu/Songbook")
_key_file = project_folder / "key-file.txt"

with _key_file.open() as key_file:
    input_list = key_file.readlines()

password = input_list[0]
login_info = "dbname='postgres' user='postgres' host='localhost' password='{}'".format(password)

try:
    conn = psycopg2.connect(login_info)
    conn.set_isolation_level(0)
    print("Database connection successful")
except:
    print("I am unable to connect to the database")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),

    html.Label('Find songs by mode'),
    dcc.Checklist(
        id='checkbox_input',
        options=[
            {'label': 'Root', 'value': 0},
            {'label': '\u266D'+'II', 'value': 1},
            {'label': 'II', 'value': 2},
            {'label': '\u266D'+'III', 'value': 3}, 
            {'label': 'III', 'value': 4},
            {'label': 'IV', 'value': 5},
            {'label': '\u266F'+'IV\/' + '\u266D' + 'V', 'value': 6},
            {'label': 'V', 'value': 7},
            {'label': '\u266F' + 'V \/' + '\u266D' + 'VI', 'value': 8},
            {'label': 'VI', 'value': 9},
            {'label': '\u266D' + 'VII', 'value': 10},
            {'label': 'VII', 'value': 11},
        ],
        value=[1, 3, 5, 6, 8, 10, 11],
        labelStyle={'display': 'inline-block'}
    ),

    html.Div(id='my-div')
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [
        Input('checkbox_input', 'value'),
        Input(component_id='my-id', component_property='value')
    ]
)
def update_output_div(checkbox_input, input_value):
    print(checkbox_input)
    return 'You\'ve entered "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True, host = '0.0.0.0')
