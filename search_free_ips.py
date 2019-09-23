import socket,os,time
from datetime import datetime

def salvar_ip(addr):
    arquivo = open('ips.txt', 'r')
    conteudo = arquivo.readlines()
    conteudo.append('\n'+addr)
    arquivo = open('ips.txt', 'w')
    arquivo.writelines(conteudo)
    arquivo.close()

net = input("Enter the IP Gateway address: ")
net1 = net.split('.')
prefeitura_gateway = "192.168.1.1"
casa_gateway = "10.2.0.1"
facul_gateway = "10.20.25.1" #LAB5
pref_mask = "255.255.252.0"
casa_mask = "255.255.255.0"
'''
essential knew what is the mask
'''


mascara = pref_mask
gateway = prefeitura_gateway
net2 = net1[0] + '.' + net1[1] + '.'
t1 = datetime.now()

def scan_t(addr):
    socket.setdefaulttimeout(0.25)
    t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        t.connect((addr, 80))
        return 1
    except:
        return 0
def scan(addr):
    socket.setdefaulttimeout(0.25)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((addr, 445))
    if result != 0:
        result = s.connect_ex((addr, 80))
        if result != 0:
            result = s.connect_ex((addr, 21))
            if result != 0:
                result = s.connect_ex((addr, 22))
                if result != 0:
                    result = s.connect_ex((addr, 23))
                    if result != 0:
                        result = s.connect_ex((addr, 53))
                        if result != 0:
                            result = s.connect_ex((addr, 135))
                            if result != 0:
                                result = s.connect_ex((addr, 139))
                                if result != 0:
                                    result = s.connect_ex((addr, 443))
    if result == 0:
        return 1
    else:
        return 0


def run1():
    for rede in range(0, 254):
        #rede = 25
        print(net2 + str(rede) + '.' + str(0))
        for ip in range(1,254):
            addr = net2 + str(rede) + '.' + str(ip)
            print("...")
            if (scan(addr)):
                print(f"{addr}: Sendo Usado")
            else:
                os.popen(f"netsh interface ip set address name=\"Ethernet\" static {addr} {mascara} {gateway} 1")
                os.popen("ipconfig /all")
                t_ip = "1.1.1.1"
                target = socket.gethostbyname(t_ip)
                time.sleep(4)
                if (scan_t(target)):
                    salvar_ip(addr)
                    print(f"------------> \"{addr}\": IP WITH INTERNET  <---------------")
                else:
                    print(f"------------> \"{addr}\": IP BLOCKED <---------------")



if __name__ == "__main__":
    t_ip = "1.1.1.1"
    print(t_ip)
    target = socket.gethostbyname(t_ip)
    if (scan_t(target)):
        print("------------ ALLRIGHT ------------")
    else:
        print("--- YOU START WITHOUT INTERNET ---")
    run1()
    t2 = datetime.now()
    total = t2 - t1
    print("Scanning completed in: ", total)