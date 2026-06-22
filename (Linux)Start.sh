#!/bin/bash

# ==========================================
# Twitch Random User Pick Bot Starter Script For Linux
# ------------------------------------------
# This script:
# 1. Makes a virtual environment
# 2. Install dependencies
# 3. Start the bot
#
# Dependencies:
# - Python 3 installed (3.12 works for sure, other are not tested)
#
# usage:
# open the terminal in the projectfile and run the next code
# chmod +x "(Linux)Start.sh"
# ./"(Linux)Start.sh"
# ==========================================

cd "$(dirname "$0")"

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt

python3 TwitchRandomUserPickBot/TwitchRandomUserPickBot.py

read -p "Press Enter to close..."
