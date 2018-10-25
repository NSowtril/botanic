# 植物信息蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from werkzeug.exceptions import abort
from . import apis

bp = Blueprint('plants', __name__,)


@bp.route('/')
def index():

    return render_template('index.html')



@bp.route('/plants/single', methods=('GET', ))
def single():

    return render_template('index.html')


# @bp.route('/search', methods=('POST', ))
# def search():
#     image = session.get('image')
#     text = session.get('text')
#     speech = session.get('speech')
#     error = None
#
#     if image is not None:
#         return None
#     elif text is not None:
#         return None
#     elif speech is not None:
#         return None
#     else:
#         error = 'No input for search.'
#
#     if error is not None:
#         flash(error)
#
#     return None

