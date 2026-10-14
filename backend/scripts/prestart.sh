#! /usr/bin/env bash

set -e
set -x

# 执行数据库迁移
alembic upgrade head

# 在数据库中创建初始数据
python app/initial_data.py
