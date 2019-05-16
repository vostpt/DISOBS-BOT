import discord, os
from os.path import join, dirname
from dotenv import load_dotenv

TRIGGER_ADD = '!type '
TRIGGER_RM = '!type rm'
TRIGGER_ENUM = '!type id'
TRIGGER_HELP = '?type'
TRIGGER_STOP = '!type stop'
MSG_SEPARATOR = '|'
MSG_FINAL_SEPARATOR = '                                     '

dotenv_path = join(dirname(__file__), 'keys.env')
load_dotenv(dotenv_path)

author_restrict = os.getenv('AUTHOR_RESTRICT') in ['true', 'True']
authorized_authors = os.getenv('AUTHORIZED_AUTHORS').split(',')
authorized_roles = os.getenv('AUTHORIZED_ROLES').split(',')

footer_content_list = []
client = discord.Client()

@client.event
async def on_message(message):
	channel = message.channel
	
	if message.author == client.user or channel != discord_channel:
		return

	elif message.content.startswith(TRIGGER_STOP):
		if check_authorization(message.author):
			await channel.send('{0.author.mention}, o bot vai desligar'.format(message))
			quit()
		
		await channel.send('{0.author.mention}, não tens autorização para desligar o bot'.format(message))

	elif message.content.startswith(TRIGGER_RM):
		await channel.send(remove_footer(message))

	elif message.content.startswith(TRIGGER_ENUM):
		await channel.send(get_message_ids(message))

	elif message.content.startswith(TRIGGER_ADD):
		await channel.send(add_footer(message))

	elif message.content.startswith(TRIGGER_HELP):
		await channel.send(help(message))

def check_authorization(author):
	if author.name in authorized_authors or author_restrict == False:
		return True

	for i in author.roles:
		if i.name in authorized_roles:
			return True

	return False

def add_footer(message):
	author = message.author

	if check_authorization(author):
		msg = message.content.split(TRIGGER_ADD,1)[1]
		footer_content_list.append([author, msg])
		write_to_file()
		return ('{0.author.mention} Mensagem adicionada: ' + msg).format(message)
	
	return ('{0.author.mention} Não tens autorização para adicionar mensagens, mensagem não adicionada').format(message)

def remove_footer(message):
	msg = message.content.split(TRIGGER_RM,1)[1]
	id_msg = int(msg)-1
	
	if id_msg > len(footer_content_list):
		return ('{0.author.mention} ID inválido, tenta outra vez!\n').format(message) + help(message)
	
	elif check_authorization(message.author):
		del footer_content_list[id_msg]
		write_to_file()
		return ('{0.author.mention} Mensagem apagada!').format(message)
	
	return ('{0.author.mention} Não tens autorização para eliminar mensagens, mensagem não apagada').format(message)

def get_message_ids(message):
	if len(footer_content_list) < 1:
		return ('Não há mensagens inseridas no rodapé')
	
	msg = 'Lista de mensagens inseridas no rodapé: \n'
	msg += '<autor> - <id> - <mensagem>\n'
	
	for content in footer_content_list:
		msg += ('<@' + str(content[0].id) + '>' + ' - ' + str(footer_content_list.index(content)+1) + ' - "' + content[1] + '"\n')
	
	return msg.format(message)

def write_to_file():
	footer = ''
	
	if len(footer_content_list) > 0:
		for i in range(len(footer_content_list)-1):
			footer += footer_content_list[i][1] + ' ' + MSG_SEPARATOR + ' '
		
		footer += footer_content_list[len(footer_content_list)-1][1] + MSG_FINAL_SEPARATOR
	
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
		msg += '**Comandos permitidos apenas para users autorizados:**\n'
	
	msg += '!type <mensagem> - Envia uma mensagem para rodapé\n'
	msg += '!type rm <id> - Remove uma mensagem de rodapé\n'
	msg += '!type stop - Desliga o bot\n'
	
	return msg

@client.event
async def on_ready():
	write_to_file()
	global discord_channel
	discord_channel = client.get_channel(int(os.getenv('CHANNEL_ID')))
	
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	
	msg = '**Vai começar um livestream da VOST!**\n'
	
	await discord_channel.send(msg + commands_msg())

client.run(os.getenv('DISCORD_TOKEN'))
