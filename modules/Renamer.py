class Renamer:
    def __init__(self, renames: dict, ignored_tasks: list) -> None:
        self.renames = renames
        self.ignored_tasks = ignored_tasks

    def rename(self, project, task):
        rtask = task
        rproject = project
        if task in self.ignored_tasks:
            rtask = None
        if project in self.renames:
            rproject = self.renames[project]
        combined = f"{rproject}___{rtask}"
        if combined in self.renames:
            s = self.renames[combined].split("___")
            rproject = s[0]
            rtask = None
            if len(s) > 1:
                rtask = s[1]
        return rproject, rtask
