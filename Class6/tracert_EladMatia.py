from scapy3k.all import *
from time import sleep

DNS_IP = "8.8.8.8"
DNS_PORT = 53
SRC_PORT = 10212


def main():
    url = input("Enter a domain: ")
    ip = dns_lookup(url)
    ipmsg = IP(dst=ip, ttl=1)
    icmpmsg = ICMP()
    ans = sr1(ipmsg/icmpmsg, verbose=0)
    index = 1
    while ans[IP].src != ip:
        print(index, ". ", ans[IP].src)
        ipmsg.ttl += 1
        index += 1
        ans = sr1(ipmsg / icmpmsg, verbose=0)
        sleep(2)

    print(index, ". ", ans[IP].src)
    print("Destination reached! Total of", index, "hopes")


def dns_lookup(url):
    """
    The function sends a dns request to 8.8.8.8 and prints the response
    :param url: the requested url to find
    :type url: str
    :return: None
    :rtype: None
    """
    ethmsg = Ether()
    ipmsg = IP(dst=DNS_IP)
    udpmsg = UDP(sport=SRC_PORT, dport=DNS_PORT)
    dnsmsg = DNS(rd=1, qd=DNSQR(qname=url))
    msg = ethmsg / ipmsg / udpmsg / dnsmsg
    ans = srp1(msg, verbose=0)
    return ans[DNS][DNSRR].rdata


if __name__ == '__main__':
    main()
