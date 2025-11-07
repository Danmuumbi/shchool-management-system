# # backend/app/utils/tenant_resolver.py
# from flask import request, g

# def get_tenant_from_request(req=None):
#     """
#     Extract tenant (school subdomain) from the request hostname.
#     Example: evol.schoolapp.com → tenant = "evol"
#     """
#     req = req or request
#     host = req.host.split(":")[0]
#     parts = host.split(".")
#     tenant = parts[0] if len(parts) > 1 else None

#     if not tenant:
#         raise ValueError("Tenant could not be determined from hostname")

#     g.tenant_subdomain = tenant
#     return tenant




# backend/app/utils/tenant_resolver.py
from flask import request

def get_tenant_from_request(req=None):
    """
    Extract tenant (school subdomain) from the request.
    Priority:
    1. X-Subdomain header (from frontend)
    2. Hostname subdomain (e.g. evol.localhost)
    """
    req = req or request

    # 1️⃣ Check for X-Subdomain header first (sent by frontend)
    header_tenant = req.headers.get("X-Subdomain")
    if header_tenant:
        return header_tenant.lower().strip()

    # 2️⃣ Fallback to hostname
    host = req.host.split(":")[0]
    parts = host.split(".")

    # Handle evol.localhost, bellavista.localhost, etc.
    if len(parts) == 2 and parts[1] == "localhost":
        return parts[0].lower().strip()

    # Handle production domains like school.example.com
    elif len(parts) > 2:
        return parts[0].lower().strip()

    # Handle plain localhost or 127.0.0.1 with no subdomain
    return "default"
