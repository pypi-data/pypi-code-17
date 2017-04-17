import ipaddress


def ip_in_range(request, ranges):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    ip = ipaddress.ip_address(ip)

    ip_ranges = ranges.split(",")
    for range in ip_ranges:
        if ip in ipaddress.ip_network(range):
            return True
    return False
