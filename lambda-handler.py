import requests

from retry import retry
from requests import Response


class GitUser:
    def __init__(self, username, name, bio):
        self.__username = username
        self.__name = name
        self.__bio = bio

    @classmethod
    def from_dict(cls, json_data: dict) -> "GitUser":
        return cls(json_data["login"], json_data["name"], json_data["bio"])

    def __str__(self):
        return f"Username: {self.__username}, Name: {self.__name}, Bio: {self.__bio}"


def lambda_handler(event, context=None) -> None:
    response_user_data = get_git_user_details(event["username"])

    user_data = GitUser.from_dict(response_user_data)

    print(user_data.__str__())


@retry(Exception, tries=3, delay=5)
def get_git_user_details(username: str) -> dict:
    try:
        data: Response = requests.get(f"https://api.github.com/users/{username}")

        if data.status_code != 200:
            print("Invalid status code")
            raise Exception("Invalid status code!")

        return data.json()

    except Exception as error:
        raise Exception(error)
