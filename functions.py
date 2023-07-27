import os
import shutil


def test_function(test_parameter):
    print(f"you wrote: {test_parameter}")

def clear_dir_only_if_exists(directory_to_remove, directory_name):
    if os.path.exists(directory_to_remove) is True:
        shutil.rmtree(directory_to_remove)
        os.mkdir(directory_to_remove)
        print(f"contents of the folder .\\{directory_name} deleted successfully\n")
    else:
        print(f"the folder .\\{directory_name} does not exist anymore. "
              "Creating it and continuing.\n")
        os.mkdir(directory_to_remove)
