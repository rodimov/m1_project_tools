from LogDownloader import LogDownloader
from LogDownloader import Server

import json
import sys
import CSVExporter as exporter
import Extractor as extractor


def run_download():
    servers = []

    with open('servers.json') as servers_file:
        servers_dict = json.load(servers_file)

        for server in servers_dict['servers']:
            servers.append(Server(server['ip'], server['name']))

        logDownloader = LogDownloader(servers)
        logDownloader.download()


def select_dir(callback):
    print('Select directory:')

    directories = exporter.get_all_dir('./')

    for i in range(len(directories)):
        print(f'{i}) {directories[i]}')

    dir_index = int(input())

    callback('./' + directories[dir_index] + '/')


def extract_logs():
    select_dir(extractor.extract_dir)


def convert_sqlite_to_csv():
    select_dir(exporter.export_dir)


if __name__ == '__main__':
    while True:

        print('Select option:')
        print('1) Download logs')
        print('2) Extract logs')
        print('3) Convert sqlite to csv')
        print('0) Exit')

        option = input()

        if option == '0':
            sys.exit(0)
        elif option == '1':
            run_download()
        elif option == '2':
            extract_logs()
        elif option == '3':
            convert_sqlite_to_csv()

