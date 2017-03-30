from ConfigParser import Error
from ConfigParser import NoSectionError
import logging
import os
from pprint import pprint
import re
import time

from argh import arg
from pnc_cli import buildconfigurations
from pnc_cli import buildconfigurationsets
from pnc_cli import products
from pnc_cli import projects
from pnc_cli import bpmbuildconfigurations
from pnc_cli.buildconfigurations import get_build_configuration_by_name
from tools.config_utils import ConfigReader


@arg('-c', '--config', help='Make-mead style configuration file possibly extended with pnc.* data fields.')
@arg('-b', '--run_build', help='Run Build')
@arg('-e', '--environment', help='PNC Environment ID')
@arg('-s', '--sufix', help='Adding suffix to artifact\'s name')
@arg('-p', '--product_name', help='Product name')
@arg('-v', '--product_version', help='Product version')
@arg('--external', help="""If bc_set the SCM URLs are considered as external and therefore the repositories will be forked to Gerrit
 and the user MUST update the config file with the new values for next runs""")
@arg('--look-up-only', help="""You can do a partial import by a config and specify, which Build Configurations
 should be looked up by name. You can specify multiple sections and separate them by comma (no spaces should be included).
 Example: --look-up-only jdg-infinispan
 Will look up jdg-infinispan section and process a look up of BC by name (jdg-infinispan-${version_field}. 
""")
def make_mead(config=None, run_build=False, environment=1, sufix="", product_name=None, product_version=None, 
              external = False, look_up_only=""):
    """
    Create Build group based on Make-Mead configuration file
    :param config: Make Mead config name
    :return:
    """    
    if validate_input_parameters(config, product_name, product_version) != 0:
        return 1

    try:
        config_reader = ConfigReader(config)
    except NoSectionError as e:
        logging.error('Missing config in %s (%r)', config, e)
        print '-c false'
        return 1
    except Error, err:
        logging.error(err)
        print '-c false'
        return 1

    bc_set = None
    product_version_id = None
    ids = dict()
    (subarts, deps_dict) = config_reader.get_dependency_structure()
    packages = config_reader.get_packages_and_dependencies()
    pprint(packages)
    logging.debug(subarts)
    logging.debug(deps_dict)

    #Lookup product version
    try:
        products_versions = products.list_versions_for_product(name=product_name)
        if not products_versions:
            logging.error('Product does not have any versions')
            return 1
        for product in products_versions:
            if product.version == product_version:
                product_version_id = product.id
    except ValueError:
        logging.error('Product version not found')
        return 1
    
    #Create a list for look-up-only
    look_up_only_list = look_up_only.split(",")

    #Iterate through all sections in configuration file
    for subartifact in subarts:
        art_params = config_reader.get_config(subartifact)
        logging.debug(art_params)
        artifact = art_params['artifact']
        if 'pnc.projectName' in art_params.keys():
            logging.debug("Overriding project name with " + art_params['pnc.projectName'])
            project_name = art_params['pnc.projectName']
        else:
            logging.debug("Using default project name " + artifact)
            project_name = artifact
            
        logging.debug(art_params)
        package = art_params['package']
        version = art_params['version']
        scm_url = art_params['scmURL']
        (scm_repo_url, scm_revision) = scm_url.split("#", 2)
        artifact_name = package + "-" + re.sub("[\-\.]*redhat\-\d+", "", version) + sufix
        target_name = product_name + "-" + product_version + "-all" + sufix

        #Lookup or create Build Configuration Set
        if bc_set is None:
            try:
                bc_set = buildconfigurationsets.get_build_configuration_set(name=target_name)
            except ValueError:
                bc_set = buildconfigurationsets.create_build_configuration_set(name=target_name, product_version_id=product_version_id)
            logging.debug(target_name + ":")
            logging.debug(bc_set.id)

        #Lookup or create a Project
        try:
            project = projects.get_project(name=project_name)        
        except ValueError:
            logging.debug('No project ' + project_name + ". Creating a new one")
            project = projects.create_project(name=project_name)
        logging.debug(artifact_name + ":")
        logging.debug(project.id)

        #Lookup or update or create Build Config
        if subartifact in look_up_only_list:
            build_config = get_build_configuration_by_name(artifact_name)
            if build_config == None:
                pprint("Look up of an existing Build Configuration failed. No build configuration with name " + artifact_name + " found.")
            else:
                buildconfigurationsets.add_build_configuration_to_set(set_id=bc_set.id, config_id=build_config.id)  
        else:
            try:
                build_config = update_build_configuration(environment, product_version_id, art_params, scm_repo_url, 
                                                          scm_revision, artifact_name, project)
            except ValueError:
                logging.debug('No build config with name ' + artifact_name)
                build_config = create_build_configuration(environment, bc_set, product_version_id, art_params, scm_repo_url, 
                                                          scm_revision, artifact_name, project,
                                                          use_external_scm_fields=external)
        if build_config == None:
            return 10
            
        ids[artifact] = build_config
        logging.debug(build_config.id)
        
    #Construct dependency tree of Build Configs
    logging.debug(ids)
    for package, dependencies in packages.iteritems():
        for artifact in dependencies:
            bc_id = ids[package]
            subid = ids[artifact]
            logging.debug(bc_id.id, subid.id)
            buildconfigurations.add_dependency(id=bc_id.id, dependency_id=subid.id)

    #Run build if requested
    if run_build:
        build_record = buildconfigurationsets.build_set(id=bc_set.id)
        pprint(build_record)

    return bc_set

def validate_input_parameters(config, product_name, product_version):
    if config is None:
        logging.error('Config file --config is not specified.')
        return 1

    if product_name is None:
        logging.error('Product Name --product-name is not specified.')
        return 1

    if product_version is None:
        logging.error('Product Version --product-version is not specified.')
        return 1

    if not os.path.isfile(config):
        logging.error('Config file %s not found.', os.path.abspath(config))
        return 1
    
    return 0
    
def get_maven_options(params):
    if 'pnc.buildScript' in params.keys():
        return params['pnc.buildScript']

    result = "mvn clean deploy"

    if 'goals' in params['options'].keys():
        for goal in params['options']['goals']:
            if goal.strip() != "":
                result += ' %s' % goal
    if 'profiles' in params['options'].keys():
        for profile in params['options']['profiles']:
            if profile.strip() != "":
                result += ' -P%s' % profile
    result += ' -DskipTests'
    if 'maven_options' in params['options'].keys():
        for maven_option in params['options']['maven_options']:
            if maven_option == '-pl':
                result += ' %s' % maven_option
            else:
                result += ' \'%s\'' % maven_option

    return result

def get_pme_properties(params):
    not_supported_params = ("strictAlignment", "version.suffix", "overrideTransitive")
    result = ""

    if 'properties' in params['options'].keys():
        for prop in sorted(list(params['options']['properties'].keys())):
            value = params['options']['properties'][prop]
            if prop not in not_supported_params:
                result += ' -D%s=%s' % (prop, value)

    return result 

def get_generic_parameters(params):
    pme_properties = get_pme_properties(params)
    if pme_properties == "":
        return dict()
    else:
        return {'CUSTOM_PME_PARAMETERS': pme_properties}
    
    
def update_build_configuration(environment, product_version_id, art_params, scm_repo_url, scm_revision, artifact_name, project):
    build_config_id = buildconfigurations.get_build_configuration_id_by_name(name=artifact_name)
    buildconfigurations.update_build_configuration(
                                                   id=build_config_id,
                                                   name=artifact_name,
                                                   project=project.id,
                                                   environment=environment, 
                                                   scm_repo_url=scm_repo_url,
                                                   scm_revision=scm_revision,
                                                   build_script=get_maven_options(art_params),
                                                   product_version_id=product_version_id,
                                                   generic_parameters=get_generic_parameters(art_params))
    return buildconfigurations.get_build_configuration(id=build_config_id)


def create_build_configuration(environment_id, bc_set, product_version_id, art_params, scm_repo_url, 
                               scm_revision, artifact_name, project, use_external_scm_fields):
    bpm_task_id = 0
    
    if use_external_scm_fields:
        #Create BPM build config using post /bpm/tasks/start-build-configuration-creation 
        #Set these SCM fields: scmExternalRepoURL and scmExternalRevision
        bpm_task_id = bpmbuildconfigurations.create_build_configuration(name=artifact_name,
                                                 project_id=project.id,
                                                 build_environment_id=environment_id,
                                                 scm_external_repo_url=scm_repo_url,
                                                 scm_external_revision=scm_revision,
                                                 build_script=get_maven_options(art_params),
                                                 product_version_id=product_version_id,
                                                 dependency_ids = [],
                                                 build_configuration_set_ids = [],
                                                 generic_parameters=get_generic_parameters(art_params))
    else:
        #Create BPM build config using post /bpm/tasks/start-build-configuration-creation 
        #Set these SCM fields: scmRepoURL and scmRevision
        #Fields scmExternalRepoURL and scmExternalRevision can be optionally filled too
        bpm_task_id = bpmbuildconfigurations.create_build_configuration(name=artifact_name,
                                                 project_id=project.id,
                                                 build_environment_id=environment_id,
                                                 scm_repo_url=scm_repo_url,
                                                 scm_revision=scm_revision,
                                                 build_script=get_maven_options(art_params),
                                                 product_version_id=product_version_id,
                                                 dependency_ids = [],
                                                 build_configuration_set_ids = [],
                                                 generic_parameters=get_generic_parameters(art_params))


    #Using polling every 30s check this endpoint: get /bpm/tasks/{bpm_task_id} 
    #until eventType is:
    # BCC_CONFIG_SET_ADDITION_ERROR BCC_CREATION_ERROR BCC_REPO_CLONE_ERROR BCC_REPO_CREATION_ERROR -> ERROR -> end with error
    # BCC_CREATION_SUCCESS  -> SUCCESS
    error_event_types = ("BCC_CONFIG_SET_ADDITION_ERROR", "BCC_CREATION_ERROR", "BCC_REPO_CLONE_ERROR", "BCC_REPO_CREATION_ERROR")
    time.sleep(2)
    while True:
        bpm_task = bpmbuildconfigurations.get_bpm_task_by_id(bpm_task_id)
        
        if contains_event_type(bpm_task.content.events, ("BCC_CREATION_SUCCESS", )):
            break
        
        if contains_event_type(bpm_task.content.events, error_event_types):
            pprint("Creation of Build Configuration failed")
            pprint(bpm_task.content)
            return None
        
        pprint("Waiting until Build Configuration " + artifact_name + " is created.")
        time.sleep(10)

    
    #Get BC - GET build-configurations?q='$NAME'
    #Not found-> BC creation failed and the task was garbage collected -> fail
    #Success -> add BC to BCSet and return BC
    build_config = get_build_configuration_by_name(artifact_name)
    if build_config == None:
        pprint("Creation of Build Configuration failed. Unfortunately the details were garbage collected on PNC side.")
        return None        
        
    pprint("Build Configuration " + artifact_name + " is created.")
    #Inform user that he should update the config
    if use_external_scm_fields:
        pprint("!! IMPORTANT !! - ACTION REQUIRED !!")
        pprint("External repository " + scm_repo_url
               + " was forked to internal Git server. YOU MUST TO UPDATE YOUR CONFIG FILE WITH THE NEW VALUE.")
        pprint("New repository URL is: " + build_config.scm_repo_url)
        
    buildconfigurationsets.add_build_configuration_to_set(set_id=bc_set.id, config_id=build_config.id)
    return build_config

    
def contains_event_type(events, types):
    for event in events:
        if(event.event_type in types):   
            return True  

    return False




