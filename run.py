from sanic import Sanic
from sanic.response import json,text
from src.main import bp
from src.login import bp_login
from src.excel import bp_excel
from src.rm import bp_rm
from sanic.handlers import ErrorHandler
from resource import common as com

class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        if hasattr(exception, 'status_code') and exception.status_code == 404:
            return com.bindHtml('masterpage/err404.html')
        else:
            return json({'Code':999,'err':str(exception)})

app = Sanic(__name__)


app.error_handler = CustomErrorHandler()
app.static('/static', './static')

app.blueprint(bp)
app.blueprint(bp_rm)
app.blueprint(bp_login)
app.blueprint(bp_excel)

app.run(host='0.0.0.0', port=8000)
# app.run(host='127.0.0.1', port=8000)

