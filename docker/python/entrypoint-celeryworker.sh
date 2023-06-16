#!/bin/bash

set -o errexit
set -o nounset

exec celery -A social_bridge.celery.celery worker --loglevel=info