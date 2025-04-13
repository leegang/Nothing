import requests
import re

def fetch_vmess_nodes(url):
    try:
        # 发送GET请求获取内容
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，抛出异常
        content = response.text

        # 使用正则表达式匹配VMess节点（示例正则表达式）
        vmess_nodes = re.findall(r'vmess://[a-zA-Z0-9+/=]+', content)

        if vmess_nodes:
            print("发现以下VMess节点：")
            for i, node in enumerate(vmess_nodes, 1):
                print(f"{node}")
        else:
            print("未找到任何VMess节点。")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")

# 指定目标URL
url = "https://raw.githubusercontent.com/leetomlee123/freenode/refs/heads/main/README.md"

# 调用函数
fetch_vmess_nodes(url)
