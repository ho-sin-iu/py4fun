import requests, json
import pandas as pd
import datetime as dt

path_exch  = 'https://www.twse.com.tw/exchangeReport/'
path_fund  = 'https://www.twse.com.tw/fund/'
istest = False

#=================================================

def get_infoType():
	prompt = """請選擇交易資訊：
1: 個股日本益比、殖利率、股淨比(以個股月查詢)
2: 個股日成交資訊
3: 類股盤後定價資訊
4: 類股融資融券彙總資訊
5: 信用額度總量管制餘額總表
61: 外資買賣超彙總表
62: 投信買賣超彙總表
63: 自營商買賣超彙總表
"""
	infoType = int(input(prompt))
	return infoType


def get_stockNo(testing=False):
	if testing == False:
		stockNo = input('請輸入股票代號: ')
		return stockNo
	else:
		return '2330'

def get_date(testing=False):
	if testing == False:
		qdate = input('請輸入查詢日期 (格式: YYYYMMDD) 或輸入 T 查詢今天: ')
		if qdate == 'T' or qdate == 't':
			today = dt.date.today()
			qdate = dt.datetime.strftime(today, '%Y%m%d')
			print(f'today = {qdate}')
		return  qdate
	else:
		return '20240712'

def get_selectType(testing=False):
	if testing == False:
		selectType = input('請輸入分類群組: ')
		return selectType
	else:
		return '24'

#=================================================

infoType = get_infoType()

APIs = {1: 'BWIBBU', 
		2: 'STOCK_DAY',
		3: 'BFT41U',
		4: 'MI_MARGN',
		5: 'TWT93U',
		61: 'TWT38U',
		62: 'TWT43U',
		63: 'TWT44U'} 

qdate = get_date(istest)
if infoType in [61, 62, 63]:
	query = f'?response=json&date={qdate:s}'
	url = path_fund + APIs[infoType] + query
else:
	if infoType in [1, 2]:
		stockNo = get_stockNo(istest)
		query = f'?response=json&date={qdate:s}&stockNo={stockNo:s}'
	elif infoType in [3, 4]:
		selectType = get_selectType(istest)
		query = f'?response=json&date={qdate:s}&selectType={selectType:s}'
	elif infoType in [5]:
		query = f'?response=json&date={qdate:s}'
	else:
		query = ''
	url = path_exch + APIs[infoType] + query



print('正在爬蟲', url, '')

html = requests.get(url)


if html.status_code == requests.codes.ok:
	print('爬蟲成功 :)\n')
else:
	print('爬蟲失敗 :()\n')



jcontent = json.loads(html.text)
print()

print(jcontent['title'])
print('-' * 120)
df = pd.DataFrame(jcontent['data'], columns=jcontent['fields'])
print(df)

fieldname_dict = {3:'證券代號', 4:'股票代號', 5:'代號', 61:'證券代號', 62:'證券代號', 63:'證券代號'}

if infoType in [3,4,5,61,62,63]:
	stockNo = get_stockNo(istest)
	print(df[df[fieldname_dict[infoType]]==stockNo].T)


