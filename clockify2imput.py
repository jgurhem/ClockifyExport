import requests
import json
from datetime import datetime, timedelta
import calendar
import argparse

URL = "https://api.clockify.me/api/v1"


def get_workspace_ids(headers: dict):
    resp = requests.get(URL + "/workspaces", headers=headers)
    ids = list()
    for workspace in resp.json():
        ids.append(workspace["id"])
    return ids


def get_user_id(headers: dict):
    resp = requests.get(URL + "/user", headers=headers)
    return resp.json()["id"]


def get_time_entries(
    headers: dict,
    workspace: str,
    userid: str,
    startdate: datetime,
    enddate: datetime,
    pagesize: int = 100,
) -> list[dict]:
    page = 1
    read = 1

    startdate_str = startdate.isoformat() + "Z"
    enddate_str = enddate.isoformat() + "Z"

    while read > 0:
        resp = requests.get(
            f"{URL}/workspaces/{workspace}/user/{userid}/time-entries?start={startdate_str}"
            + f"&end={enddate_str}&page={page}&page-size={pagesize}&hydrated=true",
            headers=headers,
        )
        page += 1

        resp_json = resp.json()
        read = len(resp_json)
        for e in resp_json:
            yield e


def extract_tag_name(entry: dict):
    tags = list()
    for t in entry["tags"]:
        tags.append(t["name"])
    return tags


parser = argparse.ArgumentParser(
    description="Download the entries in Clockify to make timesheets for Aneo.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("token", help="User token for API authentication", type=str)
parser.add_argument(
    "-b",
    "--include-not-billable",
    dest="billable",
    help="Include not billable entries in the output sheet",
    action="store_true",
    default=False,
)
args = parser.parse_args()

headers = {
    "content-type": "application/json",
    "X-Api-Key": args.token,
}

now = datetime.now()
print("now", now)
ndays = calendar.monthrange(now.year, now.month)[1]

start = datetime(now.year, now.month, 1, 0, 0, 0)
end = datetime(now.year, now.month, ndays, 23, 59, 59)
print("From :", start, "to :", end)
print()
print()
print()

days = dict()
maxlenghtname = 0

workspaces = get_workspace_ids(headers)
user = get_user_id(headers)
for w in workspaces:
    for e in get_time_entries(headers, w, user, start, end):
        # print(json.dumps(e, indent=4))

        billable = e["billable"]
        if not args.billable and not billable:
            continue

        proj = e["project"]["name"]
        tags = extract_tag_name(e)

        enddate = datetime.fromisoformat(e["timeInterval"]["end"].rstrip("Z"))
        startdate = datetime.fromisoformat(e["timeInterval"]["start"].rstrip("Z"))
        duration = enddate - startdate

        d = days.get(startdate.date(), dict())
        if len(tags) == 0 or "Daily" in tags or "Entretien Technique" in tags:
            k = proj
        else:
            k = proj + "___" + str(tags)
        maxlenghtname = max(maxlenghtname, len(k))
        v = d.get(k, timedelta())
        v += duration
        d[k] = v
        days[startdate.date()] = d

for k1 in days.keys().__reversed__():
    v1 = days[k1]
    print(k1, v1)
    sum = timedelta()
    for v2 in v1.values():
        sum += v2
    # sum = timedelta(hours=7.5)
    for k2, v2 in v1.items():
        print("\t", f"{k2:{maxlenghtname}s}", " --- ", f"{v2/sum:.2f}")
    print()
