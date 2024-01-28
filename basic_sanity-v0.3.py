import paramiko
import psutil

# SSH credentials
username = "your_username"
password = "your_password"

# Function to execute a command on a remote host via SSH
def execute_remote_command(host, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)
        result = stdout.read().decode("utf-8")
        client.close()
        return result
    except Exception as e:
        return f"Error executing command on {host}: {str(e)}"


# Function to get local system information
def get_local_system_info():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_usage, ram_usage, disk_usage


# Define your server details
web_servers = {
    # "web_server_1": {},
    # "web_server_2": {},
    # Commented out web servers
}

app_servers = {
    "app_server_1": {"ip_address": "10.10.0.20"},
    "app_server_2": {"ip_address": "10.10.0.19"},
    # Add more app servers as needed
}

db_servers = {
    # "db_server_1": {},
    # "db_server_2": {},
    # Commented out db servers
}

# Check Web Servers
# print("Web Servers:")
# for hostname, server_info in web_servers.items():
#     print(f"\n{hostname}:")
#     # Add checks for web servers as needed

# Check App Servers
print("\nApp Servers:")
for hostname, server_info in app_servers.items():
    print(f"\n{hostname} ({server_info['ip_address']}):")
    
    # Check Docker containers count
    docker_command = "docker ps -q | wc -l"
    container_count = int(execute_remote_command(server_info['ip_address'], docker_command))
    print(f"  - Docker Containers Running: {container_count}")
    
    # Add more checks for app servers as needed

# Check DB Servers
# print("\nDB Servers:")
# for hostname, server_info in db_servers.items():
#     print(f"\n{hostname}:")
#     # Add checks for db servers as needed

# Local System Information
print("\nLocal System Information:")
cpu, ram, disk = get_local_system_info()
print(f"  - CPU Usage: {cpu}%")
print(f"  - RAM Usage: {ram}%")
print(f"  - Disk Usage: {disk}%")
