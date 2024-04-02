from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Message
from . import db


views = Blueprint('views', __name__)


@views.route('/about')
@login_required
def about():
    return render_template('about.html', user=current_user)


@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():

    if request.method == 'POST':
        name = request.form.get('name')
        text = request.form.get('text')

        new_message = Message(name=name, text=text,user=current_user)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('views.contact'))

    return render_template('contact.html', user=current_user)


@views.route('/')
@login_required
def intro():
    return render_template('intro.html', user=current_user)


@views.route('/menu')
@login_required
def menu():
    return render_template('menu.html', user=current_user)
