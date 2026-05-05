import random
from ClearTerminal import clear_console
from rich import print

class Gambling():
    def __init__(self, join_message):
        self.join_message = join_message
        self.joined_users = []
    def join(self, user_message, username):
        if self.join_message in user_message:
            if username not in self.joined_users:
                self.joined_users.append(username)
        clear_console()
        print(f"[yellow]{len(self.joined_users)} users joined[/yellow]")
        print(f"[yellow]{username}:{user_message}[/yellow]")
    def chose_winner(self):
        if len(self.joined_users) == 0:
            return "no one joined"
        return random.choice(self.joined_users)

    def announce_winner(self, winner):
        clear_console()
        print(f"[yellow]{len(self.joined_users)} users joined[/yellow]")
        for user in self.joined_users:
            if user == winner:
                print(f"[green]{winner}[/green]")
            else:
                print(f"[red]{user}[/red]")
        print(f"[green]Winner: {winner}[/green]")