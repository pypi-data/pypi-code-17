volume_schema = {
    'container_path': {'type': 'string'},
    'host_path': {'type': 'string', 'required': True},
    'mode': {'type': 'string'}
}

docker_info_schema = {
    'image': {'type': 'string', 'required': True},
    'network': {'type': 'string'},
    'force_pull_image': {'type': 'boolean'},
    'parameters': {'type': 'dict', 'keyschema': {'type': 'string'}, 'valueschema': {'type': 'string'}},
}

container_schema = {
    'type': {'type': 'string', 'allowed': ['MESOS', 'DOCKER']},
    'docker': {'type': 'dict', 'schema': docker_info_schema}
}