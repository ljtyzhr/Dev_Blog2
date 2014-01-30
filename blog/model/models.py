# -*- coding: utf-8 -*-
from datetime import datetime
from flask.ext.mongoengine import MongoEngine
from mongoengine.errors import ValidationError

db = MongoEngine()


class User(db.Document):
    name = db.StringField(max_length=50, required=True)
    password = db.StringField()
    email = db.StringField()
    avatar = db.StringField()
    signature = db.StringField()
    created_at = db.DateTimeField(default=datetime.now, required=True)


class Category(db.Document):
    name = db.StringField(max_length=120, required=True, unique=True)
    publish_time = db.DateTimeField(default=datetime.now, required=True)

    meta = {
        'indexes': ['name'],
        'ordering': ['-publish_time']
    }


class Post(db.Document):
    permalink = db.StringField(required=True, unique=True)
    title = db.StringField(required=True)
    content = db.StringField()
    pure_content = db.StringField()
    summary = db.StringField()
    html = db.StringField()
    status = db.StringField(choices=('Published', 'Draft'), required=True)
    author = db.ReferenceField(User)
    comments = db.SortedListField(db.EmbeddedDocumentField('CommentEm'))
    update_time = db.DateTimeField(default=datetime.now, required=True)
    publish_time = db.DateTimeField()

    def clean(self):
        """Ensures that only published essays have a `pub_date` and
        automatically sets the pub_date if published and not set"""
        if self.status == 'Draft' and self.publish_time is not None:
            msg = 'Draft entries should not have a publication date.'
            raise ValidationError(msg)
        # Set the pub_date for published items if not set.
        if self.status == 'Published' and self.publish_time is None:
            self.publish_time = datetime.now()

    meta = {
        'indexes': ['permalink'],
        'ordering': ['-publish_time'],
        'allow_inheritance': True
    }


class Diary(Post):
    categories = db.SortedListField(db.StringField())
    tags = db.SortedListField(db.StringField())


class Page(Post):
    pass


class Photo(db.Document):
    url = db.StringField(required=True)
    title = db.StringField(required=True)
    album_name = db.StringField(default='uncategorized')
    description = db.StringField()
    publish_time = db.DateTimeField(default=datetime.now, required=True)


class Tag(db.Document):
    name = db.StringField(max_length=120, required=True)
    diaries = db.SortedListField(db.ReferenceField(Diary))
    publish_time = db.DateTimeField(default=datetime.now, required=True)


class Comment(db.Document):
    content = db.StringField(required=True)
    author = db.StringField(max_length=120, required=True)
    email = db.EmailField()
    diary = db.ReferenceField(Diary)
    publish_time = db.DateTimeField(default=datetime.now, required=True)


class CommentEm(db.EmbeddedDocument):
    content = db.StringField(required=True)
    author = db.StringField(max_length=120, required=True)
    email = db.EmailField()
    publish_time = db.DateTimeField(default=datetime.now, required=True)
