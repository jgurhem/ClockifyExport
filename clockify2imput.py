from datetime import timedelta
import itertools

from modules.Parser import Parser
from modules.Clockify import Clockify
from modules.utils import update_add

args = Parser()

print("From :", args.startdate, "to :", args.enddate)
print()
print()
print()

clockify = Clockify(args.token)

days = dict()
projects = dict()
total_work = timedelta()
maxlenghtname = 0
maxlenghtproject = 0
day_set = set()
projects_set = set()

for w in clockify.get_workspaces():
    for e in clockify.get_time_entries(w, args.startdate, args.enddate):
        if not args.billable and not e.billable:
            continue

        d = days.get(e.startdate.date(), dict())
        if e.task_name in args.tasknames or e.task_name == "":
            k = e.project
        else:
            k = e.project + "___" + e.task_name

        maxlenghtname = max(maxlenghtname, len(k))
        maxlenghtproject = max(maxlenghtproject, len(e.project))

        update_add(d, k, lambda x : x + e.duration, timedelta())
        update_add(d, "Sum", lambda x : x + e.duration, timedelta())
        update_add(projects, k, lambda x : x + e.duration, timedelta())

        days[e.startdate.date()] = d

        day_set.add(e.startdate.date())
        projects_set.add(k)

        total_work += e.duration

if args.perday:
    for k1 in days.keys().__reversed__():
        v1 = days[k1]
        print(k1, v1)
        # sum = timedelta(hours=7.5)
        for k2, v2 in v1.items():
            if k2 == 'Sum':
                continue
            print("\t", f"{k2:{maxlenghtname}s}", " --- ", f"{v2/v1['Sum']:.2f}")
        print()
    print()
    print()
    print()

day_set = sorted(day_set)
for key, group in itertools.groupby(day_set, key=lambda e : (e.year, e.month)):
    group = list(group)
    print(f"{str(key):{maxlenghtname}s}", end='  ')
    for d in group:
        print(f"{d.day:6d}", end='')
    print(f"{'Sum':>7}", end='')
    print()
    print()
    for p in sorted(projects_set):
        line = f"{p:{maxlenghtname}s}  "
        s = 0
        for d in group:
            t = int(days[d].get(p, timedelta(0))/days[d]['Sum']*100)
            s += t
            line += f"{t:6d}"
        line += f"{s:7d}"
        if s > 0:
            print(line)
    print()
    print()
    print()

for k in sorted(projects.keys()):
    v = projects[k]
    print(f"{k:{maxlenghtname}s}", " --- ", f"{v/total_work*100:=6.2f}")

print()
print()
print()

for key, group in itertools.groupby(sorted(projects.keys()), key=lambda e : e.split("___")[0]):
    v = timedelta()
    for p in list(group):
        v += projects[p]
    print(f"{key:{maxlenghtproject}s}", " --- ", f"{v/total_work*100:=6.2f}")
