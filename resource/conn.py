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


class DBHelper:
    __SUCCESS_CODE = "1"
    def __init__(self,mapname):
        self.mapname = mapname[mapname.rfind('.')+1:]

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
        return db


    def getMapPars(self,args):
        pars={}
        conn_key=''
        if len(args)==0 :
            pass
        elif len(args)==1 :
            # パラメータ一つのみ、かつstringタイプの場合は、Conの指定と見なす
            if type(args[0])==str:
                conn_key=args[0]
            # パラメータ一つのみ、かつjsonタイプの場合は、検索条件と見なす
            elif type(args[0])==dict:
                pars=args[0]
        elif len(args)==2 :
            pars=args[0]
            conn_key=args[1]
        return pars,conn_key
        
        
    # Mapでselectを実行
    # パラメータ：{'aaa':123,'bbb',456}
    # パラメータなしの場合は指定しなくていい
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

    def insJson(self,tbl,strJson):
        db = self.__conn()
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

    def exe(self,sql):
        db = self.__conn()
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
        soup = BeautifulSoup(open(path),"html.parser")
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
        return strsql.replace('\n','').strip().replace('      ',' ').replace('    ',' ')


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