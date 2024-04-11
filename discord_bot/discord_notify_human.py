# Auto send message to discord channel via web request
import requests

from env._secrete import discord_web_Auth, your_channel_id


def send_msg_to_discord_request(msg, channel_id=your_channel_id, auth=discord_web_Auth):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    payload = {
        "content": msg,
    }

    header = {
        'Authorization': auth,
    }

    r = requests.post(url, data=payload, headers=header)

    print(r)


if __name__ == '__main__':
    send_msg_to_discord_request("test 01 via web auth call", your_channel_id, discord_web_Auth)
