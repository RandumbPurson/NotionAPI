import requests

# Element type vars
DATABASE, PAGE, BLOCK, USER = 0, 1, 2, 3

# A class to simplify interaction with notion's API by using Block objects
class NotionAPI(object):

	# Provide auth_key and version at init
	def __init__(self, auth_key, version):
		self.auth_key = auth_key
		self.version = version

		# Set default headers w/ authkey + version
		self.default_headers = {
				"Authorization" : "Bearer " + self.auth_key,
				"Notion-Version" : self.version
			}

	# Combine root url and type/url
	def get_endpoint(self, element_type, element_id = ""):
		'''
		element_type string conversion:
			DATABASE = "databases"
			PAGE = "pages"
			BLOCK = "blocks"
			USER = "users"
		'''
		element_types = ["databases", "pages", "blocks", "users"]

		root = "https://api.notion.com/v1/"
		endpoint = root + element_types[element_type] + "/" + element_id
		
		return endpoint

	# Get element as a dict 
	def get_element(self, element_type, element_id = "", page_size=100):

		# Get endpoint url
		endpoint = self.get_endpoint(element_type, element_id)
		if element_type == BLOCK: # Add tail to url for getting block children
			endpoint = endpoint + "/children?page_size="+str(page_size)

		# Perform https get
		response = requests.get(endpoint, headers = self.default_headers)

		return response.json()

	# Create Page
	def create_page(self, page):

		# If the provided page object is missing the linking attributes, return with an error message
		if page.linked == False or not (hasattr(page, 'parent_type') or hasattr(page, 'parent_id')):
			print("ERROR - provided page wasn't properly linked, the page must have a parent id and type")
			return

		# Get endpoint url
		endpoint = self.get_endpoint(PAGE)
		# Update headers for the json dump
		headers = self.default_headers
		headers.update({"Content-Type": "application/json"})

		# Perform https post
		response = requests.post(endpoint, headers=headers, json=page.get_json())

		# Set page uuid to the uuid of the generated page
		page_id = str(response.json()["id"])
		page.link_notion(uuid = page_id)

		# Return the response object
		return response

# Provides common json structures 
class Structures(object):

	# Provides the value of a JSON "text" key-value pair
	def text(text, link=None):
		# set content to the provided text
		json_dict = {"content": text}
		# if a link is provided, add the link to the structure
		if not link is None:
			json_dict.update({"link": link})
		return json_dict

	# Provides the value of a JSON "rich-text" key-value pair
	def rich_text(text, link = None, bold = False, italic = False, strikethrough = False, underline = False, code = False, color = "default"):
		# create basic structure
		json_dict =
			{
				"type": "text",
				"text": Structures.text(text, link),
				"annotations": {
					"color": color
				}
			}

		# a dict of all possible annotations
		annotations = {"bold": bold, "italic": italic, "strikethrough": strikethrough, "underline": underline, "code": code}

		# remove any key-value pairs from 'annotations' that is default
		for arg in annotations:
			if annotations[arg] == False:
				del annotations[arg]

		# update the final dict with all the annotations that were modified
		json_dict["annotations"].update(annotations)
		return json_dict

# Basic element in notion
class Block(Structures):

	# Requires block type at init
	def __init__(self, block_type, content = {}, metadata = {}):
		self.type = block_type

		self.content = content
		self.metadata = metadata
		
		# if type isn't specified in content and the block isn't a page
		#   create basic type structure
		if not self.type in self.content.keys() and self.type != "child_page":
			self.content[self.type] = {}

		# all blocks initially unlinked
		self.linked = False

	# get properties in a properly formatted JSON obj
	def get_json(self, content_only = True):
		# set content as output
		json_dict = self.content
		# if content_only = False, update JSON dict with stored metadata
		if not content_only:
			json_dict.update(metadata)
			# if properly linked and has a uuid, update JSON dict
			if self.linked and not self.uuid is None:
				json_dict["id"] = self.uuid 

		return json_dict
 	
 	# Set text property
	def set_text(self, text):
		self.content[self.type].update(
			{
				"rich_text":[rich_text(text)]
			})

	# Set arbitrary property 'key' to generic value 'val'
	def set_prop(self, key, val):
 		self.content.update({key : val})

 	# Set linking variables
	def link_notion(self, uuid = None, parent_type = -1, parent_id = None):

		self.uuid = uuid
		self.parent_type = parent_type
		self.parent_id = parent_id

		self.link_data = {}
		# if uuid provided, add to 'link_data'
		if not uuid is None:
			self.link_data.update(
				{
					"id": self.uuid
				})

		self.linked = True

# Page object
class Page(Block):

	# No required parameters
	def __init__(self, properties = {}, children = []):
		# set content to provided values
		content = {"properties":properties, "children":children}

		super().__init__("child_page", content)

	# Set the title property
	def set_title(self, title):
		  self.content["properties"].update(
		  	{
		  	"title": {
			  	"title": [
			  		{
			  			"type": "text",
			  			"text":Structures.text(title)
			  		}]
		  		}
		  	})

	# Set arbitrary property 'key' to generic value 'val'
	def set_prop(self, key, val):
 		self.content["properties"].update({key : val})

 	# Set linking variables and proper content/metadata
	def link_notion(self, uuid = None, parent_type = -1, parent_id = None):
		# Set linking vars
		super().link_notion(uuid, parent_type, parent_id)

		'''
		element_type string conversion:
			DATABASE = "database_id"
			PAGE = "page_id"
		'''
		parent_types = ["database_id", "page_id"]

		# if parent type and id are provided, add to 'link_data'
		if not (parent_type is None or parent_id is None):
			self.link_data.update(
				{
					"parent": {
						parent_types[parent_type]: parent_id
					}
				})

		# if parent is a datbase, get the schema
		if self.parent_type == DATABASE:
 			schema = NotionAPI.get_element(DATABASE, parent_id)["properties"].keys()
 			print(schema)


