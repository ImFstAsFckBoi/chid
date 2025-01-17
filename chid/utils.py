from typing import Tuple
from colorama import Fore
from subprocess import Popen, PIPE


def print_err(txt: str):
    _txt = txt.replace("\n", "\n      ")
    print(f"[{Fore.RED}ERR{Fore.RESET}] {_txt}")


def shell(cmd: str) -> Tuple[int, str]:
    p = Popen(cmd, shell=True, stdout=PIPE)
    return p.wait(), p.communicate()[0].decode()


def git_get_field(field: str) -> Tuple[str, int]:
    cmd = f"git config --global {field}"
    res, out = shell(cmd)
    return out.strip(), res


def git_get_matching_fields(regex: str) -> Tuple[str, int]:
    cmd = f"git config --global -l | grep -E '{regex}'"
    res, out = shell(cmd)
    return out, res


def git_set_field(field: str, value: str) -> Tuple[str, int]:
    cmd = f"git config --global {field} '{value}'"
    res, out = shell(cmd)
    return out, res

