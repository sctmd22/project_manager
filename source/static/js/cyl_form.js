//Get data from the <script></script> tags passed from Python to Jinja
const CONDITIONS_TABLE = conditions_table_json;
const CYL_EDITING = cyl_editing_json;
const IS_SCC = cyl_isSCC_json;

const STRENGTH_TABLE = strength_table_json;
 


//Assign the IIFE to a constant named STR_FUNCTIONS so any returned functions can be accessed 
const STR_FUNCTIONS = (function(){
		
		
	const numStrTargets = STRENGTH_TABLE.length;

	let targetElement = '';
	
	for (let row of STRENGTH_TABLE){
		console.log(row);
		
		targetElement = document.getElementById(row['name']);
		console.log(targetElement);
		
	}
	
	
	function addStrTarget(){
		

		
	}
	
	function removeStrTarget(){
		
		
	}
		
		

	return {addStrTarget, removeStrTarget};
 
 })();
 
 
 

//Create an IIFE (Immediately Invoked Function Expression) to create a local scope and execute automatically using the (function(){})(); syntax
(function(){
	
	// Get references to the radio buttons and the target element
	const sccRadioButtons = document.querySelectorAll('input[name="cylIsScc"]');

	console.log(sccRadioButtons)

	// Add event listeners to the radio buttons
	sccRadioButtons.forEach(button => {
		button.addEventListener('change', toggleElement);
	});
	
	// Call the function initially to set the correct state
	toggleElement();


	// Function to show or hide the element based on the selected radio button
	function toggleElement() {
		//console.log("Triggered");
		let sccVal = IS_SCC;
		let currentKey = 'CYL';
		let prevKey = 'SCC';
		
		//Get SCC value either directly from checkboxes or from the IS_SCC variable passed from flask/python
		if(CYL_EDITING === true){
			//input[name="cylSCC"] is CSS selector syntax
			sccVal = document.querySelector('input[name="cylIsScc"]:checked').value;

		}
		
		//Reverse current and prev keys if sccVal set
		if (sccVal === 'yes'){
			currentKey = 'SCC';
			prevKey = 'CYL';
			
		}

		for (let row of CONDITIONS_TABLE){
			let targetElement = document.getElementById(row['name']+'Row');
			
			//Show all table rows initially
			targetElement.classList.remove('cylHidden');
			
			//Hide only where the currentKey is false and different from other key
			if(!row[currentKey] && (row[currentKey] !== row[prevKey])){
				
				targetElement.classList.add('cylHidden');
				
				//Grab the inputs under the table row and clear the values
					//All inputs are text EXCEPT auto_id which is hidden, which we do not want to reset
				const inputs = targetElement.querySelectorAll('input[type="text"]');
				
			
				
			   inputs.forEach(input => {
					input.value = '';
				});
				
		
			}
			
			/*
			//Get each table row element
			let targetElement = document.getElementById(row['name']+row['suffix']['id']+'Row');
			
			//Hide all elements
			targetElement.classList.add('cylConditionsHidden');

			//Show only elements where key is true
			if(row[key] === true){
				targetElement.classList.remove('cylConditionsHidden');		
			}
			*/
		
		}
		
	}
	
})();



