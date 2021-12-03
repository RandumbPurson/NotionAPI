const { 
	Integration, 
	DATABASE, 
	PAGE, 
	BLOCK,
	USER 
} = require('./integration');
const {text, rich_text, Block, Page} = require('./structures');

module.exports = {
	Integration,
	DATABASE,
	PAGE,
	BLOCK,
	USER,
	
	text, 
	rich_text, 
	Block, 
	Page
}