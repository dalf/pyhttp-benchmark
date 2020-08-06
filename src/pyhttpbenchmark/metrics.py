import typing
import statistics
import pstats
from . import model, output


class Measure(typing.NamedTuple):
    runtime: float
    cputime: float


class Metrics:

    __slots__ = "values",

    def __init__(self):
        self.values = dict()

    def add(self, case: model.LoadedCase, measure: Measure) -> None:
        stat = self.values.setdefault(case, list())
        stat.append((measure.runtime, measure.cputime))

    def save(self, scenario: model.Scenario) -> None:
        with open(output.get_csv_file(scenario), "w", encoding="utf-8") as f:
            f.write("case;runtime;cputime\n")
            for case, stat in self.values.items():
                for measure in stat:
                    f.write("%s, %.2f, %.2f\n" % (case.full_name, measure[0], measure[1]))

    def save_png(self, scenario: model.Scenario) -> None:
        from . import graph
        graph.save(self, scenario)

    def print(self) -> None:
        """
        Print the statistics recorded by report_time and async_report_time

        Run in the main process
        """
        case_name_length = max(map(lambda case: len(case.name), self.values.keys()))
        # at least 32 characters
        case_name_length = max(32, case_name_length)

        print(f"| {' ' * case_name_length} | Runtime |         |         | Cputime |         |         |")  # noqa
        print(f"|-{'-' * case_name_length}-|---------|---------|---------|---------|---------|---------|")  # noqa
        print(f"| {' ' * case_name_length} |  median |    mean |   stdev |  median |    mean |   stdev |")  # noqa
        for case, stat in self.values.items():
            runtime = list(map(lambda s: s[0], stat))
            cputime = list(map(lambda s: s[1], stat))

            runtime_median = statistics.median(runtime)
            runtime_mean = statistics.mean(runtime)
            runtime_stdev = statistics.stdev(runtime)

            cputime_median = statistics.median(cputime)
            cputime_mean = statistics.mean(cputime)
            cputime_stdev = statistics.stdev(cputime)
            print(
                f"| %-{case_name_length}s | %7.2f | %7.2f | %7.2f | %7.2f | %7.2f | %7.2f |"
                % (case.full_name,
                   runtime_median, runtime_mean, runtime_stdev,
                   cputime_median, cputime_mean, cputime_stdev,)
            )
        print("\n")


class Stats:

    __slots__ = "values",

    def __init__(self):
        self.values = dict()

    def add(self, case: model.LoadedCase, stat: typing.Optional[pstats.Stats]) -> None:
        if stat:
            stat_for_case = self.values.setdefault(case, pstats.Stats())
            stat_for_case.add(stat)

    def save(self, scenario: model.Scenario):
        for case, stat in self.values.items():
            stat.dump_stats(output.get_prof_file(scenario, case))
