import sys
import ipaddress as ipa
import scapy.all as sc

# Very slow and impractical solution just for fun!

def iprange(cidr):
    return [str(ip) for ip in ipa.IPv4Network(cidr)]

def icmp_er(ip):
    icmp = sc.IP(dst=ip)/sc.ICMP()
    resp = sc.sr1(icmp, timeout=.5)
    if resp == None:
        stat='\033[911m-\033[0m'
    else:
        stat='\033[92m+\033[0m'

    return ip + stat

def main():
    for ip in iprange(sys.argv[1]):
        try:
            print(icmp_er(ip))
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
        main()
