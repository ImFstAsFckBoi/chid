from dataclasses import dataclass, field
from chid.utils import (
    git_get_matching_fields,
    git_set_field,
    git_get_field,
)

@dataclass
class Profile:
    PROFILE_NAME: str
    email: str
    name: str
    desc: str = field(default_factory=str)

    def write(self):
        git_set_field(f"chid.profile.{self.PROFILE_NAME}.email", self.email)
        git_set_field(f"chid.profile.{self.PROFILE_NAME}.name ", self.name)
        git_set_field(f"chid.profile.{self.PROFILE_NAME}.desc ", self.desc)


def get_current_profile() -> Profile:
    current, _ = git_get_field("chid.meta.current")
    output, _ = git_get_matching_fields(rf"chid\.profile\.{current.strip()}")
    
    fields = {}
    for line in output.splitlines():
        k, v = line.split("=", 1)
        split_k = k.split(".")
        fields[split_k[-1]] = v

    return Profile(current, **fields)

def get_profile(profile_name: str) -> Profile:
    output, _ = git_get_matching_fields(rf"chid\.profile\.{profile_name}")
    
    fields = {}
    for line in output.splitlines():
        k, v = line.split("=", 1)
        split_k = k.split(".")
        fields[split_k[-1]] = v

    return Profile(profile_name, **fields)

def get_all_profiles() -> list[Profile]:
    output, _ = git_get_matching_fields(r"chid\.profile\.[^.]*")
    lines = output.splitlines()
    profile_fields: dict[str, dict[str, str]] = {}

    for line in lines:
        k, v = line.split("=", 1)
        split_k = k.split(".")
        p = split_k[2]

        if p not in profile_fields:
            profile_fields[p] = {}

        profile_fields[p][split_k[-1]] = v

    return [Profile(n, **v) for n, v in profile_fields.items()]
