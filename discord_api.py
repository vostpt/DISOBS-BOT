import discord, os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)
author_restrict = os.getenv('AUTHOR_RESTRICT') in ['true', 'True']
authorized_authors = os.getenv('AUTHORIZED_AUTHORS').split(',')
authorized_roles = os.getenv('AUTHORIZED_ROLES').split(',')

client = discord.Client()
message_list = []
trigger_add = '!type '
trigger_rm = '!type rm'
trigger_enum = '!type id'
trigger_help = '?type'
trigger_stop = '!type stop'
msg_separator = '|'
msg_final_separator = '                                     '

@client.event
async def on_message(message):
	channel = message.channel
	# we do not want the bot to reply to itself
	if message.author == client.user or channel != channel_obs:
		return

	elif message.content.startswith(trigger_stop):
		if checkAuthorization(message.author):
			await channel.send('{0.author.mention}, o bot vai desligar'.format(message))
			quit()
		await channel.send('{0.author.mention}, não tens autorização para desligar o bot'.format(message))

	elif message.content.startswith(trigger_rm):
		await channel.send(removeFooter(message))

	elif message.content.startswith(trigger_enum):
		await channel.send(showFooterMsgId(message))

	elif message.content.startswith(trigger_add):
		await channel.send(addFooter(message))

	elif message.content.startswith(trigger_help):
		await channel.send(help(message))

def checkAuthorization(author):
	if author.name in authorized_authors or author_restrict == False:
		return True
	for i in author.roles:
		if i.name in authorized_roles:
			return True
	return False

def addFooter(message):
	author = message.author
	if checkAuthorization(author):
		msg = message.content.split(trigger_add,1)[1]
		message_list.append([author, msg])
		writeOnFile()
		return ('{0.author.mention} Mensagem adicionada: ' + msg).format(message)
	return ('{0.author.mention} Não tens autorização para adicionar mensagens, mensagem não adicionada').format(message)

def removeFooter(message):
	msg = message.content.split(trigger_rm,1)[1]
	id_msg = int(msg)-1
	if id_msg > len(message_list):
		return ('{0.author.mention} ID inválido, tenta outra vez!\n').format(message) + help(message)
	elif checkAuthorization(message.author):
		del message_list[id_msg]
		writeOnFile()
		return ('{0.author.mention} Mensagem apagada!').format(message)
	return ('{0.author.mention} Não tens autorização para eliminar mensagens, mensagem não apagada').format(message)

def showFooterMsgId(message):
	if len(message_list) < 1:
		return ('Não há mensagens inseridas no rodapé')
	resp = 'Lista de mensagens inseridas no rodapé: \n'
	resp += '<autor> - <id> - <mensagem>\n'
	for x in message_list:
		resp += ('<@' + str(x[0].id) + '>' + ' - ' + str(message_list.index(x)+1) + ' - "' + x[1] + '"\n')
	return resp.format(message)

def writeOnFile():
	footer = ''
	if len(message_list) > 0:
		for i in range(len(message_list)-1):
			footer += message_list[i][1] + ' ' + msg_separator + ' '
		footer += message_list[len(message_list)-1][1] + msg_final_separator
	file = open("footer.txt", "w")
	file.write(footer)
	file.close()

def help(message):
	msg = '{0.author.mention} Aqui tens os comandos:\n'
	return (msg + commands_msg()).format(message)

def commands_msg():
	msg = '?type - Mostra os comandos disponíveis\n'
	msg += '**Comandos permitidos para todos:**\n!type id - Mostra os ids das mensagens\n'
	if author_restrict == True:
		msg += '**Comandos para users autorizados:**\n'
	msg += '!type <mensagem> - Envia uma mensagem para rodapé\n'
	msg += '!type rm <id> - Remove uma mensagem de rodapé\n'
	msg += '!type stop - Desliga o bot\n'
	return msg

@client.event
async def on_ready():
	writeOnFile()
	global channel_obs
	channel_obs = client.get_channel(int(os.getenv('CHANNEL_ID')))
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	msg = '**Vai começar um livestream da VOST!**\n'
	await channel_obs.send(msg + commands_msg())

client.run(os.getenv('DISCORD_TOKEN'))