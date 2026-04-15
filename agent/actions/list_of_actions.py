from .hello import hello
from .create_file import create_file
from .welcom import welcom
from .delete_file import delete_file
from .writein_file import writein_file
from .deletein_file import deletein_file


LIST_OF_ACTIONS = {
    "create_file": create_file,
    "hello": hello,
    "welcom": welcom,
    "delete_file": delete_file,
    "writein_file": writein_file,
    "deletein_file": deletein_file
}