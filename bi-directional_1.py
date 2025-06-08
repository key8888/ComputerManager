# ==== 双方向チャット対応マルチクライアントサーバー ====
import socket
import threading

def handle_receive(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"[受信:{addr}] {data.decode()}")
        except:
            break

def handle_send(conn, addr):
    while True:
        try:
            msg = input(f"[送信:{addr}] > ")
            conn.sendall(msg.encode())
        except:
            break

def handle_client(conn, addr):
    print(f"[サーバー] 接続：{addr}")
    recv_thread = threading.Thread(target=handle_receive, args=(conn, addr))
    send_thread = threading.Thread(target=handle_send, args=(conn, addr))
    recv_thread.start()
    send_thread.start()
    recv_thread.join()
    send_thread.join()
    conn.close()
    print(f"[サーバー] 切断：{addr}")

def start_server(host='0.0.0.0', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[サーバー] ポート{port}で待機中...")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    start_server()
