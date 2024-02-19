import itertools
from datetime import timedelta

from modules.TaskTime import TaskTime
from .Table import Table

class Summary:
    def __init__(self, ptday: list[TaskTime]) -> None:
        self.ptday = ptday

    def print(self, l=lambda x: x.getFullName()):
        table = Table()
        table.add_header(["Project", "Percentage"])
        table.set_cols_align(["l", "c"])

        total_work = 0
        for el in self.ptday:
            total_work += el.duration

        agg = dict()
        for key, group in itertools.groupby(sorted(self.ptday, key=l), key=l):
            v = agg.get(key,0)
            group = list(group)
            for p in group:
                v += p.duration
            agg[key] = v

        for key in sorted(agg):
            table.add_row([key, f"{agg[key]/total_work*100:=6.2f}"])

        print(table.draw())
