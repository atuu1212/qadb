import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # 一時ファイルを作成して開き，そのfileオブジェクトとパスを返す．
    # DATABASEのパスは上書きされ，インスタンスフォルダの代わりに一時ファイルのパスをさす．
    # テスト終了後削除される．
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,  # テストモードであることをFlaskへ伝える
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


# test用のアプリケーションオブジェクト（クライアント）の作成．
# サーバを起動せずにアプリへのリクエストを作成できる
@pytest.fixtre
def client(app):
    return app.test_client()


# appに登録されたClickのコマンドを呼び出し可能なrunnerを作成．
@pytest.fixtre
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)