#
# A library to manage ARCFIRE experiments
#
#    Sander Vrijders   <sander.vrijders@intec.ugent.be>
#    Vincenzo Maffione <v.maffione@nextworks.it>
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

import abc

import rumba.log as log


logger = log.get_logger(__name__)


# Represents generic testbed info
#
# @username [string] user name
# @password [string] password
# @proj_name [string] project name
# @exp_name [string] experiment name
#
class Testbed:
    def __init__(self, exp_name, username, password, proj_name):
        self.username = username
        self.password = password
        self.proj_name = proj_name
        self.exp_name = exp_name

    @abc.abstractmethod
    def swap_in(self, experiment):
        raise Exception('swap_in() not implemented')

    @abc.abstractmethod
    def swap_out(self, experiment):
        logger.info("swap_out(): nothing to do")


# Base class for DIFs
#
# @name [string] DIF name
#
class DIF:
    def __init__(self, name, members=None):
        self.name = name
        if members is None:
            members = list()
        self.members = members
        self.ipcps = list()

    def __repr__(self):
        s = "DIF %s" % self.name
        return s

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return other is not None and self.name == other.name

    def __neq__(self, other):
        return not self == other

    def add_member(self, node):
        self.members.append(node)

    def del_member(self, node):
        self.members.remove(node)

    def get_ipcp_class(self):
        return IPCP


# Shim over UDP
#
class ShimUDPDIF(DIF):
    def __init__(self, name, members=None):
        DIF.__init__(self, name, members)

    def get_ipcp_class(self):
        return ShimUDPIPCP


# Shim over Ethernet
#
# @link_speed [int] Speed of the Ethernet network, in Mbps
#
class ShimEthDIF(DIF):
    def __init__(self, name, members=None, link_speed=0):
        DIF.__init__(self, name, members)
        self.link_speed = int(link_speed)
        if self.link_speed < 0:
            raise ValueError("link_speed must be a non-negative number")

    def get_ipcp_class(self):
        return ShimEthIPCP


# Normal DIF
#
# @policies [dict] Policies of the normal DIF
#
class NormalDIF(DIF):
    def __init__(self, name, members=None, policies=None):
        DIF.__init__(self, name, members)
        if policies is None:
            policies = dict()
        self.policies = policies

    def add_policy(self, comp, pol):
        self.policies[comp] = pol

    def del_policy(self, comp):
        del self.policies[comp]

    def show(self):
        s = DIF.__repr__(self)
        for comp, pol in self.policies.items():
            s += "\n       Component %s has policy %s" % (comp, pol)
        return s


# SSH Configuration
#
class SSHConfig:
    def __init__(self, hostname, port=22, proxycommand=None):
        self.hostname = hostname
        self.port = port
        self.proxycommand = proxycommand


# A node in the experiment
#
# @difs: DIFs the node will have an IPCP in
# @dif_registrations: Which DIF is registered in which DIF
# @registrations: Registrations of names in DIFs
# @bindings: Binding of names on the processing system
#
class Node:
    def __init__(self, name, difs=None, dif_registrations=None,
                 registrations=None, bindings=None):
        self.name = name
        if difs is None:
            difs = list()
        self.difs = difs
        for dif in self.difs:
            dif.add_member(self)
        if dif_registrations is None:
            dif_registrations = dict()
        self.dif_registrations = dif_registrations
        if registrations is None:
            registrations = dict()
        self.registrations = registrations
        if bindings is None:
            bindings = dict()
        self.bindings = bindings
        self.ssh_config = SSHConfig(name)
        self.ipcps = []

        self._validate()

    def get_ipcp_by_dif(self, dif):
        for ipcp in self.ipcps:
            if ipcp.dif == dif:
                return ipcp

    def _undeclared_dif(self, dif):
        if dif not in self.difs:
            raise Exception("Invalid registration: node %s is not declared "
                            "to be part of DIF %s" % (self.name, dif.name))

    def _validate(self):
        # Check that DIFs referenced in self.dif_registrations and
        # in self.registrations are part of self.difs
        for upper in self.dif_registrations:
            self._undeclared_dif(upper)
            for lower in self.dif_registrations[upper]:
                self._undeclared_dif(lower)

        for appl in self.registrations:
            for dif in self.registrations[appl]:
                self._undeclared_dif(dif)

    def __repr__(self):
        s = "Node " + self.name + ":\n"

        s += "  DIFs: [ "
        s += " ".join([d.name for d in self.difs])
        s += " ]\n"

        s += "  DIF registrations: [ "
        rl = []
        for upper in self.dif_registrations:
            difs = self.dif_registrations[upper]
            x = "%s => [" % upper.name
            x += " ".join([lower.name for lower in difs])
            x += "]"
            rl.append(x)
        s += ", ".join(rl)
        s += " ]\n"

        s += "  Name registrations: [ "
        for name in self.registrations:
            difs = self.registrations[name]
            s += "%s => [ " % name
            s += ", ".join([dif.name for dif in difs])
            s += " ]"
        s += " ]\n"

        s += "  Bindings: [ "
        s += ", ".join(["'%s' => '%s'" % (ap, self.bindings[ap])
                       for ap in self.bindings])
        s += " ]\n"

        return s

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return other is not None and self.name == other.name

    def __neq__(self, other):
        return not self == other

    def add_dif(self, dif):
        self.difs.append(dif)
        dif.add_member(self)
        self._validate()

    def del_dif(self, dif):
        self.difs.remove(dif)
        dif.del_member(self)
        self._validate()

    def add_dif_registration(self, upper, lower):
        self.dif_registrations[upper].append(lower)
        self._validate()

    def del_dif_registration(self, upper, lower):
        self.dif_registrations[upper].remove(lower)
        self._validate()

    def add_registration(self, name, dif):
        self.dif_registrations[name].append(dif)
        self._validate()

    def del_registration(self, name, dif):
        self.dif_registrations[name].remove(dif)
        self._validate()

    def add_binding(self, name, ap):
        self.bindings[name] = ap
        self._validate()

    def del_binding(self, name):
        del self.bindings[name]
        self._validate()


# Base class representing an IPC Process to be created in the experiment
#
# @name [string]: IPCP name
# @node: Node where the IPCP gets created
# @dif: the DIF the IPCP belongs to
#
class IPCP:
    def __init__(self, name, node, dif):
        self.name = name
        self.node = node
        self.dif = dif
        self.registrations = []

        # Is this IPCP the first in its DIF, so that it does not need
        # to enroll to anyone ?
        self.dif_bootstrapper = False

    def __repr__(self):
        return "{IPCP=%s,DIF=%s,N-1-DIFs=(%s)%s}" % \
                (self.name, self.dif.name,
                 ' '.join([dif.name for dif in self.registrations]),
                 ',bootstrapper' if self.dif_bootstrapper else ''
                 )

    def __hash__(self):
        return hash((self.name, self.dif.name))

    def __eq__(self, other):
        return other is not None and self.name == other.name \
                                and self.dif == other.dif

    def __neq__(self, other):
        return not self == other


class ShimEthIPCP(IPCP):
    def __init__(self, name, node, dif, ifname=None):
        IPCP.__init__(self, name, node, dif)
        self.ifname = ifname


class ShimUDPIPCP(IPCP):
    def __init__(self, name, node, dif):
        IPCP.__init__(self, name, node, dif)
        # TODO: add IP and port


# Base class for ARCFIRE experiments
#
# @name [string] Name of the experiment
# @nodes: Nodes in the experiment
#
class Experiment:
    def __init__(self, testbed, nodes=None):
        if nodes is None:
            nodes = list()
        self.nodes = nodes
        self.testbed = testbed
        self.enrollment_strategy = 'minimal'  # 'full-mesh', 'manual'
        self.dif_ordering = []
        self.enrollments = []  # a list of per-DIF lists of enrollments

        # Generate missing information
        self.generate()

    def __repr__(self):
        s = ""
        for n in self.nodes:
            s += "\n" + str(n)

        return s

    def add_node(self, node):
        self.nodes.append(node)
        self.generate()

    def del_node(self, node):
        self.nodes.remove(node)
        self.generate()

    # Compute registration/enrollment order for DIFs
    def compute_dif_ordering(self):
        # Compute DIFs dependency graph, as both adjacency and incidence list.
        difsdeps_adj = dict()
        difsdeps_inc = dict()

        for node in self.nodes:
            for upper in node.dif_registrations:
                for lower in node.dif_registrations[upper]:
                    if upper not in difsdeps_inc:
                        difsdeps_inc[upper] = set()
                    if lower not in difsdeps_inc:
                        difsdeps_inc[lower] = set()
                    if upper not in difsdeps_adj:
                        difsdeps_adj[upper] = set()
                    if lower not in difsdeps_adj:
                        difsdeps_adj[lower] = set()
                    difsdeps_inc[upper].add(lower)
                    difsdeps_adj[lower].add(upper)

        # Kahn's algorithm below only needs per-node count of
        # incident edges, so we compute these counts from the
        # incidence list and drop the latter.
        difsdeps_inc_cnt = dict()
        for dif in difsdeps_inc:
            difsdeps_inc_cnt[dif] = len(difsdeps_inc[dif])
        del difsdeps_inc

        # Run Kahn's algorithm to compute topological
        # ordering on the DIFs graph.
        frontier = set()
        self.dif_ordering = []
        for dif in difsdeps_inc_cnt:
            if difsdeps_inc_cnt[dif] == 0:
                frontier.add(dif)

        while len(frontier):
            cur = frontier.pop()
            self.dif_ordering.append(cur)
            for nxt in difsdeps_adj[cur]:
                difsdeps_inc_cnt[nxt] -= 1
                if difsdeps_inc_cnt[nxt] == 0:
                    frontier.add(nxt)
            difsdeps_adj[cur] = set()

        circular_set = [dif for dif in difsdeps_inc_cnt
                        if difsdeps_inc_cnt[dif] != 0]
        if len(circular_set):
            raise Exception("Fatal error: The specified DIFs topology"
                            "has one or more"
                            "circular dependencies, involving the following"
                            " DIFs: %s" % circular_set)

        logger.debug("DIF topological ordering: %s", self.dif_ordering)

    # Compute all the enrollments, to be called after compute_dif_ordering()
    def compute_enrollments(self):
        dif_graphs = dict()
        self.enrollments = []

        for dif in self.dif_ordering:
            neighsets = dict()
            dif_graphs[dif] = dict()
            first = None

            # For each N-1-DIF supporting this DIF, compute the set of nodes
            # that share such N-1-DIF. This set will be called the 'neighset' of
            # the N-1-DIF for the current DIF.

            for node in self.nodes:
                if dif in node.dif_registrations:
                    dif_graphs[dif][node] = []  # init for later use
                    if first is None:  # pick any node for later use
                        first = node
                    for lower_dif in node.dif_registrations[dif]:
                        if lower_dif not in neighsets:
                            neighsets[lower_dif] = []
                        neighsets[lower_dif].append(node)

            # Build the graph, represented as adjacency list
            for lower_dif in neighsets:
                # Each neighset corresponds to a complete (sub)graph.
                for node1 in neighsets[lower_dif]:
                    for node2 in neighsets[lower_dif]:
                        if node1 != node2:
                            dif_graphs[dif][node1].append((node2, lower_dif))

            self.enrollments.append([])

            if first is None:
                # This is a shim DIF, nothing to do
                continue

            er = []
            for node in dif_graphs[dif]:
                for edge in dif_graphs[dif][node]:
                    er.append("%s --[%s]--> %s" % (node.name,
                                                   edge[1].name,
                                                   edge[0].name))
            logger.debug("DIF graph for %s: %s", dif, ', '.join(er))

            if self.enrollment_strategy == 'minimal':
                # To generate the list of enrollments, we simulate one,
                # using breadth-first trasversal.
                enrolled = {first}
                frontier = {first}
                while len(frontier):
                    cur = frontier.pop()
                    for edge in dif_graphs[dif][cur]:
                        if edge[0] not in enrolled:
                            enrolled.add(edge[0])
                            enrollee = edge[0].get_ipcp_by_dif(dif)
                            assert(enrollee is not None)
                            enroller = cur.get_ipcp_by_dif(dif)
                            assert(enroller is not None)
                            self.enrollments[-1].append({'dif': dif,
                                                         'enrollee': enrollee,
                                                         'enroller': enroller,
                                                         'lower_dif': edge[1]})
                            frontier.add(edge[0])

            elif self.enrollment_strategy == 'full-mesh':
                for cur in dif_graphs[dif]:
                    for edge in dif_graphs[dif][cur]:
                        if cur < edge[0]:
                            enrollee = cur.get_ipcp_by_dif(dif)
                            assert(enrollee is not None)
                            enroller = edge[0].get_ipcp_by_dif(dif)
                            assert(enroller is not None)
                            self.enrollments[-1].append({'dif': dif,
                                                         'enrollee': enrollee,
                                                         'enroller': enroller,
                                                         'lower_dif': edge[1]})

            else:
                # This is a bug
                assert False

        log_string = "Enrollments:\n"
        for el in self.enrollments:
            for e in el:
                log_string += ("    [%s] %s --> %s through N-1-DIF %s\n"
                               % (e['dif'],
                                  e['enrollee'].name,
                                  e['enroller'].name,
                                  e['lower_dif']))
        logger.debug(log_string)

    def compute_ipcps(self):
        # For each node, compute the required IPCP instances, and associated
        # registrations
        for node in self.nodes:
            node.ipcps = []
            # We want also the node.ipcps list to be generated in
            # topological ordering
            for dif in self.dif_ordering:
                if dif not in node.difs:
                    continue

                # Create an instance of the required IPCP class
                ipcp = dif.get_ipcp_class()(
                    name='%s.%s' % (dif.name, node.name),
                    node=node, dif=dif)

                if dif in node.dif_registrations:
                    for lower in node.dif_registrations[dif]:
                        ipcp.registrations.append(lower)

                node.ipcps.append(ipcp)
                dif.ipcps.append(ipcp)

    def compute_bootstrappers(self):
        for node in self.nodes:
            for ipcp in node.ipcps:
                ipcp.dif_bootstrapper = True
                for el in self.enrollments:
                    for e in el:
                        if e['dif'] != ipcp.dif:
                            # Skip this DIF
                            break
                        if e['enrollee'] == ipcp:
                            ipcp.dif_bootstrapper = False
                            # Exit the loops
                            break
                    if not ipcp.dif_bootstrapper:
                        break

    # Examine the nodes and DIFs, compute the registration and enrollment
    # order, the list of IPCPs to create, registrations, ...
    def generate(self):
        self.compute_dif_ordering()
        self.compute_ipcps()
        self.compute_enrollments()
        self.compute_bootstrappers()
        for node in self.nodes:
            logger.info("IPCPs for node %s: %s", node.name, node.ipcps)

    @abc.abstractmethod
    def install_prototype(self):
        raise Exception('run_prototype() method not implemented')

    @abc.abstractmethod
    def bootstrap_prototype(self):
        raise Exception('run_prototype() method not implemented')

    def swap_in(self):
        # Realize the experiment testbed (testbed-specific)
        self.testbed.swap_in(self)

    def swap_out(self):
        # Undo the testbed (testbed-specific)
        self.testbed.swap_out(self)
