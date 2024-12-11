import base64

# Function to decode SS URL
def decode_ss_url(ss_url):
    encoded_part = ss_url.split('ss://')[1].split('#')[0]
    decoded_data = base64.urlsafe_b64decode(encoded_part).decode('utf-8')
    password, server_info = decoded_data.split('@')
    server, port = server_info.split(':')
    return password, server, port

# Function to generate proxy configuration
def generate_proxy_config(lines):
    proxy_config = "[Proxy]\\nDIRECT = direct\\n"
    for line in lines:
        if line.strip():  # Skip empty lines
            ss_url = line.split('|')[1].strip()
            password, server, port = decode_ss_url(ss_url)
            name = ss_url.split('#')[1]
            config_line = f'"{name}" = ss, {server}, {port}, encrypt-method=aes-256-cfb, password={password}, tfo=false, udp-relay=false\\n'
            proxy_config += config_line
    return proxy_config

# Read the contents of url.txt
with open('url.txt', 'r') as file:
    lines = file.readlines()

# Generate and print the proxy configuration
proxy_config = generate_proxy_config(lines)
print(proxy_config)
