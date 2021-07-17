const { Notion, DATABASE, PAGE,
	BLOCK,
	USER } = require('./APIHelper');
const {text, rich_text, Block, Page} = require('./structures');

module.exports = {
	Notion,
	DATABASE,
	PAGE,
	BLOCK,
	USER,
	
	text, 
	rich_text, 
	Block, 
	Page
}