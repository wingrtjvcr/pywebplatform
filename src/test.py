from sanic import Blueprint,response
from sanic.response import json, text, html,file
from resource import conn as dbto
from resource import common as com
import time

bp_test = Blueprint('bp_test')

@bp_test.route("/excel")
async def bp_excel(request):
    strJons=[{"id":1,"name":"wing","age":33},{"id":2,"name":"mimi","age":32}]
    ticks = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return com.jsonToXls(strJons,'testdownloadexcel'+ticks,'testsheet_1')

@bp_test.route("/sessiontest")
async def index(request):
    request['session']['user'] = 'session user'
    data ={'request':request,'greetings':'Hello, sanic!'}
    return com.bindHtml('index.html',data)


@bp_test.route('/test')
async def bp_test1(request):
    return com.bindHtml('masterpage/test.html')

@bp_test.route('/test2')
async def bp_test2(request):
    return com.bindHtml('masterpage/test2.html')

@bp_test.route('/tag/<tag>')
async def tag_handler(request, tag):
    return text('Tag - {}'.format(tag))

@bp_test.route('/number/<integer_arg:int>')
async def integer_handler(request, integer_arg):
    return text('Integer - {}'.format(integer_arg))

@bp_test.route('/number/<number_arg:number>')
async def number_handler(request, number_arg):
    return text('Number - {}'.format(number_arg))

@bp_test.route('/person/<name:[A-z]+>')
async def person_handler(request, name):
    return text('Person - {}'.format(name))

@bp_test.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(request, folder_id):
    return text('Folder - {}'.format(folder_id))


@bp_test.route('/matt01')
async def index_json(request):
    # 用户定义一些传入参数
    content = request.args.get('titles')
    return json(content)
    # content _list = request.args.getlist('titles')
    # # 获取数据
    # return json({'titles':content ,'title_list':content _list,'args1':request.args['titles'],
    #              "args2": request.args, "url": request.url, "query_string": request.query_string })