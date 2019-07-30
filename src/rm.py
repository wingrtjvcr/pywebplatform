from sanic import Blueprint,response
from sanic.response import json, text, html,file
from resource import conn as db2
from resource import common as com

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
    # ユーザーのログインName
    userid=getEmployeeInfo(loginid)['id']
    # ログインNameでユーザーの詳細情報を取得
    url="http://redmine.trechina.cn/issues.json?key=3677a9378645bf393c08579ee395fe7c5dba5586&assigned_to_id="+str(userid)
    resultIssue=com.getWSdata(url)
    arrIss = []
    for iss in resultIssue['issues']:
        pjid=iss['project']["id"]
        # 一回判断をつけたPJを再度判断しないように
        urlpj="http://redmine.trechina.cn/projects/"+str(pjid)+".json?key=3677a9378645bf393c08579ee395fe7c5dba5586"
        resultPj=com.getWSdata(urlpj)
        for custf in resultPj['project']['custom_fields']:
            if custf["name"]=="PJCD" and custf["value"]!="" :
                    arrIss.append(iss)
    return json(arrIss)

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
    wt=request.args.get('wt')
    # url="http://10.2.1.171/system/api/PMMSS003"
    url="http://172.17.6.81/time_entries.json?key=3677a9378645bf393c08579ee395fe7c5dba5586"
    pars={"time_entry": {"issue_id": "20052","spent_on": "2019-07-25","hours": "10","activity_id": "13","comments": "test"}}
    result=com.postWSdata(url,pars)
    
    return json(result)


def getEmployeeInfo(loginid):
    # ログインNameでユーザーの詳細情報を取得
    url="http://redmine.trechina.cn/users.json?key=3677a9378645bf393c08579ee395fe7c5dba5586&name="+loginid
    result=com.getWSdata(url)
    return result['users'][0]

