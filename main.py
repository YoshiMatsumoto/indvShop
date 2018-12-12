# モジュールのインポート
import json
import urllib.request
import pandas as pd
import folium

# API を使う関数の定義
def GnaviApi(key, lat, lon, url):
    params = urllib.parse.urlencode({
        'keyid': key,
        'latitude' : lat,
        'longitude' : lon,
        'range' : '2',
    })
    response = urllib.request.urlopen(url + '?' + params)
    return response.read()

# 特定のキーのものを取り出す
def GetData(readData, key):
    ln = []
    for dic in readData:
        ln.append(dic.get(key))
    return ln

# データフレームにする
def GetDf(code, readData):
    df = pd.DataFrame(index=[])
    for i in code:
        ln = GetData(readData, i)
        ln = pd.Series(ln)
        df = df.append(ln, ignore_index=True)
    return df.T

def Address(path):
    ad = pd.read_csv(path, ',', header=None, names=('name', 'lat', 'lon'))
    return ad

def main():
    ad = Address('station.csv')
    # API に渡すパラメータの値の指定
    url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"
    key = "5e7d5d18655d2a151e83b2c92950d967" 

    allDf = pd.DataFrame(index=[])

    # 各地下鉄駅でループ
    for i in range(len(ad)):
        lat = ad['lat'][i]
        lon = ad['lon'][i]

        # データの取得
        data = GnaviApi(key, lat, lon, url)
        # データから取り出す
        readData = json.loads(data)["rest"]
        code = ['latitude', 'longitude', 'name', 'category']
        df = GetDf(code, readData)
        allDf = pd.concat([allDf, df], ignore_index=True)

    # csvとして出力
    allDf.to_csv('df.csv')

if __name__ == '__main__':
    main()