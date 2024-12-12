import base64

def decode_ss_url(ss_url):
    try:
        if 'ss://' not in ss_url:
            raise ValueError("Invalid SS URL format: missing 'ss://' prefix")
        
        parts = ss_url.split('ss://')
        if len(parts) != 2:
            raise ValueError("Invalid SS URL format")
        
        encoded_parts = parts[1].split('#', 1)
        encoded_part = encoded_parts[0]
        
        padding = 4 - (len(encoded_part) % 4)
        if padding != 4:
            encoded_part += '=' * padding

        decoded_data = base64.urlsafe_b64decode(encoded_part).decode('utf-8')
        
        if '@' not in decoded_data:
            raise ValueError("Invalid SS URL format: missing '@' separator")
        
        method_password, server_info = decoded_data.split('@', 1)
        if ':' not in method_password:
            raise ValueError("Invalid SS URL format: missing method:password separator")
        
        method, password = method_password.split(':', 1)
        server, port = server_info.split(':', 1)
        
        return method, password, server, port
    except Exception as e:
        raise ValueError(f"Failed to decode SS URL: {str(e)}")

def format_proxy_name(name, existing_names):
    formatted_name = name.replace(',', '').strip()
    if formatted_name in existing_names:
        index = 1
        new_name = f"{formatted_name}_{index}"
        while new_name in existing_names:
            index += 1
            new_name = f"{formatted_name}_{index}"
        formatted_name = new_name
    return formatted_name

def get_region_code(name):
    region_patterns = {
        'HK': ['HK', '香港', 'Hong Kong', 'HongKong'],
        'US': ['US', '美国', 'United States', 'USA'],
        'JP': ['JP', '日本', 'Japan'],
        'TW': ['TW', '台湾', 'Taiwan'],
        'SG': ['SG', '新加坡', 'Singapore'],
        'KR': ['KR', '韩国', 'Korea'],
        'CA': ['CA', '加拿大', 'Canada'],
        'UK': ['UK', '英国', 'United Kingdom'],
        'DE': ['DE', '德国', 'Germany'],
        'FR': ['FR', '法国', 'France'],
        'AU': ['AU', '澳大利亚', 'Australia'],
    }
    
    region_map = {
        'HK': '香港',
        'US': '美国',
        'JP': '日本',
        'TW': '台湾',
        'SG': '新加坡',
        'KR': '韩国',
        'CA': '加拿大',
        'UK': '英国',
        'DE': '德国',
        'FR': '法国',
        'AU': '澳大利亚',
    }
    
    name_upper = name.upper()
    for code, patterns in region_patterns.items():
        for pattern in patterns:
            if pattern.upper() in name_upper:
                return code, region_map[code]
    
    return None, None

def generate_proxy_config(lines):
    region_proxies = {}
    proxy_configs = "[Proxy]\nDIRECT = direct\n"
    existing_names = set()
    
    for line in lines:
        if line.strip():
            ss_url = line.strip()
            method, password, server, port = decode_ss_url(ss_url)
            base_name = ss_url.split('#')[1] if '#' in ss_url else server
            name = format_proxy_name(base_name, existing_names)
            existing_names.add(name)
            region_code, region_name = get_region_code(name)
            
            if region_code:
                if region_code not in region_proxies:
                    region_proxies[region_code] = {'name': region_name, 'proxies': []}
                region_proxies[region_code]['proxies'].append(name)
            
            config_line = f'"{name}" = ss, {server}, {port}, encrypt-method={method}, password={password}, tfo=false, udp-relay=false\n'
            proxy_configs += config_line

    config = """#!MANAGED-CONFIG  https://cdn.jsdelivr.net/gh/leegang/Nothing@main/REMOTE.conf interval=21600 strict=false
    [General]
loglevel = notify
bypass-system = true
skip-proxy = 127.0.0.1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,100.64.0.0/10,localhost,*.local,e.crashlytics.com,captive.apple.com,::ffff:0:0:0:0/1,::ffff:128:0:0:0/1
bypass-tun = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12
dns-server = system,119.29.29.29,223.5.5.5

"""
    config += proxy_configs

    config += "\n[Proxy Group]\n"
    
    all_region_groups = ['DIRECT'] + [f'{name}节点' for code, name in sorted([(k, v['name']) for k, v in region_proxies.items()])]
    config += f'Proxy = select, {", ".join(all_region_groups)}\n'
    
    for region_code, region_info in sorted(region_proxies.items()):
        region_name = region_info['name']
        proxies = region_info['proxies']
        if proxies:
            config += f'{region_name}节点 = url-test, {", ".join(proxies)}, url=http://www.gstatic.com/generate_204, interval=600, tolerance=100\n'

    config += """
[Rule]
FINAL,Proxy
"""
    return config

def main():
    try:
        with open('url.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        proxy_config = generate_proxy_config(lines)

        with open('REMOTE.conf', 'w', encoding='utf-8') as file:
            file.write(proxy_config)

        print("Configuration generated successfully:")
        print(proxy_config)
        
    except FileNotFoundError:
        print("Error: url.txt file not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
