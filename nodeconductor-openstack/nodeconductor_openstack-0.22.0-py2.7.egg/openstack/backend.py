import logging
import uuid

from django.db import transaction
from django.utils import six, timezone

from cinderclient import exceptions as cinder_exceptions
from glanceclient import exc as glance_exceptions
from keystoneclient import exceptions as keystone_exceptions
from neutronclient.client import exceptions as neutron_exceptions
from novaclient import exceptions as nova_exceptions

from nodeconductor.structure import log_backend_action, SupportedServices

from nodeconductor_openstack.openstack_base.backend import (
    OpenStackBackendError, BaseOpenStackBackend, update_pulled_fields,
    handle_resource_not_found, handle_resource_update_success)
from . import models

logger = logging.getLogger(__name__)


class OpenStackBackend(BaseOpenStackBackend):
    DEFAULTS = {
        'tenant_name': 'admin',
    }
    TENANT_UPDATE_FIELDS = ('name', 'description', 'error_message', 'runtime_state')
    FLOATING_IP_UPDATE_FIELDS = ('name', 'description', 'address', 'backend_network_id', 'runtime_state')
    SECURITY_GROUP_UPDATE_FIELDS = ('name', 'description')
    NETWORK_UPDATE_FIELDS = ('name', 'description', 'is_external', 'type', 'segmentation_id', 'runtime_state')
    SUBNET_UPDATE_FIELDS = ('name', 'description', 'allocation_pools', 'cidr', 'ip_version',
                            'enable_dhcp', 'gateway_ip', 'dns_nameservers')

    def check_admin_tenant(self):
        try:
            self.keystone_admin_client
        except keystone_exceptions.AuthorizationFailure:
            return False
        except keystone_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            return True

    def sync(self):
        # pull service properties
        self.pull_flavors()
        self.pull_images()
        self.pull_service_settings_quotas()

        # pull resources
        self.pull_tenants()
        self.pull_security_groups()
        self.pull_floating_ips()
        self.pull_networks()
        self.pull_subnets()

    def pull_tenants(self):
        keystone = self.keystone_admin_client
        nova = self.nova_admin_client
        cinder = self.cinder_admin_client
        neutron = self.neutron_admin_client

        try:
            backend_tenants = keystone.projects.list(domain=self._get_domain())
            neutron_quotas = neutron.list_quotas()['quotas']
        except (keystone_exceptions.ClientException, neutron_exceptions.NeutronClientException) as e:
            six.reraise(OpenStackBackendError, e)

        backend_tenants_mapping = {tenant.id: tenant for tenant in backend_tenants}
        neutron_quotas_mapping = {quota['tenant_id']: quota for quota in neutron_quotas}

        tenants = models.Tenant.objects.filter(
            state__in=[models.Tenant.States.OK, models.Tenant.States.ERRED],
            service_project_link__service__settings=self.settings,
        )
        with transaction.atomic():
            for tenant in tenants:
                backend_tenant = backend_tenants_mapping.get(tenant.backend_id)
                if backend_tenant is None:
                    handle_resource_not_found(tenant)
                    continue

                # XXX: Consider changing, when nova and cinder clients introduce quotas fetch in bulk for all tenants.
                try:
                    nova_quotas = nova.quotas.get(tenant_id=tenant.backend_id)
                    cinder_quotas = cinder.quotas.get(tenant_id=tenant.backend_id)
                except (nova_exceptions.ClientException, cinder_exceptions.ClientException) as e:
                    six.reraise(OpenStackBackendError, e)

                neutron_quotas = neutron_quotas_mapping.get(tenant.backend_id, {})
                imported_backend_tenant = self._backend_tenant_to_tenant(backend_tenant,
                                                                         nova_quotas, cinder_quotas, neutron_quotas)
                update_pulled_fields(tenant, imported_backend_tenant, self.TENANT_UPDATE_FIELDS)
                for quota_name, limit in imported_backend_tenant._quota_limits.items():
                    tenant.set_quota_limit(quota_name, limit)
                handle_resource_update_success(tenant)

    def _backend_tenant_to_tenant(self, backend_tenant, nova_quotas=None,
                                  cinder_quotas=None, neutron_quotas=None, **kwargs):
        tenant = models.Tenant(
            name=backend_tenant.name,
            description=backend_tenant.description,
            backend_id=backend_tenant.id,
            state=models.Tenant.States.OK,
        )
        for field, value in kwargs.items():
            setattr(tenant, field, value)

        tenant._quota_limits = {}
        if nova_quotas is not None:
            tenant._quota_limits.update({
                models.Tenant.Quotas.ram: nova_quotas.ram,
                models.Tenant.Quotas.vcpu: nova_quotas.cores,
                models.Tenant.Quotas.instances: nova_quotas.instances,
            })
        if cinder_quotas is not None:
            tenant._quota_limits.update({
                models.Tenant.Quotas.storage: self.gb2mb(cinder_quotas.gigabytes),
                models.Tenant.Quotas.snapshots: cinder_quotas.snapshots,
                models.Tenant.Quotas.volumes: cinder_quotas.volumes,
            })
        if neutron_quotas is not None:
            tenant._quota_limits.update({
                models.Tenant.Quotas.security_group_count: neutron_quotas.get('security_group', -1),
                models.Tenant.Quotas.security_group_rule_count: neutron_quotas.get('security_group_rule', -1),
                models.Tenant.Quotas.floating_ip_count: neutron_quotas.get('floatingip', -1),
                models.Tenant.Quotas.network_count: neutron_quotas.get('network', -1),
                models.Tenant.Quotas.subnet_count: neutron_quotas.get('subnet', -1),
            })

        return tenant

    def _get_domain(self):
        """ Get current domain """
        keystone = self.keystone_admin_client
        return keystone.domains.find(name=self.settings.domain or 'Default')

    def get_or_create_ssh_key_for_tenant(self, key_name, fingerprint, public_key):
        nova = self.nova_client

        try:
            return nova.keypairs.find(fingerprint=fingerprint)
        except nova_exceptions.NotFound:
            # Fine, it's a new key, let's add it
            try:
                logger.info('Propagating ssh public key %s to backend', key_name)
                return nova.keypairs.create(name=key_name, public_key=public_key)
            except nova_exceptions.ClientException as e:
                six.reraise(OpenStackBackendError, e)
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

    def remove_ssh_key_from_tenant(self, tenant, key_name, fingerprint):
        nova = self.nova_client

        # There could be leftovers of key duplicates: remove them all
        keys = nova.keypairs.findall(fingerprint=fingerprint)
        for key in keys:
            # Remove only keys created with NC
            if key.name == key_name:
                nova.keypairs.delete(key)

        logger.info('Deleted ssh public key %s from backend', key_name)

    def _get_current_properties(self, model):
        return {p.backend_id: p for p in model.objects.filter(settings=self.settings)}

    def _are_rules_equal(self, backend_rule, nc_rule):
        if backend_rule['from_port'] != nc_rule.from_port:
            return False
        if backend_rule['to_port'] != nc_rule.to_port:
            return False
        if backend_rule['ip_protocol'] != nc_rule.protocol:
            return False
        if backend_rule['ip_range'].get('cidr', '') != nc_rule.cidr:
            return False
        return True

    def _are_security_groups_equal(self, backend_security_group, nc_security_group):
        if backend_security_group.name != nc_security_group.name:
            return False
        if len(backend_security_group.rules) != nc_security_group.rules.count():
            return False
        for backend_rule, nc_rule in zip(backend_security_group.rules, nc_security_group.rules.all()):
            if not self._are_rules_equal(backend_rule, nc_rule):
                return False
        return True

    def _normalize_security_group_rule(self, rule):
        if rule['ip_protocol'] is None:
            rule['ip_protocol'] = ''

        if 'cidr' not in rule['ip_range']:
            rule['ip_range']['cidr'] = '0.0.0.0/0'

        return rule

    def pull_flavors(self):
        nova = self.nova_admin_client
        try:
            flavors = nova.flavors.findall(is_public=True)
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        with transaction.atomic():
            cur_flavors = self._get_current_properties(models.Flavor)
            for backend_flavor in flavors:
                cur_flavors.pop(backend_flavor.id, None)
                models.Flavor.objects.update_or_create(
                    settings=self.settings,
                    backend_id=backend_flavor.id,
                    defaults={
                        'name': backend_flavor.name,
                        'cores': backend_flavor.vcpus,
                        'ram': backend_flavor.ram,
                        'disk': self.gb2mb(backend_flavor.disk),
                    })

            models.Flavor.objects.filter(backend_id__in=cur_flavors.keys()).delete()

    def pull_images(self):
        glance = self.glance_client
        try:
            images = glance.images.list()
        except glance_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        with transaction.atomic():
            cur_images = self._get_current_properties(models.Image)
            for backend_image in images:
                if backend_image.is_public and not backend_image.deleted:
                    cur_images.pop(backend_image.id, None)
                    models.Image.objects.update_or_create(
                        settings=self.settings,
                        backend_id=backend_image.id,
                        defaults={
                            'name': backend_image.name,
                            'min_ram': backend_image.min_ram,
                            'min_disk': self.gb2mb(backend_image.min_disk),
                        })

            models.Image.objects.filter(backend_id__in=cur_images.keys()).delete()

    @log_backend_action('push quotas for tenant')
    def push_tenant_quotas(self, tenant, quotas):
        cinder_quotas = {
            'gigabytes': self.mb2gb(quotas.get('storage')) if 'storage' in quotas else None,
            'volumes': quotas.get('volumes'),
            'snapshots': quotas.get('snapshots'),
        }
        cinder_quotas = {k: v for k, v in cinder_quotas.items() if v is not None}

        nova_quotas = {
            'instances': quotas.get('instances'),
            'cores': quotas.get('vcpu'),
            'ram': quotas.get('ram'),
        }
        nova_quotas = {k: v for k, v in nova_quotas.items() if v is not None}

        neutron_quotas = {
            'security_group': quotas.get('security_group_count'),
            'security_group_rule': quotas.get('security_group_rule_count'),
        }
        neutron_quotas = {k: v for k, v in neutron_quotas.items() if v is not None}

        try:
            if cinder_quotas:
                self.cinder_client.quotas.update(tenant.backend_id, **cinder_quotas)
            if nova_quotas:
                self.nova_client.quotas.update(tenant.backend_id, **nova_quotas)
            if neutron_quotas:
                self.neutron_client.update_quota(tenant.backend_id, {'quota': neutron_quotas})
        except Exception as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action('pull quotas for tenant')
    def pull_tenant_quotas(self, tenant):
        for quota_name, limit in self.get_tenant_quotas_limits(tenant.backend_id).items():
            tenant.set_quota_limit(quota_name, limit)
        for quota_name, usage in self.get_tenant_quotas_usage(tenant.backend_id).items():
            tenant.set_quota_usage(quota_name, usage, fail_silently=True)

    def pull_floating_ips(self, tenants=None):
        neutron = self.neutron_admin_client

        if tenants is None:
            tenants = models.Tenant.objects.filter(
                state=models.Tenant.States.OK,
                service_project_link__service__settings=self.settings).prefetch_related('floating_ips')
        tenant_mappings = {tenant.backend_id: tenant for tenant in tenants}
        if not tenant_mappings:
            return

        try:
            backend_floating_ips = neutron.list_floatingips(
                tenant_id=tenant_mappings.keys())['floatingips']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        floating_ip_uuids = []
        with transaction.atomic():
            for backend_ip in backend_floating_ips:
                tenant = tenant_mappings[backend_ip['tenant_id']]
                imported_floating_ip = self._backend_floating_ip_to_floating_ip(
                    backend_ip, tenant=tenant, service_project_link=tenant.service_project_link)
                try:
                    floating_ip = tenant.floating_ips.get(backend_id=imported_floating_ip.backend_id)
                except models.FloatingIP.DoesNotExist:
                    imported_floating_ip.save()
                    floating_ip = imported_floating_ip
                else:
                    # Don't update user defined name.
                    if floating_ip.address != floating_ip.name:
                        imported_floating_ip.name = floating_ip.name
                    update_pulled_fields(floating_ip, imported_floating_ip, self.FLOATING_IP_UPDATE_FIELDS)
                    handle_resource_update_success(floating_ip)

                floating_ip_uuids.append(floating_ip.uuid)

            for floating_ip in models.FloatingIP.objects.filter(
                    state__in=[models.FloatingIP.States.OK, models.FloatingIP.States.ERRED],
                    service_project_link__service__settings=self.settings).exclude(uuid__in=floating_ip_uuids):
                handle_resource_not_found(floating_ip)

    @log_backend_action('pull floating IPs for tenant')
    def pull_tenant_floating_ips(self, tenant):
        neutron = self.neutron_client

        try:
            backend_floating_ips = neutron.list_floatingips(tenant_id=self.tenant_id)['floatingips']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        floating_ips = {ip.backend_id: ip for ip in tenant.floating_ips.filter(
            state__in=[models.FloatingIP.States.OK, models.FloatingIP.States.ERRED])}
        with transaction.atomic():
            for backend_ip in backend_floating_ips:
                imported_floating_ip = self._backend_floating_ip_to_floating_ip(
                    backend_ip,
                    tenant=tenant,
                    service_project_link=tenant.service_project_link,
                )
                floating_ip = floating_ips.pop(imported_floating_ip.backend_id, None)
                if floating_ip is None:
                    imported_floating_ip.save()
                    continue

                # Don't update user defined name.
                if floating_ip.address != floating_ip.name:
                    imported_floating_ip.name = floating_ip.name
                update_pulled_fields(floating_ip, imported_floating_ip, self.FLOATING_IP_UPDATE_FIELDS)
                handle_resource_update_success(floating_ip)

            for floating_ip in tenant.floating_ips.filter(backend_id__in=floating_ips.keys()):
                handle_resource_not_found(floating_ip)

    def _backend_floating_ip_to_floating_ip(self, backend_floating_ip, **kwargs):
        floating_ip = models.FloatingIP(
            name=backend_floating_ip['floating_ip_address'],
            description=backend_floating_ip['description'],
            address=backend_floating_ip['floating_ip_address'],
            backend_network_id=backend_floating_ip['floating_network_id'],
            runtime_state=backend_floating_ip['status'],
            backend_id=backend_floating_ip['id'],
            state=models.FloatingIP.States.OK,
        )
        for field, value in kwargs.items():
            setattr(floating_ip, field, value)

        return floating_ip

    def pull_security_groups(self, tenants=None):
        neutron = self.neutron_admin_client

        if tenants is None:
            tenants = models.Tenant.objects.filter(
                state=models.Tenant.States.OK,
                service_project_link__service__settings=self.settings,
            ).prefetch_related('security_groups')
        tenant_mappings = {tenant.backend_id: tenant for tenant in tenants}
        if not tenant_mappings:
            return

        try:
            backend_security_groups = neutron.list_security_groups(
                tenant_id=tenant_mappings.keys())['security_groups']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        security_group_uuids = []
        with transaction.atomic():
            for backend_security_group in backend_security_groups:
                tenant = tenant_mappings[backend_security_group['tenant_id']]

                imported_security_group = self._backend_security_group_to_security_group(
                    backend_security_group, tenant=tenant, service_project_link=tenant.service_project_link)

                try:
                    security_group = tenant.security_groups.get(backend_id=imported_security_group.backend_id)
                except models.SecurityGroup.DoesNotExist:
                    imported_security_group.save()
                    security_group = imported_security_group
                else:
                    update_pulled_fields(security_group, imported_security_group, self.SECURITY_GROUP_UPDATE_FIELDS)
                    handle_resource_update_success(security_group)

                security_group_uuids.append(security_group.uuid)
                self._extract_security_group_rules(security_group, backend_security_group)

            for security_group in models.SecurityGroup.objects.filter(
                    state__in=[models.SecurityGroup.States.OK, models.SecurityGroup.States.ERRED],
                    service_project_link__service__settings=self.settings).exclude(uuid__in=security_group_uuids):
                handle_resource_not_found(security_group)

    @log_backend_action('pull security groups for tenant')
    def pull_tenant_security_groups(self, tenant):
        neutron = self.neutron_client
        try:
            backend_security_groups = neutron.list_security_groups(tenant_id=self.tenant_id)['security_groups']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        security_groups = {group.backend_id: group for group in tenant.security_groups.filter(
            state__in=[models.SecurityGroup.States.OK, models.SecurityGroup.States.ERRED])}
        with transaction.atomic():
            for backend_security_group in backend_security_groups:
                imported_security_group = self._backend_security_group_to_security_group(
                    backend_security_group, tenant=tenant, service_project_link=tenant.service_project_link)

                security_group = security_groups.pop(imported_security_group.backend_id, None)
                if security_group is None:
                    imported_security_group.save()
                    security_group = imported_security_group
                else:
                    update_pulled_fields(security_group, imported_security_group, self.SECURITY_GROUP_UPDATE_FIELDS)
                    handle_resource_update_success(security_group)

                self._extract_security_group_rules(security_group, backend_security_group)

            for floating_ip in tenant.security_groups.filter(backend_id__in=security_groups.keys()):
                handle_resource_not_found(floating_ip)

    def _backend_security_group_to_security_group(self, backend_security_group, **kwargs):
        security_group = models.SecurityGroup(
            name=backend_security_group['name'],
            description=backend_security_group['description'],
            backend_id=backend_security_group['id'],
            state=models.SecurityGroup.States.OK,
        )

        for field, value in kwargs.items():
            setattr(security_group, field, value)

        return security_group

    def _extract_security_group_rules(self, security_group, backend_security_group):
        backend_rules = backend_security_group['security_group_rules']
        cur_rules = {rule.backend_id: rule for rule in security_group.rules.all()}
        for backend_rule in backend_rules:
            # Currently we support only rules for incoming traffic
            if backend_rule['direction'] != 'ingress':
                continue
            cur_rules.pop(backend_rule['id'], None)
            security_group.rules.update_or_create(
                backend_id=backend_rule['id'],
                defaults={
                    'from_port': backend_rule['port_range_min'],
                    'to_port': backend_rule['port_range_max'],
                    'protocol': backend_rule['protocol'] if backend_rule['protocol'] is not None else '',
                    'cidr': backend_rule['remote_ip_prefix']
                    if backend_rule['remote_ip_prefix'] is not None else '0.0.0.0/0',
                })
        security_group.rules.filter(backend_id__in=cur_rules.keys()).delete()

    def pull_networks(self, tenants=None):
        neutron = self.neutron_client

        if tenants is None:
            tenants = models.Tenant.objects.filter(
                state=models.Tenant.States.OK,
                service_project_link__service__settings=self.settings,
            ).prefetch_related('networks')
        tenant_mappings = {tenant.backend_id: tenant for tenant in tenants}
        if not tenant_mappings:
            return

        try:
            backend_networks = neutron.list_networks(tenant_id=tenant_mappings.keys())['networks']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        network_uuids = []
        with transaction.atomic():
            for backend_network in backend_networks:
                tenant = tenant_mappings[backend_network['tenant_id']]

                imported_network = self._backend_network_to_network(
                    backend_network, tenant=tenant, service_project_link=tenant.service_project_link)

                try:
                    network = tenant.networks.get(backend_id=imported_network.backend_id)
                except models.Network.DoesNotExist:
                    imported_network.save()
                    network = imported_network
                else:
                    update_pulled_fields(network, imported_network, self.NETWORK_UPDATE_FIELDS)
                    handle_resource_update_success(network)

                network_uuids.append(network.uuid)

            for network in models.Network.objects.filter(
                    state__in=[models.Network.States.OK, models.Network.States.ERRED],
                    service_project_link__service__settings=self.settings).exclude(uuid__in=network_uuids):
                handle_resource_not_found(network)

    def _backend_network_to_network(self, backend_network, **kwargs):
        network = models.Network(
            name=backend_network['name'],
            description=backend_network['description'],
            is_external=backend_network['router:external'],
            runtime_state=backend_network['status'],
            backend_id=backend_network['id'],
            state=models.Network.States.OK,
        )
        if backend_network.get('provider:network_type'):
            network.type = backend_network['provider:network_type']
        if backend_network.get('provider:segmentation_id'):
            network.segmentation_id = backend_network['provider:segmentation_id']

        for field, value in kwargs.items():
            setattr(network, field, value)

        return network

    def pull_subnets(self, networks=None):
        neutron = self.neutron_client

        if networks is None:
            networks = models.Network.objects.filter(
                state=models.Network.States.OK,
                service_project_link__service__settings=self.settings,
            ).prefetch_related('subnets')
        network_mappings = {network.backend_id: network for network in networks}
        if not network_mappings:
            return

        try:
            backend_subnets = neutron.list_subnets(network_id=network_mappings.keys())['subnets']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        subnet_uuids = []
        with transaction.atomic():
            for backend_subnet in backend_subnets:
                network = network_mappings[backend_subnet['network_id']]

                imported_subnet = self._backend_subnet_to_subnet(
                    backend_subnet, network=network, service_project_link=network.service_project_link)

                try:
                    subnet = network.subnets.get(backend_id=imported_subnet.backend_id)
                except models.SubNet.DoesNotExist:
                    imported_subnet.save()
                    subnet = imported_subnet
                else:
                    update_pulled_fields(subnet, imported_subnet, self.SUBNET_UPDATE_FIELDS)
                    handle_resource_update_success(subnet)

                subnet_uuids.append(subnet.uuid)

            for subnet in models.SubNet.objects.filter(
                    state__in=[models.SubNet.States.OK, models.SubNet.States.ERRED],
                    service_project_link__service__settings=self.settings).exclude(uuid__in=subnet_uuids):
                handle_resource_not_found(subnet)

    def _backend_subnet_to_subnet(self, backend_subnet, **kwargs):
        subnet = models.SubNet(
            name=backend_subnet['name'],
            description=backend_subnet['description'],
            allocation_pools=backend_subnet['allocation_pools'],
            cidr=backend_subnet['cidr'],
            ip_version=backend_subnet['ip_version'],
            enable_dhcp=backend_subnet['enable_dhcp'],
            gateway_ip=backend_subnet.get('gateway_ip'),
            dns_nameservers=backend_subnet['dns_nameservers'],
            backend_id=backend_subnet['id'],
            state=models.SubNet.States.OK,
        )

        for field, value in kwargs.items():
            setattr(subnet, field, value)

        return subnet

    @log_backend_action()
    def create_tenant(self, tenant):
        keystone = self.keystone_admin_client
        try:
            backend_tenant = keystone.projects.create(
                name=tenant.name, description=tenant.description, domain=self._get_domain())
            tenant.backend_id = backend_tenant.id
            tenant.save(update_fields=['backend_id'])
        except keystone_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

    def import_tenant(self, tenant_backend_id, service_project_link=None, save=True):
        keystone = self.keystone_admin_client
        try:
            backend_tenant = keystone.projects.get(tenant_backend_id)
        except keystone_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        tenant = models.Tenant()
        tenant.name = backend_tenant.name
        tenant.description = backend_tenant.description
        tenant.backend_id = tenant_backend_id

        if save and service_project_link:
            tenant.service_project_link = service_project_link
            tenant.state = models.Tenant.States.OK
            tenant.save()
        return tenant

    @log_backend_action()
    def pull_tenant(self, tenant):
        import_time = timezone.now()
        imported_tenant = self.import_tenant(tenant.backend_id, save=False)

        tenant.refresh_from_db()
        # if tenant was not modified in NC database after import.
        if tenant.modified < import_time:
            update_pulled_fields(tenant, imported_tenant, ('name', 'description'))

    @log_backend_action()
    def add_admin_user_to_tenant(self, tenant):
        """ Add user from openstack settings to new tenant """
        keystone = self.keystone_admin_client

        try:
            admin_user = keystone.users.find(name=self.settings.username)
            admin_role = keystone.roles.find(name='admin')
            try:
                keystone.roles.grant(
                    user=admin_user.id,
                    role=admin_role.id,
                    project=tenant.backend_id)
            except keystone_exceptions.Conflict:
                pass
        except keystone_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action('add user to tenant')
    def create_tenant_user(self, tenant):
        keystone = self.keystone_client

        try:
            user = keystone.users.create(
                name=tenant.user_username,
                password=tenant.user_password,
                domain=self._get_domain(),
            )
            try:
                role = keystone.roles.find(name='Member')
            except keystone_exceptions.NotFound:
                role = keystone.roles.find(name='_member_')
            keystone.roles.grant(
                user=user.id,
                role=role.id,
                project=tenant.backend_id,
            )
        except keystone_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action('change password for tenant user')
    def change_tenant_user_password(self, tenant):
        keystone = self.keystone_client

        try:
            keystone_user = keystone.users.find(name=tenant.user_username)
            keystone.users.update(user=keystone_user, password=tenant.user_password)
        except keystone_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

    def get_resources_for_import(self, resource_type=None):
        return self.get_tenants_for_import()

    def get_tenants_for_import(self):
        keystone = self.keystone_admin_client
        try:
            tenants = keystone.projects.list(domain=self._get_domain())
        except keystone_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        cur_tenants = set(models.Tenant.objects.filter(
            service_project_link__service__settings=self.settings
        ).values_list('backend_id', flat=True))

        return [{
            'id': tenant.id,
            'name': tenant.name,
            'description': tenant.description,
            'type': SupportedServices.get_name_for_model(models.Tenant)
        } for tenant in tenants if tenant.id not in cur_tenants]

    def get_managed_resources(self):
        return []

    @log_backend_action()
    def delete_tenant_floating_ips(self, tenant):
        if not tenant.backend_id:
            # This method will remove all floating IPs if tenant `backend_id` is not defined.
            raise OpenStackBackendError('This method should not be called if tenant has no backend_id')

        neutron = self.neutron_admin_client

        try:
            floatingips = neutron.list_floatingips(tenant_id=tenant.backend_id)
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        for floating_ip in floatingips.get('floatingips', []):
            self._delete_backend_floating_ip(floating_ip['id'], tenant.backend_id)

    @log_backend_action()
    def delete_tenant_ports(self, tenant):
        if not tenant.backend_id:
            # This method will remove all ports if tenant `backend_id` is not defined.
            raise OpenStackBackendError('This method should not be called if tenant has no backend_id')

        neutron = self.neutron_admin_client

        try:
            ports = neutron.list_ports(tenant_id=tenant.backend_id)
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        for port in ports.get('ports', []):
            logger.info("Deleting port %s interface_router from tenant %s", port['id'], tenant.backend_id)
            try:
                neutron.remove_interface_router(port['device_id'], {'port_id': port['id']})
            except neutron_exceptions.NotFound:
                logger.debug("Port %s interface_router is already gone from tenant %s", port['id'],
                             tenant.backend_id)
            except neutron_exceptions.NeutronClientException as e:
                six.reraise(OpenStackBackendError, e)

            logger.info("Deleting port %s from tenant %s", port['id'], tenant.backend_id)
            try:
                neutron.delete_port(port['id'])
            except neutron_exceptions.NotFound:
                logger.debug("Port %s is already gone from tenant %s", port['id'], tenant.backend_id)
            except neutron_exceptions.NeutronClientException as e:
                six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def delete_tenant_routers(self, tenant):
        if not tenant.backend_id:
            # This method will remove all routers if tenant `backend_id` is not defined.
            raise OpenStackBackendError('This method should not be called if tenant has no backend_id')

        neutron = self.neutron_admin_client

        try:
            routers = neutron.list_routers(tenant_id=tenant.backend_id)
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        for router in routers.get('routers', []):
            logger.info("Deleting router %s from tenant %s", router['id'], tenant.backend_id)
            try:
                neutron.delete_router(router['id'])
            except neutron_exceptions.NotFound:
                logger.debug("Router %s is already gone from tenant %s", router['id'], tenant.backend_id)
            except neutron_exceptions.NeutronClientException as e:
                six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def delete_tenant_networks(self, tenant):
        if not tenant.backend_id:
            # This method will remove all networks if tenant `backend_id` is not defined.
            raise OpenStackBackendError('This method should not be called if tenant has no backend_id')

        neutron = self.neutron_admin_client

        try:
            networks = neutron.list_networks(tenant_id=tenant.backend_id)
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        for network in networks.get('networks', []):
            if network['router:external']:
                continue
            for subnet in network['subnets']:
                logger.info("Deleting subnetwork %s from tenant %s", subnet, tenant.backend_id)
                try:
                    neutron.delete_subnet(subnet)
                except neutron_exceptions.NotFound:
                    logger.info("Subnetwork %s is already gone from tenant %s", subnet, tenant.backend_id)
                except neutron_exceptions.NeutronClientException as e:
                    six.reraise(OpenStackBackendError, e)

            logger.info("Deleting network %s from tenant %s", network['id'], tenant.backend_id)
            try:
                neutron.delete_network(network['id'])
            except neutron_exceptions.NotFound:
                logger.debug("Network %s is already gone from tenant %s", network['id'], tenant.backend_id)
            except neutron_exceptions.NeutronClientException as e:
                six.reraise(OpenStackBackendError, e)

        tenant.set_quota_usage(tenant.Quotas.network_count, 0)
        tenant.set_quota_usage(tenant.Quotas.subnet_count, 0)

    @log_backend_action()
    def delete_tenant_security_groups(self, tenant):
        nova = self.nova_client

        try:
            sgroups = nova.security_groups.list()
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        for sgroup in sgroups:
            logger.info("Deleting security group %s from tenant %s", sgroup.id, tenant.backend_id)
            try:
                sgroup.delete()
            except nova_exceptions.NotFound:
                logger.debug("Security group %s is already gone from tenant %s", sgroup.id, tenant.backend_id)
            except nova_exceptions.ClientException as e:
                six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def delete_tenant_instances(self, tenant):
        nova = self.nova_client

        try:
            servers = nova.servers.list()
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        for server in servers:
            logger.info("Deleting instance %s from tenant %s", server.id, tenant.backend_id)
            try:
                server.delete()
            except nova_exceptions.NotFound:
                logger.debug("Instance %s is already gone from tenant %s", server.id, tenant.backend_id)
            except nova_exceptions.ClientException as e:
                six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def are_all_tenant_instances_deleted(self, tenant):
        nova = self.nova_client

        try:
            servers = nova.servers.list()
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            return not servers

    @log_backend_action()
    def delete_tenant_snapshots(self, tenant):
        cinder = self.cinder_client

        try:
            snapshots = cinder.volume_snapshots.list()
        except cinder_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        for snapshot in snapshots:
            logger.info("Deleting snapshot %s from tenant %s", snapshot.id, tenant.backend_id)
            try:
                snapshot.delete()
            except cinder_exceptions.NotFound:
                logger.debug("Snapshot %s is already gone from tenant %s", snapshot.id, tenant.backend_id)
            except cinder_exceptions.ClientException as e:
                six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def are_all_tenant_snapshots_deleted(self, tenant):
        cinder = self.cinder_client

        try:
            snapshots = cinder.volume_snapshots.list()
        except cinder_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            return not snapshots

    @log_backend_action()
    def delete_tenant_volumes(self, tenant):
        cinder = self.cinder_client

        try:
            volumes = cinder.volumes.list()
        except cinder_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        for volume in volumes:
            logger.info("Deleting volume %s from tenant %s", volume.id, tenant.backend_id)
            try:
                volume.delete()
            except cinder_exceptions.NotFound:
                logger.debug("Volume %s is already gone from tenant %s", volume.id, tenant.backend_id)
            except cinder_exceptions.ClientException as e:
                six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def are_all_tenant_volumes_deleted(self, tenant):
        cinder = self.cinder_client

        try:
            volumes = cinder.volumes.list()
        except cinder_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            return not volumes

    @log_backend_action()
    def delete_tenant_user(self, tenant):
        keystone = self.keystone_client
        try:
            user = keystone.users.find(name=tenant.user_username)
            logger.info('Deleting user %s that was connected to tenant %s', user.name, tenant.backend_id)
            user.delete()
        except keystone_exceptions.NotFound:
            logger.debug("User %s is already gone from tenant %s", tenant.user_username, tenant.backend_id)
        except keystone_exceptions.ClientException as e:
            logger.error('Cannot delete user %s from tenant %s. Error: %s', tenant.user_username, tenant.backend_id, e)

    @log_backend_action()
    def delete_tenant(self, tenant):
        if not tenant.backend_id:
            raise OpenStackBackendError('This method should not be called if tenant has no backend_id')

        keystone = self.keystone_admin_client

        logger.info("Deleting tenant %s", tenant.backend_id)
        try:
            keystone.projects.delete(tenant.backend_id)
        except keystone_exceptions.NotFound:
            logger.debug("Tenant %s is already gone", tenant.backend_id)
        except keystone_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def push_security_group_rules(self, security_group):
        nova = self.nova_client
        backend_security_group = nova.security_groups.get(group_id=security_group.backend_id)
        backend_rules = {
            rule['id']: self._normalize_security_group_rule(rule)
            for rule in backend_security_group.rules
        }

        # list of nc rules, that do not exist in openstack
        nonexistent_rules = []
        # list of nc rules, that have wrong parameters in in openstack
        unsynchronized_rules = []
        # list of os rule ids, that exist in openstack and do not exist in nc
        extra_rule_ids = backend_rules.keys()

        for nc_rule in security_group.rules.all():
            if nc_rule.backend_id not in backend_rules:
                nonexistent_rules.append(nc_rule)
            else:
                backend_rule = backend_rules[nc_rule.backend_id]
                if not self._are_rules_equal(backend_rule, nc_rule):
                    unsynchronized_rules.append(nc_rule)
                extra_rule_ids.remove(nc_rule.backend_id)

        # deleting extra rules
        for backend_rule_id in extra_rule_ids:
            logger.debug('About to delete security group rule with id %s in backend', backend_rule_id)
            try:
                nova.security_group_rules.delete(backend_rule_id)
            except nova_exceptions.ClientException:
                logger.exception('Failed to remove rule with id %s from security group %s in backend',
                                 backend_rule_id, security_group)
            else:
                logger.info('Security group rule with id %s successfully deleted in backend', backend_rule_id)

        # deleting unsynchronized rules
        for nc_rule in unsynchronized_rules:
            logger.debug('About to delete security group rule with id %s', nc_rule.backend_id)
            try:
                nova.security_group_rules.delete(nc_rule.backend_id)
            except nova_exceptions.ClientException:
                logger.exception('Failed to remove rule with id %s from security group %s in backend',
                                 nc_rule.backend_id, security_group)
            else:
                logger.info('Security group rule with id %s successfully deleted in backend',
                            nc_rule.backend_id)

        # creating nonexistent and unsynchronized rules
        for nc_rule in unsynchronized_rules + nonexistent_rules:
            logger.debug('About to create security group rule with id %s in backend', nc_rule.id)
            try:
                # The database has empty strings instead of nulls
                if nc_rule.protocol == '':
                    nc_rule_protocol = None
                else:
                    nc_rule_protocol = nc_rule.protocol

                nova.security_group_rules.create(
                    parent_group_id=security_group.backend_id,
                    ip_protocol=nc_rule_protocol,
                    from_port=nc_rule.from_port,
                    to_port=nc_rule.to_port,
                    cidr=nc_rule.cidr,
                )
            except nova_exceptions.ClientException as e:
                logger.exception('Failed to create rule %s for security group %s in backend',
                                 nc_rule, security_group)
                six.reraise(OpenStackBackendError, e)
            else:
                logger.info('Security group rule with id %s successfully created in backend', nc_rule.id)

    @log_backend_action()
    def create_security_group(self, security_group):
        nova = self.nova_client
        try:
            backend_security_group = nova.security_groups.create(
                name=security_group.name, description=security_group.description)
            security_group.backend_id = backend_security_group.id
            security_group.save()
            self.push_security_group_rules(security_group)
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def delete_security_group(self, security_group):
        nova = self.nova_client
        try:
            nova.security_groups.delete(security_group.backend_id)
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)
        security_group.decrease_backend_quotas_usage()

    @log_backend_action()
    def update_security_group(self, security_group):
        nova = self.nova_client
        try:
            backend_security_group = nova.security_groups.find(id=security_group.backend_id)
            nova.security_groups.update(
                backend_security_group, name=security_group.name, description=security_group.description)
            self.push_security_group_rules(security_group)
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action('create external network for tenant')
    def create_external_network(self, tenant, neutron, network_ip, network_prefix,
                                vlan_id=None, vxlan_id=None, ips_count=None):
        if tenant.external_network_id:
            self.connect_tenant_to_external_network(tenant, tenant.external_network_id)

        neutron = self.neutron_admin_client

        # External network creation
        network_name = 'nc-{0}-ext-net'.format(uuid.uuid4().hex)
        network = {
            'name': network_name,
            'tenant_id': tenant.backend_id,
            'router:external': True,
            # XXX: provider:physical_network should be configurable.
            'provider:physical_network': 'physnet1'
        }

        if vlan_id:
            network['provider:network_type'] = 'vlan'
            network['provider:segmentation_id'] = vlan_id
        elif vxlan_id:
            network['provider:network_type'] = 'vxlan'
            network['provider:segmentation_id'] = vxlan_id
        else:
            raise OpenStackBackendError('VLAN or VXLAN ID should be provided.')

        create_response = neutron.create_network({'networks': [network]})
        network_id = create_response['networks'][0]['id']
        logger.info('External network with name %s has been created.', network_name)
        tenant.external_network_id = network_id
        tenant.save(update_fields=['external_network_id'])

        # Subnet creation
        subnet_name = '{0}-sn01'.format(network_name)
        cidr = '{0}/{1}'.format(network_ip, network_prefix)

        subnet_data = {
            'network_id': tenant.external_network_id,
            'tenant_id': tenant.backend_id,
            'cidr': cidr,
            'name': subnet_name,
            'ip_version': 4,
            'enable_dhcp': False,
        }
        create_response = neutron.create_subnet({'subnets': [subnet_data]})
        logger.info('Subnet with name %s has been created.', subnet_name)

        # Router creation
        self.get_or_create_router(network_name, create_response['subnets'][0]['id'])

        # Floating IPs creation
        floating_ip = {
            'floating_network_id': tenant.external_network_id,
        }

        if vlan_id is not None and ips_count is not None:
            for i in range(ips_count):
                ip = neutron.create_floatingip({'floatingip': floating_ip})['floatingip']
                logger.info('Floating ip %s for external network %s has been created.',
                            ip['floating_ip_address'], network_name)

        return tenant.external_network_id

    @log_backend_action()
    def detect_external_network(self, tenant):
        neutron = self.neutron_client
        try:
            routers = neutron.list_routers(tenant_id=tenant.backend_id)['routers']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)
        if bool(routers):
            router = routers[0]
        else:
            logger.warning('Tenant %s (PK: %s) does not have connected routers.', tenant, tenant.pk)
            return

        ext_gw = router.get('external_gateway_info', {})
        if ext_gw and 'network_id' in ext_gw:
            tenant.external_network_id = ext_gw['network_id']
            tenant.save()
            logger.info('Found and set external network with id %s for tenant %s (PK: %s)',
                        ext_gw['network_id'], tenant, tenant.pk)

    @log_backend_action('delete tenant external network')
    def delete_external_network(self, tenant):
        neutron = self.neutron_admin_client

        try:
            floating_ips = neutron.list_floatingips(
                floating_network_id=tenant.external_network_id)['floatingips']

            for ip in floating_ips:
                neutron.delete_floatingip(ip['id'])
                logger.info('Floating IP with id %s has been deleted.', ip['id'])

            ports = neutron.list_ports(network_id=tenant.external_network_id)['ports']
            for port in ports:
                neutron.remove_interface_router(port['device_id'], {'port_id': port['id']})
                logger.info('Port with id %s has been deleted.', port['id'])

            subnets = neutron.list_subnets(network_id=tenant.external_network_id)['subnets']
            for subnet in subnets:
                neutron.delete_subnet(subnet['id'])
                logger.info('Subnet with id %s has been deleted.', subnet['id'])

            neutron.delete_network(tenant.external_network_id)
            logger.info('External network with id %s has been deleted.', tenant.external_network_id)
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            tenant.external_network_id = ''
            tenant.save()

    @log_backend_action()
    def create_network(self, network):
        neutron = self.neutron_admin_client

        data = {'name': network.name, 'tenant_id': network.tenant.backend_id}
        try:
            response = neutron.create_network({'networks': [data]})
        except neutron_exceptions.NeutronException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            backend_network = response['networks'][0]
            network.backend_id = backend_network['id']
            network.runtime_state = backend_network['status']
            if backend_network.get('provider:network_type'):
                network.type = backend_network['provider:network_type']
            if backend_network.get('provider:segmentation_id'):
                network.segmentation_id = backend_network['provider:segmentation_id']
            network.save()
            # XXX: temporary fix - right now backend logic is based on statement "one tenant has one network"
            # We need to fix this in the future.
            network.tenant.internal_network_id = network.backend_id
            network.tenant.save()

    @log_backend_action()
    def update_network(self, network):
        neutron = self.neutron_admin_client

        data = {'name': network.name}
        try:
            neutron.update_network(network.backend_id, {'network': data})
        except neutron_exceptions.NeutronException as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def delete_network(self, network):
        for subnet in network.subnets.all():
            self.delete_subnet(subnet)

        neutron = self.neutron_admin_client
        try:
            neutron.delete_network(network.backend_id)
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            network.decrease_backend_quotas_usage()

    def import_network(self, network_backend_id):
        neutron = self.neutron_admin_client
        try:
            backend_network = neutron.show_network(network_backend_id)['network']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        return self._backend_network_to_network(backend_network)

    @log_backend_action()
    def pull_network(self, network):
        import_time = timezone.now()
        imported_network = self.import_network(network.backend_id)

        network.refresh_from_db()
        if network.modified < import_time:
            update_pulled_fields(network, imported_network, self.NETWORK_UPDATE_FIELDS)

    @log_backend_action()
    def create_subnet(self, subnet):
        neutron = self.neutron_admin_client

        data = {
            'name': subnet.name,
            'network_id': subnet.network.backend_id,
            'tenant_id': subnet.network.tenant.backend_id,
            'cidr': subnet.cidr,
            'allocation_pools': subnet.allocation_pools,
            'ip_version': subnet.ip_version,
            'enable_dhcp': subnet.enable_dhcp,
        }
        if subnet.dns_nameservers:
            data['dns_nameservers'] = subnet.dns_nameservers
        try:
            response = neutron.create_subnet({'subnets': [data]})
            # Automatically create router for subnet
            # TODO: Ideally: Create separate model for router and create it separately.
            #       Good enough: refactor `get_or_create_router` method: split it into several method.
            self.get_or_create_router(subnet.network.name, response['subnets'][0]['id'],
                                      tenant_id=subnet.network.tenant.backend_id)
        except neutron_exceptions.NeutronException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            backend_subnet = response['subnets'][0]
            subnet.backend_id = backend_subnet['id']
            if backend_subnet.get('gateway_ip'):
                subnet.gateway_ip = backend_subnet['gateway_ip']
            subnet.save()

    @log_backend_action()
    def update_subnet(self, subnet):
        neutron = self.neutron_admin_client

        data = {'name': subnet.name}
        try:
            neutron.update_subnet(subnet.backend_id, {'subnet': data})
        except neutron_exceptions.NeutronException as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action()
    def delete_subnet(self, subnet):
        neutron = self.neutron_admin_client
        try:
            neutron.delete_subnet(subnet.backend_id)
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            subnet.decrease_backend_quotas_usage()

    def import_subnet(self, subnet_backend_id):
        neutron = self.neutron_admin_client
        try:
            backend_subnet = neutron.show_subnet(subnet_backend_id)['subnet']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        subnet = models.SubNet(
            name=backend_subnet['name'],
            description=backend_subnet['description'],
            allocation_pools=backend_subnet['allocation_pools'],
            cidr=backend_subnet['cidr'],
            ip_version=backend_subnet.get('ip_version'),
            gateway_ip=backend_subnet.get('gateway_ip'),
            enable_dhcp=backend_subnet.get('enable_dhcp', False),
            state=models.Network.States.OK,
        )
        return subnet

    @log_backend_action()
    def pull_subnet(self, subnet):
        import_time = timezone.now()
        imported_subnet = self.import_subnet(subnet.backend_id)

        subnet.refresh_from_db()
        if subnet.modified < import_time:
            update_fields = ('name', 'cidr', 'allocation_pools', 'ip_version', 'gateway_ip', 'enable_dhcp')
            update_pulled_fields(subnet, imported_subnet, update_fields)

    @log_backend_action('pull floating ip')
    def pull_floating_ip(self, floating_ip):
        neutron = self.neutron_client
        try:
            backend_floating_ip = neutron.show_floatingip(floating_ip.backend_id)['floatingip']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        imported_floating_ip = self._backend_floating_ip_to_floating_ip(backend_floating_ip, floating_ip.tenant)
        update_pulled_fields(floating_ip, imported_floating_ip, self.FLOATING_IP_UPDATE_FIELDS)

    @log_backend_action('delete floating ip')
    def delete_floating_ip(self, floating_ip):
        self._delete_backend_floating_ip(floating_ip.backend_id, floating_ip.tenant.backend_id)
        floating_ip.decrease_backend_quotas_usage()

    def _delete_backend_floating_ip(self, backend_id, tenant_backend_id):
        neutron = self.neutron_client
        try:
            logger.info("Deleting floating IP %s from tenant %s", backend_id, tenant_backend_id)
            neutron.delete_floatingip(backend_id)
        except neutron_exceptions.NotFound:
            logger.debug("Floating IP %s is already gone from tenant %s", backend_id, tenant_backend_id)
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

    @log_backend_action('create floating ip')
    def create_floating_ip(self, floating_ip):
        neutron = self.neutron_client
        try:
            backend_floating_ip = neutron.create_floatingip({
                'floatingip': {
                    'floating_network_id': floating_ip.tenant.external_network_id,
                    'tenant_id': floating_ip.tenant.backend_id,
                }
            })['floatingip']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)
        else:
            floating_ip.runtime_state = backend_floating_ip['status']
            floating_ip.address = backend_floating_ip['floating_ip_address']
            floating_ip.name = backend_floating_ip['floating_ip_address']
            floating_ip.backend_id = backend_floating_ip['id']
            floating_ip.backend_network_id = backend_floating_ip['floating_network_id']
            floating_ip.save()

    @log_backend_action()
    def connect_tenant_to_external_network(self, tenant, external_network_id):
        neutron = self.neutron_admin_client
        logger.debug('About to create external network for tenant "%s" (PK: %s)', tenant.name, tenant.pk)

        try:
            # check if the network actually exists
            response = neutron.show_network(external_network_id)
        except neutron_exceptions.NeutronClientException as e:
            logger.exception('External network %s does not exist. Stale data in database?', external_network_id)
            six.reraise(OpenStackBackendError, e)

        network_name = response['network']['name']
        subnet_id = response['network']['subnets'][0]
        # XXX: refactor function call, split get_or_create_router into more fine grained
        self.get_or_create_router(network_name, subnet_id,
                                  external=True, network_id=response['network']['id'])

        tenant.external_network_id = external_network_id
        tenant.save()

        logger.info('Router between external network %s and tenant %s was successfully created',
                    external_network_id, tenant.backend_id)

        return external_network_id

    def get_or_create_router(self, network_name, subnet_id, external=False, network_id=None, tenant_id=None):
        neutron = self.neutron_admin_client
        tenant_id = tenant_id or self.tenant_id
        router_name = '{0}-router'.format(network_name)

        try:
            routers = neutron.list_routers(tenant_id=tenant_id)['routers']
        except neutron_exceptions.NeutronClientException as e:
            six.reraise(OpenStackBackendError, e)

        if routers:
            logger.info('Router(s) in tenant with id %s already exist(s).', tenant_id)
            router = routers[0]
        else:
            try:
                router = neutron.create_router({'router': {'name': router_name, 'tenant_id': tenant_id}})['router']
                logger.info('Router %s has been created.', router['name'])
            except neutron_exceptions.NeutronClientException as e:
                six.reraise(OpenStackBackendError, e)

        try:
            if not external:
                ports = neutron.list_ports(device_id=router['id'], tenant_id=tenant_id)['ports']
                if not ports:
                # XXX: Ilja: revert to old behaviour as new check breaks setup of router legs
                # if subnet_id in [port['fixed_ips'][0]['subnet_id'] for port in ports]:
                    neutron.add_interface_router(router['id'], {'subnet_id': subnet_id})
                    logger.info('Internal subnet %s was connected to the router %s.', subnet_id, router_name)
                else:
                    logger.info('Internal subnet %s is already connected to the router %s.', subnet_id, router_name)
            else:
                if (not router.get('external_gateway_info') or
                        router['external_gateway_info'].get('network_id') != network_id):
                    neutron.add_gateway_router(router['id'], {'network_id': network_id})
                    logger.info('External network %s was connected to the router %s.', network_id, router_name)
                else:
                    logger.info('External network %s is already connected to router %s.', network_id, router_name)
        except neutron_exceptions.NeutronClientException as e:
            logger.warning(e)

        return router['id']

    @log_backend_action()
    def update_tenant(self, tenant):
        keystone = self.keystone_admin_client
        try:
            keystone.projects.update(tenant.backend_id, name=tenant.name, description=tenant.description)
        except keystone_exceptions.NotFound as e:
            logger.error('Tenant with id %s does not exist', tenant.backend_id)
            six.reraise(OpenStackBackendError, e)

    def pull_service_settings_quotas(self):
        nova = self.nova_admin_client
        try:
            stats = nova.hypervisor_stats.statistics()
        except nova_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        self.settings.set_quota_limit(self.settings.Quotas.openstack_vcpu, stats.vcpus)
        self.settings.set_quota_usage(self.settings.Quotas.openstack_vcpu, stats.vcpus_used)

        self.settings.set_quota_limit(self.settings.Quotas.openstack_ram, stats.memory_mb)
        self.settings.set_quota_usage(self.settings.Quotas.openstack_ram, stats.memory_mb_used)

        self.settings.set_quota_usage(self.settings.Quotas.openstack_storage, self.get_storage_usage())

    def get_storage_usage(self):
        cinder = self.cinder_admin_client

        try:
            volumes = cinder.volumes.list()
            snapshots = cinder.volume_snapshots.list()
        except cinder_exceptions.ClientException as e:
            six.reraise(OpenStackBackendError, e)

        storage = sum(self.gb2mb(v.size) for v in volumes + snapshots)
        return storage

    def get_stats(self):
        tenants = models.Tenant.objects.filter(service_project_link__service__settings=self.settings)
        quota_names = ('vcpu', 'ram', 'storage')
        quota_values = models.Tenant.get_sum_of_quotas_as_dict(
            tenants, quota_names=quota_names, fields=['limit'])
        quota_stats = {
            'vcpu_quota': quota_values.get('vcpu', -1.0),
            'ram_quota': quota_values.get('ram', -1.0),
            'storage_quota': quota_values.get('storage', -1.0)
        }

        stats = {}
        for quota in self.settings.quotas.all():
            name = quota.name.replace('openstack_', '')
            if name not in quota_names:
                continue
            stats[name] = quota.limit
            stats[name + '_usage'] = quota.usage
        stats.update(quota_stats)
        return stats
