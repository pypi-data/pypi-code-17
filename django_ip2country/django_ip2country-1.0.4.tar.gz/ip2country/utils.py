import re

from ip2country.models import IPLocation


def convert_csv(pth, update_mode=False):
    f = open(pth)
    batch = []
    for l in f.readlines():
        z = l.split(',')
        if len(z) < 3:
            continue
        tmp = IPLocation()
        tmp.country_code = z[2].replace('"', '').strip()
        tmp.ip_from = convert_ip_int(z[0].replace('"', '').strip())
        tmp.ip_to = convert_ip_int(z[1].replace('"', '').strip())
        batch.append(tmp)
    if not update_mode:
        IPLocation.objects.all().delete()
    IPLocation.objects.bulk_create(batch)


def convert_ip_int(ip):
    if ip is None:
        print 'ip is None'
        return 0
    elif re.match(
            "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$",
            ip):
        split_ip = ip.split('.')
    else:
        print 'error on %s' % ip
        return 0
    w = int(split_ip[0]) * 16777216
    x = int(split_ip[1]) * 65536
    y = int(split_ip[2]) * 256
    z = int(split_ip[3])
    t = w+x+y+z
    return t


def get_country_from_ip(ip):
    t = convert_ip_int(ip)
    res = IPLocation.objects.filter(ip_from__lte=t, ip_to__gte=t).first()
    if not res:
        return ''
    return res.country_code
