import itertools
from datetime import timedelta
from .Table import Table
import random


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
        random.seed(1)

    def print(self):
        for key, group in itertools.groupby(
            self.days_set, key=lambda e: (e.year, e.month)
        ):
            table = Table()
            group = list(group)
            header = [key]
            align = ["l"]
            for d in group:
                header.append(f"{d.day:3d}")
                align.append("r")
            header.append("Sum")
            align.append("r")
            table.add_header(header)
            table.set_cols_align(align)

            lines = []
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
                    lines.append(line)

            total = self.__compute_total__(lines, len(group), "Total (debug)")

            # randomly adjust values so that total per column is 100
            for i in range(1, len(group) + 1):
                if total[i] == 100:
                    continue
                count = 0
                indexes = list()
                for j in range(len(lines)):
                    if lines[j][i] > 0:
                        count += 1
                        indexes.append(j)
                for j in random.sample(indexes, 100 - total[i]):
                    lines[j][i] += 1
                    lines[j][len(group) + 1] += 1

            for l in lines:
                table.add_row(l)
            print()
            print()
            print(table.draw())

    def __compute_total__(self, lines, days, name):
        total = [name]
        for i in range(1, days + 2):
            total.append(0)
            for j in range(len(lines)):
                total[i] += lines[j][i]
        return total
