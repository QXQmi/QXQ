import requests
import re
import os
import sys
import argparse
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def banner():
    test = """
    ██████╗ ███████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔════╝██╔══██╗
    ██████╔╝█████╗  ██║     ██║   ██║█████╗  ██████╔╝
    ██╔══██╗██╔══╝  ██║     ██║   ██║██╔══╝  ██╔══██╗
    ██████╔╝███████╗╚██████╗╚██████╔╝███████╗██║  ██║
    ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝

                                            CVE-2023-44487 检测工具
                                            author: QXQ
                                            date: 2024.09.17
                                            version: 1.0
    """
    print(test)


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="HTTP/2 Rapid Reset Attack 漏洞检测工具 (CVE-2023-44487)")
    parse.add_argument("-u", "--url", dest="url", type=str, help="指定单个检测URL")
    parse.add_argument("-f", "--file", dest="file", type=str, help="指定包含多个URL的文件")

    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"使用方法:\n\t python3 {sys.argv[0]} -h 查看帮助")


def poc(target):
    payload = '/test'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        if not target.startswith(('http://', 'https://')):
            target = f"https://{target}"

        res = requests.get(
            url=target + payload,
            headers=headers,
            verify=False,
            timeout=10,
            allow_redirects=True
        )

        vulnerable_phrases = ["internal server error", "service unavailable"]
        vulnerable = False
        for phrase in vulnerable_phrases:
            if phrase in res.text.lower():
                vulnerable = True
                break
        if 500 <= res.status_code < 600:
            vulnerable = True

        if vulnerable:
            print(f"[+]{target} 可能存在CVE-2023-44487漏洞")
            with open('CVE-2023-44487_result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f"[-]{target} 未检测到漏洞迹象")

    except requests.exceptions.Timeout:
        print(f"[!]{target} 请求超时")
    except requests.exceptions.ConnectionError:
        print(f"[!]{target} 连接错误")
    except Exception as e:
        print(f"[!]{target} 发生错误: {str(e)}")


if __name__ == '__main__':

    main()
