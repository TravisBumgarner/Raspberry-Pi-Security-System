# http://jessenoller.com/blog/2009/02/05/ssh-programming-with-paramiko-completely-different
import time
import paramiko
import socket
import dropbox
import datetime
import os
import sys

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


class Uploader:
    def __init__(self, ssh_host=None, ssh_username=None, ssh_password=None, dropbox_key=None):
        self.ssh_host = ssh_host
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        if self.ssh_host is not None:
            self.ssh = paramiko.SSHClient()
        self.dropbox_key = dropbox_key

    def is_connected_to_internet(self):
        """
        Check if there is an internet connection
        """
        try:
            host = socket.gethostbyname("www.google.com")
            s = socket.create_connection((host, 80), 2)
            return True
        except:
            pass
        return False

    def is_connected_to_ssh(self):
        try:
            self.ssh.get_transport().is_active()
        except AttributeError:
            return False
    
    def connect_to_ssh(self):
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ssh_host,
                             username = self.ssh_username,
                             password = self.ssh_password,
                             timeout = 5.0)
            time.sleep(6)
        except (TimeoutError, paramiko.ssh_exception.AuthenticationException):
            return "Check login credentials and/or internet connection."

        except:
            return "Some other error with Uploader.connect() occured."

    def upload_to_ssh(self, file_origin, file_destination ):
        sftp = self.ssh.open_sftp()
        _, filename = os.path.split(file_origin)
        file_data = datetime.datetime.strptime(filename[:-4], "%Y-%m-%d-%H-%M-%S")
        date = file_data.strftime("%Y-%m-%d")
        hour = file_data.strftime("%H")
        path = date + "/" + hour + "/"
        print(file_destination + path + filename)
        # This whole mess is because mkdir returns an error if the dir exists
        if file_destination is not "":
            try:
                sftp.mkdir(file_destination)
            except IOError:
                pass
        try:
            sftp.put(file_origin, file_destination + path + filename)
        except IOError:
            try:
                sftp.mkdir(file_destination + date)
            except IOError:
                try:
                    sftp.mkdir(file_destination + path)
                except:
                    sftp.put(file_origin, file_destination + path + filename)   
        return True

    def upload_to_dropbox(self, file):
        """
        Try to upload file to dropbox, return true if successful, otherwise false
        """
        try:
            client = dropbox.client.DropboxClient(self.dropbox_key)
            f = open(file, 'rb')
            response = client.put_file('/' + file, f)
            return True
        except dropbox.rest.ErrorResponse:
            raise RuntimeError("Check Dropbox installation instructions in readme.txt.")
            return False
