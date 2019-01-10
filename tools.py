import socket
import logging

FQDN = socket.getfqdn()


def is_local(fqdn: str):
    return fqdn != FQDN


def get_debug(fqdn: str, debug: bool = True):
    local = is_local(fqdn)

    if not local:
        logging.debug("Being on the production machine returns always false for debug mode")
        return False

    debug = local and debug
    logging.debug("Debug mode for local machine is %s" % debug)
    return debug
