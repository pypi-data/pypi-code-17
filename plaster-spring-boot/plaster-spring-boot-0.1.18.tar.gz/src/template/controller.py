import src.converter.controller as controller_converter
import src.converter.model as model_converter
import src.converter.service as service_converter
import src.data.settings as settings
import src.template.template_util as template_util
import src.util.util as util

_template = """package {package};

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

{dependencies}
import {service_package}.{service_class};
import {model_package}.{model_class};

@RestController
@RequestMapping("/{base_route}")
public class {class_name} {{

    private final {service_class} {service_var};

    @Autowired
    public {class_name} ({service_class} {service_var}) {{
        this.{service_var} = {service_var};
    }}

    @RequestMapping(value = "/", method = RequestMethod.POST)
    public {model_class} create(@RequestBody {model_class} {model_var}) {{
        return this.{service_var}.create({model_var});
    }}

    @RequestMapping(value = "/{{{id.name}}}", method = RequestMethod.GET)
    public {model_class} read(@PathVariable {id.field_type.class_name} {id.name}) {{
        return this.{service_var}.read({id.name});
    }}

    @RequestMapping(value = "/{{{id.name}}}", method = RequestMethod.PUT)
    public {model_class} update(@PathVariable {id.field_type.class_name} {id.name}, @RequestBody {model_class} {model_var}) {{
        return this.{service_var}.update({model_var});
    }}

    @RequestMapping(value = "/{{{id.name}}}", method = RequestMethod.DELETE)
    public void delete(@PathVariable {id.field_type.class_name} {id.name}) {{
        this.{service_var}.delete({id.name});
    }}

}}

"""


def gen_contents(file_info):
    service_package = service_converter.gen_package_name()
    service_class = service_converter.gen_class_name(file_info.seed_name)
    model_package = model_converter.gen_package_name()
    model_class = model_converter.gen_class_name(file_info.seed_name)
    dependencies = template_util.gen_dependency_string([settings.ID])

    return template_util.format_template(_template.format(
        base_route=util.type_to_snake_case(controller_converter.gen_root_name(file_info.seed_name)),
        package=file_info.package,
        class_name=file_info.class_name,
        model_package=model_package,
        model_class=model_class,
        model_var=util.type_to_var(model_class),
        service_package=service_package,
        service_class=service_class,
        service_var=util.type_to_var(service_class),
        dependencies=dependencies,
        id=settings.ID))
