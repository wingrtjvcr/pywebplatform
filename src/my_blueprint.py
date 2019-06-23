# more my_blueprint.py 
from sanic import Blueprint
from sanic.response import json, text, html
from resource import DBHelper
from resource import common as com
from sanic_session import Session,InMemorySessionInterface

bp = Blueprint(__name__)
db2 = DBHelper(__name__)

# router define
@bp.route('/')
async def bp_root(request):
    result = db2.selectByMap('selt1',{})
    return com.bindHtml('index.html',result)

@bp.route('/testdb')
async def bp_testdb(request):
    n = db2.exe('insert into t1(id,name) values((select count(1)+1 from t1),3333);insert into t1(id,name) values((select count(1)+1 from t1),4444)')
    return text(n)

@bp.route('/testjson')
async def bp_testjson(request):
    strjson = [{"id":"99603","name":"yiyiyi"},{"id":"99602","name":"lololo"}]
    # strjson = {"id":"996","name":"heiheihei"}
    newid = db2.insJson('t1',strjson)
    return text(newid)

@bp.route('/deltest',methods=['GET','POST'])
async def bp_deltest(request):
    if request.method == 'POST':
        strid=request.args.get('id')
        result = db2.deleteByMap('delUser',{'delid':strid})
        return json(result)

@bp.route('/updatetest',methods=['GET','POST'])
async def bp_updatetest(request):
        if request.method == 'POST':
            name=request.args.get('name')
            strid=request.args.get('id')
            result = db2.updateByMap('updateUser',{'updateid':strid,'name':name})
            return json(result)