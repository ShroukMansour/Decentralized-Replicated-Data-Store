import json
import socket
import threading
import msgpack
import pprint
from queuingModule import QueuingModule
from dataGenerator import DataGenerator

class Node:
    def __init__(self, node_name):
        self.name = node_name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 0))
        self.port = self.socket.getsockname()[1]
        self.queuing_module = QueuingModule()
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
            data, address = self.socket.recvfrom(65536)  # get data and sender address
            data = msgpack.unpackb(data)
            data = json.loads(data)
            if data['type'] == 'greetings':
                new_peer = data['data']
                with open('peers_info.json', 'w') as f:
                    json.dump(new_peer, f)
            elif data['type'] == 'fake_data':
                print("Iam peer ", self.name, " received fake data")
                self.queuing_module.add_data(data['data'])

    def get_all_nodes(self):
        peers = []
        with open('peers_info.json') as f:
            peers_json = json.load(f)
        for port, name in peers_json.items():
            peers.append([name, port])
        return peers

    def broadcast_data(self, data, type):
        all_nodes = self.get_all_nodes()
        for node in all_nodes:
            self.send_data(node, data, type)

    def run(self):
        receiving_thread = threading.Thread(target=self.receive_data)
        receiving_thread.start()



node1 = Node("node1")
node2 = Node("node2")
data_generator = DataGenerator()

# node1.send_data(['127.0.0.1', node2.port], "data")
# n2.broadcast_data("Im node 2 and msg is broadcasted")
