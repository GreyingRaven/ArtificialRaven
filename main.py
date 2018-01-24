import config
import utility
import pattern
import socket
import time
import csv
import re



CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

command_list = utility.loadCommands()

try:
	s = socket.socket()
	s.connect((config.HOST, config.PORT))
	s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
	s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
	s.send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
	connected = True #Socket succefully connected
	print("Connection to " + config.CHAN + " succesful")
	print(command_list.keys())
except Exception as e:
	print("Failed to connect:")
	print(str(e))
	connected = False #Socket failed to connect

def bot_loop():
	while connected:
		response = s.recv(1024).decode("utf-8")
		if response == "PING :tmi.twitch.tv\r\n":
			s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
			print("Pong")
		else:
			username = re.search(r"\w+", response).group(0) 
			message = CHAT_MSG.sub("", response)
			print(username + ": " + message)
			# Ban pattern check
			for pat in pattern.BAN_PAT:
				if re.match(pat, message):
					utility.ban(s, username)					
					utility.chat(s,"Tap, tap, tap. Nevermore. " + username + " banned")
					break
			# Time out pattern check
			for pat in pattern.TO_PAT:
				if re.match(pat, message):
					utility.timeout(s, username)
					utility.chat(s,"Caw caw! " + username + " silence! You know what you've done...")
					break
			# Command check
			if re.match(r'^(![A-Z,a-z])\w', message):
				# Check if command exists
				if message.strip() in command_list:
					utility.runCommand(s, message.strip(), command_list[message.strip()])
				else:					
					# New command check
					if re.match(r'^(![A-Z,a-z])\w+\s([A-Z,a-z])', message):
						command = message.split(" ", 1)[0]
						action = message.split(" ", 1)[1]
						utility.newCommand(s, command, action, command_list.keys())
						command_list[command] = action
						print("A new command: " + command + " action: " + action)					
					else:
						utility.chat(s, "Command doesn't exists")

		time.sleep(1 / config.RATE)
if __name__ == "__main__":
	bot_loop()