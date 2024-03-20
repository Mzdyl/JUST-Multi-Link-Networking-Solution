import paramiko

# 定义OpenWRT路由器的IP地址、用户名和密码
router_ip = 'your_router_ip'
username = 'your_username'
password = 'your_password'

# 要添加的接口配置信息
new_interface_config = """
config interface 'VWAN'
        option proto 'dhcp'
        option ifname 'veth0.2'
#       option macaddr 'D8:C8:E9:E4:3A:22'
        option metric '12'
"""
        
new_veth_config="""
config device 'veth0.2'
        option name 'veth0.2'
        option ifname 'eth0.2'
        option type 'macvlan'
"""

# 连接到路由器
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(router_ip, username=username, password=password)

# 执行命令以将新接口配置添加到/etc/config/network文件中
command_interface = f"echo '{new_interface_config}' >> /etc/config/network"
stdin_interface, stdout_interface, stderr_interface = ssh_client.exec_command(command_interface)

command_veth = f"echo '{new_veth_config}' >> /etc/config/network"
stdin_veth, stdout_veth, stderr_veth = ssh_client.exec_command(command_veth)

# 保存配置并重新启动网络
stdin_restart, stdout_restart, stderr_restart = ssh_client.exec_command("/etc/init.d/network restart")

# 执行命令以获取VWAN接口的IP地址
stdin_ip, stdout_ip, stderr_ip = ssh_client.exec_command("ifconfig VWAN_1 | grep 'inet ' | awk '{print $2}'")

# 读取命令输出
vwan_ip = stdout_ip.read().decode().strip()

# 关闭SSH连接
ssh_client.close()

# 打印命令执行结果
#print("Output:", stdout.read().decode('utf-8'))


requests.post('http://172.18.254.15/api/v1/login', json={"username":"{username}","password":"{password}","ifautologin":"1","channel":"{channel}","pagesign":"secondauth","usripadd":"{vwan_ip}"}, headers={'Content-Type': 'application/json'}, verify=False)



