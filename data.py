import json


class Data:
    def __init__(self, data, size, synced=False):
        self.data = data
        self.size = size
        self.synced = synced
        self.synced_with = []

    def json_data(self):
        return {"data": self.data, "size": self.size}

    def sync_with_peer(self, peer):
        self.synced_with.append(peer)

    def check_synced(self, all_peers):
        true_sync  =0
        for peer in all_peers:
            if peer[1] in self.synced_with:
                true_sync = true_sync + 1
        if true_sync == len(self.synced_with) and len(self.synced_with) == len(all_peers):
            self.synced = True
