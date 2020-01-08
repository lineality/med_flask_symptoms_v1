import dash
# contains widgets that can be dropped into app
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import pickle

########### Initiate the app
# 'app' is required by heroku
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
# server name is specified in proc file
server = app.server
app.title='knn'

########### Set up the layout
# generates HTML code
app.layout = html.Div(children=[
    html.H1('Iris Classification'),
    # multi line single-Div
    html.Div([
        # sections have similar code but unique slider id
        # header
        html.H6('Sepal Length'),
        dcc.Slider(
            id='slider-1',
            min=1,
            max=8,
            step=0.1,
            marks={i:str(i) for i in range(1,9)},
            # default value
            value=5
        ),
        #added linebreak so no overlap on screen
        html.Br(),
        # header
        html.H6('Petal Length'),
        dcc.Slider(
            id='slider-2',
            min=1,
            max=8,
            step=0.1,
            marks={i:str(i) for i in range(1,9)},
            # default value
            value=5
        ),
        #added linebreak so no overlap on screen
        html.Br(),
        # where choice is made
        html.H6('# of Neighbors'),
        dcc.Dropdown(
            id = 'k-drop',
            value=5,
            options=[{'label': i, 'value':i} for i in [5,10,15,20,25]]
        ),
        # where output data will go
        html.H6(id='output-message', children='output will go here')
    ]),

    html.Br(),
    html.A('See The Underlying Code On Github', href='https://github.com/lineality/intro_knn_plotly'),
])
############ Interactive Callbacks
# call back function, functions with decorators(specify input and output)
@app.callback(Output('output-message', 'children'),
            [Input('k-drop', 'value'),
            Input('slider-1', 'value'),
            Input('slider-2', 'value')
            ])

#
def display_results(k, value0, value1):
    # this opens the pickle
    # the opposite of pickling the file
    file = open(f'resources/model_k{k}.pkl', 'rb')
    model=pickle.load(file)
    file.close
    new_obs=[[value0,value1]]
    pred=model.predict(new_obs)
    specieslist=['setosa', 'versicolor','verginica']
    final_pred=specieslist[pred[0]]
    return f'For a flower with sepal length {value0} and petal length {value1}, the predicted species is"{final_pred}"'

############ Execute the app
if __name__ == '__main__':
    app.run_server()
