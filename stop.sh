#!/bin/bash
# FastAPI（uvicorn）を停止するスクリプト

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$APP_DIR/uvicorn.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "PID ファイルが見つかりません。アプリが起動していない可能性があります。"
    exit 1
fi

PID=$(cat "$PID_FILE")

if kill -0 "$PID" 2>/dev/null; then
    kill "$PID"
    rm "$PID_FILE"
    echo "停止しました（PID: $PID）"
else
    echo "プロセス（PID: $PID）は既に停止しています。"
    rm "$PID_FILE"
fi
