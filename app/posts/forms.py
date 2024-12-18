from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeLocalField, StringField, TextAreaField,
                     SelectField, SelectMultipleField, SubmitField)
from wtforms.validators import DataRequired, Length
from app.posts.models import Tag
from app.users.models import User

CATEGORIES = [("tech", "Tech"),
              ("science", "Science"),
              ("lifestyle", "Lifestyle")]


class PostForm(FlaskForm):
    title = StringField("Title",
                        validators=[DataRequired(), Length(max=100)],
                        render_kw={"class": "form-control",
                                   "placeholder": "Enter the title"})

    content = TextAreaField("Content",
                            validators=[DataRequired()],
                            render_kw={"rows": 5,
                                       "cols": 40,
                                       "class": "form-control",
                                       "placeholder": "Enter the content"
                                       })

    is_active = BooleanField("Active Post")

    publish_date = DateTimeLocalField("Publish Date",
                                      format="%Y-%m-%dT%H:%M",
                                      validators=[DataRequired()],
                                      default=datetime.now())

    category = SelectField("Category",
                           choices=CATEGORIES,
                           validators=[DataRequired()])

    author = SelectField("Author",
                         coerce=int,
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})

    tags = SelectMultipleField("Tags",
                               coerce=int,
                               choices=[],
                               render_kw={"class": "form-control"})

    submit = SubmitField("Submit",
                         render_kw={"class": "btn btn-primary"})

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        users = User.query.all()
        self.author.choices = [(user.id, user.username) for user in users]

        tags = Tag.query.all()
        self.tags.choices = [(tag.id, tag.name) for tag in tags]