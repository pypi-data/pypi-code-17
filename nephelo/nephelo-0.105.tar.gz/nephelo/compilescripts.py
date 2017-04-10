import network as Network
import json
import os
import sys
import boto3
import re

accepted_config_keys = ["region", "cidr_prefix", "region_prefix", "subnet", "stage"]


def compilePath(libpath, path, config, stage, references):
    replacementdict = {
        "stage": stage
    }
    for key in config:
        if key in accepted_config_keys:
            replacementdict[key] = config[key]
    files = []
    print path
    for step in os.walk(path):
        print step
        dirpath = step[0]
        if dirpath != "/":
            dirpath += "/"
        for filename in step[2]:
            files.append(dirpath + filename)
    files = filter(lambda x: ".json" in x, files)
    jsonobjects = []
    for filepath in files:
        try:
            jsonobjects.append(loadfile(libpath, filepath, replacementdict, references))
        except Exception as e:
            print e
    compiledresources = {}
    for jsonobject in jsonobjects:
        for key in jsonobject:
            compiledresources[key] = jsonobject[key]
    return compiledresources


def loadfile(libpath, path, replacementdict, reference_dict):
    try:
        filestring = open(path).read()
        # print filestring
        filename = path.split("/")[-1]
        for key in replacementdict:
            if key not in accepted_config_keys:
                continue
            # find the iterators
            iterator_start = "%{"
            iterator_end = "}%"
            # print "Regex"
            # print iterator_start + '(.*?)' + iterator_end
            iterators = re.findall(iterator_start + '(.*?)' + iterator_end, filestring, re.DOTALL)
            # print iterators
            for iterator in iterators:
                # what are we iterating and what is the local variable?
                # print "THIS HERE"
                iteration_object = iterator.split(" as ")[0].replace(" ", "")
                # print iteration_object
                iteration_name = iterator.split(" as ")[1].split("|,")[0].replace("|", "").replace(" ", "")
                iteration_template = iterator.split(" as ")[1].split("|,")[1]
                # print iteration_template
                if iteration_object in replacementdict or iteration_object in reference_dict:
                    iteration_list = reference_dict[iteration_object] if iteration_object in reference_dict else replacementdict[iteration_object]
                    # print iteration_list
                    if isinstance(iteration_list, (list, tuple)):
                        results = []
                        for item in iteration_list:
                            replacestring = "${" + iteration_name + "}"
                            replacevalue = item if isinstance(item, str) else str(item)
                            iteration_result = iteration_template.replace(replacestring, replacevalue)
                            replacestring = "@{" + iteration_name + "}"
                            replacevalue = item if isinstance(item, str) else str(item)
                            iteration_result = iteration_result.replace(replacestring, "{\"Ref\": \"" + replacevalue + "\"}")
                            results.append(iteration_result)
                        resultstring = "".join(results)
                        # print resultstring
                        filestring = filestring.replace(iterator_start + iterator + iterator_end, resultstring)
                    else:
                        filestring = filestring.replace(iterator_start + iterator + iterator_end, "")
                else:
                    filestring = filestring.replace(iterator_start + iterator + iterator_end, "")


            filestring = filestring.replace("${" + key + "}", replacementdict[key])
            if 'subnet-ids' in reference_dict:
                subnet_ids = map(lambda x: json.loads(x), reference_dict["subnet-ids"])
                filestring = filestring.replace("!{subnets}", json.dumps(subnet_ids))
                for index in range(len(reference_dict['subnet-ids'])):
                    filestring = filestring.replace("!{subnets[" + str(index) + "]}", reference_dict["subnet-ids"][index])
            env_start = "@@{"
            env_end = "}@@"
            env_var_refs = re.findall(env_start + '(.*?)' + env_end, filestring, re.DOTALL)
            print env_var_refs
            for env_ref in env_var_refs:
                replacement_value = os.environ.get(env_ref, "")
                filestring = filestring.replace(env_start + env_ref + env_end, replacement_value)
            start = "@{"
            end = "}"
            # print "Reference Regex"
            # print start + '(.*?)' + end
            references = re.findall(start + '(.*?)' + end, filestring, re.DOTALL)
            # print references
            for reference in references:
                if reference in reference_dict:
                    filestring = filestring.replace("@{" + reference + "}", "{ \"Ref\":\"" + reference_dict.get(reference) + "\"}")
                else:
                    filestring = filestring.replace("@{" + reference + "}", "{ \"Ref\":\"" + reference + "\"}")

        return json.loads(filestring)
    except Exception as e:
        print filestring
        print reference_dict
        print e
    return {}


def deCamel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1\2', s1).lower()