# Provides common json structures 
class BasicStructures(object):

	# Provides the value of a JSON "text" key-value pair
	def text(text, link=None):
		# set content to the provided text
		text_obj = {"content": text}
		# if a link is provided, add the link to the structure
		if not link is None:
			text_obj.update({"link": link})
		return text_obj

	# Provides the value of a JSON "rich-text" key-value pair
	def rich_text(text, link = None, bold = False, italic = False, strikethrough = False, underline = False, code = False, color = "default"):
		# create basic structure
		rich_text_obj =
			{
				"type": "text",
				"text": BasicStructures.text(text, link),
				"annotations": {
					"color": color
				}
			}

		# a dict of all possible annotations
		annotations = {
			"bold": bold, 
			"italic": italic, 
			"strikethrough": strikethrough, 
			"underline": underline, 
			"code": code
		}

		# remove any key-value pairs from 'annotations' that is default
		for arg in annotations:
			if annotations[arg] == False:
				del annotations[arg]

		# update the final dict with all the annotations that were modified
		rich_text_obj["annotations"].update(annotations)
		return rich_text_obj

# Basic element in notion
class Block(BasicStructures):

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
	def link_notion(self, uuid = None, parent_type = None, parent_id = None):

		self.uuid = uuid
		self.parent_type = parent_type
		self.parent_id = parent_id

		self.link_data = {}

		'''
		element_type string conversion:
			DATABASE = "database_id"
			PAGE = "page_id"
		'''
		parent_types = ["database_id", "page_id"]

		# if uuid provided, add to 'link_data'
		if not uuid is None:
			self.link_data.update(
				{
					"id": self.uuid
				})

		# if parent type and id are provided, add to 'link_data'
		if (not self.parent_type is None and not self.parent_id is None):
			self.link_data.update(
				{
					"parent": {
						parent_types[self.parent_type]: self.parent_id
					}
				})

		self.linked = True



# Page object
class Page(Block):

	# No required parameters
	def __init__(self, properties = {}, children = []):
		# set content to provided values
		self.content = {"properties":properties, "children":children}

		super().__init__("child_page", content)

	# Set the title property
	def set_title(self, title):
		  self.content["properties"].update(
		  	{
		  	"title": {
			  	"title": [
			  		{
			  			"type": "text",
			  			"text":BasicStructures.text(title)
			  		}]
		  		}
		  	})

	# Set arbitrary property 'key' to arbitrary value 'val'
	def set_prop(self, key, val):
 		self.content["properties"].update({key : val})


