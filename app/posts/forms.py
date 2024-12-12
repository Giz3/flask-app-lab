from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, StringField, TextAreaField,
                     SelectField, SubmitField)
from wtforms.validators import DataRequired, Length


CATEGORY_CHOICES = [
    ("tech", "Tech"),
    ("science", "Science"),
    ("lifestyle", "Lifestyle")
]


class PostForm(FlaskForm):
    """Форма для створення та редагування посту."""

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=100)],
        render_kw={"class": "form-control", "placeholder": "Enter the title"}
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired()],
        render_kw={"rows": 5, "cols": 40, "class": "form-control", "placeholder": "Enter the content"}
    )

    is_active = BooleanField("Active Post")

    publish_date = DateField(
        "Publish Date",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Category",
        choices=CATEGORY_CHOICES,
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Submit",
        render_kw={"class": "btn btn-primary"}
    )