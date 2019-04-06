import socket

FQDN = socket.getfqdn()


def is_local(fqdn: str):
    return fqdn != FQDN


def get_debug(fqdn: str, debug: bool = True, force_remote_debug=False):
    local = is_local(fqdn)

    if debug and force_remote_debug:
        return True

    if not local:
        return False

    debug = local and debug
    return debug
