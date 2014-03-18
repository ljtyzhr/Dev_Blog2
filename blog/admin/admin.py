# -*- coding: utf-8 -*-
import json
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, url_for, request, redirect
from flask.ext.login import (LoginManager, login_required,
                             login_user, logout_user, UserMixin)

from functions import (user_func, diary_func, cat_func)
from templates import templates

admin = Blueprint('admin', __name__, template_folder='templates',
                  static_folder='static')

login_manager = LoginManager()
login_manager.login_view = "admin.login"
login_manager.login_message = u"Please log in to access this page."


class User(UserMixin):

    """ User object for Flasklogin

    define name, id, and active for Flasklogin use
    """

    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        return self.active


@login_manager.user_loader
def load_user(id):
    user = user_func.get_profile()
    return User(user.name, user.pk)


@admin.route("/login", methods=["GET", "POST"])
def login():
    """Login page for user to auth.

    use Flasklogin Class login_user() to login user.

    Methods:
        GET and POST

    Args:
        GET:
            none
        POST:
            username: string
            password: string

    Returns:
        GET:
            none
        POST:
            none
    """
    if request.method == "POST" and "username" in request.form:
        password = request.form["password"]
        user = user_func.get_profile()

        if user and check_password_hash(user.password, password):
            login_user(User(user.name, user.pk))
            return redirect(request.args.get("next") or url_for("admin.index"))
        else:
            return redirect(url_for("admin.login"))
    else:
        return render_template(templates["login"])


@admin.route("/logout")
@login_required
def logout():
    """Action for logout current_user.

    call this method for logout current_user.
    """
    logout_user()
    return redirect(url_for("admin.index"))


@admin.route('/')
@login_required
def index():
    """Page for dashboard.

    only display static page.
    """

    profile = user_func.get_profile()
    return render_template(templates["dashboard"], profile=profile)


@admin.route('/diary/list')
@login_required
def diary_list():
    """Admin Diary lit page.

    show all diaries.

    Methods:
        GET

    Args:
        none

    Returns:
        Diary object
    """
    profile = user_func.get_profile()
    diaries = diary_func.get_all_diaries()
    return render_template(templates["diary_list"], diaries=diaries,
                           profile=profile)


@admin.route('/diary/edit/<diary_id>', methods=['GET', 'POST'])
@login_required
def diary_edit(diary_id=None):
    """ Edit diary from admin

    receives title, content(markdown), tags and cagetories

    Args:
        diary_id: diary_id
        title: string
        permalink: string
        content: markdown string
        cagetory: list
        tags: string
    """
    if request.method == 'POST':
        title = request.form["title"]
        categories = request.form.getlist("categories")
        tags = request.form["tags"]
        permalink = request.form["permalink"]
        content = request.form["content"]

        splited_tags = tags.split(',')

        diary_func.edit_diary(permalink, title, content, categories,
                              splited_tags)

        return redirect(url_for('admin.diary_list'))

    else:
        diary = diary_func.get_by_id(diary_id=diary_id)

        profile = user_func.get_profile()
        categories = cat_func.get_all_categories()
        return render_template(templates["diary_edit"], profile=profile,
                               categories=categories, diary=diary)


@admin.route('/category/add', methods=['POST'])
def category_new():
    """Admin Add New Category function.

    Methods:
        POST

    Args:
        cat_name: string

    Return:
        success: true/false
        cid: category_object_id
    """
    if request.method == 'POST':
        cat_name = request.form["cat_name"]
        cat = cat_func.add_new_category(cat_name)

        return json.dumps({'success': 'true', 'cat_id': str(cat.pk),
                          'cat_name': cat_name})
