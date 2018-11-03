# 植物信息蓝图
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

from werkzeug.exceptions import abort
from . import apis

bp = Blueprint('plants', __name__,)

@bp.before_request
def before_request():
    if True:
        print("[ Headers ]", request.headers)
        print("[ Path ]", request.path)
        print("[ Args ]", request.args)
        print("[ Data ]", request.data)
        print("[ Form ]", request.form)
        print("[ Access Route ]", request.access_route)
        print("[ Files ]", request.files)

def search_by_name(name):
    error = None
    if name is None:
        error = 'name required.'

    if error is not None:
        abort(404, error)

@bp.route('/')
def index():

    return render_template('index.html')


@bp.route('/plants/single', methods=('GET', ))
def single():

    return render_template('index.html')



