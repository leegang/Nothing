import base64

def decode_ss_url(ss_url):
    encoded_part = ss_url.split('ss://')[1].split('#')[0]
    decoded_data = base64.urlsafe_b64decode(encoded_part).decode('utf-8')
    method, password_server_info = decoded_data.split(':', 1)
    password, server_info = password_server_info.split('@')
    server, port = server_info.split(':')
    return method, password, server, port

def generate_proxy_config(lines):
    proxy_config = "[Proxy]\nDIRECT = direct\n"
    for line in lines:
        if line.strip():  # Skip empty lines
            ss_url = line.strip()
            method, password, server, port = decode_ss_url(ss_url)
            name = ss_url.split('#')[1]
            config_line = f'"{name}" = ss, {server}, {port}, encrypt-method={method}, password={password}, tfo=false, udp-relay=false\n'
            proxy_config += config_line
    return proxy_config

with open('url.txt', 'r') as file:
    lines = file.readlines()

proxy_config = generate_proxy_config(lines)
print(proxy_config)
