import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# 'auth'という青写真を作成．アプリオブジェクト同様に__name__で定義する場所を指定．url_prefixでこの青写真と関連するURLの先頭に'/auth'を付与．
bp = Blueprint('auth', __name__, url_prefix='/auth')  # これをアプリ(__init__)で登録．


# ユーザ認証用のBluePrintの登録
@bp.route('/register', methods=('GET', 'POST'))  # @bp.routeにより/registerURLとregister関数を関連付け
# ユーザ登録の関数
def register():
    # ユーザがフォームをsubmitしようとすると，methodはPOSTになる．その場合はフォームの検証を走らせる．
    if request.method == 'POST':
        username = request.form['username']  # 提出されたformのキーと値を対応させる．
        password = request.form['password']
        db = get_db()  # get_db()のreturnはg.db
        error = None  # Initialized error

        # 入力データに不備がある場合
        if not username:
            error = 'ユーザ名を入力しやがれください．'
        elif not password:
            error = 'パスワードをにゅうりょくしやがれください．'
        # ユーザが既に登録されている場合
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)  # ユーザの登録状況をＤＢに問い合わせ，結果が返るか検証．db.executeは、ユーザのどの入力にも対応するプレースホルダ?
            # を持つSQLのqueryと、プレースホルダを置き換える値のtupleを受け取り，データベースライブラリはSQLインジェクション攻撃に対して脆弱にならないように、値のエスケープを取り計らう。
        ).fetchone() is not None:  # fetchoneはqueryの結果から１行を返す．何もなければNoneを返す．
            error = '{}は既に登録されています．'.format(username)

        # エラーがなければユーザを登録．パスワードはhash化
        if error is None:
            # dbでqueryをexecute(実行)する
            db.execute(
                'INSERT INTO user (username, password) VALUES (?,?)',
                (username, generate_password_hash(password))  # generate_password_hashにより，パスワードをDBに直接格納せずにハッシュとして格納
            )
            # dbに変更をコミット
            db.commit()
            # 登録完了後はログイン後画面にリダイレクト
            return redirect(url_for('auth.login'))

        # エラーがあればそれを表示．flash()はテンプレを変換(render_template)するときに取得可能なメッセージを格納できる．
        flash(error)

    return render_template('auth/register.html')


# ログイン用BluePrint
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # ユーザ情報は先に問い合わせして検証，
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        if user is None:
            error = 'ユーザー名が間違っているか，登録されていません．'

        # check_password_hash()でDBに格納されているパスワード(user['password'])と
        # フォームに入力されたパスワード(request.form['password'])を検証
        elif not check_password_hash(user['password'], password):
            error = 'パスワードがまちがってまっせ．'
        elif error is None:
            session.clear()
            # sessionはリクエストをまたいで格納されるデータのdict．検証成功時，userのidを初期化したsessionに格納する．
            # これはブラウザへ送信されるCookieに格納し，以降のリクエストでCookieを送信し返すことができる．(他のViewからも使用可能となる．)
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# どのURLがリクエストされたかにかかわらず，Viewの関数の前に実行する関数を登録
@bp.before_app_request
# ユーザidがsession，もしくはDBに格納されているかを確認する関数（ログインの確認）なければg.userはNone
def load_logged_in_user():
    user_id = session.get('user_id')

    # ユーザidがsessionにない場合
    if user_id is None:
        g.user = None
    # ユーザidがデータベースにあるか確認
    else:
        # ユーザidを，リクエスト期間中保持できるg.userへ格納する．
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# ログアウト
@bp.route('/logout')
def logout():
    # sessionからユーザidを取り除く
    session.clear()
    # ホーム画面へ
    return redirect(url_for('qamenu.index'))


# 他のViewでの認証の要求のためのデコレータの作成
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    # 認証を適用した新しいViewをwrapped_viewとして返す．
    return wrapped_view
