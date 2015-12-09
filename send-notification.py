#!/usr/bin/env python
"""
A simple script that runs within the drone-hipchat Docker container.
Accepts input from Drone via stdin/args, sends messages to the room designated
in the input.
"""
import datetime

import drone
import requests

ROOM_URL = "https://api.hipchat.com/v2/room/{room_id_or_name}/notification"


def get_message_color(payload):
    state = payload["build"]["status"]
    if state == "success":
        return "green"
    if state in ["failure", "error", "killed"]:
        return "red"
    else:
        return "yellow"


def get_build_time_str(payload):
    build_start = int(payload["build"]["started_at"])
    build_end = int(payload["build"]["finished_at"])
    build_delt = build_end - build_start
    return str(datetime.timedelta(seconds=build_delt))


def get_message(payload):
    state = payload["build"]["status"]
    if state == "pending":
        message = (
            "<a href='{system_link_url}'Build</a> #{build_number} has"
            "been enqueued for branch <strong>{build_branch_name}</strong> "
            "of <strong>{repo_full_name}</strong><br>"
            "{build_author}: {build_message} (<code>{build_commit}</code>)"
        )
    elif state == "running":
        message = (
            "<a href='{system_link_url}'Build</a> #{build_number} of branch "
            "<strong>{build_branch_name}</strong> "
            "for <strong>{repo_full_name}</strong> has started.<br>"
            "{build_author}: {build_message} (<code>{build_commit}</code>)"
        )
    elif state in "failure":
        message = (
            "<a href='{system_link_url}'>Build</a> #{build_number} of branch "
            "<strong>{build_branch_name}</strong> "
            "for <strong>{repo_full_name}</strong> failed.<br>"
            "{build_author}: {build_message} (<code>{build_commit}</code>)"
        )
    elif state == "error":
        message = (
            "An error was encountered during "
            "<a href='{system_link_url}'>build</a> #{build_number} of branch "
            "<strong>{build_branch_name}</strong> "
            "for <strong>{repo_full_name}</strong>.<br>"
            "{build_author}: {build_message} (<code>{build_commit}</code>)"
        )
    elif state == "killed":
        message = (
            "<a href='{system_link_url}'>Build</a> #{build_number} of branch "
            "<strong>{build_branch_name}</strong> "
            "for <strong>{repo_full_name}</strong> was killed.<br>"
            "{build_author}: {build_message} (<code>{build_commit}</code>)"
        )
    elif state == "success":
        message = (
            "<a href='{system_link_url}'>Build</a> #{build_number} "
            "for branch <strong>{build_branch_name}</strong> "
            "of <strong>{repo_full_name}</strong> succeeded after "
            "{build_time}. (<code>{build_commit}</code>)"
        )
    else:
        message = (
            "<a href='{system_link_url}'>Build</a> #{build_number} for branch "
            "<strong>{build_branch_name}</strong> "
            "of <strong>{repo_full_name}</strong> has ended up in an"
            "unknown state: {state}<br>"
            "(<code>{build_commit}</code>)"
        )
    return message.format(
        repo_full_name=payload["repo"]["full_name"],
        build_number=payload["build"]["number"],
        build_author=payload["build"]["author"],
        build_branch_name=payload["build"]["branch"],
        build_message=payload["build"]["message"],
        build_commit=payload["build"]["commit"],
        build_time=get_build_time_str(payload),
        system_link_url=payload["system"]["link_url"],
        state=state,
    )


def main():
    payload = drone.plugin.get_input()
    vargs = payload["vargs"]

    data = {
        "auth_token": vargs["room_auth_token"],
        "message": get_message(payload),
        "message_format": "html",
        "color": get_message_color(payload),
        "notify": vargs.get("message_notify") == True,
    }
    response = requests.post(
        ROOM_URL.format(room_id_or_name=vargs["room_id_or_name"]),
        data=data)
    response.raise_for_status()

if __name__ == "__main__":
    main()
