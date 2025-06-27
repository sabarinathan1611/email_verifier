import re
import socket
import smtplib
import dns.resolver

def verify_email(
    email: str,
    from_address: str = "verify@yourdomain.com",
    timeout: float = 10.0
) -> bool:
    """
    Verifies if an email address is deliverable by:
      1. Regex syntax check
      2. DNS MX lookup (using dnspython)
      3. SMTP RCPT TO probe (HELO, MAIL FROM, RCPT TO)

    Returns True if the mail server acknowledges the address (code 250), False otherwise.
    """
    # 1) Basic syntax check
    regex = re.compile(
        r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
        re.IGNORECASE
    )
    if not regex.match(email):
        return False

    # 2) MX lookup
    domain = email.split('@', 1)[1]
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        mx_record = str(answers[0].exchange).rstrip('.')
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return False

    # 3) SMTP probe
    host = socket.gethostname()
    try:
        server = smtplib.SMTP(timeout=timeout)
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(host)
        server.mail(from_address)
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except Exception:
        return False

# # Example usage:
# if __name__ == '__main__':
#     test_emails = [
#         'admin@capitalreach.ai',
#         'sabarinathan@anonshare.live',
#         'support@anonshare.live',
#         'david.schincariol@bdc.ca',
#         'sabari@capitalreach.ai',
#         'vsabarinathan1611@gmail.com',
#         'sabarinathan.capitalreach@gmail.com',
#     ]
#     for addr in test_emails:
#         result = verify_email(addr, from_address='verify@acme-corp.com')
#         print(f"{addr:30s} -> {'Reachable' if result else 'Unreachable'}")
