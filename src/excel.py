from sanic import Blueprint,response
from sanic.response import json, text, html,file
from resource import conn as dbto
from resource import common as com
import time

bp_excel = Blueprint('bp_excel')

@bp_excel.route("/excel")
async def bp_excel2(request):
    strJons=[{"id":1,"name":"wing","age":33},{"id":2,"name":"mimi","age":32}]
    ticks = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return com.jsonToXls(strJons,'testdownloadexcel'+ticks,'testsheet_1')