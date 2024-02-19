from datetime import timedelta, date


class TaskTime:
    def __init__(self, project: str, task: str, date: date, duration: timedelta) -> None:
        self.project = project
        self.task = task
        self.date = date
        self.duration = duration

    def getFullName(self) -> str:
        if self.task:
            return f"{self.project}___{self.task}"
        else:
            return self.project