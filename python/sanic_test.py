#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { sanic性能测试 }
# @Date: 2023/09/10 12:24
import json
from datetime import timedelta

from py_tools.connections.db.mysql import SQLAlchemyManager, DBManager
from py_tools.connections.db.redis_client import RedisManager
from sanic import Sanic
from sanic.response import json as sanic_json

app = Sanic("sanic_test")


async def init_orm():
    db_client = SQLAlchemyManager(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="123456",
        db_name="house_rental"
    )
    db_client.init_mysql_engine()
    DBManager.init_db_client(db_client)


async def init_redis():
    RedisManager.init_redis_client(
        async_client=True,
        host="127.0.0.1",
        port=6379,
        db=0,
    )


@app.listener('before_server_start')
async def server_start_event(app, loop):
    await init_orm()
    await init_redis()


@app.get(uri="/http/sanic/test")
async def fastapi_test(req):
    return sanic_json({"code": 0, "message": "sanic_http_test", "data": {}})


@app.get(uri="/http/sanic/mysql/test")
async def sanic_myql_query_test(req):
    sql = "select id, username, role from user_basic where username='hui'"
    ret = await DBManager().run_sql(sql)

    column_names = [desc[0] for desc in ret.cursor.description]
    result_tuple = ret.fetchone()
    user_info = dict(zip(column_names, result_tuple))

    return sanic_json({"code": 0, "message": "sanic_mysql_test", "data": {**user_info}})


@app.get(uri="/http/sanic/redis/<username>")
async def sanic_redis_query_test(req, username: str):
    # 先判断缓存有没有
    user_info = await RedisManager.client.get(name=username)
    if user_info:
        user_info = json.loads(user_info)
        return sanic_json({"code": 0, "message": "sanic_redis_test", "data": {**user_info}})

    sql = f"select id, username, role from user_basic where username='{username}'"
    ret = await DBManager().run_sql(sql)

    column_names = [desc[0] for desc in ret.cursor.description]
    result_tuple = ret.fetchone()
    user_info = dict(zip(column_names, result_tuple))

    # 存入redis缓存中, 3min
    await RedisManager.client.set(
        name=user_info.get("username"),
        value=json.dumps(user_info),
        ex=timedelta(minutes=3)
    )

    return sanic_json({"code": 0, "message": "sanic_redis_test", "data": {**user_info}})


def main():
    app.run(host="127.0.01", port=8001)


if __name__ == '__main__':
    # sanic sanic_test.app -p 8001 -w 4 --access-log=False
    main()
