import os
import tempfile

import pytest
from botanic_website import create_app
from botanic_website.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()  # 创建并打开一个临时文件，返回该文件对象和路径
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


# client 固件调用 app.test_client() 由 app 固件创建的应用对象。
# 测试会使用客户端来向应用发送请求，而不用启动服务器。
@pytest.fixture
def client(app):
    return app.test_client()


# runner 固件类似于client。
# app.test_cli_runner() 创建一个运行器，可以调用应用注册的 Click 命令。
@pytest.fixture
def runner(app):
    return app.test_cli_runner()


# 验证
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)