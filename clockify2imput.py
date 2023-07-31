from datetime import timedelta

from modules.Parser import Parser
from modules.Clockify import Clockify
from modules.Summary import Summary
from modules.TimeTable import TimeTable
from modules.utils import update_add

args = Parser()

print("From :", args.startdate, "to :", args.enddate)
print()
print()

clockify = Clockify(args.token)

days = dict()
projects = dict()
total_work = timedelta()

for w in clockify.get_workspaces():
    for e in clockify.get_time_entries(w, args.startdate, args.enddate):
        if not args.billable and not e.billable:
            continue

        d = days.get(e.startdate.date(), dict())
        if e.task_name in args.tasknames or e.task_name == "":
            k = e.project
        else:
            k = e.project + "___" + e.task_name

        update_add(d, k, lambda x : x + e.duration, timedelta())
        update_add(d, "Sum", lambda x : x + e.duration, timedelta())
        update_add(projects, k, lambda x : x + e.duration, timedelta())

        days[e.startdate.date()] = d

        total_work += e.duration

if args.perday:
    for k1 in days.keys().__reversed__():
        v1 = days[k1]
        print(k1, v1)
        # sum = timedelta(hours=7.5)
        for k2, v2 in v1.items():
            if k2 == 'Sum':
                continue
            print("\t", f"{k2:{40}s}", " --- ", f"{v2/v1['Sum']:.2f}")
        print()
    print()
    print()
    print()

summary = Summary(projects, total_work)
summary.print()
print()
print()
summary.print(lambda e : e.split("___")[0])

ttable = TimeTable(days, projects)
ttable.print()
