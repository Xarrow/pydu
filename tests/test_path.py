import os
import pytest
from pydu.platform import WINDOWS
from pydu.path import cd, is_super_path, normjoin, filename, fileext
from pydu.path import FileNameAndPath


def test_cd(tmpdir):
    path = str(tmpdir)
    cwd = os.getcwd()
    with cd(path):
        assert os.getcwd() == path
    assert os.getcwd() == cwd


class TestIsSupoerPath:
    def test_is_super_path_general(self):
        assert is_super_path('/aa/bb/cc', '/aa/bb/cc')
        assert is_super_path('/aa/bb', '/aa/bb/cc')
        assert is_super_path('/aa', '/aa/bb/cc')
        assert is_super_path('/', '/aa/bb/cc')
        assert is_super_path('/', '/')
        assert not is_super_path('/a', '/aa/bb/cc')

    @pytest.mark.skipif(not WINDOWS, reason='Not support on none-windows')
    def test_is_super_path_win(self):
        assert is_super_path('c:/aa/bb', 'c:/aa/bb\\cc')
        assert is_super_path('c:/aa/bb', 'c:/aa\\bb/cc')
        assert is_super_path('c:/aa\\bb', 'c:\\aa/bb/cc')
        assert is_super_path('c:/', 'c:\\')


def test_normjoin():
    if WINDOWS:
        assert normjoin('C:\\', 'b') == 'C:\\b'
        assert normjoin('C:\\', '\\b') == 'C:\\b'
        assert normjoin('C:\\a', '\\b') == 'C:\\b'
        assert normjoin('C:\\a', '..\\b') == 'C:\\b'
    else:
        assert normjoin('/a', 'b') == '/a/b'
        assert normjoin('/a', '/b') == '/b'
        assert normjoin('/a', '../b') == '/b'


def test_filename():
    assert filename('/foo/bar') == 'bar'
    assert filename('/foo/bar.ext') == 'bar'
    assert filename('/foo/bar.more.ext') == 'bar.more'


def test_fileext():
    assert fileext('/foo/bar') == ''
    assert fileext('/foo/bar.ext') == '.ext'
    assert fileext('/foo/bar.more.ext') == '.ext'

def test_FileNameAndPath():
    fnap = FileNameAndPath(file_path_and_name="C:\\foo\\bar.txt")
    assert fnap.path == 'C:\\foo\\bar.txt'
    assert fnap.raw_file_path_and_name == 'C:\\foo\\bar.txt'
    assert fnap.exists == False
    assert fnap.file_name_tuple ==('bar','.txt')
    assert fnap.file_name == 'bar.txt'
    assert fnap.only_path == 'C:\\foo\\'
    assert fnap.only_name =='bar'
    assert fnap.only_suffix == '.txt'

    fnap2 = FileNameAndPath(file_path_and_name="/User/foo/bar.txt")
    assert fnap2.raw_file_path_and_name == '/User/foo/bar.txt'
    assert fnap2.path == '/User/foo/bar.txt'
    assert fnap2.exists == False
    assert fnap2.file_name_tuple ==('bar','.txt')
    assert fnap2.file_name == 'bar.txt'
    assert fnap2.only_path == '/User/foo/'
    assert fnap2.only_name =='bar'
    assert fnap2.only_suffix == '.txt'

