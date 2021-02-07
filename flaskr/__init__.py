import os
from flask import Flask


def create_app(test_config=None):
    # Appの作成と設定(application factory)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # Deploy時には乱数で上書き
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),  # データベースファイルの保存場所
    )

    if test_config is None:
        # もしインスタンスフォルダにconfig.pyがあれば，値を底から取り出して上書きする．デプロイ時のSECRET_KEYを設定できる
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # アプリのインスタンスフォルダが確実に存在するように設定．Flaskでは自動作成されない．
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    # データベースの初期化
    from . import db
    db.init_app(app)

    # BluePrintの登録(factory関数の最後で，appを返す直前に置く．)
    from . import auth
    app.register_blueprint(auth.bp)

    from . import qamenu
    app.register_blueprint(qamenu.bp)
    app.add_url_rule('/', endpoint='index')

    return app
