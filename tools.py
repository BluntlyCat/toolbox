import socket
FQDN = socket.getfqdn()


def is_local(fqdn: str):
    return fqdn != FQDN


def get_debug(fqdn: str, debug: bool = True):
    local = is_local(fqdn)

    if not local:
        return False

    debug = local and debug
    return debug
