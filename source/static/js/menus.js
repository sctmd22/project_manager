const MENU_HELPERS = function(){
	
	//Displays the correct sidebar nav-item and nav-link as being open and/or active
	(function(){
		//pageData is passed in index.html
		const pageData = page_data_json;
	
		const CLASS_NAME_MENU_OPEN = 'menu-open';
		const CLASS_MENU_LINK_ACTIVE = 'active';
		
		const navItemID = pageData['navItemID'];
		const navItemLink = pageData['navLinkID'];

		if(navItemID){
			const menuItem = document.getElementById(navItemID);
			menuItem.classList.add(CLASS_NAME_MENU_OPEN);
		}
		
		if(navItemLink){
			const menuLink = document.getElementById(navItemLink);
			menuLink.classList.add(CLASS_MENU_LINK_ACTIVE);
		}

		
	})();
	
	
	
}();