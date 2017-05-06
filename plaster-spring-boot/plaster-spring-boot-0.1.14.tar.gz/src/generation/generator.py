import src.data.types as gen_types
import src.template.controller as controller_file_gen
import src.template.model.model as model_file_gen
import src.template.repository as repo_file_gen
import src.template.service as service_file_gen
from src.domain.file_information import FileInformation
from src.util.util import *

_template_map = {
    gen_types.MODEL: model_file_gen,
    gen_types.REPOSITORY: repo_file_gen,
    gen_types.SERVICE: service_file_gen,
    gen_types.CONTROLLER: controller_file_gen,
}


def generate_file(file_info):
    template = _template_map[file_info.file_type]

    file_contents = template.gen_contents(file_info)
    create_file(file_info.file_path, file_info.file_name, file_contents)


def perform(gen_type, gen_name, fields):
    generations = gen_types.fetch_related_types(gen_type)

    if not (gen_name and gen_type):
        return "Missing required argument"
    if not generations:
        return "Unknown generation type :", gen_type

    files_to_generate = [FileInformation(gen_name, fields, elem) for elem in generations]
    for file_to_generate in files_to_generate:
        generate_file(file_to_generate)
