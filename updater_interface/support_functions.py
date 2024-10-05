from ipaddress import ip_address, ip_network

ignored_cidr = ()  # example: "192.168.0.0/24",


def allowed_ip(ip: str) -> bool:
    """
    Checks if an IP is in the ignored_cidr list
    :param ip: The IP to check e.g. 192.168.0.1
    :return: True if the IP is in the ignored_cidr list, False otherwise
    """
    for i in ignored_cidr:
        if ip_address(ip) in ip_network(i):
            return False
    return True


def get_parameter(name, request):
    """
    Gets a parameter from the request or header
    :param name: The name of the parameter to get
    :param request: The request to get the parameter from, defaults to None
    :param header: The header to get the parameter from, defaults to None
    :return: The parameter, or None if it doesn't exist
    """
    d = request.args.get(name, None) if request is not None else None
    if d is None:
        d = request.headers.get(name, None)
    return d
