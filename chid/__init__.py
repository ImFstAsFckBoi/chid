from chid.utils import git_get_field, git_set_field
from typing import Literal, Dict, Callable
from chid.utils import print_err
from argparse import ArgumentParser
from chid.profile import (
    get_current_profile,
    get_all_profiles,
    get_profile,
    Profile,
)

def check_managed() -> bool:
    return git_get_field("chid.meta.managed") == ('yes', 0)

def setup() -> int:
    git_set_field("chid.meta.current", '')

    pname = input('Name your current profile: ').strip()
    email, r1 = git_get_field('user.email')
    name, r2 = git_get_field('user.name')

    assert not (r1 or r2)
    if create("--profile", pname, "--email", email, "--name", name):
        return 1
    if switch(pname):
        return 1
    
    git_set_field("chid.meta.managed", 'yes')
    return 0

def phelp(*args: str):
    print(" === CHID PROFILE MANAGER === ")
    print()
    print("Commands: ")
    print("  help             | show this message")
    print("  show <profile>   | show profile info")
    print("  list             | show all profiles")
    print("  whoami           | show current profile")
    print("  create           | add profile")
    print("  switch <profile> | switch current profile")
    print("  current          | show just current profile name")

def whoami(*args: str):
    p = get_current_profile()
    print(f"'{p.PROFILE_NAME}', {p.desc}")
    print(f"{p.name} <{p.email}>")

def plist(*args: str):
    cur = get_current_profile()
    profiles = get_all_profiles()
    padding = max([len(p.PROFILE_NAME) for p in profiles])
    for p in sorted(get_all_profiles(), key=lambda p: len(p.PROFILE_NAME)):
        name = p.PROFILE_NAME
        if len(name) > 19:
            name = name[:16] + "..."

        mark = "*" if p.PROFILE_NAME == cur.PROFILE_NAME else " "
        print(f" {mark} {name:<{padding}} | {p.desc}")

def current(*args: str):
    p = get_current_profile()
    print(p.PROFILE_NAME)

def create(*args: str):
    fields = ("profile", "email", "name", "desc")

    parser = ArgumentParser("chid create")
    for f in fields:
        parser.add_argument(f"--{f}", required=False)
    v = vars(parser.parse_args(args))

    for f in fields:
        if v[f] is None:
            v[f] = input(f"Enter {f}: ")
        else:
            print(f"{f} = {v[f]}")
    print()

    prof = Profile(v["profile"], v["email"], v["name"], v["desc"])

    if prof.PROFILE_NAME in [p.PROFILE_NAME for p in get_all_profiles()]:
        print_err("Profile already exists, aborting!")
        return

    prof.write()

    if prof.PROFILE_NAME in [p.PROFILE_NAME for p in get_all_profiles()]:
        print(f"Successfully create profile '{prof.PROFILE_NAME}'!")
    else:
        print_err(f"Creating profile '{prof.PROFILE_NAME}' failed!")

def switch(*args: str):
    if len(args) < 1:
        print_err(
            "No profile specified!\nUsage: chid switch <profile>",
        )
        return 1

    new_p_name = args[0]

    cur = get_current_profile()
    if cur.PROFILE_NAME == new_p_name:
        print_err(f"Profile '{new_p_name}' is already in use!")
        return 1

    profiles = get_all_profiles()
    if new_p_name not in [p.PROFILE_NAME for p in profiles]:
        print_err(
            f"Not profile named '{new_p_name}'!\n"
            "See available profiles with 'profile list'"
        )
        return 1

    new_p = [p for p in profiles if p.PROFILE_NAME == new_p_name]
    assert len(new_p) == 1
    new_p = new_p[0]

    git_set_field("user.name", new_p.name)
    git_set_field("user.email", new_p.email)
    git_set_field("chid.meta.current", new_p.PROFILE_NAME)

    cur = get_current_profile()
    if cur.PROFILE_NAME != new_p_name:
        print_err("Something went wrong!")
    
    print(f"Successfully switch to '{new_p_name}'")

def show(*args: str):
        if len(args) < 1:
            print_err(
                "No profile specified!\nUsage: chid show <profile>",
            )
            return 1
        p_name = args[0]
        
        p = get_profile(p_name)
        l1 = f"Profile: '{p.PROFILE_NAME}', {p.desc}"
        l2 = f"Name:    {p.name}"
        l3 = f"Email:   {p.email}"
        
        print(l1)
        print('-' * len(l1))
        print(f"{l2}\n{l3}")


Commands = Literal['', 'help', 'whoami', 'list', 'current', 'create', 'switch', 'show'] | str

__commands: Dict[Commands, Callable[[], None | int]] = {
    '': phelp,
    'help': phelp,
    'show': show,
    'list': plist,
    'whoami': whoami,
    'create': create,
    'switch': switch,
    'current': current,
}


def main(command: Commands, *args: str):
    if not check_managed():
        print_err("Not managed!")
        i = input("Run setup? [Y/n] ")
        while True:
            if i in ('', 'y', 'Y'):
                return setup()
            elif i in('n', 'N'):
                return 1

    cmd = __commands.get(command, None)

    if cmd is None:
        print_err(f"No commands named '{command}'")
        return 1

    return cmd(*args)