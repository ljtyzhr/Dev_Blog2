# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, redirect, request, url_for,
                   abort, Response)
from functions import (user_func, diary_func, cat_func, page_func,
                       other_func)
from templates import templates

frontend = Blueprint('frontend', __name__, template_folder='templates',
                     static_folder='static')


@frontend.route('/')
def home():
    """ HomePage.

     list newest 10 diaries.

    Args:
        none

    Return:
        diaries: 10 diaries list
        categories: used for sidebar
        pages: used for top-nav
        profile: user object
        next_page: boolen
    """
    profile = user_func.get_profile()
    categories = cat_func.get_all_categories('-publish_time')
    pages = page_func.get_all_pages('-publish_time')
    prev, next, diaries = diary_func.get_diary_list(0, 10)

    return render_template(templates['home'],
                           diaries=diaries, categories=categories,
                           pages=pages, profile=profile, next=next)


@frontend.route('/diary/<diary_id>/<diary_title>')
def diary_detail(diary_id, diary_title=None):
    """ Diary Detail Page.

    show diary details.

    Args:
        diary_id: ObjectedId
        diary_title: string used for SEO Only

    Return:
        diary_detail: diary_object
        categories: used for sidebar
        guest_name: string cookie for guest comment auto complete filed
        guest_email: string cookie for guest comment auto complete filed
        pages: used for top-nav
        profile: user object
        prev: if has previous diary
        next: if has next diary
    """
    profile = user_func.get_profile()
    prev, next, diary = diary_func.get_diary_width_navi(diary_id=diary_id)
    categories = cat_func.get_all_categories('-publish_time')
    pages = page_func.get_all_pages('-publish_time')

    guest_name = request.cookies.get('guest_name')
    guest_email = request.cookies.get('guest_email')

    return render_template(templates['diary_detail'],
                           diary=diary, categories=categories,
                           guest_name=guest_name, guest_email=guest_email,
                           pages=pages, profile=profile, prev=prev, next=next)


@frontend.route('/diary/route/<prev_or_next>/<diary_id>')
def diary_prev_or_next(prev_or_next, diary_id):
    """ Diary Next_Or_Prev page function.

    show next or previous diary details.

    Args:
        prev_or_next: string 'next' or 'prev'
        diary_id: objectID

    Return:
        redirect: diary_detail_page
    """

    next_diary = diary_func.get_next_or_prev_diary(prev_or_next, diary_id)

    try:
        return redirect(
            url_for('frontend.diary_detail', diary_id=next_diary.pk,
                    diary_title=next_diary.title))
    except Exception as e:
        print str(e)
        abort(404)


@frontend.route('/diary/page/<int:page_num>')
@frontend.route('/category/<cat_name>')
@frontend.route('/category/<cat_name>/page/<int:page_num>')
@frontend.route('/tag/<tag_name>/page/<int:page_num>')
def diary_list(page_num=None, cat_name=None, tag_name=None):
    """Diary list page.

    listed 10 diaries each page.Adjusted for diary, category and tag pagging.

    Args:
        page_num: numberic and int
        cate_name: string, can be none
        tag_name: string, can be none

    Return:
        diaries: listed 10 diaries objects
        next: bool True or False
        prev: bool True or False
        categories: used for sidebar
        pages: used for top-nav
        page_num: current page_num
        profile: user object
    """
    profile = user_func.get_profile()
    categories = cat_func.get_all_categories('-publish_time')
    pages = page_func.get_all_pages('-publish_time')

    if not page_num:
        page_num = 1

    start = (int(page_num) - 1) * 10
    end = int(page_num) * 10

    if tag_name:
        pass
    elif cat_name:
        prev, next, diaries = cat_func.get_diary_list(cat_name, start, end)
    else:
        prev, next, diaries = diary_func.get_diary_list(start, end)

    return render_template(templates['diary_list'], diaries=diaries,
                           categories=categories, next=next, prev=prev,
                           page_num=page_num, pages=pages, profile=profile,
                           cat_name=cat_name, tag_name=tag_name)


@frontend.route('/feed')
def rss():
    """ RSS2 Support.

        support xml for RSSItem with 12 diaries.

    Args:
        none
    Return:
        none
    """
    content = other_func.get_rss(12)

    return Response(content, mimetype='text/xml')


@frontend.route('/page/<page_url>')
def page(page_url):
    """CMS page.
    show page for page_name.

    Methods:
        POST

    Args:
        page_url: string

    Return:
        categories: used for sidebar
        page object
        pages: used for top-nav
        profile: user object
    """
    profile = user_func.get_profile()
    categories = cat_func.get_all_categories('-publish_time')
    pages = page_func.get_all_pages('-publish_time')
    page = page_func.get_page(page_url=page_url)

    return render_template(templates['page'], page=page,
                           categories=categories, pages=pages, profile=profile)
