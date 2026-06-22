import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import base64
import plotly.graph_objects as go
from flask import Flask
import os
import charts


server = Flask(__name__)

app = dash.Dash(
    __name__, server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0, shrink-to-fit=no'
        }
    ],
)


app.title = 'Air Bnb Sentiment Analysis'
app.config.suppress_callback_exceptions = True
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
logo_file = 'Images/logo.png'
csv_file = 'Dataset/Cleaned Data/reviews.csv'


header_text = html.Div('Air Bnb Sentiment Analysis Dashboard', id='main_header_text', className='main-header',
                       style=dict(color='#DC143C',
                                  fontWeight='bold', width='100%', paddingTop='1vh',
                                  display='flex', alignItems='center', justifyContent='center'))

db_header_text = dbc.Col([header_text],
                         xs=dict(size=7, offset=0), sm=dict(size=7, offset=0),
                         md=dict(size=8, offset=0), lg=dict(size=8, offset=0), xl=dict(size=8, offset=0))


encoded = base64.b64encode(open(logo_file, 'rb').read())
logo_img = html.Div(html.Img(src='data:image/jpg;base64,{}'.format(encoded.decode()), id='logo_img', className='mylogo'

                             ), style=dict(paddingTop='2vh', paddingLeft='2vw', paddingBottom='0.5vh'))

db_logo_img = dbc.Col([logo_img],
                      xs=dict(size=3, offset=0), sm=dict(size=3, offset=0),
                      md=dict(size=2, offset=0), lg=dict(size=2, offset=0), xl=dict(size=2, offset=0))

df = pd.read_csv(csv_file)

# ---------------------------------------------------------------------------------------

tweets_num_text = html.Div(html.H1('Total Number of Reviews', className='info-header', id='tweets_num_text',
                                   style=dict(fontWeight='bold', color='black')),
                           style=dict(textAlign="center", width='100%'))

tweets_num = df['cleaned_comments'].count()

tweets_num_fig = go.Figure()

indicator_size = 27
tweets_num_fig.add_trace(go.Indicator(
    mode="number",
    value=tweets_num,
    number={'font': {'color': '#DC143C',
                     'size': indicator_size}, 'valueformat': ","},
    domain={'row': 0, 'column': 0}
))


tweets_num_fig.update_layout(paper_bgcolor="#f7f7f7", plot_bgcolor='white', height=50, margin=dict(l=0, r=0, t=0, b=0),

                             )

tweets_num_indicator = html.Div(dcc.Graph(figure=tweets_num_fig, config={
                                'displayModeBar': False}, id='tweets_num_indicator', style=dict(width='100%')), className='num', style=dict(width='100%'))

# ---------------------------------------------------------------------------------------

retweets_avg_text = html.Div(html.H1('Average Number of Reviews', className='info-header', id='retweets_avg_text',
                                     style=dict(fontWeight='bold', color='black')),
                             style=dict(textAlign="center", width='100%'))


retweets_avg = round(df['cleaned_comments'].count() + 3500 /
                     len(df['cleaned_comments'].unique()), 2)

retweets_avg_fig = go.Figure()

retweets_avg_fig.add_trace(go.Indicator(
    mode="number",
    value=retweets_avg,
    number={'font': {'color': '#DC143C',
                     'size': indicator_size}, 'valueformat': ","},
    domain={'row': 0, 'column': 0}
))


retweets_avg_fig.update_layout(paper_bgcolor="#f7f7f7", plot_bgcolor='white', height=50, margin=dict(l=0, r=0, t=0, b=0),

                               )

retweets_avg_indicator = html.Div(dcc.Graph(figure=retweets_avg_fig, config={
                                  'displayModeBar': False}, id='retweets_avg_indicator', style=dict(width='100%')), className='num', style=dict(width='100%'))

# ---------------------------------------------------------------------------------------

likes_avg_text = html.Div(html.H1('Average Number of Positive Reviews', className='info-header', id='likes_avg_text',
                                  style=dict(fontWeight='bold', color='black')),
                          style=dict(textAlign="center", width='100%'))

# getting avg positive sentiments from the dataframe
likes_avg = round(df[df['sentiment'] == 'positive']
                  ['sentiment'].count() / len(df) * 100, 2)

likes_avg_fig = go.Figure()

likes_avg_fig.add_trace(go.Indicator(
    mode="number",
    value=likes_avg,
    number={'font': {'color': '#DC143C', 'size': indicator_size}, 'suffix': "%"},
    domain={'row': 0, 'column': 0}
))

likes_avg_fig.update_layout(paper_bgcolor="#f7f7f7", plot_bgcolor='white', height=50, margin=dict(l=0, r=0, t=0, b=0),

                            )

likes_avg_indicator = html.Div(dcc.Graph(figure=likes_avg_fig, config={
                               'displayModeBar': False}, id='likes_avg_indicator', style=dict(width='100%')), className='num', style=dict(width='100%'))

# ---------------------------------------------------------------------------------------

replies_avg_text = html.Div(html.H1('Average Number of Negative Reviews', className='info-header', id='replies_avg_text',
                                    style=dict(fontWeight='bold', color='black')),
                            style=dict(textAlign="center", width='100%'))


replies_avg = round(df[df['sentiment'] == 'negative']
                    ['sentiment'].count() / len(df['sentiment']) * 100, 2)


replies_avg_fig = go.Figure()

replies_avg_fig.add_trace(go.Indicator(
    mode="number",
    value=replies_avg,
    number={'font': {'color': '#DC143C', 'size': indicator_size}, 'suffix': "%"},
    domain={'row': 0, 'column': 0}
))

replies_avg_fig.update_layout(paper_bgcolor="#f7f7f7", plot_bgcolor='white', height=50, margin=dict(l=0, r=0, t=0, b=0),

                              )

replies_avg_indicator = html.Div(dcc.Graph(figure=replies_avg_fig, config={
                                 'displayModeBar': False}, id='replies_avg_indicator', style=dict(width='100%')), className='num', style=dict(width='100%'))


# ---------------------------------------------------------------------------------------

countries_num_text = html.Div(html.H1('Average Number of Neutral Reviews', className='info-header', id='countries_num_text',
                                      style=dict(fontWeight='bold', color='black')),
                              style=dict(textAlign="center", width='100%'))

countries_num = round(df[df['sentiment'] == 'neutral']
                      ['sentiment'].count() / len(df['sentiment']) * 100, 2)


countries_num_fig = go.Figure()

countries_num_fig.add_trace(go.Indicator(
    mode="number",
    value=countries_num,
    number={'font': {'color': '#DC143C',
                     'size': indicator_size}, 'suffix': "%"},
    domain={'row': 0, 'column': 0}
))

countries_num_fig.update_layout(paper_bgcolor="#f7f7f7", plot_bgcolor='white', height=50, margin=dict(l=0, r=0, t=0, b=0),

                                )

countries_num_indicator = html.Div(dcc.Graph(figure=countries_num_fig, config={
                                   'displayModeBar': False}, id='countries_num_indicator', style=dict(width='100%')), className='num', style=dict(width='100%'))


# ---------------------------------------------------------------------------------------

hor_bar_chart_header = html.Div(html.H1('Sentiment Score by Reviewer Name', className='date-chart-header', id='hor_bar_chart_header',
                                        style=dict(fontWeight='bold', color='black',
                                                   marginTop='')),
                                style=dict(textAlign="center", width='100%'))


hor_bar_chart = charts.create_graph(df)
hor_bar_chart_div = html.Div([
    dcc.Graph(id='hor_bar_chart', config={'displayModeBar': True, 'displaylogo': False,
                                          'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']}, className='hor-bar-fig',
              style=dict(height='', backgroundColor='#f7f7f7', border=''), figure=hor_bar_chart
              )], id='hor_bar_chart_div'
)

# ---------------------------------------------------------------------------------------


ver_bar_chart_header = html.Div(html.H1('Sentiment Score by Reviews', className='date-chart-header', id='ver_bar_chart_header',
                                        style=dict(fontWeight='bold', color='black')),
                                style=dict(textAlign="center", width='100%'))


ver_bar_chart = charts.create_graph2(df)
ver_bar_chart_div = html.Div([
    dcc.Graph(id='ver_bar_chart', config={'displayModeBar': True, 'displaylogo': False,
                                          'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']}, className='ver-bar-fig',
              style=dict(height='', backgroundColor='#f7f7f7', border=''), figure=ver_bar_chart
              )], id='ver_bar_chart_div'
)

# ---------------------------------------------------------------------------------------

common_words = html.Div(html.H1('Common Words', className='date-chart-header', id='common_words',
                                style=dict(fontWeight='bold', color='black')),
                        style=dict(textAlign="center", width='100%'))

common_words_fig = charts.wordcloud(df)
common_words_div = html.Div([
    dcc.Graph(id='common_words', config={'displayModeBar': True, 'displaylogo': False,
                                         'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']}, className='ver-bar-fig',
              style=dict(height='', backgroundColor='#f7f7f7', border=''), figure=common_words_fig
              )], id='common_words_div'
)

# ---------------------------------------------------------------------------------------

circle_chart_header = html.Div(html.H1('Sentiments', className='date-chart-header', id='circle_chart_header',
                                       style=dict(fontWeight='bold', color='black')),
                               style=dict(textAlign="center", width='100%'))


circle_chart = charts.circle(df)
circle_chart_div = html.Div([
    dcc.Graph(id='circle_chart', config={'displayModeBar': True, 'displaylogo': False,
                                         'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']}, className='ver-bar-fig',
              style=dict(height='', backgroundColor='#f7f7f7', border=''), figure=circle_chart
              )], id='circle_chart_div'
)

# ---------------------------------------------------------------------------------------

bubble_chart_header = html.Div(html.H1('Sentiments', className='date-chart-header', id='bubble_chart_header',
                                       style=dict(fontWeight='bold', color='black')),
                               style=dict(textAlign="center", width='100%'))

bubble_chart = charts.bubble(df)
bubble_chart_div = html.Div([
    dcc.Graph(id='bubble_chart', config={'displayModeBar': True, 'displaylogo': False,
                                         'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']}, className='ver-bar-fig',
              style=dict(height='', backgroundColor='#f7f7f7', border=''), figure=bubble_chart
              )], id='bubble_chart_div'
)

# ---------------------------------------------------------------------------------------

polar_area_chart_header = html.Div(html.H1('Sentiments', className='date-chart-header', id='polar_area_chart_header',
                                           style=dict(fontWeight='bold', color='black')),
                                   style=dict(textAlign="center", width='100%'))

polar_area_chart = charts.polar_area(df)
polar_area_chart_div = html.Div([
    dcc.Graph(id='polar_area_chart', config={'displayModeBar': True, 'displaylogo': False,
                                             'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']}, className='ver-bar-fig',
              style=dict(height='', backgroundColor='#f7f7f7', border=''), figure=polar_area_chart
              )], id='polar_area_chart_div'
)

# ---------------------------------------------------------------------------------------

time_series_chart_header = html.Div(html.H1('Frequency of Reviews by Year', className='date-chart-header', id='time_series_chart_header',
                                            style=dict(fontWeight='bold', color='black')),
                                    style=dict(textAlign="center", width='100%'))

time_series_chart = charts.time_series(df)
time_series_chart_div = html.Div([
    dcc.Graph(id='time_series_chart', config={'displayModeBar': True, 'displaylogo': False,
                                              'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']}, className='ver-bar-fig',
              style=dict(height='', backgroundColor='#f7f7f7', border=''), figure=time_series_chart
              )], id='time_series_chart_div'
)


# ---------------------------------------------------------------------------------------

time_sentiment_chart_header = html.Div(html.H1('Sentiment Score by Date', className='date-chart-header', id='time_sentiment_chart_header',
                                               style=dict(fontWeight='bold', color='black')),
                                       style=dict(textAlign="center", width='100%'))

time_sentiment_chart = charts.time_sentiment(df)
time_sentiment_chart_div = html.Div([
    dcc.Graph(id='time_sentiment_chart', config={'displayModeBar': True, 'displaylogo': False,
                                                 'modeBarButtonsToRemove': ['lasso2d', 'pan', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d']}, className='ver-bar-fig',
              style=dict(height='', backgroundColor='#f7f7f7', border=''), figure=time_sentiment_chart
              )], id='time_sentiment_chart_div'
)

# ---------------------------------------------------------------------------------------

main_layout = html.Div([dbc.Row([db_logo_img, db_header_text],
                                style=dict(backgroundColor='white'), id='main_header'),
                        # html.Br(),

                       dbc.Row([
                           html.Div([

                               dbc.Card(dbc.CardBody([tweets_num_text,
                                                     dbc.Spinner([tweets_num_indicator], size="lg", color="primary",
                                                                 type="border", fullscreen=False,
                                                                 spinner_style=dict(marginTop=''))

                                                      ]), style=dict(backgroundColor='#f7f7f7'), id='card3',
                                        className='info-card'),


                               dbc.Card(dbc.CardBody([retweets_avg_text,
                                                      dbc.Spinner([retweets_avg_indicator], size="lg", color="primary",
                                                                  type="border", fullscreen=False,
                                                                  spinner_style=dict(marginTop=''))

                                                      ]), style=dict(backgroundColor='#f7f7f7', marginLeft='1vw'), id='card4',
                                        className='info-card'),

                               dbc.Card(dbc.CardBody([likes_avg_text,
                                                      dbc.Spinner([likes_avg_indicator], size="lg",
                                                                  color="primary",
                                                                  type="border", fullscreen=False,
                                                                  spinner_style=dict(marginTop=''))

                                                      ]), style=dict(backgroundColor='#f7f7f7', marginLeft='1vw'), id='card4',
                                        className='info-card'),

                               dbc.Card(dbc.CardBody([replies_avg_text,
                                                      dbc.Spinner([replies_avg_indicator], size="lg",
                                                                  color="primary",
                                                                  type="border", fullscreen=False,
                                                                  spinner_style=dict(marginTop=''))

                                                      ]), style=dict(backgroundColor='#f7f7f7', marginLeft='1vw'), id='card5',
                                        className='info-card'),

                               dbc.Card(dbc.CardBody([countries_num_text,
                                                      dbc.Spinner([countries_num_indicator], size="lg",
                                                                  color="primary",
                                                                  type="border", fullscreen=False,
                                                                  spinner_style=dict(marginTop=''))

                                                      ]), style=dict(backgroundColor='#f7f7f7', marginLeft='1vw'), id='card6',
                                        className='info-card'),
                           ], style=dict(display='flex', alignItems='center',
                                         justifyContent='center', width='100%'))
                       ]),
    html.Br(),

    dbc.Row([


        dbc.Col([dbc.Card(dbc.CardBody([hor_bar_chart_header,
                                        dbc.Spinner([hor_bar_chart_div], size="lg", color="primary",
                                                    type="border",
                                                    fullscreen=False),

                                        ]), style=dict(backgroundColor='#f7f7f7'), id='card8',
                          className='charts-card'), html.Br()
                 ], xl=dict(size=4, offset=0), lg=dict(size=6, offset=0),
                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                style=dict(paddingLeft='0.5vw', paddingRight='0.5vw')),

        dbc.Col([dbc.Card(dbc.CardBody([ver_bar_chart_header,
                                        dbc.Spinner([ver_bar_chart_div], size="lg", color="primary",
                                                    type="border",
                                                    fullscreen=False),

                                        ]), style=dict(backgroundColor='#f7f7f7'), id='card8',
                          className='charts-card'), html.Br()
                 ], xl=dict(size=4, offset=0), lg=dict(size=6, offset=0),
                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                style=dict(paddingLeft='0.5vw', paddingRight='0.5vw')),

        dbc.Col([dbc.Card(dbc.CardBody([common_words,
                                        dbc.Spinner([common_words_div], size="lg", color="primary",
                                                    type="border",
                                                    fullscreen=False),

                                        ]), style=dict(backgroundColor='#f7f7f7'), id='card8',
                          className='charts-card'), html.Br()
                 ], xl=dict(size=4, offset=0), lg=dict(size=6, offset=0),
                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                style=dict(paddingLeft='0.5vw', paddingRight='0.5vw')),

        dbc.Col([dbc.Card(dbc.CardBody([circle_chart_header,
                                        dbc.Spinner([circle_chart_div], size="lg", color="primary",
                                                    type="border",
                                                    fullscreen=False),

                                        ]), style=dict(backgroundColor='#f7f7f7'), id='card8',
                          className='charts-card'), html.Br()
                 ], xl=dict(size=4, offset=0), lg=dict(size=6, offset=0),
                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                style=dict(paddingLeft='0.5vw', paddingRight='0.5vw')),


        dbc.Col([dbc.Card(dbc.CardBody([bubble_chart_header,
                                        dbc.Spinner([bubble_chart_div], size="lg", color="primary",
                                                    type="border",
                                                    fullscreen=False),

                                        ]), style=dict(backgroundColor='#f7f7f7'), id='card8',
                          className='charts-card'), html.Br()
                 ], xl=dict(size=4, offset=0), lg=dict(size=6, offset=0),
                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                style=dict(paddingLeft='0.5vw', paddingRight='0.5vw')),

        dbc.Col([dbc.Card(dbc.CardBody([polar_area_chart_header,
                                        dbc.Spinner([polar_area_chart_div], size="lg", color="primary",
                                                    type="border",
                                                    fullscreen=False),

                                        ]), style=dict(backgroundColor='#f7f7f7'), id='card8',
                          className='charts-card'), html.Br()
                 ], xl=dict(size=4, offset=0), lg=dict(size=6, offset=0),
                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                style=dict(paddingLeft='0.5vw', paddingRight='0.5vw')),

        dbc.Col([dbc.Card(dbc.CardBody([time_series_chart_header,
                                        dbc.Spinner([time_series_chart_div], size="lg", color="primary",
                                                    type="border",
                                                    fullscreen=False),

                                        ]), style=dict(backgroundColor='#f7f7f7'), id='card8',
                          className='charts-card'), html.Br()
                 ], xl=dict(size=6, offset=0), lg=dict(size=6, offset=0),
                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                style=dict(paddingLeft='0.5vw', paddingRight='0.5vw')),

        dbc.Col([dbc.Card(dbc.CardBody([time_sentiment_chart_header,
                                        dbc.Spinner([time_sentiment_chart_div], size="lg", color="primary",
                                                    type="border",
                                                    fullscreen=False),

                                        ]), style=dict(backgroundColor='#f7f7f7'), id='card8',
                          className='charts-card'), html.Br()
                 ], xl=dict(size=6, offset=0), lg=dict(size=6, offset=0),
                md=dict(size=6, offset=0), sm=dict(size=12, offset=0), xs=dict(size=12, offset=0),
                style=dict(paddingLeft='0.5vw', paddingRight='0.5vw')),


    ], className='g-0')
])


app.layout = html.Div([dbc.Spinner([html.Div(id='layout')], size="lg", color="primary", type="border", fullscreen=True, id='spinner'), dcc.Location(id='url', refresh=True, pathname='/Dashboard')
                       ], style=dict(backgroundColor='white'), className='main',
                      id='main_div')


@app.callback([Output('layout', 'children'), Output('spinner', 'delay_show')], Input('url', 'pathname'))
def landing_page(pathname):
    if pathname == '/Dashboard':
        return (main_layout, 60000)
    else:
        return (dash.no_update, dash.no_update)


@app.callback(Output('date_chart', 'figure'), Input('topics_menu', 'value'))
def update_date_chart(selected_topic):
    fig = go.Figure()
    graph_data = df.copy()
    # setting the index to 'created' column
    graph_data.set_index('created', inplace=True)
    # mapping sentiment numbers to text values
    sent_dict = {'negative': 'negative',
                 'neutral': 'neutral', 'positive': 'positive'}
    sent_colors = {'1': 'red', '2': '#e3a817', '3': 'green'}

    # checking if selected topic is not all topics ( user choosed one topic )
    if (selected_topic != 'Reviewer Name'):
        # filtering dataframe based on that topic
        graph_data = graph_data[graph_data['reviewer_name'] == selected_topic]

    for i in range(1, 4):
        # looping through the data filtered with each sentiment
        data = graph_data[graph_data['sentiment'] == str(i)]
        # getting the count of tweets for each day
        data = data.resample('1D').count()

        # line chart

        fig.add_trace(
            go.Scatter(x=data.index, y=data['tweetId'].astype('int64'), mode='lines', name=sent_dict[str(i)],
                       marker_color=sent_colors[str(i)]
                       # , stackgroup='one'
                       ))

    fig.update_layout(
        xaxis_title='<b>Date<b>', yaxis_title='<b>Number of Tweets<b>',
        font=dict(size=14, family='Arial', color='black'), hoverlabel=dict(
            font_size=14, font_family="Rockwell", font_color='black', bgcolor='white'), plot_bgcolor='#f7f7f7',
        paper_bgcolor='#f7f7f7',
        xaxis=dict(

            tickwidth=2, tickcolor='#80ced6',
            ticks="outside",
            tickson="labels",
            rangeslider_visible=False
        ), margin=dict(l=0, r=0, t=30, b=0)
    )
    fig.update_xaxes(showgrid=False, showline=True,
                     zeroline=False, linecolor='black')
    fig.update_yaxes(showgrid=False, showline=True,
                     zeroline=False, linecolor='black')
    return fig


@app.callback(Output('word_cloud', 'src'), Input('topics_menu2', 'value'))
def update_word_cloud(selected_topic):

    dire = os.path.join(THIS_FOLDER, '{}.png'.format(selected_topic))

    encoded = base64.b64encode(open(dire, 'rb').read())

    return 'data:image/jpg;base64,{}'.format(encoded.decode())


if __name__ == '__main__':
    app.run_server(host='localhost', port=8044, debug=False,
                   dev_tools_silence_routes_logging=True)
