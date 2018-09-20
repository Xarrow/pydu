import os
from contextlib import contextmanager
from .platform import WINDOWS, LINUX


@contextmanager
def cd(path):
    """
    Context manager for cd the given path.
    """
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)


def is_super_path(path1, path2):
    """
    Whether `path1` is the super path of `path2`.
    Note that if `path1` is same as `path2`, it's also regarded as
    the super path os `path2`.
    For instance "/", "/opt" and "/opt/test" are all the super paths of "/opt/test",
    while "/opt/t" is the super path of "/opt/test".
    """
    path1 = os.path.normpath(path1)
    current_path2 = os.path.normpath(path2)
    parent_path2 = os.path.dirname(current_path2)
    if path1 == current_path2:
        return True

    while parent_path2 != current_path2:
        if path1 == parent_path2:
            return True
        current_path2 = parent_path2
        parent_path2 = os.path.dirname(parent_path2)

    return False


def normjoin(path, *paths):
    """Join one or more path components intelligently and normalize it."""
    return os.path.normpath(os.path.join(path, *paths))


def filename(path):
    """Return the filename without extension."""
    return os.path.splitext(os.path.basename(path))[0]


def fileext(path):
    """
    Return the file extension.
    If file has not extension, return empty string.
    """
    return os.path.splitext(os.path.basename(path))[1]


WINDOWS_FILE_PATH_SEP = "\\"

LINUX_FILE_PATH_SEP = "/"


class FileNameAndPath(object):
    """
    FileNameAndPath provider multiple properties
     which include  `raw_file_name`,`path`,`exists`,`file_name_tuple`,
     `file_name`,`only_suffix`,`only_name` and `only path`

    parse properties of  file path  more convenient
    """
    def __init__(self, file_path_and_name):
        self.file_path_and_name = file_path_and_name

    @property
    def raw_file_path_and_name(self):
        """property of `raw_file_path_and_name`"""
        return self.file_path_and_name

    @property
    def path(self):
        """property of `path`"""
        ret_join_path = ""

        if WINDOWS:
            for single_item in self.file_path_and_name.split(WINDOWS_FILE_PATH_SEP):
                if single_item.__contains__(":"):
                    ret_join_path = os.path.join(ret_join_path, single_item, WINDOWS_FILE_PATH_SEP)
                else:
                    ret_join_path = os.path.join(ret_join_path, single_item)
            return ret_join_path

        else:
            # Not Windows , default linux file path sep
            for single_item in self.file_path_and_name.split(LINUX_FILE_PATH_SEP):
                ret_join_path = os.path.join(ret_join_path, single_item)
            return ret_join_path


    @property
    def exists(self):
        """ property of  `exists` , check file whether  exists"""
        return os.path.exists(self.path)

    @property
    def file_name_tuple(self):
        """ property of  `file_name_tuple`  , show name tuple include file name and file suffix ,
         sample as ("a",".txt")"""
        return os.path.splitext(os.path.basename(self.path))

    @property
    def file_name(self):
        """ property of `file_name` , show file name string include file name and file suffix ,sample as `a.txt` """
        return "".join(self.file_name_tuple)

    @property
    def only_suffix(self):
        """ property of  `only_suffix` , only show file suffix if file has specific suffix else show `None`
            sample as `.txt`
        """
        if not self.raw_file_path_and_name.__contains__("."):
            return None
        return self.file_name_tuple[1]

    @property
    def only_name(self):
        """ property of  `only_name`  , only show file name exclude path , sample as `a` """
        return self.file_name_tuple[0]

    @property
    def only_path(self):
        """ property of  `only_path`  , only show file path exclude file name"""
        return self.file_path_and_name.replace(self.file_name, "")

if __name__ == '__main__':
    fnas = FileNameAndPath(file_path_and_name="/User/foo/bar.txt")
    print(fnas)