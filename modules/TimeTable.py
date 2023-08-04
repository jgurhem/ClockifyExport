import itertools
from datetime import timedelta
from .Table import Table
import random
import os.path
import csv
import json


class TimeTable:
    def __init__(self, days: dict) -> None:
        self.days: dict = days

        self.days_set = set()
        self.days_set.update(days.keys())
        self.days_set = sorted(self.days_set)

        self.projects_set = set()
        for v in days.values():
            self.projects_set.update(v.keys())
        self.projects_set.remove("Sum")
        self.projects_set = sorted(self.projects_set)

        random.seed(1)

        self.tables: dict = dict()

        for key, group in itertools.groupby(
            self.days_set, key=lambda e: (e.year, e.month)
        ):
            group = list(group)
            header = [key]
            for d in group:
                header.append(d.day)
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

            size_col_first=0
            size_col_sum=0
            for l in lines:
                size_col_first = max(size_col_first, len(str(l[0])))
                size_col_sum = max(size_col_sum, len(str(l[len(lines[0]) - 1])))
            table.set_cols_width([size_col_first] + [3] * (len(lines[0]) - 2) + [size_col_sum])

            for l in lines[1:]:
                table.add_row(l)
            print()
            print()
            print(table.draw())

    def export_csv(self, export_dir="./exports", renames={}):
        TimeTable.__validate_export_dir(export_dir)
        for key, lines in self.tables.items():
            name = str(key)
            if type(key) is tuple:
                name = "_".join([str(k) for k in key])
            with open(f"{export_dir}/{name}.csv", "w") as f:
                writer = csv.writer(f)
                for l in lines:
                    writer.writerow([renames.get(l[0], l[0])] + l[1:])

    def export_json(self, export_dir="./exports"):
        TimeTable.__validate_export_dir(export_dir)
        with open(f"{export_dir}/export.json", "w") as f:
            json.dump(dict([(str(k), v) for k, v in self.tables.items()]), f, indent=2)

    def __validate_export_dir(export_dir):
        if os.path.isdir(export_dir):
            pass
        else:
            os.makedirs(export_dir, exist_ok=True)
        if os.path.exists(export_dir) and not os.path.isdir(export_dir):
            raise Exception(f"{export_dir} already exists and is not a directory")

    def __compute_total__(self, lines, days, name):
        total = [name]
        for i in range(1, days + 2):
            total.append(0)
            for j in range(1, len(lines)):
                total[i] += lines[j][i]
        return total
