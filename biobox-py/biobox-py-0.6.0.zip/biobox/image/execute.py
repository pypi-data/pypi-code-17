import docker.utils, funcy
import biobox.util         as util
import biobox.config       as cfg
import biobox.image.volume as vol

from functools import partial

def prepare_biobox_file(version, config):
    """
    Creates a biobox file in a temporary directory and returns a
    Docker volume string for that directory's location.
    """
    f = funcy.compose(
        vol.biobox_file,
        cfg.create_biobox_directory,
        partial(cfg.generate_biobox_file_content, version),
        cfg.remap_biobox_input_paths)
    return f(config)


def prepare_volumes(config, output_directory, metadata_directory = None, version = "0.9.0"):
    """
    Returns an arrary of Docker volume strings that may be used to mount required
    input and output directories into the Docker container.

    Keyword arguments:
      config             -- Biobox configuration as specified by the biobox.yaml
                            format
      output_directory   -- Destination directory path for output files
      metadata_directory -- Destination directory path for metadata files, this is
                            optional and if is None will be ignored and not mounted.
      version            -- Version string for biobox config format. Default is 0.9.0

    Raises:
        BioboxesInputVolumeNotFound
            If the parent directory of the input files does not exist.
    """
    # Ensure the input directories exist before proceeding
    input_paths = cfg.get_all_biobox_paths(config)
    vol.validate_host_volumes(input_paths)

    # Create volumes to be mounted into the container
    docker_volumes = vol.create_volume_string_set(input_paths) + \
           [prepare_biobox_file(version, config)] + \
           [vol.output(output_directory)]
    if metadata_directory:
        return docker_volumes + [vol.metadata(metadata_directory)]
    else:
        return docker_volumes


def create_container(image, config, directories, task = "default", version = "0.9.0", docker_args = {}):
    """
    Returns a new biobox Docker container created from the given image name. The
    container is not started. Networking will be enabled by default until an issue
    with Docker stats collection is resolved - docker/docker-py#1195.

    Keyword arguments:
      image       -- name of a docker image, may optionally include sha256
      config      -- biobox configuration as specified by the biobox.yaml format
      directories -- dictionary of host directories locations with the keys:
                     output   -- REQUIRED location of output destination directory
                     metadata -- OPTIONAL location of metadata destination directory
      task        -- biobox container task to execute, defaults to "default".
      docker_args -- Optional cgroup data passed to the docker daemon. See the
                     docker documentation for a list of available values

    Raises:
        BioboxesInputVolumeNotFound
            If the parent directory of the input files does not exist.
    """

    volumes = prepare_volumes(config, directories.get('output'), directories.get('metadata'), version)
    docker_args['volumes']          = list(map(vol.get_host_path, volumes))
    docker_args['network_disabled'] = False

    host_config = {'binds' : volumes}
    if 'mem_limit' in docker_args:
        host_config['mem_limit'] = docker_args['mem_limit']
        del docker_args['mem_limit']

    docker_args['host_config'] = util.client().create_host_config(**host_config)
    return util.client().create_container(image, task, **docker_args)
