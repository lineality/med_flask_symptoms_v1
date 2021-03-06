# https://dash.plot.ly/dash-core-components

import dash
# contains widgets that can be dropped into app
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import pickle

# new imports
#pip install basilica

import basilica
import numpy as np
import pandas as pd
from scipy import spatial



# get data
#wget https://raw.githubusercontent.com/MedCabinet/ML_Machine_Learning_Files/master/med1.csv
# turn data into dataframe
df = pd.read_csv('med1.csv')

# get pickled trained embeddings for med cultivars
#wget https://github.com/lineality/4.4_Build_files/raw/master/medembedv2.pkl
#unpickling file of embedded cultivar descriptions
unpickled_df_test = pd.read_pickle("./medembedv2.pkl")



########### Initiate the app
# 'app' is required by heroku
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
# server name is specified in proc file
server = app.server
app.title='knn'

########### Set up the layout
# generates HTML code
app.layout = html.Div(children=[
    html.H1('Medicinal Cultivar Recommendations'),
    # multi line single-Div
    html.Div([
        # sections have similar code but unique slider id
        # header
        html.H6('Description of Requested Medicinal Effects'),

        dcc.Textarea(
            id='textarea',
            placeholder='Text placeholder text...',
            value='Please describe your treatment needs & wait for new results',
            style={'width': '100%'}
        ),
        #added linebreak so no overlap on screen
        html.Br(),
        # header
        # where output data will go
        html.H6(id='output-message', children='output will go here')
    ]),

    html.Br(),
    html.A('Inspect and Get The Open Source Code On Github', href='https://github.com/lineality/medflask1v1'),
])
############ Interactive Callbacks
# call back function, functions with decorators(specify input and output)
@app.callback(Output('output-message', 'children'),
            [Input('textarea', 'value')
            ])




#
def display_results(user_input):
    # this opens the pickle
    # the opposite of pickling the file

    # file = open(f'resources/model_k{k}.pkl', 'rb')
    # model=pickle.load(file)
    # file.close
    # new_obs=[[value0,value1]]
    # pred=model.predict(new_obs)
    # specieslist=['setosa', 'versicolor','verginica']
    # final_pred=specieslist[pred[0]]



    def predict(user_input):

      # Part 1
      # a function to calculate_user_text_embedding
      # to save the embedding value in session memory
        user_input_embedding = 0

        def calculate_user_text_embedding(input, user_input_embedding):

            # setting a string of two sentences for the algo to compare
            sentences = [input]

            # calculating embedding for both user_entered_text and for features
            with basilica.Connection('36a370e3-becb-99f5-93a0-a92344e78eab') as c:
                user_input_embedding = list(c.embed_sentences(sentences))

            return user_input_embedding

        # run the function to save the embedding value in session memory
        user_input_embedding = calculate_user_text_embedding(user_input, user_input_embedding)




        # part 2
        score = 0

        def score_user_input_from_stored_embedding_from_stored_values(input, score, row1, user_input_embedding):

            # obtains pre-calculated values from a pickled dataframe of arrays
            embedding_stored = unpickled_df_test.loc[row1, 0]

            # calculates the similarity of user_text vs. product description
            score = 1 - spatial.distance.cosine(embedding_stored, user_input_embedding)

            # returns a variable that can be used outside of the function
            return score



        # Part 3
        for i in range(2351):
            # calls the function to set the value of 'score'
            # which is the score of the user input
            score = score_user_input_from_stored_embedding_from_stored_values(user_input, score, i, user_input_embedding)

            #stores the score in the dataframe
            df.loc[i,'score'] = score


        # Part 4
        output = df['Strain'].groupby(df['score']).value_counts().nlargest(5, keep='last')
        output_string = str(output)


        # Part 5: the output
        return output_string

    # user input
    #output_string = "text, Relaxed, Violet, Aroused, Creative, Happy, Energetic, Flowery, Diesel"
    #user_input = "text, Relaxed, Violet, Aroused, Creative, Happy, Energetic, Flowery, Diesel"

    #med model
    #predict(user_input)

    return f'The predicted species/cultivar/strain is"{predict(user_input)}"'

############ Execute the app
if __name__ == '__main__':
    app.run_server()
