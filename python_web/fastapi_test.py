#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { fastapi性能测试 }
# @Date: 2023/09/10 12:24
import json
from datetime import timedelta

import uvicorn
from fastapi import FastAPI
from py_tools.connections.db.mysql import SQLAlchemyManager, DBManager
from py_tools.connections.db.redis_client import RedisManager

app = FastAPI(summary="fastapi性能测试")


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


@app.on_event("startup")
async def startup_event():
    """项目启动时准备环境"""

    await init_orm()

    await init_redis()


@app.get(path="/http/fastapi/test")
async def fastapi_test():
    return {"code": 0, "message": "fastapi_http_test", "data": {}}


@app.get(path="/http/fastapi/mysql/test")
async def fastapi_myql_query_test():
    sql = "select id, username, role from user_basic where username='hui'"
    ret = await DBManager().run_sql(sql)

    column_names = [desc[0] for desc in ret.cursor.description]
    result_tuple = ret.fetchone()
    user_info = dict(zip(column_names, result_tuple))

    return {"code": 0, "message": "fastapi_mysql_test", "data": {**user_info}}


@app.get(path="/http/fastapi/redis/{username}")
async def fastapi_redis_query_test(username: str):
    # 先判断缓存有没有
    user_info = await RedisManager.client.get(name=username)
    if user_info:
        user_info = json.loads(user_info)
        return {"code": 0, "message": "fastapi_redis_test", "data": {**user_info}}

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

    return {"code": 0, "message": "fastapi_redis_test", "data": {**user_info}}


if __name__ == '__main__':
    # uvicorn python_web.fastapi_test:app --log-level critical --port 8000 --workers 4
    uvicorn.run(app, host="127.0.0.1", port=8000)
