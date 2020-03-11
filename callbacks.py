import dash
import dash_html_components as html
from app import app
from dash.dependencies import Input, Output, State
from api import get_meme


@app.callback(Output('filename', 'children'),
             [Input('upload-image', 'contents')],
             [State('upload-image', 'filename')])
def show_filename(c, f):
    if c is not None:
        return html.H5("File uploaded: " + f)


@app.callback(Output('output-image-upload', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('upload-image', 'contents'),
               State('meme-text', 'value')])
def update_output(n, c, t):
    if c is not None:
        children = [parse_contents(c, t.upper())]
        return children


def parse_contents(contents, text):
    return html.Div([
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=get_meme(contents, text)),
    ], id="image-holder")