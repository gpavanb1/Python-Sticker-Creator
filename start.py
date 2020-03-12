import callbacks
import dash
import dash_core_components as dcc
import dash_html_components as html
from app import app


server = app.server

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',
    port=80,
    debug=False)