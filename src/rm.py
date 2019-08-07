from sanic import Blueprint,response
from sanic.response import json, text, html,file
from resource import DBHelper
from resource import common as com
import aioodbc
import pyodbc
from redminelib import Redmine
import datetime
import time

db2 = DBHelper(__name__)
bp_rm = Blueprint('bp_rm')
dsn = 'DRIVER={%s};SERVER=172.17.1.13;DATABASE=QCDDB;UID=PMOread;PWD=PMOread' % pyodbc.drivers()[1]

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
    result = db2.selectByMap("selectMyIssue",{'loginid':loginid,'status':'2'})
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
    uname=request.args.get('uname')
    memo=request.args.get('memo')
    wkhour=request.args.get('wkhour')
    wkid=request.args.get('wt')
    pjid=request.args.get('pjid')
    loginifo=getEmployeeInfo(uname)
    employeecd=loginifo['custom_fields'][0]['value']
    date=request.args.get('date')
    date=time.strftime('%Y%m%d', time.strptime(date, '%Y-%m-%d'))
  
    pars={"regist_req":[{"employee_cd":employeecd,"man_hour":wkhour,"project_id":pjid,"remarks":memo,"work_date":date,"work_detail_id":0,"work_id":wkid,"work_result_id":0,"upd_type_id":1}]}
    url="http://10.2.1.171/system/api/PMRMS001"
    # ★★ QCDシステムに反映 ★★
    result=com.postWSdata(url,pars)

    return json(result)

@bp_rm.route("/insQCDandRM",methods=['GET','POST'])
async def insQCDandRM(request):
    uname=request.args.get('uname')
    pjcode=request.args.get('pjcode')
    memo=request.args.get('memo')
    wkhour=request.args.get('wkhour')
    issueid=request.args.get('issueid')
    done=request.args.get('done')

    loginifo=getEmployeeInfo(uname)
    employeecd=loginifo['custom_fields'][0]['value']
    api_key=loginifo['api_key']

    # QCDシステムに登録
    # dsn = 'DRIVER={%s};SERVER=172.17.1.13;DATABASE=QCDDB;UID=PMOread;PWD=PMOread' % pyodbc.drivers()[1]
    conn = await aioodbc.connect(dsn=dsn)
    cur = await conn.cursor()
    await cur.execute("SELECT top 1 pj.project_id,wk.work_id FROM projects pj INNER JOIN mst_work wk ON pj.work_type_id=wk.work_type_id WHERE pj.delete_flg = 0 and pj.project_cd =%s ORDER BY wk.work_cd DESC;" % pjcode)
    rows = await cur.fetchall()
    pjid=rows[0][0]
    wkid=rows[0][1]
    pars={"regist_req":[{"employee_cd":employeecd,"man_hour":wkhour,"project_id":pjid,"remarks":memo,"work_date":datetime.datetime.now().strftime('%Y%m%d'),"work_detail_id":0,"work_id":wkid,"work_result_id":0,"upd_type_id":1}]}
    url="http://10.2.1.171/system/api/PMRMS001"
    # ★★ QCDシステムに反映 ★★
    # result=com.postWSdata(url,pars)
    await cur.close()
    await conn.close()
    
    # # RMシステムに登録
    # api_key = '3677a9378645bf393c08579ee395fe7c5dba5586'
    redminelib = Redmine('http://redmine.trechina.cn/', key=api_key)
    time_entry = redminelib.time_entry.new()
    time_entry.issue_id = issueid
    time_entry.spent_on = datetime.datetime.now().strftime('%Y-%m-%d')
    time_entry.hours = wkhour
    time_entry.activity_id = 13
    time_entry.comments = memo
    # ★★ RMに反映 ★★
    # time_entry.save()

    # チケットの進捗率、履歴を更新
    issue = redminelib.issue.get(issueid)
    issue.done_ratio  = done
    issue.notes = memo
    # ★★ RMに反映 ★★
    # issue.save()
    
    return json('result')
    # return json(result)


def getEmployeeInfo(loginid):
    api_key = '3677a9378645bf393c08579ee395fe7c5dba5586'
    # ログインNameでユーザーの詳細情報を取得
    url=("http://redmine.trechina.cn/users.json?key=%s&name="+loginid) % api_key
    result=com.getWSdata(url)
    uid=result['users'][0]['id']

    url2="http://redmine.trechina.cn/users/%s.json?key=3677a9378645bf393c08579ee395fe7c5dba5586" % uid 
    result=com.getWSdata(url2)
    return result['user']
