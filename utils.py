import ipaddress

class ThreadResult:
    def __init__(self) -> None:
        self.result = None

def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False