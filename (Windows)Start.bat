@echo off

REM Go to the folder the script is at
cd /d "%~dp0"

REM (optioneel) virtual environment maken
REM python -m venv venv

REM (optioneel) venv activeren
REM call venv\Scripts\activate

REM install the dependencies
python -m pip install -r requirements.txt

REM start the bot
python TwitchGamblingBot\TwitchGamblingBot.py

REM wait for input bevore closing the terminal
pause