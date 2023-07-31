import texttable
import itertools
from datetime import timedelta
import os


class TimeTable:
    def __init__(self, days: dict, projects: dict) -> None:
        self.days: dict = days
        self.projects: dict = projects

        self.days_set = set()
        self.days_set.update(days.keys())
        self.days_set = sorted(self.days_set)

        self.projects_set = set()
        self.projects_set.update(projects.keys())
        self.projects_set = sorted(self.projects_set)

    def print(self):
        tsize = os.get_terminal_size()

        for key, group in itertools.groupby(
            self.days_set, key=lambda e: (e.year, e.month)
        ):
            table = texttable.Texttable(tsize.columns)
            group = list(group)
            header = [key]
            align = ["l"]
            for d in group:
                header.append(f"{d.day:3d}")
                align.append("r")
            header.append("Sum")
            align.append("r")
            table.header(header)
            table.set_cols_align(align)

            for p in sorted(self.projects_set):
                line = [p]
                s = 0
                for d in group:
                    t = int(
                        self.days[d].get(p, timedelta(0)) / self.days[d]["Sum"] * 100
                    )
                    s += t
                    line.append(t)
                line.append(s)
                if s > 0:
                    table.add_row(line)
            print()
            print()
            print(table.draw())
