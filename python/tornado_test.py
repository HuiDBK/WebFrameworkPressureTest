#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { tornado 性能测试 }
# @Date: 2023/09/20 22:42
import asyncio
from datetime import timedelta
import json
import tornado.web
import tornado.ioloop
from tornado.httpserver import HTTPServer
from py_tools.connections.db.mysql import SQLAlchemyManager, DBManager
from py_tools.connections.db.redis_client import RedisManager


class TornadoBaseHandler(tornado.web.RequestHandler):
    pass


class TornadoTestHandler(TornadoBaseHandler):
    async def get(self):
        self.write({"code": 0, "message": "tornado_http_test", "data": {}})


class TornadoMySQLTestHandler(TornadoBaseHandler):
    async def get(self):
        sql = "select id, username, role from user_basic where username='hui'"
        ret = await DBManager().run_sql(sql)

        column_names = [desc[0] for desc in ret.cursor.description]
        result_tuple = ret.fetchone()
        user_info = dict(zip(column_names, result_tuple))
        self.write({"code": 0, "message": "tornado_mysql_test", "data": {**user_info}})


class TornadoRedisTestHandler(TornadoBaseHandler):
    async def get(self, username):
        user_info = await RedisManager.client.get(name=username)
        if user_info:
            user_info = json.loads(user_info)
            self.write(
                {"code": 0, "message": "tornado_redis_test", "data": {**user_info}}
            )
            return

        sql = f"select id, username, role from user_basic where username='{username}'"
        ret = await DBManager().run_sql(sql)

        column_names = [desc[0] for desc in ret.cursor.description]
        result_tuple = ret.fetchone()
        user_info = dict(zip(column_names, result_tuple))

        # 存入redis缓存中, 3min
        await RedisManager.client.set(
            name=user_info.get("username"),
            value=json.dumps(user_info),
            ex=timedelta(minutes=3),
        )
        self.write({"code": 0, "message": "tornado_redis_test", "data": {**user_info}})


def init_orm():
    db_client = SQLAlchemyManager(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="123456",
        db_name="house_rental",
    )
    db_client.init_mysql_engine()
    DBManager.init_db_client(db_client)


def init_redis():
    RedisManager.init_redis_client(
        async_client=True,
        host="127.0.0.1",
        port=6379,
        db=0,
    )


def init_setup():
    init_orm()
    init_redis()


def make_app():
    init_setup()
    return tornado.web.Application(
        [
            (r"/http/tornado/test", TornadoTestHandler),
            (r"/http/tornado/mysql/test", TornadoMySQLTestHandler),
            (r"/http/tornado/redis/(.*)", TornadoRedisTestHandler),
        ]
    )


app = make_app()


async def main():
    # init_setup()
    # app = make_app()
    server = HTTPServer(app)
    server.bind(8002)
    # server.start(4) # start 4 worker
    # app.listen(8002)
    await asyncio.Event().wait()


if __name__ == "__main__":
    # gunicorn -k tornado -w=4 -b=127.0.0.1:8002 python.tornado_test:app
    asyncio.run(main())
