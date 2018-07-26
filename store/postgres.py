from store.dblayer import DBLayer, DuplicateError
import asyncpg


class PGWrapper(DBLayer):
	async def _connect(self):
		return await asyncpg.connect(dsn = self._credentials.uri)

	async def execute(self, sql, *args):
		conn = None
		try:
			conn = await self._connect()
			await conn.execute(sql, *args)
		except asyncpg.UniqueViolationError as e:
			raise DuplicateError()
		finally:
			if conn:
				await conn.close()

	async def fetchone(self, sql, *args):
		conn = None 
		row = None 
		try:
			conn = await self._connect()
			row = await conn.fetchrow(sql, *args)
		#except Exception as e:
		#	pass 
			# gonna need to detect duplicate primary key exceptions here
		finally:
			if conn:
				await conn.close()
		return row 
	async def fetch(self, sql, *args):
		conn = None 
		result = None 
		try:
			conn = await self._connect()
			result = await conn.fetch(sql, *args)
		#except Exception as e:
		#	pass 
			# gonna need to detect duplicate primary key exceptions here
		finally:
			if conn:
				await conn.close()
		return result 
