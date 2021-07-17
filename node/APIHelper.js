const axios = require('axios')

const [DATABASE, PAGE, BLOCK, USER] = [0, 1, 2, 3]
console.log(DATABASE)

class APIHelper {
	constructor(auth_key, version){
		this.notion = axios.create({
			baseURL: "https://api.notion.com/v1/",
			headers:{
				"Authorization" : `Bearer ${String(auth_key)}`,
				"Notion-Version" : String(version)
			}
		})
	}

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

	async create_page(page){
		if (page.linked == false || page.parent_type == undefined || page.parent_id == undefined) {
			console.log("ERROR - provided page wasn't properly linked, the page must have a parent id and type");
			return
		}

		let endpoint = this.get_endpoint(PAGE);
		const response = await this.notion.post(endpoint, page.get_json(false), {
			headers: {
				"Content-Type": "application/json"
			}
		})

		page.link_notion({uuid: String(response.data['id'])});

	}
}
module.exports = {
	APIHelper,
	DATABASE,
	PAGE,
	BLOCK,
	USER
}