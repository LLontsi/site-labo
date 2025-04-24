import re
import socket
import dns.resolver
from django.core.exceptions import ValidationError
def validate_email_domain(email):
    """Vérifie si le domaine de l'email existe via DNS."""
    domain = email.split('@')[1]
    try:
        # Vérifier si le domaine a des enregistrements MX
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        try:
            # Si pas de MX, vérifier s'il y a au moins un enregistrement A
            dns.resolver.resolve(domain, 'A')
            return True
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            raise ValidationError(f"Le domaine '{domain}' semble ne pas exister.")


# 3. Validation simplifiée à intégrer dans la vue
def is_valid_email_domain(email):
    """Version simplifiée pour vérifier le domaine sans dépendances externes."""
    domain = email.split('@')[1]
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False
