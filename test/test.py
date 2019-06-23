# import xml.dom.minidom as xmldom
import os
from bs4 import BeautifulSoup
# from xml.etree import ElementTree

def sql_filter(val):
    val = str(val)
    dirty_stuff = ["\"", "\\", "/", "'", ]
    for stuff in dirty_stuff:
        val = val.replace(stuff, "")
    return val

# def iftosql(ifEls):
#     for ifEl in ifEls:
def getSQL(sqlid, sqltype,pars):
    soup = BeautifulSoup(open(os.path.split(os.path.realpath(__file__))[0]+'/aaa.xml'),"html.parser")
    strsql=""
    selsqls = soup.find_all("select")
    for selsql_El in selsqls:
        if selsql_El.attrs['id']==sqlid :
            for content in selsql_El.contents:
                if content.name == 'isnotnull':
                    if content.attrs['col'] in pars:
                        _col=content.attrs['col']
                        if pars[_col] != "" :
                            strsql = strsql + content.text
                elif content.name == 'isnull':
                    if content.attrs['col'] in pars :
                        _col=content.attrs['col']
                        if pars[_col] == "" :
                            strsql = strsql + content.text
                else:
                    strsql = strsql + content

    for key in pars:
        keyinsql1 = "#{"+key + "}"
        keyinsql2 = "${"+key + "}"
        strsql = strsql.replace(keyinsql1, str("'"+sql_filter(pars[key])+"'")).replace(keyinsql2, str(pars[key]))
    return strsql





pars = {'usrname': 10120869, 'pwd': 'wing'}

# print(getSQL('selectuser', 'select',pars))
print(getSQL('selectuser', 'select',pars))




            # if_Els=selsql_El.select('isNotNull')
            # for if_El in if_Els:
            #     # カラムがパラメータに存在する場合
            #     if if_El.attrs['col'] in pars :
            #         strcol=if_El.attrs['col']
            #         if_str=if_El.text
            #         if pars[strcol] != "" :
            #             _s = str(sqlsql_str).find("<isnotnull")
            #             _e = str(sqlsql_str).find("</isnotnull>") + len("</isnotnull>")
            #             oldstr=sqlsql_str[_s:_e]
            #             newstr=if_str
            #             selsql_El=sqlsql_str.replace(oldstr,newstr)
            #             strsql = str(selsql_El).replace('\n','').strip().replace('      ',' ').replace('    ',' ')
            




# sss = '1234<isNotNull col="usrname">           and ( CUS_CUSTOMER_TBL.CUS_WEB_FROM LIKE #{usrname})        1</isNotNull> and wing'

# sss1 = sss.find("<isNotNull")
# sss2 = sss.find("</isNotNull>") + len("</isNotNull>")

# print(sss1)
# print(sss2)
# print(sss[sss1:sss2])



















# str1 = 'sss.src.aaaa'
# i = str1.rfind('.')
# print(i)
# print(str1[i+1:])





# soup = BeautifulSoup(open(os.path.split(os.path.realpath(__file__))[0]+'/aaa.xml'),"html.parser")

# els = soup.find_all("select")

# for el in els:
#     print(el)

# print(els)