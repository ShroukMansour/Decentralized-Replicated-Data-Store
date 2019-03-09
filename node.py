import json
import socket
import threading
import msgpack
import pprint


class Node:
    def __init__(self, node_name):
        self.name = node_name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 0))
        self.port = self.socket.getsockname()[1]
        self.send_greetings()
        self.run()

    def send_greetings(self):
        node = {self.port: self.name}
        with open('nodes_info.json') as f:
            nodes = json.load(f)
        nodes.update(node)
        with open('nodes_info.json', 'w') as f:
            json.dump(nodes, f)
        print("Hello, I'm ", self.name," and I've joined the network with port %s" % str(self.port))
        self.broadcast_data(nodes, "greetings")

    def send_data(self, node, data, type):
        data_to_send = msgpack.packb({'type': type, 'data': data})
        self.socket.sendto(data_to_send, (node[0], int(node[1])))

    def receive_data(self):
        while True:
            data, address = self.socket.recvfrom(65536)  # get data and sender address
            try:
                data = msgpack.unpackb(data)
                if data['type'] == 'greetings':
                    nodes = data['data']
                    with open('nodes_info.json', 'w') as f:
                        json.dump(nodes, f)
                    self.send_data(['127.0.0.1', address], True, 'chain')  # TODO right ip address
                elif data['type'] == 'transaction':
                    pass
                elif data['type'] == 'chain':
                    pass

                pprint.pprint(data)
            except:
                print('Could not unpack data from peer')

    def get_all_nodes(self):
        nodes = []
        with open('nodes_info.json') as f:
            nodes_json = json.load(f)
        for port, name in nodes_json.items():
            nodes.append([name, port])
        return nodes

    def broadcast_data(self, data, type):
        all_nodes = self.get_all_nodes()
        for node in all_nodes:
            self.send_data(node, data, type)

    def run(self):
        receiving_thread = threading.Thread(target=self.receive_data)
        receiving_thread.start()



shrouk = Node("node1")
nada = Node("node2")

shrouk.send_data(['127.0.0.1', nada.port], "data")
# n2.broadcast_data("Im node 2 and msg is broadcasted")