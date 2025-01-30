//Get data from the <script></script> tags passed from Python to Jinja
const CONDITIONS_TABLE = conditions_table_json;
const CYL_EDITING = cyl_editing_json;
const IS_SCC = cyl_isSCC_json;

const STRENGTH_TABLE = strength_table_json;
 


/*
	-Implement the functionality for "Add Target" and "Remove Target" for cylinder strength table
	-How it works:
		1. Initially loop through the STRENGTH_TABLE to get the HTML ID's in order to read the values of the "visible" inputs.
			1 = visible 
			0 or empty = not visible
		2. Hide strength table rows where visible = 0 (or none) by assigning the classId "cylHidden"
		3. Count the number of inputs that are visible (value = 1) to get the index for the addStrTarget() and removeStrTarget() functions
	
	Assign the IIFE to a constant named STR_FUNCTIONS so any returned functions can be accessed 
*/
const STR_FUNCTIONS = (function(){
		
	const numStrTargets = STRENGTH_TABLE.length;

	let strIndex = 0;
	
	
	function addStrTarget(){
		
		if(strIndex <= (numStrTargets - 1)){
			//Select the correct row based on the strIndex
			let targetRow = STRENGTH_TABLE[strIndex];
			
			//Get the hidden input which holds the 'visible' value and set to 1
			let visibleInput = document.getElementById(targetRow['labels']['visible']);
			visibleInput.value = 1;
			
			//Get the strength table row based on the id (which is stored as the 'name' in STRENGTH_TABLE)  
			let strTr = document.getElementById(targetRow['name']);
			strTr.classList.remove("cylHidden");
			
			
			strIndex++; //Increment last

		}
		
	}
	
	
	function removeStrTarget(){
		
		if(strIndex > 1){
			strIndex--; //Decrement last
			
			const targetRow = STRENGTH_TABLE[strIndex];
			
			const visibleInput = document.getElementById(targetRow['labels']['visible']);
			visibleInput.value = 0;
			
			const strTr = document.getElementById(targetRow['name']);
			strTr.classList.add("cylHidden");
			
			//Reset inputs to ''
			const inputs = strTr.querySelectorAll('input[type="number"]'); //Select all inputs of number type from the table row
			
			inputs.forEach(input => {
				input.value = '';
			});
			
		}
		
	}
	
	
	//Hide/show the necessary elements. Also count the number of visible elements to get start index
	

	for (let row of STRENGTH_TABLE){
		
		//Get the hidden input that stores the visibility data
		let visibleInput = document.getElementById(row['labels']['visible']);
		
		let visibleInputVal;
		
		
		if(isNaN(visibleInput.value)){
			visibleInputVal = 0;

		} else {
			visibleInputVal = Number(visibleInput.value);
		}

		let strTr = document.getElementById(row['name']);

		const inputs = strTr.querySelectorAll('input[type="number"]'); //Select all inputs of number type from the table row

		//Assign any non-zero values to zero
		if(!visibleInputVal){
			visibleInputVal.value = 0;
			strTr.classList.add("cylHidden"); //Assign the cylHidden class to the table row to hide it, also reset inputs if set
			
			
			inputs.forEach(input => {
				input.value = '';
			});
			
		} else {
			strIndex++;
		}
		
	}

	
		

	return {addStrTarget, removeStrTarget};
 
 })();
 
 
 

//Create an IIFE (Immediately Invoked Function Expression) to create a local scope and execute automatically using the (function(){})(); syntax
(function(){
	
	// Get references to the radio buttons and the target element
	const sccRadioButtons = document.querySelectorAll('input[name="cylIsScc"]');

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



