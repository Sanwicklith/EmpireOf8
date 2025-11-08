#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
REPO_SSH="git@github.com:YOURUSER/EmpireOf8_Mastermind.git"
git branch -M main
git remote add origin "$REPO_SSH"
git push -u origin main
