import json
import socket
import threading
import time

import msgpack
from data import Data
import random


class DataGenerator:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 0))
        self.port = self.socket.getsockname()[1]
        self.send_fake_data()

    def send_fake_data(self):
        all_peers = self.get_all_peers()
        while True:
            peer_num = random.randint(0, len(all_peers)-1)
            peer = all_peers[peer_num]
            data_obj = Data(random.randint(1, 1000), random.randint(1, 30)).json_data()
            data_to_send = msgpack.packb(json.dumps({'type': "fake_data", 'data': data_obj}))
            self.socket.sendto(data_to_send, ('127.0.0.1', int(peer[1])))
            time.sleep(random.randint(0, 3))  # in seconds

    def get_all_peers(self):
        peers = []
        with open('peers_info.json') as f:
            peers_json = json.load(f)
        for port, name in peers_json.items():
            peers.append([name, port])
        return peers

    # def run(self):
    #     sending_thread = threading.Thread(target=self.send_fake_data())
    #     sending_thread.start()

