import asyncpg
from asyncpg import UniqueViolationError

class DuplicateError(Exception):
	pass

class DBLayer(object):
	def __init__(self, credentials):
		self._credentials = credentials