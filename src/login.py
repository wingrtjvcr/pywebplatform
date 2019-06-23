from sanic import Blueprint,response
from sanic.response import json, text, html,file
from resource import DBHelper
from resource import common as com
from sanic_session import Session


bp_login = Blueprint('bp_login')
db2 = DBHelper(__name__)

@bp_login.route('/islogin',methods=['GET','POST'])
async def bp_usrLogin(request):
    result = {}
    if request.method == 'POST':
        usrname=request.args.get('usrname')
        pwd=request.args.get('pwd')
        # strsql = "select * from users where usrname='%s' and pwd='%s'"%(usrname,pwd)
        # # strsql2 = ";select * from users where usrname='%s' and pwd='%s'"%(usrname,pwd)
        # # strsql = strsql+strsql2
        # result = dbto.(strsql)
        # request["session"]["employeecode"] = result[0]["usrname"]
    return json(result)

@bp_login.route('/login')
async def bp_pageLogin(request):
    return com.bindHtml('login/login.html')

@bp_login.route('/loginok')
async def bp_pageLoginok(request):
    return com.bindHtml('loginok.html',request)
