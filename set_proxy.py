import subprocess

conf_template = """
server {{
    listen 80;
    server_name {server};
    return 301 https://$server_name$request_uri; # 强制重定向到HTTPS
}}

server {{
    listen 443 ssl;
    server_name {server};

    ssl_certificate /etc/letsencrypt/live/trianglesnake.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/trianglesnake.com/privkey.pem;

    location / {{
        proxy_pass http://{target};
        include proxy_params; # 包含proxy_set_header等指令
    }}
}}
"""

server = input("Please input the domain name (e.g., photos.trianglesnake.com): ")
target = input("Please input the target IP address and port (e.g., 192.168.22.10:8080): ")
if ":" not in target:
    target += ":80"

conf = conf_template.format(server=server, target=target)

# 确保您有权限写入/etc/nginx/sites-enabled/，这可能需要sudo权限
file_path = "/etc/nginx/sites-enabled/" + server.replace('.', '_')
with open(file_path, "w") as f:
    f.write(conf)

print(f"Nginx configuration for {server} has been created.")

# 重载Nginx配置
try:
    subprocess.run(['sudo', 'nginx', '-t'], check=True)  # 测试Nginx配置
    subprocess.run(['sudo', 'systemctl', 'reload', 'nginx'], check=True)  # 重载Nginx
    print("Nginx has been reloaded successfully.")
except subprocess.CalledProcessError:
    print("Failed to reload Nginx. Please check the configuration.")
