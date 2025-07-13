import socket
import threading
from queue import Queue
import time

# --- 設定項目 ---

# スキャンを試みるポートのリスト
# 一般的なポートを追加すると、より多くのデバイスを検出できる可能性があります。
# (HTTP, HTTPS, Windows NetBIOS, SSH, SMB, RDPなど)
PORTS_TO_SCAN = [5000]

# 同時に実行するスレッドの数（値を大きくすると高速になりますが、PCやネットワークへの負荷が上がります）
THREAD_COUNT = 100

# 接続試行のタイムアウト時間（秒）
CONNECTION_TIMEOUT = 1

# --- プログラム本体 ---

# スキャン対象のIPアドレスを格納するキュー
ip_queue = Queue()
# 発見したデバイスのIPアドレスを格納するリスト
found_devices = []
# 複数のスレッドからリストへ安全に書き込むためのロック
list_lock = threading.Lock()


def get_network_prefix():
    """
    実行中PCのローカルIPアドレスを取得し、ネットワークプレフィックスを返します。
    例: 192.168.1.10 -> 192.168.1.
    """
    # UDPソケットを作成して自身のIPアドレスを取得するテクニック
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # このIPアドレスには実際にパケットは送信されません
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        # ネットワークに接続されていない場合などはlocalhostを返す
        ip = '127.0.0.1'
    finally:
        s.close()

    # IPアドレスの最後の部分を取り除き、ネットワーク部を返す
    return ".".join(ip.split('.')[:-1]) + "."


def scan_ports(ip):
    """
    単一のIPアドレスに対して、定義されたポートリストをスキャンします。
    """
    for port in PORTS_TO_SCAN:
        try:
            # TCPソケットを作成
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # タイムアウトを設定
                sock.settimeout(CONNECTION_TIMEOUT)
                # connect_exは接続失敗時にエラーを送出せず、戻り値で結果を返す
                # 接続成功時は 0 を返す
                if sock.connect_ex((ip, port)) == 0:
                    # ポートが開いている＝デバイス発見
                    with list_lock:
                        # まだリストに追加されていないIPアドレスのみ追加
                        if ip not in found_devices:
                            print(f"✅ デバイス発見: {ip} (ポート {port} がオープン)")
                            found_devices.append(ip)
                    # 1つでもポートが見つかれば、そのIPのスキャンは終了
                    return
        except socket.error:
            # ソケット関連のエラーが発生した場合はスキップ
            pass


def worker():
    """
    キューからIPアドレスを取り出し、スキャンを実行するワーカースレッドの処理。
    """
    while not ip_queue.empty():
        ip = ip_queue.get()
        scan_ports(ip)
        ip_queue.task_done()


def get_live_devices() -> list:
    """
    メインの実行関数。
    """
    print("ローカルネットワークのスキャンを開始します...")

    # 1. スキャン対象のネットワークプレフィックスを取得
    network_prefix = get_network_prefix()
    if network_prefix == '127.0.0.':
        print("❌ ローカルネットワーク接続が確認できませんでした。")
        return []

    print(f"📡 対象ネットワーク: {network_prefix}0/24")
    print(f"🔎 スキャンポート: {PORTS_TO_SCAN}")
    print("-" * 40)

    # 2. スキャン対象の全IPアドレス（1〜254）をキューに追加
    for i in range(1, 255):
        ip_queue.put(network_prefix + str(i))

    start_time = time.time()

    # 3. 指定された数のスレッドを作成して実行開始
    threads = []
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=worker)
        thread.daemon = True  # メインプログラム終了時にスレッドも終了させる
        thread.start()
        threads.append(thread)

    # 4. キューのすべてのタスクが完了するのを待つ
    ip_queue.join()

    end_time = time.time()

    # 5. 結果を表示
    print("-" * 40)
    print("スキャン完了 ✨")
    print(f"所要時間: {end_time - start_time:.2f} 秒")
    if found_devices:
        print("\n発見されたデバイスのIPアドレス一覧:")
        # IPアドレスを数値としてソートして見やすくする
        sorted_devices = sorted(
            found_devices, key=lambda ip: int(ip.split('.')[-1]))
        for device in sorted_devices:
            print(f"  - {device}")
        return sorted_devices
    else:
        print("\nアクティブなデバイスは見つかりませんでした。")
        print("（注意: ファイアウォールの設定や、スキャン対象のポートが開いていないため検出できない可能性があります）")
        return []

