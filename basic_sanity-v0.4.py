import requests
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
    "web_server_1": {"ip_address": "10.10.0.1"},
    "web_server_2": {"ip_address": "10.10.0.2"},
    # Add more web servers as needed
}

app_servers = {
    "app_server_1": {"ip_address": "10.10.0.3"},
    "app_server_2": {"ip_address": "10.10.0.4"},
    # Add more app servers as needed
}

db_servers = {
    "db_server_1": {"ip_address": "10.10.0.5"},
    "db_server_2": {"ip_address": "10.10.0.6"},
    # Add more db servers as needed
}

# Check Web, App, and DB Servers
for server_type, servers in [("Web Servers", web_servers), ("App Servers", app_servers), ("DB Servers", db_servers)]:
    print(f"\n{server_type}:")
    
    for hostname, server_info in servers.items():
        print(f"\n{hostname} ({server_info.get('ip_address', 'No IP Address')}):")
        
        # Check CPU Usage
        cpu_command = "top -b -n 1 | grep '%Cpu(s)'"
        cpu_result = execute_remote_command(hostname, cpu_command)
        print(f"  - CPU Usage: {cpu_result.strip()}")
        
        # Check Mount Point Utilization
        mount_point_command = "df -h /"
        mount_point_result = execute_remote_command(hostname, mount_point_command)
        print(f"  - Mount Point Utilization:\n{mount_point_result.strip()}")
        
        # Check Memory Utilization
        memory_command = "free -m | grep Mem"
        memory_result = execute_remote_command(hostname, memory_command)
        print(f"  - Memory Utilization:\n{memory_result.strip()}")

        # Example: Check Docker containers count using a hypothetical API endpoint
        api_endpoint = f"http://{server_info.get('ip_address', '')}/api/docker/containers/count"
        try:
            response = requests.get(api_endpoint)
            container_count = response.json().get("count", "Error retrieving count")
            print(f"  - Docker Containers Running: {container_count}")
        except Exception as e:
            print(f"  - Error: {str(e)}")

# Local System Information
print("\nLocal System Information:")
cpu, ram, disk = get_local_system_info()
print(f"  - CPU Usage: {cpu}%")
print(f"  - RAM Usage: {ram}%")
print(f"  - Disk Usage: {disk}%")
