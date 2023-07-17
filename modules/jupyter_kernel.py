from jupyter_client import KernelManager
from jupyter_client import BlockingKernelClient

import sys
import subprocess
import os
import queue
import json
import signal
import pathlib
import threading
import time
import atexit
import traceback
from time import sleep
from modules import config


def start_kernel():
    # カーネル接続ファイルのパス
    kernel_connection_file = os.path.join(os.getcwd(), "kernel_connection_file.json")

    # 既にファイル・フォルダが存在していたら削除
    if os.path.isfile(kernel_connection_file):
        os.remove(kernel_connection_file)
    if os.path.isdir(kernel_connection_file):
        os.rmdir(kernel_connection_file)

    # カーネル起動スクリプトのパス
    launch_kernel_script_path = os.path.join(
        pathlib.Path(__file__).parent.resolve(), "launch_kernel.py"
    )

    # 作業用フォルダの作成
    os.makedirs('workspace/', exist_ok=True)

    # 新しいプロセスでカーネルを起動
    kernel_process = subprocess.Popen(
        [
            sys.executable,                       # 現在のPython環境を指定
            launch_kernel_script_path,            # カーネル起動スクリプトのパス
            "--IPKernelApp.connection_file",      # カーネル接続ファイルのパスオプション
            kernel_connection_file,               # カーネル接続ファイルのパス
            "--matplotlib=inline",                # matplotlibを使用する際、インラインプロットを有効にするオプション
            "--quiet",                            # 無駄なログを出力しないオプション
        ],
        cwd='workspace/'                          # 作業ディレクトリの指定
    )

    # カーネルプロセスのPIDをファイルに書き込む
    str_kernel_pid = str(kernel_process.pid)
    os.makedirs(config.KERNEL_PID_DIR, exist_ok=True)
    with open(os.path.join(config.KERNEL_PID_DIR, str_kernel_pid + ".pid"), "w") as p:
        p.write("kernel")

    # カーネル接続情報が書き込まれるまで待機
    while True:
        if not os.path.isfile(kernel_connection_file):
            sleep(0.1)
        else:
            # JSONファイルが正しく読み込めるか確認
            try:
                with open(kernel_connection_file, 'r') as fp:
                    json.load(fp)
                # 正しく読み込めたらループを抜ける
                break
            except json.JSONDecodeError:
                pass

    # 上記のループを抜けたらカーネル接続情報が書き込まれたとみなし、カーネルに接続
    kc = BlockingKernelClient(connection_file=kernel_connection_file)
    kc.load_connection_file()
    kc.start_channels()
    kc.wait_for_ready()

    return kc


def execute_code(code:str, kernel_client) -> str:
    kc = kernel_client
    
    # コードの実行を要求
    kc.execute(code)

    # メッセージの受信と表示
    while True:
        msg = kc.get_iopub_msg()
        print(f"{msg}\n\n")
        msg_type = msg["header"]["msg_type"]

        if msg_type == "display_data":
            # 結果が画像の場合
            if "image/png" in msg["content"]["data"]:
                result = msg["content"]["data"]["image/png"]
                message_type = "image/png"
                return result, message_type
        
        if msg_type == "execute_result":
            # 結果がテキストの場合
            if "text/plain" in msg["content"]["data"]:
                result = msg["content"]["data"]["text/plain"]
                message_type = "text/plain"
                return result, message_type
        
        if msg_type == "stream":
            return msg["content"]["text"], "text/plain"

        if msg_type == "status":
            # カーネルの状態が idle（アイドル状態）ならループを終了
            if msg["content"]["execution_state"] == "idle":
                break

if __name__ == "__main__":
    kc = start_kernel()
    print(execute_code("print('Hello, world!')", kc))