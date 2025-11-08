#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
source myvenv/bin/activate
uvicorn core.coa_main:app --reload --port 8080
