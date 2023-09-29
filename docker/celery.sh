#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    celery app=app.core.celery:celery_app worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery app=app.core.celery:celery_app flower
fi

done