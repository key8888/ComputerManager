# ==== マルチクライアント対応サーバー ====
import socket
import threading
import screen_locker
import password

def handle_client(conn, addr):
    print(f"[サーバー] 接続：{addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data: # 終了のサインif data == b'': と同じ意味
                    print("ここで終了させていただきます")
                    break
                recved_data = data.decode()
                
                if recved_data == "lock":
                    password_str = password.make_password()
                    screen_locker.locker(password_str)
                
                print(f"[サーバー] 受信({addr})：{data.decode()}")
                conn.sendall(f"受信しました: {data.decode()}".encode())
                
            except ConnectionResetError:
                print(f"[サーバー] クライアント({addr})が強制的に接続を切断しました。")
                break
            except ConnectionRefusedError:
                print(f"[サーバー] 接続が拒否されました（{addr}）。")
                break
            except TimeoutError:
                print(f"[サーバー] タイムアウトが発生しました（{addr}）。")
                break
            except BrokenPipeError:
                print(f"[サーバー] 接続が切れている状態で送信が行われました（{addr}）。")
                break
            except socket.gaierror:
                print(f"[サーバー] ホスト名の解決に失敗しました（{addr}）。")
                break
            except OSError as e:
                print(f"[サーバー] OSエラーが発生しました（{addr}）: {e}")
                break
            

def start_server(host='0.0.0.0', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[サーバー] ポート{port}で待機中...")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[サーバー] 現在の接続数: {threading.active_count() - 1}")

if __name__ == '__main__':
    start_server()
