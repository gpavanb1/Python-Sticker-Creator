import callbacks
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Sticker Creator'
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    # Heading
    html.H1("Sticker Creator", id="heading"),
    # Text box
    dcc.Input(
            id="meme-text",
            type="text",
            placeholder="Enter meme text"
        ),
    # File Upload
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.U('Click Here')
        ]),
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id="filename"),
    html.Button(id='submit-button', n_clicks=0, children='Stickerify'),
    html.Div(id='output-image-upload'),
])