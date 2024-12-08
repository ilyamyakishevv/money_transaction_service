#!/usr/bin/env sh


python3 -m alembic -c alembic.ini revision --autogenerate --message "$@"
