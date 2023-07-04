import dateutil.parser
import json
import inspect
from datetime import datetime, timedelta

class Entry:
    def __init__(self, entry : dict) -> None:
        self.__entry = entry

        self.id : str = self.__entry["id"]
        self.description : str = self.__entry["description"]
        self.billable : bool = self.__entry["billable"]
        self.project : str = self.__entry["project"]["name"]

        self.enddate : datetime = dateutil.parser.isoparse(self.__entry["timeInterval"]["end"])
        self.startdate : datetime = dateutil.parser.isoparse(self.__entry["timeInterval"]["start"])
        self.duration : timedelta = self.enddate - self.startdate

        self.task_id : str = ""
        self.task_name : str = ""

        if self.__entry["task"]:
            if "id" in self.__entry["task"]:
                self.task_id = self.__entry["task"]["id"]
            if "name" in self.__entry["task"]:
                self.task_name = self.__entry["task"]["name"]

        self.tags : list[str] = list()
        for t in self.__entry["tags"]:
            self.tags.append(t["name"])

    def dump(self) -> str:
        return json.dumps(self.__entry, indent=4)

    def __str__(self) -> str:
        d = dict()
        for member in inspect.getmembers(self):
            if member[0].startswith("_") or inspect.ismethod(member[1]): continue
            member_type = type(member[1])
            if member_type == timedelta:
                d[member[0]] = str(member[1])
            elif member_type == datetime:
                d[member[0]] = f'{member[1]:%Y-%m-%d %H:%M:%S}'
            else:
                d[member[0]] = member[1]
        return str(d)