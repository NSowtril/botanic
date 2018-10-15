# botanic_website/auth.py: 认证功能
# 认证蓝图包括注册新用户、登陆和注销视图
# url_for()根据视图名称生成URL
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from botanic_website.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 注册视图
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:   # fetchone()返回一个记录行
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            # url_for()根据视图名称生成响应的URL
            # redirect()为生成的URL生成重定向响应
            return redirect(url_for('auth.login'))
        # flash()存储在渲染模块时可以调用的信息
        flash(error)

    return render_template('auth/register.html')


# 登陆视图
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username, )
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        # 检查密码
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # session是一个dict，存储跨域请求的值
        if error is None:
            session.clear()
            # 验证成功后，用户id被存储于新的会话中
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# 注册一个在视图函数之前运行的函数
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE  id = ?', (user_id,)
        ).fetchone()


# 注销：把用户id从session中移除
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 装饰器
def login_required(view):
    # 检查用户是否载入
    # 如果已载入，继续正常执行原视图
    # 否则重定向到登录页面
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    # 返回一个新的视图，该视图包含了传递给装饰器的原视图
    return wrapped_view
