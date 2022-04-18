import os
import subprocess
from datetime import date


def make_remote_command(server, command):
    stdout, stderr = subprocess.Popen(f"ssh root@{server.ip} {command}", shell=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return stdout


def archive_data(server):
    today = date.today()
    filename = today.strftime(f"amppot_%Y%m%d_{server.name}.tar.gz")
    command = f"tar -zcvf /data/{filename} --directory=/data/ddos ."
    make_remote_command(server, command)
    return filename


def remove_archive(server, filename):
    command = f"rm /data/{filename}"
    make_remote_command(server, command)


def download_data(server, filename):
    today = date.today()
    date_string = today.strftime("%Y%m%d")
    logs_dir_name = f"archives_{date_string}"

    if not os.path.exists(logs_dir_name):
        os.mkdir(logs_dir_name)

    scp_command = f"scp root@{server.ip}:/data/{filename} ./{logs_dir_name}/"

    subprocess.Popen(scp_command, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).communicate()

    return os.path.exists(logs_dir_name + f"/{filename}")


class Server:
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name


class LogDownloader:
    def __init__(self, servers):
        self.servers = servers

    def download(self):
        for server in self.servers:
            filename = archive_data(server)

            if download_data(server, filename):
                print(f"file - {filename} downloaded")
                remove_archive(server, filename)
            else:
                print(f"file - {filename} failed")
