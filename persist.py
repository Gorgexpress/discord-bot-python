from botcommand import BotCommand
savecmd = 'INSERT INTO commands (command, response, count) VALUES ($1, $2, $3)'
getcmd = 'SELECT response, count FROM commands WHERE command = $1'
updatecmd = 'UPDATE commands SET count = $1 WHERE command = $2'
top10 = "SELECT command, count FROM commands ORDER BY count DESC LIMIT 10"
randomcmd = "SELECT response, command FROM commands ORDER BY RANDOM() LIMIT 1"
class Persist(object):
	def __init__(self):
		pass
    
	async def save(self, storage, obj):
		try:
			await storage.execute(savecmd, obj.command, obj.response, obj.count)
		except Exception as e:
			raise e
	
	async def get(self, storage, key):
		row = await storage.fetchone(getcmd, key)
		if row:
			botcommand = BotCommand(key, row['response'], row['count'])
		else:
			return None
		return botcommand

	async def update(self, storage, obj):
		await storage.execute(updatecmd, obj.count, obj.command)

	async def gettop10(self, storage):
		result = await storage.fetch(top10)
		return [BotCommand(row['command'], '', row['count']) for row in result]
	
	async def random(self, storage):
		result = await storage.fetchone(randomcmd)
		return BotCommand(result['command'], result['response'], 0)