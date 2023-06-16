#!/bin/sh
alembic upgrade head

exec uvicorn social_bridge.main:app --reload --host 0.0.0.0