import requests
from datetime import datetime

URL = "https://api.clockify.me/api/v1"

class Clockify:
    def __init__(self, token : str) -> None:
        self.__token : str = token

        self.__headers = {
            "content-type": "application/json",
            "X-Api-Key": self.__token,
        }

        self.user = self.__get_user_id()


    def get_workspaces(self) -> list[str]:
        resp = requests.get(URL + "/workspaces", headers=self.__headers)
        ids = list()
        for workspace in resp.json():
            ids.append(workspace["id"])
        return ids


    def __get_user_id(self) -> str:
        resp = requests.get(URL + "/user", headers=self.__headers)
        return resp.json()["id"]


    def get_time_entries(
        self,
        workspace: str,
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
                f"{URL}/workspaces/{workspace}/user/{self.user}/time-entries?start={startdate_str}"
                + f"&end={enddate_str}&page={page}&page-size={pagesize}&hydrated=true",
                headers=self.__headers,
            )
            page += 1

            resp_json = resp.json()
            read = len(resp_json)
            for e in resp_json:
                yield e