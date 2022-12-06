
from flask import render_template, request, flash, redirect, url_for
from app import app
from app.models import db, Payment, TgUser, Url


@app.route('/<link>', methods=['GET'])
def redirect_test(link):

    source_link = Url.query.filter_by(redirect=link).first()
    if source_link is None:
        return "Такой страницы еще нет, но вы можете её купить здесь..."

    source_link.uses += 1
    db.session.commit()
    return redirect(source_link.source)

