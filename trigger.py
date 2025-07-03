import psutil
import time

def kill_calc():
    # 実行中のプロセス一覧から"calc.exe"を探して終了させる
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'Calculator.exe' or proc.info['name'] == 'CalculatorApp.exe':
            try:
                proc.kill()
                print("電卓を終了させました。")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

def monitor_calc():
    print("電卓の状態を監視し、起動されたら強制終了します。Ctrl+Cで終了。")
    try:
        while True:
            kill_calc()  # 常に電卓を探していたら終了させる
            time.sleep(0.1)  # 0.1秒ごとにチェック
    except KeyboardInterrupt:
        print("\n監視を終了しました。")

