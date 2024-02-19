import itertools
from datetime import datetime, timedelta, date

from modules.TaskTime import TaskTime

from .Table import Table
import random
import os.path
import csv
import json

class TimeTable:
    def __init__(self, day: list[TaskTime], ptday: list[TaskTime]) -> None:
        self.projects_set: set[str] = set()
        for e in ptday:
            self.projects_set.add(e.getFullName())
        self.day: dict[date, timedelta] = dict()
        for el in day:
            self.day[el.date] = el.duration

        random.seed(1)

        self.tables: dict = dict()

        for key, group in itertools.groupby(
            ptday, key=lambda e: (e.date.year, e.date.month)
        ):
            group = list(group)
            days: set[int] = set()
            pos_days: dict[int, int] = dict()
            # create association between date and its position in the array
            for el in group:
                days.add(el.date.day)
            i = 0
            for el in days:
                pos_days[el] = i
                i = i + 1

            header = [key]
            header.extend(sorted(days))
            header.append("Sum")
            lines = [header]
            self.tables[key] = lines
            # create empty table and association between project and its
            # position in the rows of the table
            pos_project: dict[str, int] = dict()
            i = 0
            for p in sorted(self.projects_set):
                lines.append([p] + [0] * (len(days) + 1))
                pos_project[p] = i
                i = i + 1

            # add values into the table
            for el in group:
                p = el.getFullName()
                lines[pos_project[p] + 1][pos_days[el.date.day] + 1] += el.duration

            # compute percentage between projects and total values each day
            for i in range(1, len(days) + 1):
                for j in range(1, len(lines)):
                    if lines[j][i] > 0:
                        lines[j][i] = int(lines[j][i] / self.day[datetime(key[0], key[1], lines[0][i]).date()] * 100)

            # compute total for each row
            for i in range(1, len(days) + 1):
                for j in range(1, len(lines)):
                    if lines[j][i] > 0:
                        lines[j][len(days) + 1] += lines[j][i]

            # remove empty lines
            newlines=[header]
            for j in range(1, len(lines)):
                if lines[j][len(days) + 1] > 0:
                    newlines.append(lines[j])
            lines = newlines
            self.tables[key] = newlines

            total = self.__compute_total__(lines, len(days), "Total (debug)")

            # randomly adjust values so that total per column is 100
            for i in range(1, len(days) + 1):
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
                    lines[j][len(days) + 1] += 1

    def print(self):
        for lines in self.tables.values():
            table = Table()
            table.add_header(lines[0])
            table.set_cols_align(["l"] + ["r"] * (len(lines[0]) - 1))

            size_col_first = 0
            size_col_sum = 0
            for l in lines:
                size_col_first = max(size_col_first, len(str(l[0])))
                size_col_sum = max(size_col_sum, len(str(l[len(lines[0]) - 1])))
            table.set_cols_width(
                [size_col_first] + [3] * (len(lines[0]) - 2) + [size_col_sum]
            )

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
                    l0 = l[0]
                    if type(l0) is tuple:
                        l0 = "_".join([str(k) for k in key])
                    writer.writerow([renames.get(l0, l0)] + l[1:])

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
