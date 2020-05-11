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


def create_domain(**kargs):
    custom_domain = kargs.get("body")
    domain_body = custom_domain.get('domain')
    ip = custom_domain.get('ip')
    if not domain_body or not ip:
        return make_response({"error": "payload is invalid"}, 400)
    for domain in custom_domains:
        if domains[domain]["ip"] == ip:
            return make_response({"error": "custom domain alredy exists"}, 400)
        
    custom_domains.add(domain_body)
    domains[domain_body] = {"domain":domain_body, "ip": ip, "custom": True}
    return make_response(domains[domain_body], 201)