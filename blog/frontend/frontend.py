# -*- coding: utf-8 -*-
import json
from operator import attrgetter
from flask import (Blueprint, render_template, redirect, request, url_for,
                   make_response, abort, Response)
from model.models import (User, Diary, Category, CommentEm, Comment, Tag,
                          Photo, StaticPage)
from config import Config
from tasks.email_tasks import send_email_task
from functions import (user_func, diary_func, category_func, page_func,
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
    categories = category_func.get_all_categories('-publish_time')
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
    categories = category_func.get_all_categories('-publish_time')
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


@frontend.route('/diary/list/<page_num>')
def diary_list(page_num):
    """Diary list page.

    listed 10 diaries each page.

    Args:
        page_num: numberic and int

    Return:
        diaries: listed 10 diaries objects
        next_page: bool True or False
        categories: used for sidebar
        pages: used for top-nav
        page_num: current page_num
        profile: user object
    """
    profile = user_func.get_profile()
    categories = category_func.get_all_categories('-publish_time')
    pages = page_func.get_all_pages('-publish_time')

    start = (int(page_num) - 1) * 10
    end = int(page_num) * 10

    prev, next, diaries = diary_func.get_diary_list(start, end)

    return render_template(templates['diary_list'], diaries=diaries,
                           categories=categories, next=next, prev=prev,
                           page_num=page_num, pages=pages, profile=profile)


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
    categories = category_func.get_all_categories('-publish_time')
    pages = page_func.get_all_pages('-publish_time')
    page = page_func.get_page(page_url=page_url)

    return render_template(templates['page'], page=page,
                           categories=categories, pages=pages, profile=profile)


@frontend.route('/category/<category_id>/<category_name>')
def category_list(category_id, category_name=None):
    """Category list page.

    show 5 diaries in this page.

    Args:
        category_id: categoryObjectID
        category_name: only for SEO

    Return:
        next_page: bool True or False
        page_num: 1
        category: category_name used for title
        diaries: listed 5 diaries in each page
        categories: used in sidebar
        pages: used for top-nav
        profile: user object
    """
    next_page = False
    diary_num = len(Category.objects(pk=category_id)[0].diaries)
    if diary_num > 5:
        next_page = True

    profile = User.objects.first()
    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    diaries = sorted(Category.objects(pk=category_id)[0].diaries,
                     key=attrgetter('publish_time'),
                     reverse=True)[:5]

    return render_template('frontend/category/list.html',
                           category=category_name, diaries=diaries,
                           categories=categories, next_page=next_page,
                           page_num=1, category_id=category_id, pages=pages,
                           profile=profile)


@frontend.route('/category/<category_id>/<category_name>/page/<page_num>')
def category_paging(category_id, page_num, category_name=None):
    """Category list page.

    show 5 diaries in each page.

    Args:
        category_id: categoryObjectID
        category_name: only for SEO
        page_num: page_num

    Return:
        next_page: bool True or False
        page_num: now page_num
        category: category_name used for title
        diaries: listed 5 diaries in each page
        categories: used in sidebar
        pages: used for top-nav
        profile: user object
    """
    next_page = False
    diary_num = len(Category.objects(pk=category_id)[0].diaries)

    if diary_num > (int(page_num) - 1) * 5 + 5:
        next_page = True

    profile = User.objects.first()
    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    diaries = sorted(Category.objects(pk=category_id)[0].diaries,
                     key=attrgetter('publish_time'),
                     reverse=True)[(int(page_num) - 1) * 5:int(page_num) * 5]

    return render_template('frontend/category/list.html',
                           category=category_name, diaries=diaries,
                           categories=categories, next_page=next_page,
                           page_num=page_num, category_id=category_id,
                           pages=pages, profile=profile)


@frontend.route('/tag/<tag_name>')
def tag_list(tag_name):
    """ TagList Page.

    used for list diaries with the same tag_name with 5 diaries each page.

    Args:
        tag_name: string

    Return:
        categories: used for sidebar list
        pages: used for top-nav
        diaries: sorted diaries_object by publish_time
        page_num: 1
        tag: tag_name used for title
        profile: user object
    """
    tags = Tag.objects.get_or_404(name=tag_name)
    profile = User.objects.first()
    next_page = False
    diary_num = len(tags.diaries)
    if diary_num > 5:
        next_page = True

    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    diaries = sorted(Tag.objects(name=tag_name)[0].diaries,
                     key=attrgetter('publish_time'),
                     reverse=True)[:5]

    return render_template('frontend/tag/list.html', diaries=diaries,
                           categories=categories, tag=tag_name,
                           next_page=next_page, page_num=1, pages=pages,
                           profile=profile)


@frontend.route('/tag/<tag_name>/page/<page_num>')
def tag_paging(tag_name, page_num):
    """ TagList Paging.

    used for list diaries with the same tag_name with 5 diaries each page.

    Args:
        tag_name: string
        page_num: page_num

    Return:
        categories: used for sidebar list
        next_page: bool True or False
        diaries: sorted diaries_object by publish_time with 5 each page
        page_num: now page_num
        tag: tag_name used for title
        pages: used for top-nav
        profile: user object
    """
    next_page = False
    diary_num = len(Tag.objects(name=tag_name)[0].diaries)
    if diary_num > int(page_num) * 5:
        next_page = True

    profile = User.objects.first()
    categories = Category.objects.order_by('-publish_time')
    pages = StaticPage.objects.all()
    diaries = sorted(Tag.objects(name=tag_name)[0].diaries,
                     key=attrgetter('publish_time'),
                     reverse=True)[(int(page_num) - 1) * 5:int(page_num) * 5]

    return render_template('frontend/tag/list.html', diaries=diaries,
                           categories=categories, tag=tag_name,
                           next_page=next_page, page_num=page_num, pages=pages,
                           profile=profile)


@frontend.route('/comment/add', methods=['POST'])
def comment_add():
    """ Comment Add AJAX Post Action.

    designed for ajax post and send reply email for admin

    Args:
        username: guest_name
        did: diary ObjectedId
        email: guest_email
        content: comment content

    Return:
        email_status: success
    """
    if request.method == 'POST':
        name = request.form['username']
        did = request.form['did']
        email = request.form['email']
        content = request.form['comment']

        post = Diary.objects(pk=did)
        diary_title = post[0].title

        commentEm = CommentEm(
            author=name,
            content=content,
            email=email
        )
        post.update_one(push__comments=commentEm)

        comment = Comment(content=content)
        comment.diary = post[0]
        comment.email = email
        comment.author = name
        comment.save(validate=False)

        try:
            send_email_task(Config.EMAIL,
                            Config.MAIN_TITLE + u'收到了新的评论, 请查收',
                            content, did, name, diary_title)

            response = make_response(json.dumps({'success': 'true'}))
            response.set_cookie('guest_name', name)
            response.set_cookie('guest_email', email)
            return response
        except Exception as e:
            return str(e)


@frontend.route('/gallery', methods=['GET', 'POST'])
def gallery():
    """GalleryPage.
     list all photo.

     Methods:
        GET and POST

    Args:
        GET:
            none
        POST:
            offset

    Return:
        photos : 5 photos
        categories: used for sidebar
        profile: user object
        pages: used for top-nav
    """
    if request.method == 'POST':
        offset = int(request.form["offset"])
        photos = Photo.objects.order_by('-publish_time')[offset: offset + 5]

        return photos.to_json()
    else:
        photos = Photo.objects.order_by('-publish_time')[0: 5]
        categories = Category.objects.order_by('-publish_time')
        profile = User.objects.first()
        pages = StaticPage.objects.all()

        return render_template('frontend/gallery/index.html', photos=photos,
                               categories=categories, profile=profile,
                               pages=pages)
