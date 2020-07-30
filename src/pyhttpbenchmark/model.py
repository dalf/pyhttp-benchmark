import typing
import pathlib
from collections import OrderedDict
from . import cases


class ServerConfig(typing.NamedTuple):
    caddy_path: pathlib.Path
    caddy_log_path: pathlib.Path


class SslConfig(typing.NamedTuple):
    local_ca_file: pathlib.Path


class Config(typing.NamedTuple):
    record_csv: bool
    record_profile: bool
    tries: int


class LoadedCase(typing.NamedTuple):
    name: str
    path: pathlib.Path

    @property
    def prof_filename(self) -> pathlib.Path:
        return pathlib.Path(f"{self.name}.prof")

    @property
    def package_name(self) -> str:
        return cases.__package__ + '.' + self.name


class Step:
    pass


class StepDelay(Step, typing.NamedTuple):
    time: int


class StepRequests(Step, typing.NamedTuple):
    urls: typing.List[str]


class StepRequest(Step, typing.NamedTuple):
    url: str


class Scenario(typing.NamedTuple):
    id: str
    name: str
    tries: int
    local_ca: typing.Union[str, bool]
    steps: typing.List[Step]


class ScenariosDict(OrderedDict):
    def __iadd__(self, scenario: Scenario):
        self[scenario.id] = scenario
        return self

    def subset(self, ids: typing.List[str]):
        return ScenariosDict((id, self[id]) for id in ids)
