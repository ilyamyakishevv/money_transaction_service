#!/usr/bin/env sh


alembic -c src/alembic.ini revision --autogenerate --message "$@"
