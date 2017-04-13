class CnameZoneMixin(object):
    """Methods for managing Cname Zones."""
    def create_cname_zone(self, hostname, partner_id):
        return self.post(
            '/cname-dns-zones/',
            json={'partner_id': partner_id, 'hostname': hostname}).json()
