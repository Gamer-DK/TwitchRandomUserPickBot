@echo off

REM Go to the folder the script is at
cd /d "%~dp0"

REM install the dependencies
python -m pip install -r requirements.txt

REM start the bot
python TwitchRandomUserPickBot/TwitchRandomUserPickBot.py

REM wait for input bevore closing the terminal
pause
