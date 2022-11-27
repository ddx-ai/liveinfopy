# live_info_api_client_py

## Dependencies

- Python 3.10

```
python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt
```

## Usage

### ニコニコ生放送 `live.nicovideo.jp`

```shell
# 番組 （ 月刊ニコニコインフォチャンネル https://live.nicovideo.jp/watch/lv339313375 ）
python3 main.py -s nicolive "lv339313375"

# コミュニティ （ ニコニコ動画プレミアムアワード https://com.nicovideo.jp/community/co5683564 ）
python3 main.py -s nicolive "co5683564"

# ユーザー （ ニコニコプレミアムDAY https://www.nicovideo.jp/user/123430062 ）
python3 main.py -s nicolive "user/123430062"

# ニコニコチャンネル （ウェザーニュースチャンネル https://ch.nicovideo.jp/weathernews ）
python3 main.py -s nicolive "ch1072"
```

#### 期待される挙動と既知の問題

放送中の番組がある場合、その番組を返します。

最後に放送した番組がある場合、その番組を返します。
番組が放送中かどうか判定するには、放送開始時間（`start_date`）と放送終了時間（`end_date`）および現在時刻が利用できます。

番組ID（`lv*`）ではなく、コミュニティID（`co*`）やユーザID（`user/*`）、ニコニコチャンネルID（`ch*`）を渡した場合、`https://live.nicovideo.jp/watch/*`に各IDを設定したときと同じ挙動をします。

既知の問題として、ニコニコ公式チャンネルの[月刊ニコニコインフォチャンネル](https://ch.nicovideo.jp/weekly-niconico-info)が放送中でないときに上記操作をしたとき、番組が存在しない（`not_found`）扱いになることが確認されています。
これはニコニコまたは当該チャンネルの仕様として、修正は考えていません。


```shell
# Return not_found (at least not-onair status)

# ニコニコチャンネル （月刊ニコニコインフォチャンネル https://ch.nicovideo.jp/weekly-niconico-info ）
python3 main.py -s nicolive "ch2646073"
```

## 既知のAPI

現在このプログラムでは使用していませんが、以下のAPIが利用できる可能性があります。

- `https://com.nicovideo.jp/api/v1/communities/{community_id}/lives/onair.json`
  - コミュニティで放送中の番組を返す（コミュニティ個別ページの放送Alert表示用）
  - `{community_id}`には、コミュニティID`co*`の数値部分（`*`）が入ります
