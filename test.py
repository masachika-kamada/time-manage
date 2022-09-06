import psutil


for proc in psutil.process_iter():
    print("----------------------")
    print("プロセスID:" + str(proc.pid))
    try:
        print("実行モジュール：" + proc.exe())
        print("コマンドライン:" + str(proc.cmdline()))
        print("カレントディレクトリ:" + proc.cwd())
    except psutil.AccessDenied:
        print("このプロセスへのアクセス権がありません。")
