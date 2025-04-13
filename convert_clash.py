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
    # 保存为 Clash 配置文件
    clash_config = {
        "proxies": clash_nodes,
        "proxy-groups": [
            {
                "name": "🚀 手动切换",
                "type": "select",
                "proxies": ["♻️ 自动选择", "🔀 负载均衡"] + [proxy['name'] for proxy in clash_nodes]
            },
            {
                "name": "♻️ 自动选择",
                "type": "url-test",
                "lazy": True,
                "url": "http://www.gstatic.com/generate_204",
                "interval": 600,
                "proxies": [proxy['name'] for proxy in clash_nodes]
            },
            {
                "name": "🔀 负载均衡",
                "type": "load-balance",
                "proxies": [proxy['name'] for proxy in clash_nodes]
            }
        ],
        "rules": [
            "RULE-SET,applications,DIRECT",
            "DOMAIN,clash.razord.top,DIRECT",
            "DOMAIN,yacd.haishan.me,DIRECT",
            "RULE-SET,private,DIRECT",
            "RULE-SET,reject,REJECT",
            "RULE-SET,icloud,DIRECT",
            "RULE-SET,apple,DIRECT",
            "RULE-SET,google,🚀 手动切换",
            "RULE-SET,proxy,♻️ 自动选择",
            "RULE-SET,direct,DIRECT",
            "RULE-SET,lancidr,DIRECT",
            "RULE-SET,cncidr,DIRECT",
            "RULE-SET,telegramcidr,♻️ 自动选择",
            "GEOIP,LAN,DIRECT",
            "GEOIP,CN,DIRECT",
            "MATCH,♻️ 自动选择"
        ],
        "rule-providers": {
            "reject": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/reject.txt",
                "path": "./ruleset/reject.yaml",
                "interval": 86400
            },
            "icloud": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/icloud.txt",
                "path": "./ruleset/icloud.yaml",
                "interval": 86400
            },
            "apple": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/apple.txt",
                "path": "./ruleset/apple.yaml",
                "interval": 86400
            },
            "google": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/google.txt",
                "path": "./ruleset/google.yaml",
                "interval": 86400
            },
            "proxy": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/proxy.txt",
                "path": "./ruleset/proxy.yaml",
                "interval": 86400
            },
            "direct": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/direct.txt",
                "path": "./ruleset/direct.yaml",
                "interval": 86400
            },
            "private": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/private.txt",
                "path": "./ruleset/private.yaml",
                "interval": 86400
            },
            "gfw": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/gfw.txt",
                "path": "./ruleset/gfw.yaml",
                "interval": 86400
            },
            "tld-not-cn": {
                "type": "http",
                "behavior": "domain",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/tld-not-cn.txt",
                "path": "./ruleset/tld-not-cn.yaml",
                "interval": 86400
            },
            "telegramcidr": {
                "type": "http",
                "behavior": "ipcidr",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/telegramcidr.txt",
                "path": "./ruleset/telegramcidr.yaml",
                "interval": 86400
            },
            "cncidr": {
                "type": "http",
                "behavior": "ipcidr",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/cncidr.txt",
                "path": "./ruleset/cncidr.yaml",
                "interval": 86400
            },
            "lancidr": {
                "type": "http",
                "behavior": "ipcidr",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/lancidr.txt",
                "path": "./ruleset/lancidr.yaml",
                "interval": 86400
            },
            "applications": {
                "type": "http",
                "behavior": "classical",
                "url": "https://cdn.jsdelivr.net/gh/Loyalsoldier/clash-rules@release/applications.txt",
                "path": "./ruleset/applications.yaml",
                "interval": 86400
            }
        }
    }

    # 保存到文件
    with open("clash_nodes.yaml", "w", encoding="utf-8") as f:
        import yaml
        yaml.dump(clash_config, f, default_flow_style=False, allow_unicode=True)

    print("\n转换完成，结果保存在 clash_nodes.yaml 文件中！")

if __name__ == "__main__":
    main()
