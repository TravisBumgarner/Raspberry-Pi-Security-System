import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("web541.webfaction.com",
                             username = "chsrasppi",
                             password = "LetsSpyGuy",
                             timeout = 5.0)
sftp = self.ssh.open_sftp()
sftp.mkdir(path)
