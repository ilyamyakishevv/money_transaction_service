#!/usr/bin/env sh


alembic -c alembic.ini revision --autogenerate --message "$@"
