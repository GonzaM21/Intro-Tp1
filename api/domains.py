from flask import abort, make_response
import dns.resolver

domains_counter = 0
domains = {}
custom_domains = set()
#IP = 'ip'
#DOMAIN = 'domain'
#CUSTOM = 'custom'


def get_ip(domain):
    """
    Esta funcion maneja el request GET  /api/domains/{domain}

    :domain         el dominio del cual quiero obtener el ip
    :return:        200 Domain, 404 dominio no encontrado
    """
    if not domain in domains:
        try:
            result_dns = dns.resolver.query(domain)
        except:
            return make_response({"error": "domain not found"}, 404) 
        
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
    

def override_domain(**kargs):
    """
    Esta funcion maneja el request PUT  /api/custom-domains/{domain}

    :param body:   el dominio a pisar y su ip
    :return:        200 dominio pisado con la nueva ip, 404 dominio no encontrado,
                    400 payload malformado.
    """
    overriding_domain = kargs.get('body')
    domain_parameter = kargs.get('domain')
    domain = overriding_domain.get('domain')
    ip = overriding_domain.get('ip')
    if(not domain in domains): 
        return make_response({"error": "domain not found"}, 404)
    elif domain is None or ip is None or domain_parameter != domain:
        return make_response({"error": "payload is invalid"}, 400)

    domains[domain] = {"domain": domain, "ip": ip,"custom": True}
    return make_response(domains[domain], 200)

def delete_domain(domain):
    """
    Esta funcion maneja el request DELETE  /api/custom-domains/{domain}

    :domain         el dominio a borrar
    :return:        200 dominio eliminado
                    404 dominio custom no existente
    """
    if(not domain in custom_domains):
        return make_response({"error": "domain not found"}, 404)
    custom_domains.remove(domain)
    del domains[domain]
    return make_response({"domain": domain}, 201)


def create_domain(**kargs):
    """
    Esta funcion maneja el request POST  /api/custom-domains/

    :param body:   el dominio y su ip
    :return:        201 creacion del dominio con su ip,
                    400 domian previamente creado.
    """
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

def get_all_domains(q = None):
    """
    Esta funcion maneja el request GET /api/custom-domains

    :return:       200 lista todos los custom domains existentes.
    """
    response = {"items": []}
    for domain in domains:
        if domains[domain]["custom"] and (q == None or q in domain):
            response["item"].append(domains[domain])
    response