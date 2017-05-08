import src.data.types as gen_types
import src.template.model.model as class_under_test
from src.domain.file_information import FileInformation


def test_insert_dependencies():
    example_file = open("../../resources/JavaExample.java")
    file_info = FileInformation("Example", ["something:date", "else:int"], gen_types.MODEL)

    class_under_test.insert_dependencies(example_file, file_info)

    return 1


if __name__ == '__main__':
    test_insert_dependencies()
