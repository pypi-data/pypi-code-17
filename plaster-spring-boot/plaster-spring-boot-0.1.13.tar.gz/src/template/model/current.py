TEMPLATE = '''package {package};

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

{dependencies}

{header}
@Entity
public class {class_name} {{

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private {id.field_type.class_name} {id.name};
    {body}
}}

'''
