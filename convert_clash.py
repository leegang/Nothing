import base64
import yaml

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

def generate_clash_config(lines):
    proxies = []
    existing_names = set()
    
    for line in lines:
        if line.strip():
            ss_url = line.strip()
            method, password, server, port = decode_ss_url(ss_url)
            base_name = ss_url.split('#')[1] if '#' in ss_url else server
            name = format_proxy_name(base_name, existing_names)
            existing_names.add(name)
            
            proxy = {
                'name': name,
                'type': 'ss',
                'server': server,
                'port': int(port),
                'cipher': method,
                'password': password,
                'udp': False
            }
            proxies.append(proxy)
    
    config = {
        'proxies': proxies,
        'proxy-groups': [
            {
                'name': 'Proxy',
                'type': 'select',
                'proxies': [proxy['name'] for proxy in proxies]
            }
        ],
        'rules': [
            'DOMAIN-SUFFIX,ipwho.is,Proxy',
            'MATCH,Proxy'
        ]
    }
    
    return yaml.dump(config, allow_unicode=True)

def main():
    try:
        with open('url.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        clash_config = generate_clash_config(lines)

        with open('clash.yaml', 'w', encoding='utf-8') as file:
            file.write(clash_config)

        print("Clash configuration generated successfully:")
        print(clash_config)
        
    except FileNotFoundError:
        print("Error: url.txt file not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
