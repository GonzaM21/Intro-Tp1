from flask import abort, make_response
import dns.resolver

domains_counter = 0
domains = {}
custom_domains = set()
#IP = 'ip'
#DOMAIN = 'domain'
#CUSTOM = 'custom'


def get_ip(domain):
    try:
        if not domain in domains:
            result_dns = dns.resolver.query(domains)
            ips = [ip.address for ip in result_dns]
            domains[domain] = {"domain": domain,
                                "ip": ips,
                                "custom": False}
        global domains_counter
        ips = domains[domain]["ip"]
        if domain in custom_domains: 
               return {"domain": domain,
                    "ip": ips,
                    "custom": True}
        
        ip = ips[domains_counter % len(ips)]
        domains_counter += 1
        return {"domain": domain, "ip": ip, "custom": False}
    except:
        return make_response({"error": "domain not found"})