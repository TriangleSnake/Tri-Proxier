conf = """
server {{
    listen 80;
    server_name {server};
    return 301 https://$server_name$request_uri; # 强制重定向到HTTPS
}}

server {{
    listen 443 ssl;
    server_name {server};

    ssl_certificate /etc/letsencrypt/live/{server}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{server}/privkey.pem;

    location / {{
        proxy_pass http://{target};
        include proxy_params; # 包含proxy_set_header等指令
    }}
}}
"""

server = input("Please input the domain name (e.g., test.trianglesnake.com): ")
target = input("Please input the target IP address and port (e.g., 192.168.22.10:8080): ")
if ":" not in target:
    target += ":80"

conf = conf.format(server=server, target=target)

# 请确保您有权限写入/etc/nginx/sites-enabled/，这可能需要sudo权限
file_path = "/etc/nginx/sites-enabled/" + server
with open(file_path, "w") as f:
    f.write(conf)

print(f"Nginx configuration for {server} has been created.")
