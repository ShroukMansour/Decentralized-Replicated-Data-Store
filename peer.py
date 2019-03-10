import json
import socket
import threading
import time

import msgpack
from queuingModule import QueuingModule
from dataGenerator import DataGenerator
from dataStorage import DataStorage

class Node:
    def __init__(self, node_name):
        self.name = node_name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 0))
        self.port = self.socket.getsockname()[1]
        self.data_storage = DataStorage()
        self.queuing_module = QueuingModule(self.data_storage)
        self.pool_of_ack = []
        self.send_greetings()
        self.run()

    def send_greetings(self):
        node = {self.port: self.name}
        with open('peers_info.json') as f:
            peers = json.load(f)
        peers.update(node)
        with open('peers_info.json', 'w') as f:
            json.dump(peers, f)
        print("Hello, I'm ", self.name," with port %s" % str(self.port))
        self.broadcast_data(peers, "greetings")

    def send_data(self, peer, data, type):
        data_to_send = msgpack.packb(json.dumps({'type': type, 'data': data}))
        self.socket.sendto(data_to_send, ('127.0.0.1', int(peer[1])))

    def receive_data(self):
        while True:
            data, peer = self.socket.recvfrom(65536)  # get data and sender address
            data = msgpack.unpackb(data)
            data = json.loads(data)
            if data['type'] == 'greetings':
                new_peer = data['data']
                with open('peers_info.json', 'w') as f:
                    json.dump(new_peer, f)
            elif data['type'] == 'fake_data':
                print("I'm peer ", self.name, " received fake data")
                self.queuing_module.add_data([data['data']])
            elif data['type'] == 'sync':
                print("data sync")  # TODO array
                self.queuing_module.add_data(data['data'], synced=True)
            elif data['type'] == 'ack_to_send':
                self.avail_amount = self.queuing_module.get_avail_amount()
                if self.avail_amount > 0:
                    self.send_data(peer, {"avail_space": self.avail_amount}, "ack_to_receive")
            elif data['type'] == 'ack_to_receive':
                self.pool_of_ack.append([peer, data['data']['avail_space']])

    def send_ack_to_peers(self):
        time.sleep(3)
        all_peers = self.get_all_peers()
        for peer in all_peers:
             self.send_data(peer, {}, "ack_to_send")

        # for data in my_data:
        #     data = data[0]
        #     if not data.synced:
        #         for peer in all_peers:
        #             if peer not in data.synced_with:
        #                 self.send_data(peer, {}, "ack_to_send")
        #                 data.sync_with_peer(peer)
        #                 self.send_data(peer, {"data":data.data, "size":data.size}, "sync")
        #         data.synced = True

    def sync_with_peers(self):
        while True:
            time.sleep(1)
            all_peers = self.get_all_peers()
            if self.pool_of_ack:
                my_data = self.data_storage.get_all_data()
                for ack in self.pool_of_ack:
                    peer = ack[0]; avail_size = ack[1]
                    data_to_send = [];  total_data_size = 0
                    for data in my_data:
                        data = data[0]
                        if (not data.synced) and data.size <= avail_size:
                            data_to_send.append(data)
                            avail_size -= data.size
                            total_data_size += data.size
                            data.sync_with_peer(peer)
                            data.check_synced(all_peers)
                            if avail_size == 0:
                                break
                    self.send_data(peer, {"data":data_to_send, "size":total_data_size}, 'sync')
                    self.pool_of_ack.remove(ack)

    def get_all_peers(self):
        peers = []
        with open('peers_info.json') as f:
            peers_json = json.load(f)
        for port, name in peers_json.items():
            peers.append([name, port])
        return peers

    def broadcast_data(self, data, type):
        all_nodes = self.get_all_peers()
        for node in all_nodes:
            self.send_data(node, data, type)

    def run(self):
        receiving_thread = threading.Thread(target=self.receive_data)
        receiving_thread.start()
        ack_thread = threading.Thread(target=self.send_ack_to_peers)
        ack_thread.start()
        sync_thread = threading.Thread(target=self.sync_with_peers())
        sync_thread.start()


p1 = Node("peer1")
p2 = Node("peer2")
data_generator = DataGenerator()



# node1.send_data(['127.0.0.1', node2.port], "data")
# n2.broadcast_data("Im node 2 and msg is broadcasted")
