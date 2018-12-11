# モジュールのインポート
import json
import urllib.request
import pandas as pd

# API に渡すパラメータの値の指定
url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"
key = "5e7d5d18655d2a151e83b2c92950d967" 

# API を使う関数の定義
def GnaviApi():
    params = urllib.parse.urlencode({
        'keyid': key,
        'latitude' : '35.156110',
        'longitude' : '136.926681',
        'range' : '1',
    })
    response = urllib.request.urlopen(url + '?' + params)
    return response.read()

data = GnaviApi()

readData = json.loads(data)["rest"]

def GetData(readData, key):
    ln = []
    for dic in readData:
        ln.append(dic.get(key))
    return ln

# 取得したいキー
# code = ['latitude', 'longitude', 'name', 'category']

def GetDf(code):
    df = pd.DataFrame([])
    for i in code:
        ln = GetData(readData, i)
        df.merge(ln)

lat = GetData(readData, 'latitude')
lon = GetData(readData, 'longitude')
name = GetData(readData, 'name')
cat = GetData(readData, 'category')
df = pd.DataFrame([lat, lon, name, cat])

print(df)