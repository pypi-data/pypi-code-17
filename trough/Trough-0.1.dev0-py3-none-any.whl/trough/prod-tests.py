from trough.sync import HostRegistry
import consulate

consul = consulate.Consul(host='wbgrp-svc110', port=6500)
registry = HostRegistry(consul=consul)
registry.consul.catalog.service('trough-sync-master')