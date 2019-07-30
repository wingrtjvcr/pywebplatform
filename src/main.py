# more my_blueprint.py 
from sanic import Blueprint
from sanic.response import json, text, html
from resource import DBHelper
from resource import common as com
import random

bp = Blueprint(__name__)
db2 = DBHelper(__name__)

# HomePage、全件検索
@bp.route('/')
async def bp_root(request):
    # mysql DBアクセステスト
    # result = db2.selectByMap('selectQCDProject','conn_rm')
    # Pgsql　DBアクセステスト
    result = db2.selectByMap('selt1')
    return com.bindHtml('index.html',result)

# RM HomePage
@bp.route('/rmindex')
async def rmindex(request):
    return com.bindHtml('menu_main.html')

# SQL実行
@bp.route('/testdb')
async def bp_testdb(request):
    n = db2.exe('insert into t1(id,name) values((select count(1)+1 from t1),3333);insert into t1(id,name) values((select count(1)+1 from t1),4444)')
    return text(n)

# Jsonでデータ插入
@bp.route('/insjson',methods=['GET','POST'])
async def bp_insjson(request):
    strjson = [{"id":random.randint(0,99999),"name":"new1"},{"id":random.randint(0,99999),"name":"new2"}]
    # strjson = {"id":"996","name":"heiheihei"}
    newid = db2.insJson('t1',strjson)
    return text(newid)

# Jsonでデータ削除
@bp.route('/deltest',methods=['GET','POST'])
async def bp_deltest(request):
    if request.method == 'POST':
        strid=request.args.get('id')
        result = db2.deleteByMap('delUser',{'delid':strid})
        return json(result)

# Jsonでデータ更新
@bp.route('/updatetest',methods=['GET','POST'])
async def bp_updatetest(request):
        if request.method == 'POST':
            name=request.args.get('name')
            strid=request.args.get('id')
            result = db2.updateByMap('updateUser',{'updateid':strid,'name':name})
            return json(result)