from config import config
import requests

class boxdoterror:
	def __init__(self, e):
		self._type = e['type']
		self._status = e['status']
		self._code = e['code']
		self._help_url = e['help_url']
		self._message = e['message']
		self._request_id = e['request_id']

class boxdotcom:
	def __init__(self, access_token):
		self._access_token = access_token
		return self

	def get_folder(self, path):
		
		path = path.split('/')

		params = {'access_token': c.config['box_token']}
		parent_id = 0
		for foldername in path:
			r = requests.get(
				'{}/folders/{}/items'.format(config['box_api'], parent_id),
				params=params
			)

			if r.status_code != requests.codes.ok:
				raise boxdoterror(r.json())

			children = {entry['name']: entry for entry in r.json()['entries']}

			if foldername in children:
				parent_id = children[foldername]['id']

			else:
				raise "folder not found: {}".format(foldername)
			

class boxdotfolder:

	def __init__(self):

		self._type 	
		# string
		# For folders is ‘folder’

		self._id   	
		# string
		# The folder’s ID.

		self._sequence_id 
		# string
					# A unique ID for use with the /events endpoint.
					# May be null for some folders such as root or trash.

		self._etag
		# string
					# A unique string identifying the version of this folder.
					# May be null for some folders such as root or trash.
		
		self._name	
		# string
					# The name of the folder.

		self._created_at  
		# timestamp
					# The time the folder was created.
					# May be null for some folders such as root or trash.

		self._modified_at 
		# timestamp
					# The time the folder or its contents were last modified.
					# May be null for some folders such as root or trash.

		self._description 
		# string
					# The description of the folder.

		self._size	
		# integer
					# The folder size in bytes. Be careful parsing this integer,
					# it can easily go into EE notation: see IEEE754 format.

		self._path_collection 
		# collection
					# The path of folders to this item, starting at the root.
		
		self._created_by
		# mini user object
					# The user who created this folder.

		self._modified_by 
		# mini user object
					# The user who last modified this folder.

		self._trashed_at 
		# timestamp
					# The time the folder or its contents were put in the trash.
					# May be null for some folders such as root or trash.
		
		self._purged_at  
		# timestamp
					# The time the folder or its contents were purged from the trash.
					# May be null for some folders such as root or trash.

		self._content_created_at 
		# timestamp
					# The time the folder or its contents were originally created (according to the uploader).
					# May be null for some folders such as root or trash.
		
		self._content_modified_at 
		# timestamp
					# The time the folder or its contents were last modified (according to the uploader).
					# May be null for some folders such as root or trash.
		
		self._owned_by 
		# mini user object
					# The user who owns this folder.
		
		self._shared_link 
		# object
					# The shared link for this folder. Null if not set.

		self._folder_upload_email 
		# object
					# The upload email address for this folder. Null if not set.
		
		self._parent 
		# mini folder object
					# The folder that contains this one.
					# May be null for folders such as root, trash and child folders whose parent is inaccessible.
		
		self._item_status 
		# string
					# Whether this item is deleted or not.
		
		self._item_collection 
		# collection
					# A collection of mini file and folder objects contained in this folder.
		
		# http://developers.box.com/docs/#folders-retrieve-a-folders-items
		# Attributes listed below will not appear 
		# in default folder requests and must be
		# explicitly asked for using the fields parameter.

		# self._sync_state 
		# string
					# Whether this folder will be synced by the Box sync clients or not. Can be synced, not_synced, or partially_synced.
		
		# self._has_collaborations 
		# boolean
					# Whether this folder has any collaborators.
		
		# self._permissions 
		# object
					# The permissions that the current user has on this folder. The keys are can_download, can_upload, can_rename, can_delete, can_share, can_invite_collaborator, and can_set_share_access. Each value is a boolean.
		
		# self._tags	
		# array of strings
					# All tags applied to this folder.

		return self

class boxdotfile:
        def __enter__(self):
            return thing
        def __exit__(self, type, value, traceback):
        	pass
        def get_file(path):
        	pass

class boxdot:
	def __init__():
		pass