import discord, os, obs_api
from os.path import join, dirname
from dotenv import load_dotenv

TRIGGER = '!type'
COMMAND_ADD = 'add'
COMMAND_RM = 'rm'
COMMAND_ENUM = 'id'
COMMAND_STOP = 'stop'

TRIGGER_HELP = '?type'

dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)

author_restrict = os.getenv('AUTHOR_RESTRICT') in ['true', 'True']
authorized_authors = os.getenv('AUTHORIZED_AUTHORS').split(',')
authorized_roles = os.getenv('AUTHORIZED_ROLES').split(',')

fields = []

footer = obs_api.ObsFooter('footer', 'Footer')
fields.append(footer)

field_top = obs_api.ObsField('field_top', 'Top field')
fields.append(field_top)

client = discord.Client()

@client.event
async def on_message(message):
	channel = message.channel

	no_command = False
	
	if message.author == client.user or channel != discord_channel:
		return

	msg = message.content.split(' ',3)

	if msg[0].startswith(TRIGGER_HELP):
		await channel.send(help().format(message))

	elif msg[0].startswith(TRIGGER):

		#Commands with 4 minimum arguments (Trigger + command + field id + message)
		if len(msg) > 3:
			field_pos = get_field(msg[2])

			if field_pos != -1:
				if msg[1] == COMMAND_ADD:
					await channel.send(add_message(field_pos, message.author, msg[3]).format(message))

				elif msg[1] == COMMAND_RM:
					await channel.send(remove_message(field_pos, message.author, msg[3]).format(message))

			else:
				no_command = True

		#Commands with 2 minimum arguments (Trigger + command)
		elif len(msg) > 1:

			if msg[1] == COMMAND_STOP:
				if check_authorization(message.author):
					await channel.send('{0.author.mention}, o bot vai desligar'.format(message))
					quit()
				
				await channel.send('{0.author.mention}, não tens autorização para desligar o bot'.format(message))

			elif msg[1] == COMMAND_ENUM:
				await channel.send(get_all_message_ids(message).format(message))

			else:
				no_command = True

		else:
			no_command = True

		if no_command == True:
			await channel.send(('{0.author.mention}, comando inválido\n' + commands_msg()).format(message))

def get_field(field_id):
	for i in range(len(fields)):

		if field_id == fields[i].field_id:
			return i

	return -1

def check_authorization(author):
	if author.name in authorized_authors or author_restrict == False:
		return True

	for i in author.roles:
		if i.name in authorized_roles:
			return True

	return False

def add_message(field_pos, author, msg):

	if check_authorization(author):

		result = fields[field_pos].add_message(author.id, msg)

		if result:
			return ('{0.author.mention} Mensagem adicionada!')

		return ('{0.author.mention} Ocorreu um erro, mensagem não adicionada')
	
	return ('{0.author.mention} Não tens autorização para adicionar mensagens, mensagem não adicionada')

def remove_message(field_pos, author, msg):
	if isinstance(fields[field_pos], ObsFooter):
		id_msg = int(msg.split(COMMAND_RM,1)[1])-1

	if check_authorization(author):

		result = fields[field_pos].remove_message(id_msg)

		return ('{0.author.mention} Mensagem apagada!')
	
	return ('{0.author.mention} Não tens autorização para eliminar mensagens, mensagem não apagada')

def get_all_message_ids(message):
	msg = "Mensagens introduzidas em todos os campos:\n"

	for field in fields:
		msg += '**' + field.field_name + '**' + ' *(id: ' + field.field_id + ')*'+ '\n'
		msg += field.get_message_ids()

	return msg.format(message)

def help():
	return obs_api.help(author_restrict)

def commands_msg():
	return obs_api.commands_msg(author_restrict)

@client.event
async def on_ready():
	global discord_channel
	discord_channel = client.get_channel(int(os.getenv('CHANNEL_ID')))

	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	
	msg = '**Vai começar um livestream da VOST!**\n'
	
	await discord_channel.send(msg + commands_msg())

client.run(os.getenv('DISCORD_TOKEN'))
