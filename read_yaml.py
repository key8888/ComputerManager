from pathlib import Path
import yaml


def get_config(key)-> str:
    file_path = Path(__file__).parent / "config.yaml"
    config = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"設定ファイルが見つかりません: {file_path}")
    except yaml.YAMLError as e:
        print(f"YAMLの解析エラー: {e}")

    return config.get(key, "")

if __name__ == "__main__":
    print(get_config("hostname"))