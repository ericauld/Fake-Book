import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import psycopg2
from psycopg2.extras import RealDictCursor
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

SQL_SONG_LIST = '''SELECT songver.SongVersionID, songver.SongVersionName, artist.ArtistName
                        FROM
                            SongVersions songver
                            INNER JOIN Artists artist
                                ON songver.ArtistID = artist.ArtistID
                    ORDER BY songver.SongVersionName;
                '''
cur = conn.cursor()
cur.execute(SQL_SONG_LIST)
song_list = cur.fetchall()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.Label('Find songs similar to your chosen song'),

    dcc.Dropdown(
        id='song-choice',
        options=[{'label': i[1] + " (" + i[2] + ")", 'value': i[0]} for i in song_list],
        value='Select Song'
    ),

#     dcc.Checklist(
#         id='checkbox_input',
# #        style = {'width': '200%'},
#         options=[
#             {'label': 'Root', 'value': 0},
#             {'label': '\u266D'+'II', 'value': 1},
#             {'label': 'II', 'value': 2},
#             {'label': '\u266D'+'III', 'value': 3}, 
#             {'label': 'III', 'value': 4},
#             {'label': 'IV', 'value': 5},
#             {'label': '\u266F'+'IV / ' + '\u266D' + 'V', 'value': 6},
#             {'label': 'V', 'value': 7},
#             {'label': '\u266F' + 'V / ' + '\u266D' + 'VI', 'value': 8},
#             {'label': 'VI', 'value': 9},
#             {'label': '\u266D' + 'VII', 'value': 10},
#             {'label': 'VII', 'value': 11},
#         ],
#         value=[1, 3, 5, 6, 8, 10, 11],
#         labelStyle={'display': 'inline-block'}
#     ),
    

    html.Button('Search', id='search-button'),
    
    dash_table.DataTable(
        id = 'table',
        columns = [{'name':'songversionname', 'id':'songversionname'}, {'name':'distance', 'id':'distance'}],
        data = [{'stuff': 1, 'stuff2': 2}]
    ),

    html.Div(id='my-div')
])


@app.callback(
    Output(component_id='table', component_property='data'),
    [Input('search-button', 'n_clicks')],
    [
        State('song-choice', 'value'),
    ]
)
def update_output_div(n_clicks, song_choice):
    SQL = '''SELECT ver.SongVersionName, pairs.distance
                 FROM 
                     SongVersionPairs pairs
                     INNER JOIN SongVersions ver
                         ON 
                             ver.SongVersionID = pairs.SongVersionID2
                             AND ver.SongVersionID != pairs.SongVersionID1
                 WHERE pairs.SongVersionID1 = 1
             ORDER BY pairs.distance
             LIMIT 20;
             '''
    cur = conn.cursor(cursor_factory = RealDictCursor)
    cur.execute(SQL)
    print(song_choice)
    return cur.fetchall()

if __name__ == '__main__':
    app.run_server(debug=True, host = '0.0.0.0')
