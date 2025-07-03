from screen_locker import locker
from password import make_password
from pathlib import Path
import server
import client
import yaml

file_path = Path(__file__).parent / "config.yaml"
config = {}

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    print(f"設定ファイルが見つかりません: {file_path}")
except yaml.YAMLError as e:
    print(f"YAMLの解析エラー: {e}")

def main():
    if config.get("type") == "server":
        server.start_server()
    elif config.get("type") == "client":
        client.start_client("192.168.40.6")

# if __name__ == "__main__":
#     PASSWORD = make_password()
#     locker(PASSWORD)

