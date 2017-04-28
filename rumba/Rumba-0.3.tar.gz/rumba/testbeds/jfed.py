#
# jFed support for Rumba
#
#    Sander Vrijders  <sander.vrijders@intec.ugent.be>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301  USA

import subprocess
import getpass
import xml.dom.minidom as xml
import os.path
import wget
import tarfile

import rumba.model as mod
import rumba.log as log


logger = log.get_logger(__name__)


class Testbed(mod.Testbed):

    def __init__(self, exp_name, username, cert_file, exp_hours="2",
                 proj_name="ARCFIRE", authority="wall2.ilabt.iminds.be",
                 image=None):
        passwd = getpass.getpass(prompt="Password for certificate file: ")
        mod.Testbed.__init__(self, exp_name, username, passwd, proj_name)
        self.authority = "urn:publicid:IDN+" + authority + "+authority+cm"
        self.auth_name = authority
        self.cert_file = cert_file
        self.exp_hours = exp_hours
        self.if_id = dict()
        self.rspec = self.exp_name + ".rspec"
        self.manifest = self.exp_name + ".rrspec"
        self.jfed_jar = "jfed_cli/experimenter-cli.jar"
        if image is not None:
            self.image = "urn:publicid:IDN+" + authority + \
                         "+image+GeniSlices:" + image
        else:
            self.image = None

        if not os.path.exists(self.jfed_jar):
            logger.info("Couldn't find jFed CLI. Downloading.")
            tarball = "jfed_cli.tar.gz"
            url = "http://jfed.iminds.be/downloads/stable/jar/" + tarball
            wget.download(url)
            tar = tarfile.open(tarball)
            tar.extractall()
            tar.close()
            logger.info("Extracted in current directory")
            os.remove(tarball)

    def create_rspec(self, experiment):
        impl = xml.getDOMImplementation()
        doc = impl.createDocument(None, "rspec", None)

        top_el = doc.documentElement
        top_el.setAttribute("xmlns", "http://www.geni.net/resources/rspec/3")
        top_el.setAttribute("type", "request")
        top_el.setAttribute("xmlns:emulab", "http://www.protogeni.net/" +
                            "resources/rspec/ext/emulab/1")
        top_el.setAttribute("xmlns:jfedBonfire", "http://jfed.iminds.be/" +
                            "rspec/ext/jfed-bonfire/1")
        top_el.setAttribute("xmlns:delay", "http://www.protogeni.net/" +
                            "resources/rspec/ext/delay/1")
        top_el.setAttribute("xmlns:jfed-command", "http://jfed.iminds.be/" +
                            "rspec/ext/jfed-command/1")
        top_el.setAttribute("xmlns:client", "http://www.protogeni.net/" +
                            "resources/rspec/ext/client/1")
        top_el.setAttribute("xmlns:jfed-ssh-keys", "http://jfed.iminds.be/" +
                            "rspec/ext/jfed-ssh-keys/1")
        top_el.setAttribute("xmlns:jfed", "http://jfed.iminds.be/rspec/" +
                            "ext/jfed/1")
        top_el.setAttribute("xmlns:sharedvlan", "http://www.protogeni.net/" +
                            "resources/rspec/ext/shared-vlan/1")
        top_el.setAttribute("xmlns:xsi", "http://www.w3.org/2001/" +
                            "XMLSchema-instance")
        top_el.setAttribute("xsi:schemaLocation", "http://www.geni.net/" +
                            "resources/rspec/3 http://www.geni.net/" +
                            "resources/rspec/3/request.xsd")

        for node in experiment.nodes:
            el = doc.createElement("node")
            top_el.appendChild(el)
            el.setAttribute("client_id", node.name)
            el.setAttribute("exclusive", "true")
            el.setAttribute("component_manager_id", self.authority)

            el2 = doc.createElement("sliver_type")
            el.appendChild(el2)
            el2.setAttribute("name", "raw-pc")

            if self.image is not None:
                image_el = doc.createElement("disk_image")
                image_el.setAttribute("name", self.image)
                el2.appendChild(image_el)

            node.ifs = 0
            for ipcp in node.ipcps:
                if isinstance(ipcp, mod.ShimEthIPCP):
                    el3 = doc.createElement("interface")
                    self.if_id[ipcp] = node.name + ":if" + str(node.ifs)
                    el3.setAttribute("client_id", self.if_id[ipcp])
                    node.ifs += 1
                    el.appendChild(el3)

        for dif in experiment.dif_ordering:
            if isinstance(dif, mod.ShimEthDIF):
                el = doc.createElement("link")
                top_el.appendChild(el)
                el.setAttribute("client_id", dif.name)

                el2 = doc.createElement("component_manager_id")
                el2.setAttribute("name", self.authority)
                el.appendChild(el2)

                for ipcp in dif.ipcps:
                    el3 = doc.createElement("interface_ref")
                    el3.setAttribute("client_id", self.if_id[ipcp])
                    el.appendChild(el3)

        file = open(self.rspec, "w")
        file.write(doc.toprettyxml())
        file.close()

    def swap_in(self, experiment):
        self.create_rspec(experiment)

        for node in experiment.nodes:
            auth_name_r = self.auth_name.replace(".", "-")
            node.ssh_config.hostname = \
                node.name + "." + self.exp_name + "." + \
                auth_name_r + "." + self.auth_name
            node.ssh_config.proxycommand = "ssh -i '" + self.cert_file + \
                                           "' -o StrictHostKeyChecking=no " + \
                                           self.username + \
                                           "@bastion.test.iminds.be nc " + \
                                           node.ssh_config.hostname + " 22"

        subprocess.call(["java", "-jar", self.jfed_jar, "create", "-S",
                         self.proj_name, "--rspec",
                         self.rspec, "-s",
                         self.exp_name, "-p", self.cert_file, "-k",
                         "usercert,userkeys,shareduserallkeys",
                         "--create-slice",
                         "--manifest", self.manifest,
                         "-P", self.password,
                         "-e", self.exp_hours])

        rspec = xml.parse(self.manifest)
        xml_nodes = rspec.getElementsByTagName("node")

        # Complete details of the nodes after swapin
        for xml_node in xml_nodes:
            n_name = xml_node.getAttribute("client_id")
            intfs = xml_node.getElementsByTagName("interface")

            for node in experiment.nodes:
                if node.name == n_name:
                    node_n = node

            for intf in intfs:
                i_name = intf.getAttribute("client_id")
                for ipcp in node_n.ipcps:
                    if isinstance(ipcp, mod.ShimEthIPCP):
                        if self.if_id[ipcp] == i_name:
                            comp_id = intf.getAttribute("component_id")
                            comp_arr = comp_id.split(":")
                            ipcp.ifname = comp_arr[-1]
                            # xml_ip = intf.getElementsByTagName("ip")
                            # interface.ip = xml_ip[0].getAttribute("address")
