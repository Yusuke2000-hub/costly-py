#!/bin/bash
# FastAPI（uvicorn）をバックグラウンドで起動するスクリプト

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$APP_DIR/logs"
PID_FILE="$APP_DIR/uvicorn.pid"

mkdir -p "$LOG_DIR"

# すでに起動中か確認
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "すでに起動中です（PID: $PID）。停止する場合は stop.sh を実行してください。"
        exit 1
    else
        echo "古い PID ファイルを削除します。"
        rm "$PID_FILE"
    fi
fi

cd "$APP_DIR"

nohup uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info \
    >> "$LOG_DIR/uvicorn.log" 2>&1 &

echo $! > "$PID_FILE"
echo "起動しました（PID: $(cat "$PID_FILE")）"
echo "ログ: $LOG_DIR/uvicorn.log"
