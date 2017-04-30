#! coding=utf-8
"""DigitalOcean APIv2 client module"""
__author__ = "Sriram Velamur<sriram.velamur@gmail.com>"
__all__ = ("DOClient",)

#pylint: disable=R0904,R0913,W0142

import sys
sys.dont_write_bytecode = True
from json import dumps as json_dumps
from re import compile as re_compile, match as re_match
from ast import literal_eval
from datetime import datetime as dt
from time import mktime, gmtime

import requests

from .base import BaseObject
from .droplet import Droplet, Image, DropletSize
from .meta import Domain, Kernel, Snapshot, \
    Region, SSHKey, DropletNetwork
from .errors import APIAuthError, InvalidArgumentError, \
    APIError, NetworkError
from .user import DOUser


class DOClient(BaseObject):

    """DigitalOcean APIv2 client"""

    api_calls_left = None
    api_quota_reset_at = None
    user = None

    droplet_url = "".join([
        "https://api.digitalocean.com/v2/",
        "droplets?page=1&per_page=100"
    ])
    images_url = "".join([
        "https://api.digitalocean.com/v2/",
        "images?page=1&per_page=100"
    ])
    sizes_url = "".join([
        "https://api.digitalocean.com/v2/",
        "sizes?page=1&per_page=100"
    ])

    power_onoff_url = "".join([
        "https://api.digitalocean.com/v2/",
        "droplets/%s/actions"
    ])

    regions_url = "https://api.digitalocean.com/v2/regions"

    userinfo_url = "https://api.digitalocean.com/v2/account"
    keys_url = userinfo_url + "/keys"

    droplet_base_url = "https://api.digitalocean.com/v2/droplets/"
    droplet_snapshot_url = "".join([
        droplet_base_url,
        "%s/snapshots?page=1&per_page=100"
    ])
    droplet_kernels_url = "".join([
        droplet_base_url,
        "%s/kernels?page=1&per_page=100"
    ])
    droplet_neighbours_url = "".join([
        droplet_base_url,
        "%s/neighbors"
    ])

    ssh_keys = []
    networks = []

    # Metadata

    poweroff_data = json_dumps({
        "type": "power_off"
    })

    poweron_data = json_dumps({
        "type": "power_on"
    })

    powercycle_data = json_dumps({
        "type": "power_cycle"
    })

    def __init__(self, token):
        """
        DigitalOcean APIv2 client init
        :param token: DigitalOcean API authentication token
        :type  token: basestring
        """
        super(DOClient, self).__init__(**{"token": token})
        self.droplets = None
        self.user = None
        self._request_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.token)
        }
        self.get_droplets()
        self.get_user_information()
        self._id = self.user.uuid
        self.get_ssh_keys()

    def get_user_information(self):
        """DigitalOcean APIv2 user information helper method"""

        response = self.api_request(url=self.userinfo_url,
                                    return_json=False)

        if not response.status_code == 200:
            raise APIAuthError("Unable to authenticate session")

        payload = response.json().get("account")
        payload.update({
            "droplet_count": len(self.droplets)
        })

        user = DOUser(**payload)
        self.user = user
        return user

    def get_ssh_keys(self):
        """
        Helper method to retrieve the list of SSH keys associated
        with a DigitalOcean user account.
        """
        response = self.api_request(
            url=self.keys_url, return_json=True)

        keys = response.get("ssh_keys", [])
        for key in keys:
            key_object = SSHKey(**key)
            if key_object not in self.ssh_keys:
                self.ssh_keys.append(key_object)

        return self.ssh_keys

    def __repr__(self):
        return "DigitalOcean API Client {0}".format(self._id)

    def __str__(self):
        return "DigitalOcean API Client {0}".format(self._id)

    @property
    def token(self):
        """
        DigitalOcean API client token property.
        Used with request headers as Authorization Bearer
        """
        return self._token

    @property
    def request_headers(self):
        """
        DigitalOcean API client base request headers property.
        Used with all of the DOClient's HTTP requests.
        """
        return self._request_headers

    def add_request_headers(self, header_data):
        """
        Helper method to add additional request headers
        to DigitalOcean API calls.
        :param header_data: Header key, values to add to request.
        :type  header_data: dict, tuple <len:2>
        :rtype: NoneType
        """
        is_valid_dict = isinstance(header_data, dict)
        is_valid_tuple = isinstance(header_data, tuple) \
            and len(header_data) == 2
        passes = is_valid_dict or is_valid_tuple
        if not passes:
            raise InvalidArgumentError(
                "".join([
                    "Request header setter requires a ",
                    "dictionary or tuple of key/value"
                ]))

        if is_valid_dict:
            for key, value in header_data.iteritems():
                self._request_headers[key] = value
        elif is_valid_tuple:
            self._request_headers[header_data[0]] = header_data[1]

    def api_request(self, url, method="GET",
                    data=None, return_json=True):
        """
        DigitalOcean API request helper method.
        :param url: REST API url to place a HTTP request to.
        :type  url: basestring
        :param method: HTTP method
        :type  method: basestring
        :param data: HTTP payload
        :type  data: dict<json>
        :param return_json: Specifies return data format.
                            If false, returns bare response, else
                            returns a constructed APIResponse object.
        :type  return_json: bool
        :rtype: dict, requests.models.Response
        """

        if self.api_calls_left is not None \
                and self.api_calls_left < 1:
            raise APIAuthError("Rate limit exceeded.")

        method = method or "GET"
        method = method.lower()
        http_method = getattr(requests, method, None)

        if http_method is None:
            raise InvalidArgumentError(
                "Invalid HTTP method requested")

        kwargs = {
            "url": url,
            "headers": self.request_headers,
        }

        if data:
            if isinstance(data, dict):
                data = json_dumps(data)
            kwargs.update({"data": data})

        try:
            response = http_method(**kwargs)
        except requests.exceptions.ConnectionError:
            error_msg = "".join([
                "No available network to ",
                "connect to DigitalOcean API."
            ])
            raise NetworkError(error_msg)

        if response.status_code == 400:
            raise APIError("Invalid request data. Please check data")

        elif response.status_code in (401, 403):
            raise APIAuthError(
                "Invalid authorization bearer. Please check token")
        elif response.status_code == 500:
            raise APIError("DigitalOcean API error. Please try later")

        reset_timestamp = response.headers.get("ratelimit-reset")
        reset_timestamp = float(reset_timestamp)
        reset_timestamp = dt.fromtimestamp(
            mktime(gmtime(reset_timestamp)))

        self.api_calls_left = \
            response.headers.get("ratelimit-remaining")
        self.api_quota_reset_at = reset_timestamp

        return response.json() if return_json else response

    @staticmethod
    def get_domain(name):
        """
        Get information for a particular domain managed through
        DigitalOcean's DNS interface
        :param name: Domain name
        :type  name: basestring
        :rtype: dict
        """
        return Domain.get(name)

    @staticmethod
    def delete_domain(name):
        """
        Delete a domain mapping managed through DigitalOcean's DNS
        interface.
        :param name: Domain name
        :type  name: basestring
        :rtype: dict
        """
        return Domain.delete(name)

    @staticmethod
    def create_domain(name, ip_address):
        """
        Create domain name mapping for domains managed through
        DigitalOcean's DNS interface.
        :param name: Domain name
        :type  name: basestring
        :param ip_address: IP address to map domain name to.
        :type ip_address: basestring
        :rtype: dict
        """
        try:
            assert isinstance(name, basestring), \
                "name needs to be a valid domain name string"
            assert isinstance(ip_address, basestring), \
                "ip_address needs to be a valid IPV4/IPV6 address"
            domain = Domain.create(name, ip_address)
            return {
                "message": "Domain mapping created successfully",
                "data": domain.as_json()
            }
        except AssertionError, error:
            raise InvalidArgumentError(error)

    @staticmethod
    def get_domains():
        """
        Get all domain maps generated through DigitalOcean's DNS.
        :rtype: list<Domain>
        """
        return Domain.get_all()

    def get_images(self):
        """
        Get list of images available in your DigitalOcean account.
        :raises: APIAuthError
        """
        response = self.api_request(url=self.images_url)
        images = response.get("images")
        return [Image(**image) for image in images]

    def get_sizes(self):
        """
        Get list of image sizes available.
        :raises: APIAuthError
        """
        response = self.api_request(url=self.sizes_url)
        sizes = response.get("sizes")
        return [DropletSize(**size) for size in sizes]

    def get_droplets(self):
        """
        Get list of droplets for the requested account.
        :raises: APIAuthError
        """

        response = self.api_request(url=self.droplet_url)

        droplets = response.get("droplets", [])
        _droplets = []

        for droplet in droplets:

            droplet_networks = droplet.get("networks", {})
            v4_networks = droplet_networks.get("v4", [])
            v6_networks = droplet_networks.get("v6", [])
            droplet_network_objects = []
            droplet_ipv4_ip, droplet_ipv6_ip = None, None

            for idx, v4_network in enumerate(v4_networks):
                ip = v4_network.get("ip_address")
                netmask = v4_network.get("netmask")
                gateway = v4_network.get("gateway")
                is_public = v4_network.get("type") == "public"
                network_type = "ipv4"
                network = DropletNetwork(**{
                    "ip_address": ip,
                    "netmask": netmask,
                    "gateway": gateway,
                    "is_public": is_public,
                    "network_type": network_type
                })
                droplet_network_objects.append(network)
                if is_public:
                    droplet_ipv4_ip = ip

            for idx, v6_network in enumerate(v6_networks):
                ip = v6_network.get("ip_address")
                netmask = v6_network.get("netmask")
                gateway = v6_network.get("gateway")
                is_public = v6_network.get("type") == "public"
                network_type = "ipv6"
                network = DropletNetwork(**{
                    "ip_address": ip,
                    "netmask": netmask,
                    "gateway": gateway,
                    "is_public": is_public,
                    "network_type": network_type
                })
                droplet_network_objects.append(network)
                if is_public:
                    droplet_ipv6_ip = ip

            droplet = Droplet(**{
                "name": droplet.get("name"),
                "_id": droplet.get("id"),
                "client": self,
                "networks": droplet_network_objects,
                "ipv4_ip": droplet_ipv4_ip,
                "ipv6_ip": droplet_ipv6_ip
            })
            _droplets.append(droplet)

        self.droplets = _droplets

    def poweroff_droplet(self, instance_id):
        """
        Instance power off helper method.
        :param instance_id: ID of the instance to turn off.
        :type  instance_id: int, basestring<int>
        :rtype: dict
        """
        url = self.power_onoff_url % instance_id
        try:
            self.api_request(url=url,
                             method="post",
                             data=self.poweroff_data)
            return {"message": "Initiated droplet poweroff"}
        except APIAuthError, error:
            return {"message": error.message}

    def poweron_droplet(self, instance_id):
        """
        Instance power on helper method.
        :param instance_id: ID of the instance to turn on.
        :type  instance_id: int, basestring<int>
        :rtype: dict
        """
        url = self.power_onoff_url % instance_id
        try:
            self.api_request(url=url,
                             method="post",
                             data=self.poweron_data)
            return {"message": "Initiated droplet poweron"}
        except APIAuthError, error:
            return {"message": error.message}

    def powercycle_droplet(self, instance_id):
        """
        Instance power cycle helper method.
        :param instance_id: ID of the instance to powercycle.
        :type  instance_id: int, basestring<int>
        :rtype: dict
        """
        url = self.power_onoff_url % instance_id
        try:
            self.api_request(url=url,
                             method="post",
                             data=self.powercycle_data)
            return {"message": "Initiated droplet power cycle"}
        except APIAuthError, error:
            return {"message": error.message}

    def get_droplet(self, droplet_id):
        """
        Basic droplet find helper.
        Filters out droplets which match the provided droplet id.
        [Essentially one droplet].
        :param droplet_id: ID to match droplets against.
        :type  droplet_id: int, basestring
        :rtype: list<Droplet>
        """

        if not isinstance(droplet_id, int):
            droplet_id = droplet_id or ""
            try:
                droplet_id = literal_eval(str(droplet_id))
            except (TypeError, ValueError):
                droplet_id = None

        if not isinstance(droplet_id, int):
            raise InvalidArgumentError(
                "Method requires a valid integer droplet id")

        droplet = [x for x in self.droplets if x.id == droplet_id]
        return droplet[0] if droplet else None

    def filter_droplets(self, matcher=None):
        """
        Basic droplet filter helper.
        Filters out droplets which pass a substring match on the name
        for the provided matcher.
        Matcher defaults to empty string and returns all instances
        :param matcher: Token to match droplet names against.
        :type  matcher: basestring
        :rtype: list<Droplet>
        """
        if matcher is None:
            return self.droplets

        if not isinstance(matcher, (int, basestring)):
            raise InvalidArgumentError(
                "Method requires a string filter token or droplet ID")

        if isinstance(matcher, int):
            return [x for x in self.droplets if x.id == matcher]

        # See if a Droplet ID is passed in (an integer) and filter
        # based on ID.
        try:
            _id = literal_eval(matcher)
            return [x for x in self.droplets if x.id == _id]
        except (TypeError, ValueError):
            matcher = re_compile(".*?{0}.*?".format(matcher))
            return [x for x in self.droplets
                    if re_match(matcher, x.name) is not None]

    def get_droplet_snapshots(self, droplet_id):
        """
        DigitalOcean APIv2 droplet snapshots helper method.
        Returns a list of snapshots created for the requested droplet.
        :param droplet_id: ID of droplet to get snapshots for.
        :type  droplet_id: int
        :rtype: list<dict>
        """
        droplet = self.get_droplet(droplet_id)
        if not droplet:
            raise InvalidArgumentError("Droplet not found")
        return droplet.get_snapshots()

    def get_droplet_kernels(self, droplet_id):
        """
        DigitalOcean APIv2 droplet kernels helper method.
        Returns a list of kernels available for the requested droplet.
        :param droplet_id: ID of droplet to get available kernels for.
        :type  droplet_id: int
        :rtype: list<doclient.droplet.Kernel>
        """
        url = self.droplet_kernels_url % droplet_id
        response = self.api_request(url=url)
        kernels = response.get("kernels")
        return [Kernel(**kernel) for kernel in kernels]

    def delete_droplet(self, droplet_id):
        """
        DigitalOcean APIv2 droplet delete method.
        Deletes a requested droplet.
        :param droplet_id: ID of droplet to delete.
        :type  droplet_id: int
        :rtype: dict
        """
        droplet = self.get_droplet(droplet_id)
        if not droplet:
            raise InvalidArgumentError("Unknown droplet")
        url = "{0}{1}".format(self.droplet_base_url, droplet_id)
        try:
            self.api_request(url=url,
                             method="delete",
                             return_json=False)
            message = "Successfully initiated droplet delete for " \
                      "droplet {0}".format(droplet)
        except APIAuthError, auth_error:
            message = auth_error.message
        except APIError:
            message = "DigitalOcean API error. Please try later"

        return {
            "message": message
        }

    def create_droplet(self, name, region, size, image,
                       ssh_keys=None, backups=False, ipv6=False,
                       user_data=None, private_networking=False):
        """
        DigitalOcean APIv2 droplet create method.
        Creates a droplet with requested payload features.
        :param name: Identifier for createddroplet.
        :type  name: basestring
        :param region: Region identifier to spawn droplet
        :type  region: basestring
        :param size: Size of droplet to create.
                     [512mb, 1gb, 2gb, 4gb,
                      8gb, 16gb, 32gb, 48gb, 64gb]
        :type  size: basestring
        :param image: Name or slug identifier of base image to use.
        :type  image: int, basestring
        :param ssh_keys: SSH keys to add to created droplet
        :type  ssh_keys: list<basestring>, list<long>
        :param backups: Droplet backups enable state parameter
        :type  backups: bool
        :param ipv6: Droplet IPV6 enable state parameter
        :type  ipv6: bool
        :param user_data: User data to be added to droplet's metadata
        :type  user_data: basestring
        :param private_networking: Droplet private networking
                                   enable parameter
        :type  private_networking: bool
        :rtype: doclient.droplet.Droplet
        """
        try:
            assert isinstance(name, basestring), \
                "Invalid droplet name. Requires a string name"
            assert isinstance(region, basestring), \
                "Invalid droplet region. Requires a string region id"
            assert isinstance(size, basestring), \
                "Invalid droplet size. Requires a string size"
            assert isinstance(image, (int, long, basestring)), \
                "Invalid base image id. Requires a numeric ID or slug"
            backups = backups if isinstance(backups, bool) else False
            private_networking = private_networking if \
                isinstance(private_networking, bool) else False
            ipv6 = ipv6 if isinstance(ipv6, bool) else False
            user_data = user_data if \
                isinstance(user_data, basestring) else None
            ssh_keys = ssh_keys if isinstance(ssh_keys, list) and \
                all((isinstance(x, (int, long, basestring))
                     for x in ssh_keys)) else False
            payload = json_dumps({
                "name": name,
                "region": region,
                "size": size,
                "image": image,
                "ssh_keys": ssh_keys,
                "backups": backups,
                "private_networking": private_networking,
                "ipv6": ipv6,
                "user_data": user_data,
            })

            params = {
                "url": self.droplet_base_url,
                "method": "POST",
                "data": payload,
                "return_json": False
            }

            response = self.api_request(**params)

            if response.status_code != 202:
                raise APIError(
                    "Unable to create a droplet with requested data")

            droplet = response.json().get("droplet")
            droplet["client"] = self
            self.get_droplets()
            return Droplet(**droplet)

        except AssertionError, err:
            raise InvalidArgumentError(err)

    def create_droplets(self, names, region, size, image,
                        ssh_keys=None, backups=False, ipv6=False,
                        user_data=None, private_networking=False):
        """
        DigitalOcean APIv2 droplet create method.
        Creates a list of droplets all with the same requested
        payload features.
        :param names: Identifiers for the droplets to be created.
        :type  names: list<basestring>
        :param region: Region identifier to spawn droplet
        :type  region: basestring
        :param size: Size of droplet to create.
                     [512mb, 1gb, 2gb, 4gb,
                      8gb, 16gb, 32gb, 48gb, 64gb]
        :type  size: basestring
        :param image: Name or slug identifier of base image to use.
        :type  image: int, basestring
        :param ssh_keys: SSH keys to add to created droplets
        :type  ssh_keys: list<basestring>, list<long>
        :param backups: Droplet backups enable state parameter
        :type  backups: bool
        :param ipv6: Droplet IPV6 enable state parameter
        :type  ipv6: bool
        :param user_data: User data to be added to droplet's metadata
        :type  user_data: basestring
        :param private_networking: Droplet private networking
                                   enable parameter
        :type  private_networking: bool
        :rtype: doclient.droplet.Droplet
        """
        try:
            assert isinstance(names, list), \
                "Invalid droplet name. Requires a list of strings"
            assert all((isinstance(x, basestring) for x in names)), \
                "".join(["One or more invalid droplet names."
                        "Requires a string name"])
            assert isinstance(region, basestring), \
                "Invalid droplet region. Requires a string region id"
            assert isinstance(size, basestring), \
                "Invalid droplet size. Requires a string size"
            assert isinstance(image, (int, long, basestring)), \
                "Invalid base image id. Requires a numeric ID or slug"
            backups = backups if isinstance(backups, bool) else False
            private_networking = private_networking if \
                isinstance(private_networking, bool) else False
            ipv6 = ipv6 if isinstance(ipv6, bool) else False
            user_data = user_data if \
                isinstance(user_data, basestring) else None
            ssh_keys = ssh_keys if isinstance(ssh_keys, list) and \
                all((isinstance(x, (int, long, basestring))
                     for x in ssh_keys)) else False
            payload = json_dumps({
                "names": names,
                "region": region,
                "size": size,
                "image": image,
                "ssh_keys": ssh_keys,
                "backups": backups,
                "private_networking": private_networking,
                "ipv6": ipv6,
                "user_data": user_data,
            })

            params = {
                "url": self.droplet_base_url,
                "method": "POST",
                "data": payload,
                "return_json": False
            }

            response = self.api_request(**params)

            if response.status_code != 202:
                raise APIError(
                    "Unable to create a droplet with requested data")

            droplets = response.json().get("droplets", [])
            _droplets = []
            for droplet in droplets:
                droplet["client"] = self
                _droplets.append(Droplet(**droplet))

            self.get_droplets()
            return _droplets

        except AssertionError, err:
            raise InvalidArgumentError(err)

    def get_regions(self):
        """
        DigitalOcean APIv2 region list method.
        Returns a list of regions available.
        :TODO: Add way to filter regions with pattern/features.
        """
        response = self.api_request(url=self.regions_url)
        regions = response.get("regions", [])
        region_objects = []
        for region in regions:
            _region = Region(**{
                "name": region.get("name"),
                "slug": region.get("slug"),
                "features": region.get("features", []),
                "sizes": region.get("sizes", []),
                "available": region.get("available", False)
            })
            region_objects.append(_region)

        return region_objects


if __name__ == "__main__":
    pass
