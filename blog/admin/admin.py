# -*- coding: utf-8 -*-
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, url_for, request, redirect
from flask.ext.login import (LoginManager, login_required,
                             login_user, logout_user, UserMixin)

from functions import (user_func, diary_func, cat_func, page_func,
                       other_func)
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
        username = request.form["username"]
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

    receives title, content(html), tags and cagetory
    save title, content(html), pure content(further use), tags and cagetory
    also auto save author as current_user.

    this method will auto save new Category or Tag if not exist otherwise save
    in existed none with push only diary_object

    Args:
        diary_id: diary_id
        title: string
        html: string
        cagetory: string
        tags: list

    Save:
        title: string
        html: string
        content: string without html tags
        category: string
        tags: list
        summary: first 80 characters in content with 3 dots in the end
        author: current_user_object
    """
    profile = user_func.get_profile()
    categories = cat_func.get_all_categories()
    return render_template(templates["diary_edit"], profile=profile,
                           categories=categories)