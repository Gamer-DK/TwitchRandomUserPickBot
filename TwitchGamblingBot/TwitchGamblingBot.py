import json
import asyncio
import os
from warnings import warn
from rich import print
from twitchio.ext import commands
from twitchio import *
from Gambling import Gambling
from ClearTerminal import clear_console
from TwitchInformationCheck import twitch_mod_oauth_token

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "TwitchInformation.json"), "r") as json_file:
    TWITCH_DATA = json.load(json_file)

with open(os.path.join(BASE_DIR,"GamblingSettings.json"), "r") as json_file:
    GAMBLING_DATA = json.load(json_file)

TOTAL_GAMBLING_USERS = 0

is_shutting_down = False

TWITCH_MOD_OAUTH_TOKEN = TWITCH_DATA["TwitchBotAuthToken"].replace("oauth:", "")
CHANNEL_NAME = TWITCH_DATA["ChannelName"]


def update_win_message(winner, win_message):
    return win_message.replace("!winner", f"@{winner}")


class AllMessagesBot(commands.Bot):
    auto_end_task = None
    error_occurred = False
    def __init__(self):
        self.is_shutting_down = False
        self.channel = None
        super().__init__(token=TWITCH_MOD_OAUTH_TOKEN, prefix='?', initial_channels=[CHANNEL_NAME])
        self.gambling = Gambling(GAMBLING_DATA["JoinMessage"])

        print('[yellow]This VIP Gambling Twitch bot is based on the Teaching Streamers to Code project from DougDoug.\nMy GitHub: Gamer-DK')

    async def event_ready(self):
        self.channel = self.get_channel(CHANNEL_NAME)
        if not self.channel:
            print()
            self.error_occurred = True
            await self.end_application()
        else:
            print(f'[green]Logged into Twitch as {self.nick}')

        if self.auto_end_task is None or self.auto_end_task.done():
            self.auto_end_task = asyncio.create_task(self.auto_end())
    
    def is_user_subscribed(self, message):
        """Check if the user is a subscriber using badges and tags"""
        # Check badges first (most reliable)
        if hasattr(message.author, 'badges'):
            badges = message.author.badges or {}
            if 'subscriber' in badges:
                return True
        # Fallback to tags
        if hasattr(message, 'tags'):
            tags = message.tags or {}
            subscriber_tag = tags.get('subscriber', '0')
            return subscriber_tag == '1'
        return False

    async def event_message(self, message):
        if message.echo:
            return
        if not message.author:
            return
        if self.is_shutting_down:
            return
        await self.process_message(message)

    def can_join(self, user_message):
        if not GAMBLING_DATA["SubbedUsersCanJoin"] and GAMBLING_DATA["NonSubbedUsersCanJoin"]:
            if GAMBLING_DATA["SubbedUsersCanJoin"]:
                return self.is_user_subscribed(user_message)
            elif GAMBLING_DATA["NonSubbedUsersCanJoin"]:
                return not self.is_user_subscribed(user_message)
            else:
                print("[red]no one can join. check the GamblinSettings.json[/red]")
                return False
        return True
    async def process_message(self, message: Message):
        username = message.author.name
        user_message = message.content

        if GAMBLING_DATA["JoinMessageToLower"]:
            user_message = user_message.lower()

        if username.lower() == CHANNEL_NAME.lower() and GAMBLING_DATA["EarlyEndMessage"] in user_message:
            await self.end_application()
            return

        if self.can_join(message):
            self.gambling.join(user_message, username)

    async def end_bot(self):
        results = self.gambling.chose_winner()
        self.gambling.announce_winner(results)
        await self.handle_winner(results)

    async def handle_winner(self, results):
        if results == "no one joined":
            if not self.channel:
                self.channel = self.get_channel(CHANNEL_NAME)
            if self.channel:
                await self.channel.send(GAMBLING_DATA["NoOneJoiningMessage"]) #Sadge
            else:
                print("[red]Couldn't get the channel to send a message to[/red]")
            return
        else:
            await self.channel.send(update_win_message(results, GAMBLING_DATA["WinMessageFromBot"]))

    async def end_application(self):

        if self.is_shutting_down:
            return

        self.is_shutting_down = True
        if not self.error_occurred:
            await self.end_bot()

        current_task = asyncio.current_task()

        if self.auto_end_task and self.auto_end_task is not current_task and not self.auto_end_task.done():
            self.auto_end_task.cancel()
            try:
                await self.auto_end_task
            except asyncio.CancelledError:
                pass

        await asyncio.sleep(2)

        try:
            await asyncio.wait_for(self.close(), timeout=5)
        except asyncio.TimeoutError:
            print("[red]TwitchIO close takes to long; event loop wil be closed anyway[/red]")
        finally:
            self.loop.call_soon(self.loop.stop)

    async def auto_end(self):
        await asyncio.sleep(GAMBLING_DATA["Timer"])
        await self.end_application()


def startBot():
    global bot

    bot = AllMessagesBot()
    bot.run()


if __name__ == '__main__':
    clear_console()
    if twitch_mod_oauth_token(TWITCH_MOD_OAUTH_TOKEN):
        startBot()
    else:
        print("[red]Token doesn't work.\nThe bot can't make connection with the Twitch channel[/red]")
