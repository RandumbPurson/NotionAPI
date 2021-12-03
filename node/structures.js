const util = require('util')

// Provides common json structures 
class BasicStructures {

	// Provides the value of a JSON "text" key-value pair
	static text(text, link=undefined){
		// set content to the provided text
		var text_obj = {"content": text}
		// if a link is provided, add the link to the structure
		if (link !== undefined){
			text_obj["link"] = link;
		}
		return text_obj
	}

	// Provides the value of a JSON "rich-text" key-value pair
	static rich_text(text, {bold = false, italic = false, strikethrough = false, underline = false, code = false, color = "default"} = {}, link = undefined){
		// create basic structure
		var rich_text_obj = {
				"type": "text",
				"text": BasicStructures.text(text, link),
				"annotations": {
					"color": color
				}
			}

		// a dict of all possible annotations
		var annotations = {
			"bold": bold, 
			"italic": italic, 
			"strikethrough": strikethrough, 
			"underline": underline, 
			"code": code
		}

		// remove any key-value pairs from 'annotations' that is default
		for (var arg in annotations){
				if (annotations[arg] == false) {
					delete annotations[arg]
				}
		}

		// update the final dict with all the annotations that were modified
		rich_text_obj["annotations"] = annotations;
		return rich_text_obj
	}
}

// Basic element in notion
class Block extends BasicStructures {

	// Requires block type at init
	constructor(block_type, content = {}, metadata = {}){
		super();
		this.type = block_type;

		this.content = content;
		this.metadata = metadata;

		// if type isn't specified in content and the block isn't a page
		//  create basic type structure
		if (!(this.type in this.content) && this.type !== "child_page") {
			this.content[this.type] = {};
		}

		// all blocks initially unlinked
		this.linked = false;
	}

	// get properties in a properly formatted JSON obj
	get_json(content_only=true) {
		// set default out to content
		var json_obj = this.content;

		// if content_only = false, include metadata && uuid
		if (!content_only){
			json_obj = Object.assign(json_obj, this.metadata);
			if (this.linked == true){
				console.log('link data2:' + util.inspect(this.link_data,  {showHidden: false, depth: null}));
				json_obj = Object.assign(json_obj, this.link_data);
				if (this.uuid !== undefined){
					json_obj['id'] = this.uuid;
				}
			}
		}
		console.log(json_obj)
		return json_obj

	}

	// Set text property
	set_text(text) {
		this.content[this.type]['rich_text'] = [rich_text(text)];
	}
	// Set arbitrary property 'key' to 'val'
	set_prop(key, val) {
		this.content[key] = val;
	}

	// Set linking vars
	link_notion({uuid = undefined, parent_type = undefined, parent_id = undefined} = {}) {
		console.log(`${parent_type} : ${parent_id}`)
		this.uuid = uuid;
		this.parent_type = parent_type;
		this.parent_id = parent_id;

		this.link_data = {};
		/*
		element_type string conversion:
			DATABASE = "database_id"
			PAGE = "page_id"
		*/
		var parent_types = ["database_id", "page_id"];

		// if uuid provided add to link data
		if (this.uuid !== undefined) {
			this.link_data['id'] = this.uuid;
		}

		// if parent type and id are provided, add to 'link_data'
		if (this.parent_type !== undefined && this.parent_id !== undefined){
			var type = parent_types[this.parent_type];
			this.link_data = {
				'parent': {}
			};
			this.link_data['parent'][type] = this.parent_id;
		}
		this.linked = true;

		// console.log('link data:' + util.inspect(this.link_data,  {showHidden: false, depth: null}));
	}
}

// PAge object
class Page extends Block{
	constructor(properties = {}, children = []) {
		//set content to provided values
		super("child_page", {"properties": properties, "children": children});
	}

	// Set the title property
	set_title(title){
		this.content["properties"]["text"] = {
		  	"title": [
		  		{
		  			"type": "text",
		  			"text": BasicStructures.text(title)
		  		}]
		}
	}

	// Set arbitrary property 'key' to arbitrary value 'val'
	set_prop(key, val){
		this.content['properties'][key] = val;
	}
}

module.exports = {
	text: BasicStructures.text,
	rich_text: BasicStructures.rich_text,
	Block,
	Page
}