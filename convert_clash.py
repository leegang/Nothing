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
            'RULE-SET,applications,DIRECT',
            'DOMAIN,clash.razord.top,DIRECT',
            'DOMAIN,yacd.haishan.me,DIRECT',
            'RULE-SET,private,DIRECT',
            'RULE-SET,reject,REJECT',
            'RULE-SET,icloud,DIRECT',
            'RULE-SET,apple,DIRECT',
            'RULE-SET,google,Proxy',
            'RULE-SET,proxy,Proxy',
            'RULE-SET,direct,DIRECT',
            'RULE-SET,lancidr,DIRECT',
            'RULE-SET,cncidr,DIRECT',
            'RULE-SET,telegramcidr,Proxy',
            'GEOIP,LAN,DIRECT',
            'GEOIP,CN,DIRECT',
            'MATCH,Proxy'
        ],
        'rule-providers': {
            'reject': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt',
                'path': './ruleset/reject.yaml',
                'interval': 86400
            },
            'icloud': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/icloud.txt',
                'path': './ruleset/icloud.yaml',
                'interval': 86400
            },
            'apple': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/apple.txt',
                'path': './ruleset/apple.yaml',
                'interval': 86400
            },
            'google': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/google.txt',
                'path': './ruleset/google.yaml',
                'interval': 86400
            },
            'proxy': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt',
                'path': './ruleset/proxy.yaml',
                'interval': 86400
            },
            'direct': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt',
                'path': './ruleset/direct.yaml',
                'interval': 86400
            },
            'private': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt',
                'path': './ruleset/private.yaml',
                'interval': 86400
            },
            'gfw': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/gfw.txt',
                'path': './ruleset/gfw.yaml',
                'interval': 86400
            },
            'tld-not-cn': {
                'type': 'http',
                'behavior': 'domain',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/tld-not-cn.txt',
                'path': './ruleset/tld-not-cn.yaml',
                'interval': 86400
            },
            'telegramcidr': {
                'type': 'http',
                'behavior': 'ipcidr',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/telegramcidr.txt',
                'path': './ruleset/telegramcidr.yaml',
                'interval': 86400
            },
            'cncidr': {
                'type': 'http',
                'behavior': 'ipcidr',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt',
                'path': './ruleset/cncidr.yaml',
                'interval': 86400
            },
            'lancidr': {
                'type': 'http',
                'behavior': 'ipcidr',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt',
                'path': './ruleset/lancidr.yaml',
                'interval': 86400
            },
            'applications': {
                'type': 'http',
                'behavior': 'classical',
                'url': 'https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/applications.txt',
                'path': './ruleset/applications.yaml',
                'interval': 86400
            }
        }
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
