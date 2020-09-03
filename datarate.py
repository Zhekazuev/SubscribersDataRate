"""
Methods need to work with CORPs(Ultra)
"""
from config import ASRS
from datetime import datetime
import paramiko
import time
import os


class SSH:
    def __init__(self, host, user, password, port=22):
        self.client = None
        self.conn = None
        self.host = host
        self.user = user
        self.password = password
        self.port = port

    def connect(self):
        """Open ssh connection."""
        if self.conn is None:
            try:
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(hostname=self.host, port=self.port, username=self.user, password=self.password)
                return self.client
            except paramiko.AuthenticationException as authException:
                print(f"{authException}, please verify your credentials")
            except paramiko.SSHException as sshException:
                print(f"Could not establish SSH connection: {sshException}")

    def shell(self, cmd, pause=5):
        """"""
        with self.connect().invoke_shell() as shell:
            shell.send(cmd)
            time.sleep(pause)
            output = shell.recv(50000).decode('utf8')
            return output

    def execute_commands(self, cmd):
        """
        Execute command in succession.

        :param cmd: One command for example: show administrators
        :type cmd: str
        """
        stdin, stdout, stderr = self.client.exec_command(cmd)
        stdout.channel.recv_exit_status()
        response = stdout.readlines()
        return response

    def put(self, localpath, remotepath):
        sftp = self.client.open_sftp()
        sftp.put(localpath, remotepath)
        time.sleep(10)
        sftp.close()
        self.client.close()

    def get(self, remotepath, localpath):
        sftp = self.client.open_sftp()
        sftp.get(remotepath, localpath)
        time.sleep(10)
        sftp.close()
        self.client.close()

    def disconnect(self):
        """Close ssh connection."""
        if self.client:
            self.client.close()


def min11asr4():
    ip_asr4 = ASRS.IP_ASR4
    user = ASRS.STAROS_SCRIPTS_TACACS_USER
    password = ASRS.STAROS_SCRIPTS_TACACS_PASS
    ssh = SSH(host=ip_asr4, user=user, password=password)
    command = """context Gi
    sho subscribers data-rate ip-pool CONS-PUB-NAT-RANGE-1
    sho subscribers data-rate ip-pool CONS-PUB-NAT-RANGE-4
    sho subscribers data-rate ip-pool CONS-PUB-NAT-RANGE-3
    context SG
    sho subscribers data-rate ip-pool AV-PUB-RANGE-1
    sho subscribers data-rate ip-pool AV-PUB-RANGE-2
    end"""
    response = ssh.shell(command, pause=6)
    ssh.disconnect()
    return response


def min77um1sae():
    ip_um1sae = ASRS.IP_UM1SAE
    user = ASRS.STAROS_SCRIPTS_TACACS_USER
    password = ASRS.STAROS_SCRIPTS_TACACS_PASS
    ssh = SSH(host=ip_um1sae, user=user, password=password)
    command = """context Gi
    sho subscribers data-rate ip-pool CONS-PUB-BOT-NAT-RANGE-1
    end"""
    response = ssh.shell(command, pause=2)
    ssh.disconnect()
    return response


def min77um2sae1():
    ip_um2sae1 = ASRS.IP_UM2SAE1
    user = ASRS.STAROS_SCRIPTS_TACACS_USER
    password = ASRS.STAROS_SCRIPTS_TACACS_PASS
    ssh = SSH(host=ip_um2sae1, user=user, password=password)
    command = """context SG
    sho subscribers data-rate ip-pool AV-PUB-RANGE-1
    end"""
    response = ssh.shell(command, pause=2)
    ssh.disconnect()
    return response


def min77um2sae2():
    ip_um2sae2 = ASRS.IP_UM2SAE2
    user = ASRS.STAROS_SCRIPTS_TACACS_USER
    password = ASRS.STAROS_SCRIPTS_TACACS_PASS
    ssh = SSH(host=ip_um2sae2, user=user, password=password)
    command = """context Gi
    sho subscribers data-rate ip-pool CONS-PUB-BTK-NAT-RANGE-1
    sho subscribers data-rate ip-pool CONS-PUB-BOT-NAT-RANGE-1
    context SG
    sho subscribers data-rate ip-pool AV-PUB-RANGE-1
    sho subscribers data-rate ip-pool AV-PUB-RANGE-2
    end"""
    response = ssh.shell(command, pause=6)
    ssh.disconnect()
    return response


def writefile(text, filename):
    """
    Write a file using
    """
    with open(f"{os.path.abspath(os.getcwd())}/{filename}.txt", "a") as file_handler:
        file_handler.write(text)


def main():
    file_time = datetime.now().strftime("%H_%M")
    writefile(min11asr4(), f"min11asr4_{file_time}")
    writefile(min77um1sae(), f"min77um1sae_{file_time}")
    writefile(min77um2sae1(), f"min77um2sae1_{file_time}")
    writefile(min77um2sae2(), f"min77um2sae2_{file_time}")
    print("Getting subscribers Data Rate successful")


if __name__ == '__main__':
    main()
