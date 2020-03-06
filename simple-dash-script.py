import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psycopg2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div')
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def generate_song_list(input):
    
    
    
    
#    return html.Table(
#        # Header
#        [html.Tr([html.Th(col) for col in dataframe.columns])] +
#
#        # Body
#        [html.Tr([
#            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#        ]) for i in range(min(len(dataframe), max_rows))]
#    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Songs'),
    generate_song_list([1,3,5])
])

if __name__ == '__main__':
    app.run_server(debug=True)
