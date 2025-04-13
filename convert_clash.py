import base64
import json

def parse_vmess_node(vmess_url):
    """
    解析vmess节点并返回JSON格式
    """
    try:
        # 解析Base64部分
        encoded_data = vmess_url[len("vmess://"):]
        decoded_data = base64.urlsafe_b64decode(encoded_data + "=" * (-len(encoded_data) % 4)).decode('utf-8')
        return json.loads(decoded_data)
    except Exception as e:
        print(f"解析失败: {e}")
        return None

def convert_to_clash(vmess_data):
    """
    将vmess数据转换为Clash节点格式
    """
    try:
        return {
            "name": vmess_data.get("ps", "Unnamed"),
            "type": "vmess",
            "server": vmess_data["add"],
            "port": int(vmess_data["port"]),
            "uuid": vmess_data["id"],
            "alterId": int(vmess_data.get("aid", 0)),
            "cipher": "auto",
            "network": vmess_data["net"],
            "tls": True if vmess_data.get("tls", "").lower() == "tls" else False,
            "ws-opts": {
                "path": vmess_data.get("path", "/"),
                "headers": {
                    "Host": vmess_data.get("host", "")
                }
            } if vmess_data["net"] == "ws" else None
        }
    except KeyError as e:
        print(f"缺少必要字段: {e}")
        return None

def main():
    # 从 ss.txt 文件读取vmess节点
    try:
        with open("ss.txt", "r") as file:
            vmess_urls = [line.strip() for line in file if line.startswith("vmess://")]
    except FileNotFoundError:
        print("未找到 ss.txt 文件，请确保文件存在于当前目录中。")
        return

    # 打印读取到的 vmess_urls
    print("\n读取到的 vmess URLs：")
    for url in vmess_urls:
        print(url)

    clash_nodes = []

    for vmess_url in vmess_urls:
        vmess_data = parse_vmess_node(vmess_url)
        if vmess_data:
            clash_node = convert_to_clash(vmess_data)
            if clash_node:
                clash_nodes.append(clash_node)

    # 打印生成的 Clash 节点
    print("\n生成的 Clash 节点：")
    for node in clash_nodes:
        print(json.dumps(node, indent=4, ensure_ascii=False))

    # 输出为Clash配置文件
    clash_config = {
        "proxies": clash_nodes
    }

    # 保存到文件
    with open("clash_nodes.yaml", "w") as f:
        import yaml
        yaml.dump(clash_config, f, default_flow_style=False, allow_unicode=True)

    print("\n转换完成，结果保存在 clash_nodes.yaml 文件中！")

if __name__ == "__main__":
    main()
