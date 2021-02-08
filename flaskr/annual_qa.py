import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# 'auth'という青写真を作成．アプリオブジェクト同様に__name__で定義する場所を指定．url_prefixでこの青写真と関連するURLの先頭に'/auth'を付与．
bp = Blueprint('annual_qa', __name__, url_prefix='/annual-qa')


@bp.route('/', methods=('GET', 'POST'))
def annual_qa():
    return render_template('/annual_qa/index.html')