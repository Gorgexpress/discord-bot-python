import discord
from functools import lru_cache
import asyncio
import asyncpg
import os
from botcommand import BotCommand
from credentials import Credentials
from persist import Persist
persist = Persist()
client = discord.Client()
token = os.environ['token']
credentials = Credentials()
credentials.uri = os.environ['DATABASE_URL']
from store.dblayer import DuplicateError
from store.postgres import PGWrapper
db = PGWrapper(credentials)


@client.event
async def on_message(message):
	if message.content.startswith("^register"):
		await register_command(message)
	if message.content.startswith("^count"):
		await get_count(message)
	if message.content.startswith("^top10"):
		await top10(message)
	elif message.content.startswith('[') and message.content[-1] == ']':
		await respond_to_command(message)
	elif message.content.startswith('^randomguess'):
		await random_guess(message)
	elif message.content.startswith('^random'):
		await random_response(message)
	


#@client.event
#async def on_reaction_add(reaction, user):
#	message = reaction.message
#	for r in message.reactions:
#		if r.count >= 10:
#			persist.add_lore(db, message.author.nick,message.channel.id, message.id, message.content)

async def top10(message):
	try:
		result = await persist.gettop10(db)
		resultstr = '\n'.join('{0}: {1} (used {2} times)'.format(idx, row.command, row.count) for idx, row in enumerate(result, 1))
		await message.channel.send(resultstr)
	except:
		pass

async def random_response(message):
	try:
		result = await persist.random(db) 
		await message.channel.send(result.response)
	except Exception as e:
		print(repr(e))

async def random_guess(message):
	try:
		result = await persist.random(db)
		await message.channel.send(f'What command is this(without brackets)? \n {result.response}')
		try:
			msg = await client.wait_for('message', check=lambda m: m.content == result.command, timeout=15)
		except asyncio.TimeoutError:
			await message.channel.send(f'The answer was {result.command}')
		else:
			await message.channel.send(f'{msg.author.display_name} is correct!')

	except Exception as e:
		print(repr(e))
	
async def register_command(message):
	if "<@" in message.content:
		await message.channel.send(
		"You cannot register anything that pings other users.")
		return
	commandstart, commandend = message.content.find(
	'['), message.content.find(']')
	if commandend <= commandstart or (commandstart == -1 or commandend == -1) or (commandend >= len(message.content) - 2 or message.content[commandend + 1] != ' '):
		await message.channel.send(
		"Invalid format. Use ^register [command] response")
	command = message.content[commandstart+1:commandend]
	response = message.content[commandend + 2:].strip()
	if len(response) < 4:
		await message.channel.send("Command not registered. Response was less than 4 characters in length.")

	botcommand = BotCommand(command.lower(), response)
	try:
		await persist.save(db, botcommand)
		await message.channel.send(f'Command "{command}" registered!')
	except DuplicateError:
		await message.channel.send("Command already exists.")
	except Exception as e:
		await message.channel.send(repr(e))
		pass
		# catch other exceptions here. say unexpected error or w/e.
	


async def respond_to_command(message):
	command = message.content[1:-1].lower()
	response = None
	# gonna have to attempt to load the command now
	try:
		response = await persist.get(db, command)
		if not response:
			await message.channel.send("Command does not exist.")
		else:
			await message.channel.send(response.response)
	except Exception as e:
		# handle other exceptions
		await message.channel.send(repr(e))
	if response:
		response.count += 1
		try:
			await persist.update(db, response)
		except Exception as e:
			print(repr(e))
	
async def get_count(message):
	commandstart, commandend = message.content.find(
	'['), message.content.find(']')
	command = message.content[commandstart+1:commandend]
	try:
		response = await persist.get(db, command)
		if not response:
			await message.channel.send("Command does not exist.")
		else:
			await message.channel.send(f"{response.command} has been used {response.count} times")
	except:
		pass	


client.run(token)
