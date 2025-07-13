from read_yaml import get_config
from client import client_check

import server

import client_GUI
import network_scanner


def main():
    if get_config("type") == "server":
        server.start_server()
    elif get_config("type") == "client":
        all_devices: list = network_scanner.get_live_devices()
        client_results: dict = client_check(all_devices)
        print(client_results)
        # client_GUI.start_gui()

if __name__ == "__main__":
    main()

