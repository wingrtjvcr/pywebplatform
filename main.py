from sanic import Sanic
from sanic.response import json,text
from src.my_blueprint import bp
from src.login import bp_login
from src.test import bp_test
from sanic.handlers import ErrorHandler
from resource import common as com
from sanic_session import Session,InMemorySessionInterface

class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        if hasattr(exception, 'status_code') and exception.status_code == 404:
            return com.bindHtml('masterpage/err404.html')
        else:
            return json({'Code':999,'err':str(exception)})

app = Sanic(__name__)

session = Session(app, interface=InMemorySessionInterface())

app.error_handler = CustomErrorHandler()
app.static('/static', './static')
# app.url_for('static', filename='jquery-1.8.3.js') == '/static/js/jquery-1.8.3.js'

app.blueprint(bp)
app.blueprint(bp_login)
app.blueprint(bp_test)

# @app.websocket('/feed')
# async def feed(request, ws):
#     while True:
#         data = 'hello!'
#         print('Sending: ' + data)
#         await ws.send(data)
#         data = await ws.recv()
#         print('Received: ' + data)

app.run(host='0.0.0.0', port=8000)
# app.run(host='127.0.0.1', port=8000)

