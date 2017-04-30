#! coding=utf-8
"""
DigitalOcean APIv2 droplet module.
Provides interface classes to Droplets, Kernels,
Snapshots, Images, and Sizes
"""

__author__ = "Sriram Velamur<sriram.velamur@gmail.com>"
__all__ = ("Droplet", "Image", "DropletSize")

import sys

sys.dont_write_bytecode = True

from .base import BaseObject
from .meta import Snapshot
from .errors import InvalidArgumentError, APIError


class Droplet(BaseObject):
    """DigitalOcean droplet object"""

    __slots__ = ("client", "name", "ipv4_ip", "ipv6_ip", "networks")

    client, name, ipv4_ip, ipv6_ip = (None,) * 4
    networks = []

    droplet_base_url = "https://api.digitalocean.com/v2/droplets/"
    droplet_snapshot_url = "".join([
        droplet_base_url,
        "%s/snapshots?page=1&per_page=100"
    ])
    droplet_neighbours_url = "".join([
        droplet_base_url,
        "{0}/neighbors"
    ])

    droplet_actions_url = "{0}{1}/actions"

    def power_off(self):
        """Droplet power off helper method"""
        print "Powering off droplet {0}".format(self.name)
        self.client.poweroff_droplet(self.id)

    def power_on(self):
        """Droplet power on helper method"""
        print "Powering on droplet {0}".format(self.name)
        self.client.poweron_droplet(self.id)

    def power_cycle(self):
        """Droplet power cycle helper method"""
        print "Power cycling droplet {0}".format(self.name)
        self.client.powercycle_droplet(self.id)

    def __repr__(self):
        return "Droplet {0} [ID: {1}]".format(self.name, self.id)

    def __str__(self):
        return "Droplet {0} [ID: {1}]".format(self.name, self.id)

    def as_dict(self):
        """Returns a dictionary representation of a Droplet"""
        return {"name": self.name, "id": self.id}

    def get_kernels(self):
        """
        DigitalOcean droplet kernels list helper.
        Returns a list of kernels available for a particular droplet.
        :rtype: list<doclient.droplet.Kernel>
        """
        return self.client.get_droplet_kernels(self.id)

    def get_neighbours(self):
        """
        DigitalOcean APIv2 droplet neighbours helper method.
        Returns a list of droplets running
        on the same physical server.
        :rtype: list<doclient.droplet.Droplet>
        """
        url = self.droplet_neighbours_url.format(self.id)
        response = self.client.api_request(url=url)
        droplets = response.get("droplets")
        return [Droplet(**droplet) for droplet in droplets]

    def delete(self):
        """
        DigitalOcean droplet delete helper.
        Deletes a particular droplet.
        :rtype: dict
        """
        return self.client.delete_droplet(self.id)

    def get_snapshots(self):
        """
        DigitalOcean droplet snapshot list helper.
        Returns a list of snapshots for a particular droplet.
        :rtype: list<Snapshot>
        """
        url = self.droplet_snapshot_url % self.id
        response = self.client.api_request(url=url, return_json=True)
        snapshots = response.get("snapshots")
        return [Snapshot(**snapshot) for snapshot in snapshots]

    def reset_password(self):
        """
        DigitalOcean droplet access password reset helper method.
        Initializes a password reset for a requested droplet.
        """
        url = self.droplet_actions_url.format(
            self.droplet_base_url, self.id)
        print "Attempting to reset password for droplet {0}".format(
            self.id)
        payload = {
            "type": "password_reset"
        }
        self.client.api_request(url=url, data=payload)

    def resize(self, new_size, disk_resize=False):
        """
        Digitalocean droplet resize helper method
        :param new_size: New droplet size to be resized to.
        :type  new_size: basestring
        :param disk_resize: Boolean to indicate disk resizing.
        :type  disk_resize: bool
        :return: Resized current droplet object.
        :rtype : doclient.droplet.Droplet
        """
        url = self.droplet_actions_url.format(
            self.droplet_base_url, self.id)
        print "".join([
            "Droplet {0} needs to be powered off before resize.",
            " Caveat emptor: Please power on the droplet",
            " via the Digitalocean console or the API after "
            "resizing."]).format(self.id)
        self.power_off()

        if not isinstance(new_size, basestring):
            raise InvalidArgumentError(
                "Invalid size specified. Required a valid string "
                "size representation")
        # TODO: Move to meta module as a global.
        valid_sizes = ("512mb", "1gb", "2gb", "4gb", "8gb", "16gb",
                       "32gb", "48gb", "64gb")
        if new_size not in valid_sizes:
            raise InvalidArgumentError(
                "Invalid size specified. Size must be an available "
                "size in {0}".format("".join(valid_sizes)))
        if not isinstance(disk_resize, bool):
            disk_resize = False

        resize_payload = {
            "type": "resize",
            "disk": disk_resize,
            "size": new_size
        }

        response = self.client.api_request(
            url=url, method="post", data=resize_payload)

        # Handle errors
        if response.get("message"):
            raise APIError(response.get("message"))

        return self.client.filter_droplets(self.id)


class Image(BaseObject):

    """DigitalOcean droplet base image object"""

    min_disk_size, slug, name, _id, regions = (None,) * 5

    def __repr__(self):
        return "Image {0} [{1}]".format(self.id, self.name)

    def __str__(self):
        return "Image {0} [{1}]".format(self.id, self.name)


class DropletSize(BaseObject):

    """DigitalOcean droplet size repr object"""

    price_monthly, price_hourly, memory, disk, slug = (None,) * 5
    regions, transfer, available, vcplus = (None,) * 4

    def __repr__(self):
        available = "Available" if self.available else "Not available"
        return "Size {0} [{1}]".format(self.slug, available)

    def __str__(self):
        available = "Available" if self.available else "Not available"
        return "Size {0} [{1}]".format(self.slug, available)
