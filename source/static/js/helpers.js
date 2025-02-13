
const HELPERS = (function(){
	
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
	

		function verifyInt(min, max, inputElement, errorElement){
			//Use regex to ensure only positive integers can be input
			validatePosIntegerInput(inputElement);
			
			
			const num = parseInt(inputElement.value);
			
			const ERROR_NAN = "Not a valid number";
			const ERROR_SIZE = `Value must be between ${min} and ${max}`;
			
			if(isNaN(num)){
				errorElement.classList.remove(HIDDEN_CLASS);
				errorElement.textContent = ERROR_NAN;
				return false;
				
			} else if (num < min){
				errorElement.classList.remove(HIDDEN_CLASS);
				errorElement.textContent = ERROR_SIZE;
				return false;
				
			} else if (num > max) {
				errorElement.classList.remove(HIDDEN_CLASS);
				errorElement.textContent = ERROR_SIZE;
				return false;
			
			
			//Valid: Hide the error message
			} else {
				errorElement.classList.add(HIDDEN_CLASS);
				errorElement.textContent = '';
				return true;
			}
			
		}
		
		
		function verifyDate(elementIn, errorElement){
			const date = elementIn.value;
			
			console.log(date);
		}
		
			
		function verifyInitials(elementIn, errorElement){
			//Use regex to ensure only upper and lower case letters can be input
			validateUpperLowerCase(elementIn);
			
			const val = elementIn.value;
			
			const ERROR_SIZE = 'Please enter at least one letter.';
			
			if(val.length == 0){
				errorElement.classList.remove(HIDDEN_CLASS);
				errorElement.textContent = ERROR_SIZE;
				return false;
			} else {
				errorElement.classList.add(HIDDEN_CLASS);
				errorElement.textContent = '';
				return true;
			}
			
		}
			
		
			
				
		//Only allows upper and lower case values to be entered into a textbox	
		function validateUpperLowerCase(input) {
			const regex = /^[a-zA-Z]*$/;
			if (!regex.test(input.value)) {
				input.value = input.value.replace(/[^a-zA-Z]/g, '');
			}
		}	
			
			
		function validatePosIntegerInput(input) {
			// Regex to allow only integers (positive or negative)
			const regex = /^\d*$/;

			// If the input doesn't match the regex, remove invalid characters
			if (!regex.test(input.value)) {
				input.value = input.value.replace(/[^\d]/g, ''); // Remove non-integer characters
			}
		}
				
			
			
		
		
	return {
		verifyInt, 
		validateUpperLowerCase, 
		validatePosIntegerInput, 
		verifyInitials,
		verifyDate
		};
			
			
			
			

})();

