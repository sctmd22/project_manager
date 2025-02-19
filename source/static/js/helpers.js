
const HELPERS = (function(){

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
			let dateString = elementIn.value;
			
			if(!dateString){
				return false;
			}
			
			//Ensures the dateString is only 10 characters (YYYY-MM-DD) 
			if(dateString.length > 10){
				dateString = dateString.slice(0,10);
				
			}
	
			//Parse the date as milliseconds and convert to a date object
			let parsedDate = Date.parse(`${dateString}T00:00:00Z`);
			
			if(isNaN(parsedDate)){
				return false;
			}
			
			newDate = new Date(parsedDate);
			
			return newDate;
	
			

			//console.log(newDate.toISOString());

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

