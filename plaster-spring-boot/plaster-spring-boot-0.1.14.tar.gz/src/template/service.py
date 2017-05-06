import src.converter.model as model_converter
import src.converter.repository as repo_converter
import src.data.settings as settings
import src.template.template_util as template_util
import src.util.util as util

_template = """package {package};

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

{dependencies}
import {model_package}.{model_class};
import {repo_package}.{repo_class};

@Service
public class {class_name} {{

    private final {repo_class} {repo_var};

    @Autowired
    public {class_name}({repo_class} {repo_var}) {{
        this.{repo_var} = {repo_var};
    }}

    public {model_class} create({model_class} {model_var}) {{
        return this.{repo_var}.save({model_var});
    }}

    public {model_class} read({id.field_type.class_name} {id.name}) {{
        return this.{repo_var}.findOne({id.name});
    }}

    public {model_class} update({model_class} {model_var}) {{
        return this.{repo_var}.save({model_var});
    }}

    public void delete({id.field_type.class_name} {id.name}) {{
        this.{repo_var}.delete({id.name});
    }}

}}

"""


def gen_contents(file_info):
    repo_package = repo_converter.gen_package_name()
    repo_class = repo_converter.gen_class_name(file_info.seed_name)
    model_package = model_converter.gen_package_name()
    model_class = model_converter.gen_class_name(file_info.seed_name)
    dependencies = template_util.gen_dependency_string([settings.ID])

    return template_util.format_template(_template.format(
        package=file_info.package,
        dependencies=dependencies,
        class_name=file_info.class_name,
        model_package=model_package,
        model_class=model_class,
        model_var=util.type_to_var(model_class),
        repo_class=repo_class,
        repo_package=repo_package,
        repo_var=util.type_to_var(repo_class),
        id=settings.ID))
