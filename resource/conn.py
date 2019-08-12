# database #
# import uvloop, peewee
from peewee_async import PostgresqlDatabase
from peewee_async import MySQLDatabase
from resource.common import getConfig
from bs4 import BeautifulSoup
from sanic import Blueprint
import os
import json
import math
# import aioodbc
import pyodbc


class DBHelper:
    __SUCCESS_CODE = "1"
    def __init__(self,mapname):
        self.mapname = mapname[mapname.rfind('.')+1:]

    # description:  DBへの接続Connectを取得
    # parameters:   ①パラメーターなし：[conn_default]に書かれた情報でDBに接続　
    #               ②パラメーター1つ：指定するConf名でDBに接続 
    #               ※ Keyの説明 
    #               dbtype:サポートされたDB種類　----　pgsql:PostgreSQL　mysql:MySQL
    #               database:接続先のDB名 
    #               host:接続先のIPorHost
    #               user:アカウント 
    #               password:パスワード 
    # return:       接続済みのConnect
    def __conn(self,*args):
        if len(args) == 0:
            db = PostgresqlDatabase(database=getConfig('conn_default','database'),
                                host=getConfig('conn_default','host'),
                                user=getConfig('conn_default','user'),
                                password=getConfig('conn_default','password'))
        elif len(args) == 1:
            conn_key=str(args[0])
            if conn_key=="":
                conn_key="conn_default"
            dbtype = getConfig(conn_key,'dbtype')
            if dbtype=='pgsql':
                db = PostgresqlDatabase(database=getConfig(conn_key,'database'),
                    host=getConfig(conn_key,'host'),
                    user=getConfig(conn_key,'user'),
                    password=getConfig(conn_key,'password'))
            elif dbtype=='mysql':
                db = MySQLDatabase(database=getConfig(conn_key,'database'),
                    host=getConfig(conn_key,'host'),
                    user=getConfig(conn_key,'user'),
                    password=getConfig(conn_key,'password'))
            elif dbtype=='mssql':
                dsn = 'DRIVER={%s};SERVER=%s;DATABASE=QCDDB;UID=read;PWD=' % pyodbc.drivers()[1],getConfig(conn_key,'database'),getConfig(conn_key,'host'),getConfig(conn_key,'user'),getConfig(conn_key,'password')

        return db

    # description:  パラメーターにより、クエリの条件やConnectを返還する
    # parameters:   ①パラメーター1つ：データタイプより、ConnectKeyかクエリの条件を返還する。str→ConnectKey、dict→クエリ条件
    #               ②パラメーター２つ：ConnectKey、クエリ条件同時に指定
    # return:       クエリ条件、ConnectKey
    def getMapPars(self,args):
        pars={}
        conn_key=''
        if len(args)==0 :
            pass
        elif len(args)==1 :
            # パラメータ一つのみ、かつstringタイプの場合は、Conの指定と見なす
            if type(args[0])==str:
                conn_key=args[0]
            # パラメータ一つのみ、かつjsonタイプの場合は、クエリの条件と見なす
            elif type(args[0])==dict:
                pars=args[0]
        elif len(args)==2 :
            pars=args[0]
            conn_key=args[1]
        return pars,conn_key
        
    # description:  Mapでselectを実行
    # parameters:   ①パラメーター1つ：無条件でSelectを実行する　例：selectByMap('selt1')
    #               ②パラメーター２つ：ConnectKey指定の場合は無条件でSelectを実行する　例：selectByMap('selt1','connect_1')
    #               　　　　　　　　　　検索条件指定の場合はディフォルトConnectで条件つけでSelectを実行する　　例：selectByMap('selt1',{name:'limingze',sex:1})
    #               ③パラメーター３つ：検索条件、ConnectKey両方指定　例：selectByMap('selt1',{name:'limingze',sex:1},'connect_1')
    # return:       検索結果（Json）
    def selectByMap(self,sqlid,*args):
        pars,conn_key=self.getMapPars(args)
        db = self.__conn(conn_key)
        sqls=self.getSQL(sqlid, 'select',pars)
        print('\n###sql###:'+sqls+'\n')
        jsonResult = {'Code':self.__SUCCESS_CODE}
        sqlarr=sqls.split(';')
        tablenum=0
        for sql in sqlarr:
            if sql=='' or sql.isspace() :
                continue
            cursor = db.execute_sql(sql) 
            jsonTable = []
            for row in cursor.fetchall():
                jsonRow={}
                for i in range(len(cursor.description)):
                    col=cursor.description[i][0]
                    jsonRow[col]=row[i]
                jsonTable.append(jsonRow)
            # jsonResult.append({'Table'+str(tablenum):jsonTable})
            jsonResult['Table'+str(tablenum)]=jsonTable
            tablenum=tablenum+1
        db.close()
        return jsonResult

    # description:  JsonデータでInsertを実行
    # parameters:   tbl:插入先テーブル名　strJson:插入データ
    #               例：   insJson('table1',[{"id":996,"name":"limingze"},{"id":998,"name":"haruya"}])
    #               　　　　　　　　　　検索条件指定の場合はディフォルトConnectで条件つけでSelectを実行する　　例：selectByMap('selt1',{name:'limingze',sex:1})
    # return:       影響行数
    def insJson(self,tbl,strJson,*args):
        # db = self.__conn()
        pars,conn_key=self.getMapPars(args)
        db = self.__conn(conn_key)
        print(pars)
        cursor = db.get_cursor()
        columns = ''
        placeholders = ''
        vallist=[]
        if type(strJson) == list:
            columns = ', '.join(list(strJson[0].keys()))
            placeholders = ', '.join(['%s'] * len(strJson[0]))
            for sj in strJson:
                vallist.append(tuple(sj.values()))
        else:
            placeholders = ', '.join(['%s'] * len(strJson))
            columns = ', '.join(list(strJson.keys()))
            vallist.append(tuple(strJson.values()))
        # sql = "INSERT INTO %s ( %s ) VALUES ( %s ) RETURNING id;" % (tbl, columns, placeholders)
        sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (tbl, columns, placeholders)
        try:
            cursor.executemany(sql, vallist)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            db.close()
            raise
        db.close()
        return {'Code':self.__SUCCESS_CODE,'Table0':cursor.rowcount}

    # description:  Mapでdeleteを実行
    # parameters:   ①パラメーター1つ:無条件でDeleteを実行する　例:deleteByMap('del1')
    #               ②パラメーター２つ:ConnectKey指定の場合は無条件でDeleteを実行する　例:deleteByMap('del1','connect_1')
    #               　　　　　　　　　　検索条件指定の場合はディフォルトConnectで条件つけでDeleteを実行する　　例:deleteByMap('del1',{name:'limingze',sex:1})
    #               ③パラメーター３つ:検索条件、ConnectKey両方指定　例:deleteByMap('del1',{name:'limingze',sex:1},'connect_1')
    # return:       影響行数
    def deleteByMap(self,sqlid,*args):
        # db = self.__conn()
        # sql=self.getSQL(sqlid, 'delete',pars)
        pars,conn_key=self.getMapPars(args)
        db = self.__conn(conn_key)
        sql=self.getSQL(sqlid, 'delete',pars)
        print('\n###sql###:'+sql+'\n')
        cursor = db.get_cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        return {'Code':self.__SUCCESS_CODE,'Table0':cursor.rowcount}

    # description:  Mapでupdateを実行
    # parameters:   ①パラメーター1つ:無条件でUpdateを実行する　例:deleteByMap('del1')
    #               ②パラメーター２つ:ConnectKey指定の場合は無条件でUpdateを実行する　例:updateByMap('update1','connect_1')
    #               　　　　　　　　　　検索条件指定の場合はディフォルトConnectで条件つけでUpdateを実行する　　例:updateByMap('update1',{name:'limingze',sex:1})
    #               ③パラメーター３つ:検索条件、ConnectKey両方指定　例:updateByMap('update1',{name:'limingze',sex:1},'connect_1')
    # return:       影響行数
    def updateByMap(self,sqlid,*args):
        # db = self.__conn()
        # sql=self.getSQL(sqlid, 'update',pars)
        pars,conn_key=self.getMapPars(args)
        db = self.__conn(conn_key)
        sql=self.getSQL(sqlid, 'update',pars)
        print('\n###sql###:'+sql+'\n')
        cursor = db.get_cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        return {'Code':self.__SUCCESS_CODE,'Table0':cursor.rowcount}

    # description:  DBにExeを実行
    # parameters:   ①パラメーター1つ:無条件でUpdateを実行する　例:deleteByMap('del1')
    #               ②パラメーター２つ:ConnectKey指定の場合は無条件でUpdateを実行する　例:updateByMap('update1','connect_1')
    # return:       実行結果
    def exe(self,sql,*args):
        # db = self.__conn()
        pars,conn_key=self.getMapPars(args)
        pars="これからSqlのパラメーター化にするかもしれない、[0][1]みたいな"
        print(pars)
        db = self.__conn(conn_key)
        cursor = db.get_cursor()
        n=cursor.execute(sql)
        db.commit()
        db.close()
        return n
        
    def sql_filter(self,val):
        val = str(val)
        dirty_stuff = ["\"", "\\", "/", "'", ]
        for stuff in dirty_stuff:
            val = val.replace(stuff, "")
        return val
   
    def getSQL(self,sqlid, sqltype,pars):
        path = os.path.split(os.path.realpath(__file__))[0] + '/sqlmap/'+self.mapname+'.xml'
        soup = BeautifulSoup(open(path,encoding='utf-8'),"html.parser")
        strsql=""
        selsqls = soup.find_all(sqltype)
        for selsql_El in selsqls:
            if selsql_El.attrs['id']==sqlid :
                for content in selsql_El.contents:
                    if content.name == 'isnotnull':
                        if content.attrs['key'] in pars:
                            _col=content.attrs['key']
                            if pars[_col] != "" :
                                strsql = strsql + content.text
                    elif content.name == 'isnull':
                        if content.attrs['key'] in pars :
                            _col=content.attrs['key']
                            if pars[_col] == "" :
                                strsql = strsql + content.text
                    else:
                        strsql = strsql + content
        for key in pars:
            keyinsql1 = "#{"+key + "}"
            keyinsql2 = "${"+key + "}"
            strsql = strsql.replace(keyinsql1, str("'"+self.sql_filter(pars[key])+"'")).replace(keyinsql2, str(pars[key]))
        return strsql.replace('\n','').strip().replace('      ',' ').replace('    ',' ').replace('\t',' ')


    # global db
    # db = PostgresqlDatabase(database=getConfig('pgdb','database'),
    #                               host=getConfig('pgdb','host'),
    #                               user=getConfig('pgdb','user'),
    #                               password=getConfig('pgdb','password'))

    # def getSQL(self,sqlid, sqltype,pars):
    #     path = os.path.split(os.path.realpath(__file__))[0] + '/sqlmap/'+self.mapname+'.xml'
    #     root = ElementTree.parse(path)
    #     subEls = root.getiterator(sqltype)
    #     strsql = ''
    #     for subEl in subEls:
    #         if subEl.attrib['id']==sqlid :
    #             strsql = subEl.text.replace('\n','').strip().replace('      ',' ').replace('    ',' ')
    #     for key in pars:
    #         keyinsql1 = "#{"+key + "}"
    #         keyinsql2 = "${"+key + "}"
    #         strsql = strsql.replace(keyinsql1, str("'"+self.sql_filter(pars[key])+"'")).replace(keyinsql2, str(pars[key]))
    #     return strsql

    # def sel(self,sql):
    #     db = self.__conn()
    #     print('\n###sql###:'+sql+'\n')
    #     cursor = db.execute_sql(sql) 
    #     jsonResult = []
    #     for row in cursor.fetchall():
    #         jsonRow={}
    #         for i in range(len(cursor.description)):
    #             col=cursor.description[i].name
    #             jsonRow[col]=row[i]
    #         jsonResult.append(jsonRow)
    #     db.close()
    #     return jsonResult

    # def insJson(self,tbl,strJson):
    #     db = self.__conn()
    #     # strJson = {"id":"996","name":"heiheihei"}
    #     cursor = db.get_cursor()
    #     placeholders = ', '.join(['%s'] * len(strJson))
    #     columns = ', '.join(list(strJson.keys()))
    #     sql = "INSERT INTO %s ( %s ) VALUES ( %s ) RETURNING id;" % (tbl, columns, placeholders)
    #     cursor.execute(sql, list(strJson.values()))
    #     db.commit()
    #     item = cursor.fetchone()
    #     db.close()
    #     return item[0]