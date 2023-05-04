from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from .models import Blog
from . import db
from datetime import datetime

blog = Blueprint('blog', __name__)


@blog.route('/create')
@login_required
def create():
    return render_template('create.html')


@blog.route('/create', methods=['POST'])
@login_required
def create_blog():
    title = request.form.get('title')
    content = request.form.get('content')

    exists = Blog.query.filter_by(title=title, content=content).first()

    if exists:
        flash("Post copied! Can't create two posts like this")
        return redirect(url_for('blog.create'))

    new_blog = Blog(title=title, content=content, date_created=datetime.utcnow(), email=current_user.email,
                    name=current_user.name)

    db.session.add(new_blog)
    db.session.commit()

    return redirect(url_for('main.index'))


@blog.route('/delete/<int:id>')
@login_required
def delete(id):
    blog_to_delete = Blog.query.get_or_404(id)
    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        return redirect(url_for('main.index'))
    except:
        flash('Something was wrong. Try again later')
        return redirect(url_for('main.index'))


@blog.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    update_blog = Blog.query.get_or_404(id)
    if request.method == "POST":
        update_blog.title = request.form['title']
        update_blog.content = request.form['content']
        try:
            db.session.commit()
            return redirect(url_for('main.index'))
        except:
            flash('Something was wrong.')
            return redirect(url_for('blog.update'))
    else:
        return render_template('update.html', blog=update_blog)
