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
except:
    print("I am unable to connect to the database")



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='text-input', value='initial value', type='text'),
    dcc.Checklist(
        id = 'checkbox-input',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF'],
        labelStyle={'display': 'inline-block'}
    ),
    html.Div(id='output-div', children = 'a')
])

@app.callback(
    Output(component_id='output-div', component_property='children'),
    [
        Input(component_id='text-input', component_property='value'),
        Input(component_id='checkbox-input', component_property='value')
    ],
)
def generate_song_list(text_input, checkbox_input):
    print(text_input)
    print(checkbox_input)
    print("asdf")
    return "test string"



#    SQL = 'SELECT * FROM SongVersions;'
#    cur = conn.cursor()
#    cur.execute(SQL)
#    print(cur.fetchall())
#    print(cur.description)
#    return "2"
    
    
#    return html.Table(
#        # Header
#        [html.Tr([html.Th(col) for col in dataframe.columns])] +
#
#        # Body
#        [html.Tr([
#            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#        ]) for i in range(min(len(dataframe), max_rows))]
#    )

if __name__ == '__main__':
    app.run_server(debug=True, host = '0.0.0.0')
