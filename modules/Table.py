from texttable import Texttable
import os


class Table:
    def __init__(self) -> None:
        tsize = os.get_terminal_size()
        self.table = Texttable(tsize.columns)

    def add_header(self, header):
        self.table.header(header)

    def add_row(self, row):
        self.table.add_row(row)

    def set_cols_align(self, align):
        self.table.set_cols_align(align)

    def draw(self) -> str:
        return self.table.draw()
