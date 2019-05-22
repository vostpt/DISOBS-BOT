MSG_SEPARATOR = '|'
MSG_FINAL_SEPARATOR = '                                     '

class ObsFooter:

	def __init__(self, field_id, field_name=''):

		self.field_id = field_id

		if field_name != '':
			self.field_name = field_id

		self.field_name = field_name
		self.file_name = field_id + '.txt'
		self.content_list = []

		write_to_file(self.file_name)

	def add_message(self, author_id, message):
		self.content_list.append([author_id, message])
		self.parse_to_file()

		return True

	def remove_message(self, msg_id):
		
		if msg_id > len(self.content_list):
			return False

		del self.content_list[msg_id]
		self.parse_to_file()

		return True

	def get_message_ids(self):
		if len(self.content_list) < 1:
			return ('Não há mensagens inseridas no rodapé\n')
		
		msg = 'Lista de mensagens inseridas no rodapé: \n'
		msg += '<autor> - <id> - <mensagem>\n'
		
		for content in self.content_list:
			msg += ('<@' + str(content[0]) + '>' + ' - ' + str(self.content_list.index(content)+1) + ' - "' + content[1] + '"\n')

		return msg

	def parse_to_file(self):
		footer = ''

		for i in range(len(self.content_list)-1):
			footer += self.content_list[i][1] + ' ' + MSG_SEPARATOR + ' '
		
		footer += self.content_list[len(self.content_list)-1][1] + MSG_FINAL_SEPARATOR

		write_to_file(self.file_name, footer)

class ObsField:

	def __init__(self, field_id, field_name=''):

		self.field_id = field_id

		if field_name != '':
			self.field_name = field_id

		self.field_name = field_name
		self.file_name = field_id + '.txt'
		self.content = []

		write_to_file(self.file_name)

	def add_message(self, author_id, message):
		self.content = [author_id, message]
		self.parse_to_file()

		return True

	def remove_message(self, msg_id=0):
		
		if len(self.content) < 2:
			return False

		self.content = []
		self.parse_to_file()

		return True

	def get_message_ids(self):
		if len(self.content) < 2:
			return ('Não há mensagens inseridas no campo\n')
		
		msg = 'Mensagem inserida no campo: \n'
		msg += '<autor> - <mensagem>\n'
		
		msg += ('<@' + str(self.content[0]) + '>' + ' - "' + self.content[1] + '"\n')

		return msg

	def parse_to_file(self):
		write_to_file(self.file_name, self.content[1])


def write_to_file(file_name, content=''):

	file = open(file_name, "w")
	file.write(content)
	file.close()

def help(author_restrict):
	msg = '{0.author.mention} Aqui tens os comandos:\n'
	
	return msg + commands_msg(author_restrict)

def commands_msg(author_restrict):
	msg = '**Comandos permitidos para todos:**\n?type - Mostra os comandos disponíveis\n'
	msg += '!type id - Mostra todos os campos (nos campos do tipo rodapé também é exibido o id das mensagens)\n'

	if author_restrict == True:
		msg += '**Comandos permitidos apenas para users autorizados:**\n'

	msg += '!type add <id campo> <mensagem> - Envia uma mensagem para rodapé\n'
	msg += '!type rm <id campo> <id mensagem> - Remove uma mensagem de rodapé\n'
	msg += '!type stop - Desliga o bot\n'
	
	return msg
