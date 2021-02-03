from flask import request, redirect, url_for, render_template, flash
from flaskr import app, db
from flaskr.models import User, QAmenu

@app.route('/')
def show_qa_menu():
    qa_menu = QAmenu.query.order_by(QAmenu.id.desc().all())
    return render_template('show_qa_menu.html', qa_menu=qa_menu)

@app.route('/add', methods=['POST'])
def add_qa_menu():
    qa_item = QAmenu(
        qa_name = request.form['QA項目名']
    )
    db.session.add(qa_item)
    db.session.commit()
    flash('新しいQA項目が追加されました．')
    return redirect(url_for('show_qa_menu'))