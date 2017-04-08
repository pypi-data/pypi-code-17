import numbers
import six
from pystachio import *

'''
https://github.com/twosigma/Cook/blob/master/scheduler/docs/scheduler-rest-api.asc
'''

# See https://github.com/twosigma/Cook/blob/master/scheduler/src/cook/mesos/api.clj


class FetchURI(Struct):
    value = Required(String)
    executable = Boolean
    extract = Default(Boolean, True)
    cache = Default(Boolean, True)


class DockerPortMapping(Struct):
    host_port = Required(Integer)
    container_port = Required(Integer)
    protocol = String


class DockerInfo(Struct):
    image = Required(String)
    network = String
    force_pull_image = Boolean
    parameters = Map(String, String)
    port_mapping = List(DockerPortMapping)


class Volume(Struct):
    container_path = String
    host_path = Required(String)
    mode = String


class Container(Struct):
    type = Required(Enum('ContainerType', ('MESOS', 'DOCKER')))
    docker = DockerInfo
    volumes = List(Volume)


class Job(Struct):
    name = Required(String)
    uuid = Required(String)
    priority = Required(Integer)
    command = Required(String)
    max_retries = Required(Integer)
    max_runtime = Integer
    cpus = Required(Float)
    mem = Required(Float)
    gpus = Integer
    ports = Integer
    container = Container
    group = String
    uris = List(FetchURI)
    env = Map(String, String)
    labels = Map(String, String)


Status = Enum('Status', ('waiting', 'running', 'completed'))


class JobInstance(Struct):
    status = Required(String)
    task_id = Required(String)
    executor_id = Required(String)
    slave_id = Required(String)
    hostname = Required(String)
    preempted = Required(Boolean)
    backfilled = Required(Boolean)
    ports = Required(Integer)
    start_time = Integer
    mesos_start_time = Integer
    end_time = Integer
    reason_code = Integer
    output_url = String
    cancelled = Boolean
    reason_string = String


class JobStatus(Struct):
    name = Required(String)
    uuid = Required(String)
    priority = Required(Integer)
    command = Required(String)
    framework_id = String
    status = Status
    state = String
    max_retries = Required(Integer)
    max_runtime = Integer
    cpus = Required(Float)
    mem = Required(Float)
    gpus = Integer
    ports = Integer
    container = Container
    group = String
    uris = List(FetchURI)
    env = Map(String, String)
    labels = Map(String, String)
    submit_time = Integer
    retries_remaining = Integer
    user = String
    groups = List(String)
    instances = List(JobInstance)