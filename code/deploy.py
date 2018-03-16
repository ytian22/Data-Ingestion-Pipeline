import paramiko
import os

def login_server(hostname, username, key):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    k = paramiko.RSAKey.from_private_key_file(key)
    ssh.connect(hostname=hostname,
                username=username, 
                pkey=k)
    print 'connected'
    return ssh

def copy_repo_2_server(ssh, repo):
    repo_name = os.path.basename(repo).split('.')[0]
    ssh.exec_command("rm -rf %s" % repo_name)  # delete if exists
    ssh.exec_command("git clone %s" % repo)   # git clone
    stdin, stdout, stderr = ssh.exec_command('ls')

    print 'Pull from Github successfully! Print the files in current directory:'
    print stdout.read().decode('utf-8')
    
def set_crontab(ssh, repo_path, script, prefix):
    # remove current crontab
    ssh.exec_command('crontab -r')

    # edd new crontab
    ssh.exec_command("echo '*/2 * * * * python " + repo_path + "/" + script + " " + prefix + "' > ~/crontabfile") 
    ssh.exec_command('crontab ~/crontabfile')

def deploy(key, hostname, username, prefix):
    ssh = login_server(hostname, username, key)
    copy_repo_2_server(ssh, git_repo)
    ssh.exec_command('python '+'~/crontab/process_json.py '+prefix)
    set_crontab(ssh, '~/crontab', 'log_rotate.py', prefix)
    ssh.close() # log out

if __name__ == '__main__':
    hostname = 'ec2-34-213-110-139.us-west-2.compute.amazonaws.com'
    username = 'testtest'
    git_repo = 'https://github.com/ytian22/crontab.git'
    key  = 'abc.pem'

    deploy(key, hostname, 'prefix')