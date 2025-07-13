import socket


def start_client(server_ip: str, port=5000, msg: str = "") -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, port))
        print(f"[クライアント] サーバーに接続：{server_ip}:{port}")

        s.sendall(msg.encode())
        data = s.recv(1024)
        print(f"[クライアント] 受信：{data.decode()}")
        return data.decode()

def client_check(ip_list: list) -> dict:
    results = {}
    for ip in ip_list:
        try:
            response = start_client(server_ip=ip, msg="hostname")
            # results[ip] = response
            results[response] = ip 
        except Exception as e:
            # results[ip] = f"接続失敗: {str(e)}"
            print(e)
    return results

if __name__ == '__main__':
    server_ip = input("サーバーのIPアドレスを入力：")
    if server_ip == "":
        server_ip = "127.0.0.1"
    start_client(server_ip)
