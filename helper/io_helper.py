"""
IO Helper.
"""

from pathlib import Path


def search_files(target_dir, suffix, writer, ingore_list=[]):

    path = Path(target_dir)

    if not path.exists():
        raise IOError("Not a directory:", target_dir)

    for child in path.iterdir():

        # Ignore pattern
        if child.name in ingore_list:
            continue

        if child.is_file() and child.suffix == suffix:
            writer(str(child))
        elif child.is_dir():
            search_files(child, suffix, writer, ingore_list)


def check_destination(directory):

    path = Path(directory)

    if not path.exists():
        path.mkdir(parents=True)

    return path


def search_and_process(target_dir, suffix, func, ingore_list=[]):

    path = Path(target_dir)

    if not path.exists():
        raise IOError("Not a directory:", target_dir)

    for child in path.iterdir():

        # Ignore pattern
        if child.name in ingore_list:
            continue

        if child.is_file() and child.suffix == suffix:
            func(child)
        elif child.is_dir():
            search_and_process(child, suffix, func, ingore_list)


def save_to_file(filename, output):

    path = Path(filename)

    if not path.parent.exists():
        path.parent.mkdir(parents=True)
        # raise IOError('Parent directory does not exist:', filename)

    with open(filename, "w") as f:
        f.write(output)


if __name__ == "__main__":

    def test_func(filename):
        print(filename)

    search_and_process(".", ".py", test_func)

    # save_to_file('/some/fake/path/name.txt', {})
    save_to_file("./name.txt", {})
