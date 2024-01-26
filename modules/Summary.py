import itertools
from datetime import timedelta
from .Table import Table


def project_name(project, task):
    if task:
        return f"{project}___{task}"
    else:
        return project

class Summary:
    def __init__(self, ptday) -> None:
        self.ptday = ptday

    def print(self, l=lambda x: project_name(x[1], x[2])):
        table = Table()
        table.add_header(["Project", "Percentage"])
        table.set_cols_align(["l", "c"])

        total_work = 0
        for el in self.ptday:
            total_work += el[3]

        agg = dict()
        for key, group in itertools.groupby(sorted(self.ptday), key=l):
            v = agg.get(key,0)
            group = list(group)
            for p in group:
                v += p[3]
            agg[key] = v

        for key in sorted(agg):
            table.add_row([key, f"{agg[key]/total_work*100:=6.2f}"])

        print(table.draw())
