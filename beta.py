#!/usr/bin/env python3

import argparse
import re
import time
import sys
import os
import os.path
import random
import string
import importlib
import hashlib
#import username
from lib import Url
from copy import deepcopy
from time import sleep
from datetime import datetime
from lib.colorama import Fore, Style
#  Version with Banner and menu
# --- UNDER CONSTRUCTION ----
# Goals:
# DONE! Create custom color banner- DONE!
# DONE! Create a menu tailored to this scraper,
# DONE! enter username prompt
# Will I need to add another class? and or functions? (if threading then yes)
# Is it possible to proxy individual requests/downloads through diffent servers to prevent IP ban?
# Offer the ability to download more than just one Instagrammer at a time. (need proxies)
# ?? import threading module & create def queueRequests(): 
# or use asyncio or other concurrency? could conflict with API calls and result in being blocked
# How to call the class and functions to run the program ??
# create a separate module , (menu.py) to be imported??
# Probably need to use the sleep() function time.sleep(5)  # pause to avoid ban
# What adjstments to the class, ( or more classes?), attributes and functions will be needed?
# Ultimately how to run the program? ie: Calling the classes, functions etc..
# Much of this code was inspired by James Kettle's HTTP Request Smuggling Python code. Thus the similarities.
host = "https://instagram.com"
smhost = "https://instagram.com"
# --------------------------------------------------------------------------------------#

# class Instagram_Downloader:
#     def __init__(self, username):
#         self.username = username
#         self.user_id = ""
#         self.jsondata = ""
#         self.apilabel = "graphql"
#         self.hash_timeline = ""


class Instagram_Downloader():
		'''SMUGGLER attributes for REFERENCE'''

		def __init__(self, smhost, username=""):
				self._host = smhost
				self.username = username
				self.user_id = ""
				self.jsondata = ""
				self.apilabel = "graphql"
				self.hash_timeline = ""

		def run(self):
			"""receivess the call sm.run() to execute the code"""
			while True:
				Parser = argparse.ArgumentParser()

		def create_download_directory(self):
			try:
				os.mkdir(self.username)
				print("Directory ", self.username, " created.")
			except FileExistsError:
				print("Directory ", self.username, " already exists.")

		def get_total_photos(self):
			return int((self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["count"]))

		def set_user_id(self):
			self.user_id = int(self.jsondata.json()[self.apilabel]["user"]["id"])

		def get_end_cursor_timeline_media(self):
			return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]

		def write_resume_end_cursor_timeline_media(self):
			# create file with last page downladed to resume if needed
			f = open("resume_"+self.username+".txt", "w")
			f.write(str(self.get_end_cursor_timeline_media()))
			f.close()

		def read_resume_end_cursor_timeline_media(self):
			if os.path.isfile("resume_"+self.username+".txt"):
				with open("resume_"+self.username+".txt") as f:
					self.hash_timeline = f.readline().strip()
					print("****************\nResume mode ON\n****************")
					return True
			else:
				print("Not resume pending")
				return False

		def remove_resume_file(self):
			if os.path.exists("resume_"+self.username+".txt"):
				os.remove("resume_"+self.username+".txt")

		def set_apilabel(self, label):
			self.apilabel = label

		def has_next_page(self):
			return self.jsondata.json()[self.apilabel]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]

		def get_jsondata_instagram(self):
			headers = {
				"Host": "www.instagram.com"
				"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
				}
			if self.apilabel == "graphql":
					self.jsondata = requests.get(
							"https://www.instagram.com/" + self.username + "/feed/?__a=1", headers=headers)
					self.hash_timeline = self.get_end_cursor_timeline_media()
					self.set_user_id()
				else:
					self.jsondata = requests.get("https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%22" + str(
							self.user_id) + "%22%2C%22first%22%3A12%2C%22after%22%3A%22" + str(self.hash_timeline) + "%22%7D", headers=headers)
					if user.has_next_page():
						self.hash_timeline = self.get_end_cursor_timeline_media()
					if (self.jsondata.status_code == 200):
						print("----------------\nJson url loaded:\n----------------\nhttps://www.instagram.com/graphql/query/?query_id=17888483320059182&variables=%7B%22id%22%3A%22" +
						      str(self.user_id) + "%22%2C%22first%22%3A12%2C%22after%22%3A%22" + str(self.hash_timeline) + "%22%7D")
					else:
						print("Error, Incorrect json data url recieved.")
					return self.jsondata

		def download_photos(self):
			pass
	

		def download_videos(self):
			pass


# --------------------------------- SMUGGLER CODE -------------------------------------#

def CF(text):
	global NOCOLOR
	if NOCOLOR:
		ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
		text = ansi_escape.sub('', text)
	return text


def banner(sm_version):
	print(CF(Fore.CYAN))
	print(CF(r" _                                                                                                  "))
	print(CF(r"| |                    ___________              _______                         __      __          "))
	print(CF(r"| |                   (____   ____) ___        /  _____)              ___      /  \    /  \         "))
	print(CF(r"| |  _____         ______  | |     /   \      / /                    /   \    / /\ \  / /\ \        "))
	print(CF(r"| | |  _  \       /  ____) | |    / / \ \     | |    ____   _____   / / \ \   | | \ \/ /  \ \       "))
	print(CF(r"| | | |  \ \     ( (_____  | |   / /___\ \    | |   (_   ) /  __   / /___\ \  | |  \__/    \ \      "))
	print(CF(r"| | | |   \ \     \_____  \| |  / _______ \   | |     \  \ | |    / _______ \ | |           \ \     "))
	print(CF(r"| | | |    \ \__________)  ) | / /       \ \_/ /______|  | | |   / /       \ \| |            \ \    "))
	print(CF(r"|_| |_|     \_____________/|_|/_/         \______________/ |_|  /_/         \___/             \_\   "))
	print(CF(r"                                                                                                                             "))
	print(CF(r"                                                                                                                             "))
	print(CF(r" _______       ____                                                                                                          "))
	print(CF(r"/  _____ \    / __ \     _            _                                              _______      _____       ________       "))
	print(CF(r"| |     \ \  / /  \ \   | |          | |           _          ____                  /  ____  \   | ____|     |  ____  \      "))
	print(CF(r"| |     | |  | |   | |  | |          | |           | |       / /\ \       ___       | |     \    | |         | |____| |      "))
	print(CF(r"| |     | |  | |   | |  | |    _     | |  _____    | |      | |  | |     /   \      | |     | |  | |___      | ____  /       "))
	print(CF(r"| |     | |  | |   | |  | |   | |    | |  |  _ \   | |      | |  | |    / / \ \     | |     | |  |  ___|     | |   \ \       "))
	print(CF(r"| |     | |  | |   | |  | |   | |    | |  | | \ \  | |      | |  | |   / /___\ \    | |     | |  | |         | |    \ \      "))
	print(CF(r"| |     | |  | |   | |  | |   | |    | |  | |  \ \ | |      | |  | |  / ______  \   | |     | |  | |     _   | |     \ \     "))
	print(CF(r"| |____/  /  | |___| |  | \__/ / \ __/ |  | |   \ \|  \_____\  \/ /  / /       \ \__| |____ / /__| |____| |__| |      \ \    "))
	print(CF(r"|________/   \_______/  \ ____/   \____/  |_|    \_______________/  /_/         \______________________________/       \_\   "))
	print(CF(r"                                                                                                                             "))
	print(CF(r"                                                                                                                             "))
	print(CF(r"     LinuxUser255                                                                                        				 %s" % (sm_version)))
	print(CF(Style.RESET_ALL))


def print_info(msg, file_handle=None):
	ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
	msg = Style.BRIGHT + Fore.MAGENTA + \
            "[%s] %s" % (Fore.CYAN + '+' + Fore.MAGENTA, msg) + Style.RESET_ALL
	plaintext = ansi_escape.sub('', msg)
	print(CF(msg))
	if file_handle is not None:
		file_handle.write(plaintext + "\n")


if __name__ == "__main__":
	global NOCOLOR
	if sys.version_info < (3, 0):
		print("Error: Instagram Downloader requires Python 3.x")
		sys.exit(1)

# Goal: Offer the ability to select more than just one Instagram User
# Redo-EDIT this menue for its puposes.
Parser = argparse.ArgumentParser()
Parser.add_argument('-u', '--user', help="INSTAGRAM_USERNAME")
Parser.add_argument('-x', '--exit_early', action='store_true',
                    help="Exit scan on first finding")
Parser.add_argument('--no-color', action='store_true',
                    help="Suppress color codes")
#Parser.add_argument('-c', '--configfile', default="default.py",help="Filepath to the configuration file of payloads")
Args = Parser.parse_args()  # returns data from the options specified (ech

NOCOLOR = Args.no_color
if os.name == 'nt':
	NOCOLOR = True

Version = "v1.1"
banner(Version)

# Run it
sm = Instagram_Downloader(host, smhost)
# this still needed??
sm.run()


# Original way of calling/executing Instagram Downloader script

# -----------Main program function calls for Instagram_Downloader -------------------------------------#
#
# try:
#    user = Instagram_Downloader(INSTAGRAM_USERNAME)
#    user.create_download_directory()
#    user.get_jsondata_instagram()
#    user.download_photos()
#    user.download_videos()
#    user.set_apilabel("data")
#    user.read_resume_end_cursor_timeline_media()
#    while True:
#        time.sleep(5)  # pause to avoid ban
#        user.get_jsondata_instagram()
#        user.download_photos()
#        user.download_videos()
#        user.write_resume_end_cursor_timeline_media()
#        if user.has_next_page() == False:
#            user.remove_resume_file()
#            print("Done. All images/videos downloaded for " +
#                  INSTAGRAM_USERNAME+" account.")
#            break
# except:
#    print("Notice: script premature finished due to daily limit of number of requests to Instagram API.")
#    print("Just execute script AGAIN in few hours to continue RESUME of pending images/videos to downloa#
#
