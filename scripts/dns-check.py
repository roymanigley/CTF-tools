import dns.resolver
import dns.query
import dns.exception
import argparse


def check_dns_cache_snooping(domain, dns_server):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        answer = resolver.resolve(domain, 'A', raise_on_no_answer=False, search=False)
        if answer.rrset:
            return True, "An attacker can query the DNS server to check if a particular domain is cached, which can provide insights into user browsing behavior or internal network structure.", f"dig @{dns_server} {domain} +norecurse"
    except dns.exception.DNSException:
        return False, "", ""
    return False, "", ""

def check_open_resolver(dns_server):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        answer = resolver.resolve('example.com', 'A')
        return True, "An open DNS resolver can be abused in DDoS attacks or to query internal networks, exposing internal IP addresses and services.", f"dig @{dns_server} example.com"
    except dns.exception.DNSException:
        return False, "", ""
    return False, "", ""

def check_dnssec(domain):
    try:
        response = dns.resolver.resolve(domain, 'DNSKEY', raise_on_no_answer=False)
        if response.rrset:
            return True, "DNSSEC is properly configured, reducing the risk of DNS spoofing attacks.", "No exploitation necessary; DNSSEC is a security measure."
    except dns.exception.DNSException:
        return False, "DNSSEC is not configured. This makes the domain vulnerable to DNS spoofing attacks, where an attacker can redirect users to malicious sites.", f"dig {domain} DNSKEY"
    return False, "", ""

def check_wildcard(domain):
    try:
        subdomain = 'nonexistent.' + domain
        response = dns.resolver.resolve(subdomain, 'A')
        if response.rrset:
            return True, "Wildcard DNS records can lead to unintended DNS responses, potentially exposing internal network information or leading to phishing attacks.", f"dig nonexistent.{domain}"
    except dns.resolver.NXDOMAIN:
        return False, "", ""
    except dns.exception.DNSException:
        return False, "", ""
    return False, "", ""

def enumerate_dns_records(domain):
    record_types = ['A', 'AAAA', 'MX', 'TXT', 'SRV', 'CNAME', 'NS']
    records = {}
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [rdata.to_text() for rdata in answers]
        except dns.exception.DNSException:
            records[record_type] = []
    return records

def check_all(*, host_name, dns_server):
    domain = host_name  # Replace with the domain you want to test

    # Check for DNS cache snooping
    result, hint, poc = check_dns_cache_snooping(domain, dns_server)
    if result:
        print(f"[+] DNS cache snooping possible for {domain} on server {dns_server}")
        print(f"[i] {hint}")
        print(f"[$] {poc}")
        print()

    # Check if DNS server is an open resolver
    result, hint, poc = check_open_resolver(dns_server)
    if result:
        print(f"[+] {dns_server} is an open resolver")
        print(f"[i] {hint}")
        print(f"[$] {poc}")
        print()

    # Check DNSSEC configuration
    result, hint, poc = check_dnssec(domain)
    if not result:
        print(f"[+] {domain} does not have DNSSEC configured")
        print(f"[i] {hint}")
        print(f"[$] {poc}")
        print()

    # Check for wildcard DNS records
    result, hint, poc = check_wildcard(domain)
    if result:
        print(f"[+] {domain} has a wildcard DNS record")
        print(f"[i] {hint}")
        print(f"[$] {poc}")
        print()

    # Enumerate DNS records
    dns_records = enumerate_dns_records(domain)
    for record_type, records in dns_records.items():
        if records:
            if record_type == 'TXT':
                print(f"[+] {record_type} records for {domain}: {records}")
                print("[i] Check if TXT records expose sensitive information like internal IPs or email addresses.")
                print(f"[$] dig {domain} TXT")
                print()
            if record_type == 'MX':
                print(f"[+] {record_type} records for {domain}: {records}")
                print("[i] Verify MX records to ensure they do not point to unauthorized mail servers.")
                print(f"[$] dig {domain} MX")
                print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-H', '--host-name', required=True, help='the target host to check on'
    )
    parser.add_argument(
        '-dns', '--dns-server', required=True, help='the target host to check on'
    )
    args = parser.parse_args()
    check_all(**args.__dict__)

