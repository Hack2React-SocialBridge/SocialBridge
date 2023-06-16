#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A social_bridge.celery.celery beat -l info