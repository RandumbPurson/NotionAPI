const axios = require('axios')

// Element type vars
const [DATABASE, PAGE, BLOCK, USER] = [0, 1, 2, 3]

// A class to simplify interaction with notion's API by using Block objects

class Integration {

	// Provide auth_key and version at init
	constructor(auth_key, version){
		this.notion = axios.create({
			baseURL: "https://api.notion.com/v1/",
			headers:{ // Set default headers w/ authkey + version
				"Authorization" : `Bearer ${String(auth_key)}`,
				"Notion-Version" : String(version)
			}
		})
	}

	// Generate endpoint url
	get_endpoint(element_type, element_id = ""){
		/*
		element_type string conversion:
			DATABASE = "databases"
			PAGE = "pages"
			BLOCK = "blocks"
			USER = "users"
		*/

		const element_types = ["databases", "pages", "blocks", "users"];

		return element_types[element_type] + "/" + String(element_id);
	}

	// Get element as JSON 
	async get_element(element_type, element_id = "", page_size=100){
		//Get endpoint url
		var endpoint = this.get_endpoint(element_type, element_id);
		if (element_type == BLOCK) { // Add tail to url for getting block children
			endpoint = `${endpoint}/children?page_size=${String(page_size)}`;
		}
		//Perform https get
		const response = await this.notion.get(endpoint);
		return response;
	}

	// Create new page on Notion
	async create_page(page){
		// If the provided page object is missing the linking attributes, return with an error message
		if (page.linked == false || page.parent_type == undefined || page.parent_id == undefined) {
			console.log("ERROR - provided page wasn't properly linked, the page must have a parent id and type");
			return
		}

		// Get endpoint url
		let endpoint = this.get_endpoint(PAGE);
		// perform https post with proper headers
		const response = await this.notion.post(endpoint, page.get_json(false), {
			headers: {
				"Content-Type": "application/json"
			}
		})

		// Link provided page with the Notion instance
		page.link_notion({uuid: String(response.data['id'])});

	}
}

module.exports = {
	Integration,
	DATABASE,
	PAGE,
	BLOCK,
	USER
}