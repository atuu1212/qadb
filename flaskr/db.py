import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


# データベース取得のための関数
def get_db():
    """
    gおぶじぇくとはリクエストの処理中に複数の関数によってアクセスされるような
    データを格納するための，リクエストごとに個別のもの．
    """

    # gに'db'が登録されていない場合は作成．
    if 'db' not in g:
        g.db = sqlite3.connect(
            # 現在リクエスト処理中のFlaskアプリをデータベースに接続
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # dictのようにふるまう行を取得する．これにより列名による列へのアクセスが可能となる．
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    # gから'db'の要素を削除し，呼び出し元にその値をかえすpop
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# アプリを受け取って登録する関数の定義
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)