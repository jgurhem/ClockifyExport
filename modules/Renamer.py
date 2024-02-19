from modules.TaskTime import TaskTime


class Renamer:
    def __init__(self, renames: dict, ignored_tasks: list) -> None:
        self.renames = renames
        self.ignored_tasks = ignored_tasks

    def rename(self, tt : TaskTime) -> TaskTime:
        rtask = tt.task
        rproject = tt.project
        if tt.task in self.ignored_tasks:
            rtask = None
        if tt.project in self.renames:
            rproject = self.renames[tt.project]
        combined = f"{rproject}___{rtask}"
        if combined in self.renames:
            s = self.renames[combined].split("___")
            rproject = s[0]
            rtask = None
            if len(s) > 1:
                rtask = s[1]
        return TaskTime(rproject, rtask, tt.date, tt.duration)
