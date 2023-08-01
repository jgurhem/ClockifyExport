import itertools
from datetime import timedelta
from .Table import Table


class Summary:
    def __init__(self, projects, total_work) -> None:
        self.projects = projects
        self.total_work = total_work

    def print(self, l=lambda x: x):
        table = Table()
        table.set_cols_align(["l", "l"])
        table.add_header(["Project", "Percentage"])

        for key, group in itertools.groupby(sorted(self.projects.keys()), key=l):
            v = timedelta()
            for p in list(group):
                v += self.projects[p]
            table.add_row([key, f"{v/self.total_work*100:=6.2f}"])

        print(table.draw())
