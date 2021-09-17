import pandas as pd
df = pd.read_csv('base.csv', encoding="shift_jis")

df_rm = df.index[df.name.str.contains(
    "マクドナルド|モスバーガー|バーガーキング|ウェンディーズ|ロッテリア|フレッシュネスバーガー|ファーストキッチン|ケンタッキー|吉野家|松屋|すき家|なか卯|ガスト|デニーズ|ロイヤルホスト|ローソン|ほっともっと|ココス|スターバックス|幸楽苑|スシロー|ピザハット|ドミノピザ|ピザーラ|ほっかほっか亭|ジョナサン|サブウェイ|いきなりステーキ|丼丸|大漁丼家|魚丼|てんや",na=False
    )]
df = df.drop(df_rm)
df.to_csv('aaa.csv')
