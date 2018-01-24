import config
import socket

"""
	Send a chat message to the server.
	Keyword arguments:
	sock -- the socket over which to send the message
	msg  -- the message to be sent
"""
def chat(sock, msg):
	sock.send(("PRIVMSG {} :{}\r\n".format(config.CHAN, msg)).encode("UTF-8"))

"""
	Ban a user from the current channel.
	Keyword arguments:
	sock -- the socket over which to send the ban command
	user -- the user to be banned
"""
def ban(sock, user):
	chat(sock, ".ban {}".format(user))

"""
	Time out a user for a set period of time.
	Keyword arguments:
	sock -- the socket over which to send the timeout command
	user -- the user to be timed out
	secs -- the length of the timeout in seconds (default 600)
"""
def timeout(sock, user, secs=600):
	chat(sock, ".timeout {}".format(user, secs))

"""
	Load commands from commands.csv file
	Keyword arguments:
	com -- the command key
	act -- the action to perform
"""
def loadCommands():
	commandList = []
	with open("commands.csv", mode='r') as inputfile:
		rows = []
		for row in inputfile:
			rows.append(row.rstrip('\n').split("|||"))
		keys = rows[0]
		for values in rows[1:]:
			commandList.append(dict(zip(keys,values)))
	return commandList


"""
	Write a NEW command|action pair to commands.csv file
	Keyword arguments:
	com -- the command key
	act -- the action to perform
	TODO:
		Check that command key is unique!!
"""
def newCommand(com, act):
	with open("commands.csv", "a") as outfile:
		outfile.write(com+"|||"+act)