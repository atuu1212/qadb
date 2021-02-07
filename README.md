### 秘密鍵（Secret Key）の設定

`$ python -c 'import os; print(os.urandom(16))'`


### 本番環境サーバでの実行

`$ pip install waitress`

```
$ waitress-serve --call 'flaskr:create_app'

Serving on http://0.0.0.0:8080
```