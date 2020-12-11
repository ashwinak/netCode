import paramiko
import time
import threading

def connect(server_ip, server_port, user, passwd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to {server_ip}')
    ssh_client.connect(hostname=server_ip, port=server_port, username=user, password=passwd,
                       look_for_keys=False, allow_agent=False)
    return ssh_client

## SOLUTION
# this function will get executed by each thread
def target_function(router):
    ssh_client = connect(server_ip=router['server_ip'], server_port=router['server_port'], user=router['user'],
                             passwd=router['passwd'])

    shell = ssh_client.invoke_shell()
    with open (router['config']) as f:
        commands = f.read().splitlines()
    for cmd in commands:
        shell.send(cmd + '\n')
        time.sleep(1)
    output = shell.recv(100000)
    print(output.decode())
    ssh_client.close()

router1 = {'server_ip': 'localhost', 'server_port': '22', 'user':'aa', 'passwd':'blah', 'config':'ospf.txt'}
router2 = {'server_ip': 'localhost', 'server_port': '22', 'user': 'aa', 'passwd': 'blah', 'config':'eigrp.txt'}
router3 = {'server_ip': 'localhost', 'server_port': '22', 'user': 'aa', 'passwd': 'blah', 'config':'router3.txt'}

devices = [router1, router2, router3]
my_threads = list()
for router in devices:
    th = threading.Thread(target=target_function, args=(router,))
    my_threads.append(th)
for th in my_threads:
    th.start()

