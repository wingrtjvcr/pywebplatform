from sanic import Blueprint,response
from sanic.response import json, text, html,file
from resource import DBHelper
from resource import common as com
import aioodbc
import pyodbc

db2 = DBHelper(__name__)
bp_rm = Blueprint('bp_rm')

@bp_rm.route("/getprjectme")
async def getprjectme(request):
    url="http://redmine.trechina.cn/users.json?key=3677a9378645bf393c08579ee395fe7c5dba5586&name=limingze"
    repo_dicts=com.getWSdata(url)
    return json(repo_dicts)

@bp_rm.route("/getIssue",methods=['GET','POST'])
async def getIssue(request):
     # チケットid
    issueid=request.args.get('issueid')
    # ログインNameでユーザーの詳細情報を取得
    url="http://redmine.trechina.cn/issues/"+str(issueid)+".json?key=3677a9378645bf393c08579ee395fe7c5dba5586"
    result=com.getWSdata(url)

    return json(result)

@bp_rm.route("/getIssueList",methods=['GET','POST'])
async def getIssueList(request):
     # ユーザーのログインid
    loginid=request.args.get('loginid')
    result = db2.selectByMap("selectMyIssue",{'loginid':loginid,'status':'1,2'})
    return json(result)

@bp_rm.route("/getWorkType",methods=['GET','POST'])
async def getWorkType(request):
    wt=request.args.get('wt')
    url="http://10.2.1.171/system/api/PMMSS003"
    pars={"disp_req":{"work_type_id":wt}}
    result=com.postWSdata(url,pars)
    return json(result)

@bp_rm.route("/getProject",methods=['GET','POST'])
async def getProject(request):
    pars={"disp_req":{}}
    url="http://10.2.1.171/system/api/PMBMS012"
    result=com.postWSdata(url,pars)
    return json(result)

@bp_rm.route("/insQCD",methods=['GET','POST'])
async def insQCD(request):
    dsn = 'DRIVER={%s};SERVER=172.20.1.15;DATABASE=QCDDB;UID=read;PWD=' % pyodbc.drivers()[1]
    conn = await aioodbc.connect(dsn=dsn)
    cur = await conn.cursor()
    await cur.execute("SELECT top 1 * FROM projects  WHERE  delete_flg = 0 and project_cd =50700318;")
    rows = await cur.fetchall()
    pjid=rows[0][0]
    pars={"regist_req":[{"employee_cd":10120869,"man_hour":"2","project_id":pjid,"remarks":"test1","work_date":20190801,"work_detail_id":0,"work_id":152,"work_result_id":0,"upd_type_id":1}]}
    url="http://10.2.1.171/system/api/PMRMS001"
    result=com.postWSdata(url,pars)

    await cur.close()
    await conn.close()
    return json(result)


def getEmployeeInfo(loginid):
    # ログインNameでユーザーの詳細情報を取得
    url="http://redmine.trechina.cn/users.json?key=3677a9378645bf393c08579ee395fe7c5dba5586&name="+loginid
    result=com.getWSdata(url)
    return result['users'][0]

