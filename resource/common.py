import configparser
import os
from io import BytesIO 
from sanic.response import json, text, html,raw
from jinja2 import Environment, PackageLoader, FileSystemLoader
import xlwt
import requests,json

# env = Environment(loader=PackageLoader('src.my_blueprint', 'templates'))
env = Environment(loader=FileSystemLoader('./templates'))

# description:  sysconfを取得
# parameters:   sec:conf名 key:confのKey    例：getConfig('conn_default','database')
# return:       keyのvalueを返還
def getConfig(sec, key):
    conf = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/sys.conf'
    conf.read(path)
    return conf.get(sec, key)

# description:  html画面に移行する
# parameters:   ①パラメーター1つ：そのまま指定された画面に移行　例：bindHtml('index.html')
#               ②パラメーター2つ：指定された画面にjsonデータをバインドする  例：bindHtml('index.html',jsondata)
# return:       なし
def bindHtml(*args):
    thtml = ''
    data = {}
    if len(args) > 2:
        return text('err')
    if len(args) > 0:
        thtml = args[0]
    if len(args) > 1:
        data = args[1]
    template = env.get_template(thtml)
    content = template.render(data)
    return html(content)

# description:  WebAPIのデータを取得する（Get）
# parameters:   url：取得先のURL　例：getWSdata('10.10.10.10/api')
# return:       取得データ
def getWSdata(url):
    r=requests.get(url)
    response_dict=r.json()
    # repo_dicts=response_dict['users']
    return response_dict

# description:  WebAPIのデータを取得する（Post）
# parameters:   url：取得先のURL　例：getWSdata('10.10.10.10/api')
# return:       取得データ
def postWSdata(url,pars):
    r=requests.post(url,json.dumps(pars))
    return r.json()

# description:  Excelのスタイルを設定する
# parameters:   なし
# return:       style:タイトル部 style1:データ部スキン style2:警告部スキン
def format_excel_style():
    # border
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.bottom_colour = 0x3A
    # タイトル部背景色
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
    # データ部背景色
    pattern1 = xlwt.Pattern()
    pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern1.pattern_fore_colour = xlwt.Style.colour_map['silver_ega']
    # 警告部背景色
    pattern2 = xlwt.Pattern()
    pattern2.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern2.pattern_fore_colour = xlwt.Style.colour_map['red']
    # タイトル部スキン
    style = xlwt.XFStyle()  # ディフォルトスキン
    font = xlwt.Font()  # font
    font.name = 'Times New Roman'
    font.bold = True
    font.height = 240
    style.font = font  # fontを設定
    style.borders = borders
    style.pattern = pattern
    # データ部スキン
    style1 = xlwt.XFStyle()  # ディフォルトスキン
    font1 = xlwt.Font()  # font
    font1.name = 'Times New Roman'
    font1.height = 240
    style1.font = font1  # fontを設定
    style1.borders = borders
    style1.pattern = pattern1
    # 警告部スキン
    style2 = xlwt.XFStyle()  # ディフォルトスキン
    style2.font = font1  # fontを設定
    style2.borders = borders
    style2.pattern = pattern2
    return style, style1, style2

# description:  Excelを作成し、ダウンロードする
# parameters:   ①strJson：ExcelでダウンロードしとうとしたJsonデータ　例：jsonToXls(jsondata)
#               ②パラメーター２つ：Jsonデータとファイル名  例：jsonToXls(jsondata,'myfilename')
#               ③パラメーター２つ：Jsonデータ、ファイル名、シート名  例：jsonToXls(jsondata,'myfilename','mysheetname')
# return:       Excelファイル
def jsonToXls(strJson,*filePara):
    dFileName = "DownLoadFile"
    dSheetName = "Sheet1"
    if type(strJson) != list and len(strJson)==0 :
        return text('err')
    if len(filePara) > 2:
        return text('err')
    if len(filePara) > 0:
        dFileName = filePara[0]
    if len(filePara) > 1:
        dSheetName = filePara[1]
    dFileName=dFileName+".xls"

    header_style,data_style,error_style = format_excel_style()
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(dSheetName)
    rows=strJson
    col = 0
    keyarr=rows[0].keys()
    for key in keyarr:
        sheet.write(0,col, key,header_style)
        col = col+1
    row = 1
    for tmprow in rows:
        list_data = tmprow.values()
        style_data = error_style
        style_data = data_style
        col = 0
        for key in keyarr:
            sheet.write(row,col, tuple(list_data)[col],style_data)
            col = col + 1
        row=row + 1
    # wb.save("/home/test.xls")
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return raw(output.getvalue(),headers={'Content-Disposition':'attachment;filename='+dFileName},content_type='application/vnd.ms-excel')
