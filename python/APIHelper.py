import requests

# Element type vars
DATABASE, PAGE, BLOCK, USER = 0, 1, 2, 3

# A class to simplify interaction with notion's API by using Block objects
class APIHelper(object):

	# Provide auth_key and version at init
	def __init__(self, auth_key, version):
		self.auth_key = auth_key
		self.version = version

		# Set default headers w/ authkey + version
		self.default_headers = {
				"Authorization" : "Bearer " + self.auth_key,
				"Notion-Version" : self.version
			}

	# Generate endpoint url
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

	# Create new page on Notion
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

		# Link provided page with the Notion instance
		page.link_notion(uuid = page_id)

		# Return the response object
		return response