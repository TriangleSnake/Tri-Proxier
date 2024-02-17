conf = """
server {
    listen 80;
    server_name a{server};
    return 301 https://$server_name$request_uri; # 强制重定向到HTTPS
}

server {
    listen 443 ssl;
    server_name {server};

    ssl_certificate /etc/letsencrypt/live/photos.trianglesnake.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/photos.trianglesnake.com/privkey.pem;

    location / {
        proxy_pass http://{target};
        include proxy_params; # 包含proxy_set_header等指令
    }
}


"""
server = input("Please input the domain name:(i.e. test.trianglesnake.com)")
target = input("Please input the target ip address:(i.e. 192.168.22.10:8080)")
if ":" not in target:
    target += ":80"

conf = conf.format(server=server, target=target)
with open("/etc/nginx/sites-enaable/"+server, "w") as f:
    f.write(conf)

# argv1=domain
# argv2=target address


    