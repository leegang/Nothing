import base64

def decode_ss_url(ss_url):
    try:
        # Split the URL and handle potential formatting issues
        if 'ss://' not in ss_url:
            raise ValueError("Invalid SS URL format: missing 'ss://' prefix")
        
        parts = ss_url.split('ss://')
        if len(parts) != 2:
            raise ValueError("Invalid SS URL format")
        
        # Split at '#' if exists, otherwise just use the encoded part
        encoded_parts = parts[1].split('#', 1)
        encoded_part = encoded_parts[0]
        
        # Add padding if necessary
        padding = 4 - (len(encoded_part) % 4)
        if padding != 4:
            encoded_part += '=' * padding

        # Decode the base64 part
        decoded_data = base64.urlsafe_b64decode(encoded_part).decode('utf-8')
        
        # Split the decoded data
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

def format_proxy_name(name):
    # Remove any commas and trim whitespace
    formatted_name = name.replace(',', '').strip()
    # Ensure name is unique by adding index if needed
    return formatted_name

def generate_proxy_config(lines):
    proxy_config = "[Proxy]\nDIRECT = direct\n"
    used_names = set()
    
    for line in lines:
        if not line.strip():  # Skip empty lines
            continue
            
        try:
            ss_url = line.strip()
            method, password, server, port = decode_ss_url(ss_url)
            
            # Extract name from URL or use server address if no name provided
            name = ss_url.split('#')[1] if '#' in ss_url else server
            
            # Format and ensure unique name
            base_name = format_proxy_name(name)
            final_name = base_name
            counter = 1
            
            while final_name in used_names:
                final_name = f"{base_name}{counter}"
                counter += 1
            
            used_names.add(final_name)
            
            config_line = (f'"{final_name}" = ss, {server}, {port}, '
                         f'encrypt-method={method}, password={password}, '
                         f'tfo=false, udp-relay=false\n')
            proxy_config += config_line
            
        except Exception as e:
            print(f"Warning: Skipping invalid line: {line.strip()} - {str(e)}")
            continue
    
    return proxy_config

def main():
    try:
        with open('url.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        proxy_config = generate_proxy_config(lines)

        with open('config.txt', 'w', encoding='utf-8') as file:
            file.write(proxy_config)

        print("Configuration generated successfully:")
        print(proxy_config)
        
    except FileNotFoundError:
        print("Error: url.txt file not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
