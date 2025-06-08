import socket


def start_client(server_ip, port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, port))
        print(f"[クライアント] サーバーに接続：{server_ip}:{port}")

        while True:
            msg = input("送信メッセージ：")
            if msg.lower() == 'exit':
                break
            s.sendall(msg.encode())
            data = s.recv(1024)
            print(f"[クライアント] 受信：{data.decode()}")


if __name__ == '__main__':
    server_ip = input("サーバーのIPアドレスを入力：")
    if server_ip == "":
        server_ip = "127.0.0.1"
    start_client(server_ip)
        
