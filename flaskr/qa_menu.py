from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('qa_menu', __name__)


@bp.route('/')
def index():
    db = get_db()
    categories = db.execute(
        'SELECT cat.id, category_name, author_id, detail, created, updated, username'
        ' FROM qacategories cat JOIN user u ON cat.author_id = u.id'
        ' ORDER BY category_name DESC'
    ).fetchall()
    return render_template('qa_menu/index.html', categories=categories)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        category = request.form['category_name']
        detail = request.form['detail']
        error = None

        if not category:
            error = '項目名をにゅうりょくしてください．'
        if not detail:
            error = '詳細をにゅうりょくしてくだちい．'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO qacategories (category_name, detail, author_id)'
                ' VALUES (?,?,?)',
                (category, detail, g.user['id'])
            )
            db.commit()
            return redirect(url_for('qa_menu.index'))

    return render_template('qa_menu/create.html')


def get_qacategory(id, check_author=True):
    category = get_db().execute(
        'SELECT cat.id, category_name, detail, created, updated, author_id, username'
        ' FROM qacategories cat JOIN user u ON cat.author_id = u.id'
        ' WHERE cat.id = ?',
        (id,)
    ).fetchone()

    # abort()によりHTTPのステータスコードを返す．エラーとともにオプションでメッセージを引き取る．
    if category is None:
        abort(404, '項目(Category)ID{0}は存在しません．'.format(id))  # 404はNot Found

    if check_author and category['author_id'] != g.user['id']:
        abort(403)  # 403はForbidden(禁止)

    return category


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    category = get_qacategory(id)

    if request.method == 'POST':
        category = request.form['category_name']
        detail = request.form['detail']
        error = None

        if not category:
            error = '項目名をにゅうりょくしてくだちい'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'UPDATE qacategories SET category_name = ?, detail = ?'
                ' WHERE id = ?',
                (category, detail, id)
            )
            db.commit()
            return redirect(url_for('qa_menu.index'))

    return render_template('qa_menu/update.html', category=category)


# 削除の関数．テンプレートはなしで．
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_qacategory(id)
    db = get_db()
    db.execute('DELETE FROM qacategories WHERE id = ?', (id,))
    db.commit()
    # テンプレ作ってないのでPOSTだけ処理してindexへ飛ばす
    return redirect(url_for('qa_menu.index'))
