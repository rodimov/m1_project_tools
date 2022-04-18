from LogDownloader import LogDownloader
from LogDownloader import Server

import json


if __name__ == '__main__':
    servers = []

    with open('servers.json') as servers_file:
        servers_dict = json.load(servers_file)

        for server in servers_dict['servers']:
            servers.append(Server(server['ip'], server['name']))

        logDownloader = LogDownloader(servers)
        logDownloader.download()

