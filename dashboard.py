import os
import joblib
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, html, dcc, callback, Input, Output, State
from wordcloud import WordCloud
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import dash


# Initialize Dash app
app = Dash(__name__, suppress_callback_exceptions=True)


# Load Data
def load_data():
    df_cleaned = pd.read_csv('Dataset/Cleaned Data/reviews.csv', nrows=100000)
    df_uncleaned = pd.read_csv(
        'Dataset/Uncleaned Data/clean_reviews.csv', nrows=100000)
    return df_cleaned.drop_duplicates().dropna(), df_uncleaned

# Load Models


def load_models():
    tfidf_vectorizer = joblib.load('Models/tfidf_vectorizer.pkl')
    logistic_regression_model = joblib.load(
        'Models/logistic_regression_model.pkl')
    return tfidf_vectorizer, logistic_regression_model


df_cleaned, df_uncleaned = load_data()
tfidf_vectorizer, logistic_regression_model = load_models()

# Define the app layout with a sidebar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        style={'width': '13%', 'float': 'left', 'height': '100vh',
               'background-color': '#f8f8f8'},  # Sidebar style
        children=[
            html.Button('Home', id='home-button', n_clicks=0, style={
                        'width': '90%', 'margin': '5px'}),
            html.Button('Uncleaned Data', id='uncleaned-button', n_clicks=0, style={
                        'width': '90%', 'margin': '5px'}),
            html.Button('Cleaned Data', id='cleaned-button', n_clicks=0, style={
                        'width': '90%', 'margin': '5px'}),
            html.Button('Sentimental Analysis',
                        id='sentimental-button', n_clicks=0, style={'width': '90%', 'margin': '5px'}),
            html.Button('Provide Review', id='review-button', n_clicks=0, style={
                        'width': '90%', 'margin': '5px'}),
        ]
    ),
    html.Div(
        style={'width': '80%', 'float': 'right'},  # Content style
        id='page-content'
    )
])


# Callback for updating page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('home-button', 'n_clicks'),
               Input('uncleaned-button', 'n_clicks'),
               Input('cleaned-button', 'n_clicks'),
               Input('sentimental-button', 'n_clicks'),
               Input('review-button', 'n_clicks')])
def display_page(home_clicks, uncleaned_clicks, cleaned_clicks, sentimental_clicks, review_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return html.Div([
            html.H3('Welcome to the Home page.')
        ])
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'home-button':
            return html.Div([
                html.H3('Welcome to the Home page.')
            ])
        elif button_id == 'uncleaned-button':
            return html.Div([
                html.H3('Uncleaned Data'),
                dcc.Graph(figure=generate_table(df_uncleaned.head(10)))
            ])
        elif button_id == 'cleaned-button':
            return html.Div([
                html.H3('Cleaned Data'),
                dcc.Graph(figure=generate_table(df_cleaned.head(10)))
            ])
        elif button_id == 'sentimental-button':
            return html.Div([
                html.H3('Sentimental Analysis'),
                dcc.Dropdown(id='visualization-choices',
                             options=[{'label': 'Sentiment Analysis Pie Chart', 'value': 'pie'},
                                      {'label': 'Word Cloud', 'value': 'cloud'},
                                      {'label': 'Sentiment Analysis Bar Chart',
                                          'value': 'bar'}
                                      ],
                             value='pie'),
                html.Div(id='visualization-output')
            ])
        elif button_id == 'review-button':
            return html.Div([
                html.H3('Provide Review'),
                dcc.Input(id='name-input', type='text',
                          placeholder='Enter your name', style={'margin': '10px'}),

                html.Br(),
                html.Br(),

                dcc.Textarea(id='review-input',
                             placeholder='Enter your review', style={'width': '50%', 'height': '200px'}),

                html.Br(),
                html.Br(),

                html.Button('Submit', id='submit-review', n_clicks=0),
                html.Div(id='review-output'),
                html.Br()

            ])

# Callback for Sentimental Analysis Visualization


@app.callback(Output('visualization-output', 'children'),
              [Input('visualization-choices', 'value')])
def update_visualization(choice):
    if choice == 'pie':
        sentiment_counts = df_cleaned['sentiment'].value_counts()
        fig = go.Figure(
            data=[go.Pie(labels=sentiment_counts.index, values=sentiment_counts)])
        return dcc.Graph(figure=fig)
    elif choice == 'cloud':
        sentiments = ['positive', 'negative', 'neutral']
        images_with_captions = []

        for sentiment in sentiments:
            text = " ".join(
                review for review in df_cleaned[df_cleaned['sentiment'] == sentiment]['cleaned_comments'])
            wordcloud = WordCloud(
                max_words=100, background_color="white").generate(text)

            img_buffer = BytesIO()
            wordcloud.to_image().save(img_buffer, format='PNG')
            img_str = base64.b64encode(img_buffer.getvalue()).decode()

            # Create a label for the word cloud
            caption = html.P(f"Word Cloud for {sentiment.capitalize()} Sentiment", style={
                'text-align': ',left', 'font-weight': 'bold'})

            # Create an HTML image element with the caption
            image_with_caption = html.Div([
                caption,
                html.Img(src='data:image/png;base64,{}'.format(img_str),
                         style={'height': '300px', 'margin': '10px'})
            ])

            images_with_captions.append(image_with_caption)

        return images_with_captions

    elif choice == 'bar':
        sentiment_counts = df_cleaned['sentiment'].value_counts()
        fig = go.Figure(
            data=[go.Bar(x=sentiment_counts.index, y=sentiment_counts)])
        return dcc.Graph(figure=fig)


# Callback for Submit Review
@app.callback(Output('review-output', 'children'),
              [Input('submit-review', 'n_clicks')],
              [State('name-input', 'value'),
               State('review-input', 'value')])
def submit_review(n_clicks, name, review):
    if n_clicks > 0:
        sentiment = logistic_regression_model.predict(
            tfidf_vectorizer.transform([review]))
        # Save review to CSV
        df = pd.DataFrame({'name': [name], 'review': [
                          review], 'sentiment': [sentiment[0]]})
        df.to_csv('Dataset/User Review/User_reviews.csv',
                  mode='a', header=False, index=False)
        return f'Thank you for your review'


# Helper function to generate table
def generate_table(dataframe):
    return go.Figure(data=[go.Table(
        header=dict(values=list(dataframe.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[dataframe[col] for col in dataframe.columns],
                   fill_color='lavender',
                   align='left'))
    ])


# Helper function to generate word cloud image
def plot_wordcloud(text):
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          min_font_size=10).generate(text)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
