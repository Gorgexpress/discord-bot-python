from store.dblayer import DBLayer, DuplicateError
import aiosqlite


class SQLite3Wrapper(DBLayer):
	async def _connect(self):
		return await aiosqlite.connect(self._credentials.uri)

	async def execute(self, sql, *args):
		conn = None
		try:
			async with aiosqlite.connect(self._credentials.uri) as conn:
				await conn.execute(sql, [*args])
		except Exception as e:
			print(repr(e))
			raise Exception from e

	async def fetchone(self, sql, *args):
		row = None 
		try:
			async with aiosqlite.connect(self._credentials.uri) as conn:
				row = await conn.fetchrow(sql, [*args])
		except Exception as e:
			pass 
			# gonna need to detect duplicate primary key exceptions here
		return row 
	async def fetch(self, sql, *args):
		result = None 
		try:
			async with aiosqlite.connect(self._credentials.uri) as conn:
				result = await conn.fetch(sql, [*args])
		except Exception as e:
			pass 
			# gonna need to detect duplicate primary key exceptions here
		return result 
