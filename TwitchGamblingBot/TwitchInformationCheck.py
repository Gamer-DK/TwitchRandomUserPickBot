import requests

def twitch_mod_oauth_token(token):
    headers = {
        "Authorization": f"OAuth {token}"
    }

    r = requests.get("https://id.twitch.tv/oauth2/validate", headers=headers)

    return r.status_code == 200