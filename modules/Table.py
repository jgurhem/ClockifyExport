from texttable import Texttable
import os


COLOR_CODE = "\033[38;2;68;69;72m"
RESET_CODE = "\x1b[0m"


class Table:
    def __init__(self) -> None:
        tsize = os.get_terminal_size()
        self.table = Texttable(tsize.columns)
        self.table._char_horiz = COLOR_CODE + "-" + RESET_CODE
        self.table._char_vert = COLOR_CODE + "|" + RESET_CODE
        self.table._char_corner = COLOR_CODE + "+" + RESET_CODE
        self.table._char_header = COLOR_CODE + "=" + RESET_CODE

    def add_header(self, header):
        self.table.header(header)

    def add_row(self, row):
        self.table.add_row(row)

    def set_cols_align(self, align):
        self.table.set_cols_align(align)

    def draw(self) -> str:
        return self.table.draw()
