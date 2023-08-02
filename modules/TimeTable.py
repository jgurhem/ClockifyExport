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

        self.tables: dict = dict()

        for key, group in itertools.groupby(
            self.days_set, key=lambda e: (e.year, e.month)
        ):
            group = list(group)
            header = [key]
            for d in group:
                header.append(f"{d.day:3d}")
            header.append("Sum")

            lines = [header]
            self.tables[key] = lines
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
                # starts from 1 to ignore header
                for j in range(1, len(lines)):
                    if lines[j][i] > 0:
                        count += 1
                        indexes.append(j)
                for j in random.sample(indexes, 100 - total[i]):
                    lines[j][i] += 1
                    lines[j][len(group) + 1] += 1

    def print(self):
        for lines in self.tables.values():
            table = Table()
            table.add_header(lines[0])
            table.set_cols_align(["l"] + ["r"] * (len(lines[0]) - 1))
            for l in lines[1:]:
                table.add_row(l)
            print()
            print()
            print(table.draw())

    def __compute_total__(self, lines, days, name):
        total = [name]
        for i in range(1, days + 2):
            total.append(0)
            for j in range(1, len(lines)):
                total[i] += lines[j][i]
        return total
