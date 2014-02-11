import dropbox
import config
import json

class Path:
	def files():
		raise NotImplementedError

	def modified_at():
		raise NotImplementedError

class File:
	def url():
		raise NotImplementedError

	def modified_at():
		raise NotImplementedError

class DropboxFile(File):
	def __init__(dct):
		self._dct = dct

	@property
	def name(self):
		return self._dct['']


class DropboxPath(Path):
	def __init__(client):
		self._client = client

	def files(self):
		metadata = json.loads(self._client.metadata(config.dropbox_folder))
		return filter(lambda l: l['is_dir']==False, metadata['contents'])

	def modified_at():
		pass