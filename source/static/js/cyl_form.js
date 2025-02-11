//Class name of CSS class which will hide an HTML element
const HIDDEN_CLASS = 'hidden';



//Handle realtime form functionality of the cylinder items part of the cylinder form
(function(){
	
	
	//Enable/disable the dateReceived and dateSepcimen input depending the dateReceivedEqual and dateSpecimenEqual checkboxes 
	(function(){
		
		
		const checkboxReceived = document.getElementById(cyl_data_json.fieldTable.labels.dateReceivedEqual);
		const dateReceived = document.getElementById(cyl_data_json.fieldTable.labels.dateReceived);
		const dateTransported = document.getElementById(cyl_data_json.fieldTable.labels.dateTransported);
		
		const checkboxSpecimen = document.getElementById(cyl_data_json.fieldTable.labels.dateSpecimenEqual);
		const dateSpecimen = document.getElementById(cyl_data_json.fieldTable.labels.dateSpecimen);
		const dateCast = document.getElementById(cyl_data_json.fieldTable.labels.castDate);
			
		const dateTransportedVal = dateTransported.value;
		const dateCastVal = dateCast.value;
		
		
		//Need an event handler for the checbox AND for dateTransported incase the value in dateTransported changes
			//Using an arrow functions " ()=> {}; " which executes toggleCheck() only when the event handler runs 
		checkboxReceived.addEventListener('change', ()=> {
			toggleCheck(checkboxReceived, dateTransported, dateReceived);	
		});
		
		dateTransported.addEventListener('change', ()=>{
			toggleCheck(checkboxReceived, dateTransported, dateReceived);		
		
		});	
		
		//Specimen ID
		checkboxSpecimen.addEventListener('change', ()=> {
			toggleCheck(checkboxSpecimen, dateCast, dateSpecimen);	
		});
		
		dateCast.addEventListener('change', ()=>{
			toggleCheck(checkboxSpecimen, dateCast, dateSpecimen);		
		
		});	
		
		//Run function to set the initial value
		toggleCheck(checkboxReceived, dateTransported, dateReceived);
		toggleCheck(checkboxSpecimen, dateCast, dateSpecimen);			
	
		function toggleCheck(cbox, source, destination){
			
			if(cbox.checked){
				destination.disabled = true;
				destination.value = source.value;
			} else {
				destination.disabled = false;
			}
			
		};
		
		
	})();
	
	
	(function(){
		const NUM_ITEMS_MAX = 30;
		const NUM_ITEMS_MIN = 1;
		const NUM_ITEMS_INPUT_ID = 'numCylinders';	//Input
		const NUM_ITEMS_ERROR_ID = 'numCylindersError';	//Error message output here
		

		
		let isValid = false;

		const numItemsErrorElem = document.getElementById(NUM_ITEMS_ERROR_ID);
		
		//Hide the error message box
		numItemsErrorElem.classList.add(HIDDEN_CLASS);
		
		
		const numItemsInput = document.querySelector(`#${NUM_ITEMS_INPUT_ID}`);
		const numItems = numItemsInput.value;
		
		//Input event listener
		numItemsInput.addEventListener("input", ()=>{
			verifyInt(NUM_ITEMS_MIN, NUM_ITEMS_MAX, numItemsInput, numItemsErrorElem, enableButton);
		});
		
		
		function enableItem(elem){
			elem.disabled = false;
		}
		
		
		enableButton = () => {
			console.log("Callback babey");
		}
		
		

		function verifyInt(min, max, inputElement, errorElement, callback){
			const num = parseInt(inputElement.value);
			
			const ERROR_NAN = "Not a valid number";
			const ERROR_SIZE = `Number must be between ${min} and ${max}`;
			
			if(isNaN(num)){
				errorElement.classList.remove(HIDDEN_CLASS);
				errorElement.textContent = ERROR_NAN;
				
			} else if (num < min){
				errorElement.classList.remove(HIDDEN_CLASS);
				errorElement.textContent = ERROR_SIZE;
				
			} else if (num > max) {
				errorElement.classList.remove(HIDDEN_CLASS);
				errorElement.textContent = ERROR_SIZE;
			
			
			//Valid: Hide the error and call the callback
			} else {
				errorElement.classList.add(HIDDEN_CLASS);
				callback();
				
			}
			

		}
		

		

		const ITEMS_TABLE_ID = 'cylItemsTable';		//Table to append elements to
		const itemsTableBody = document.querySelector(`#${ITEMS_TABLE_ID} tbody`);	
		
		
		createCylItemsRow();
		
		function createCylItemsRow(){
			
			const tableRow = document.createElement('tr');
			tableRow.innerHTML = `
				<td><input type="text" maxlength="16" class="form-control" id="" name=" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="8" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="8" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="3" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="3" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="3" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="5" class="form-control" id="" name="" value="" aria-describedby="textDesc" disabled></td>
				<td><input type="text" maxlength="6" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="6" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="1" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
				<td><input type="text" maxlength="4" class="form-control" id="" name="" value="" aria-describedby="textDesc" disabled></td>
				<td><input type="text" maxlength="4" class="form-control" id="" name="" value="" aria-describedby="textDesc" disabled></td>
				<td><input type="text" maxlength="3" class="form-control" id="" name="" value="" aria-describedby="textDesc"></td>
			
			`;
			
			itemsTableBody.appendChild(tableRow);	
		
		}
		
		
	})();
	
	
})();



const STR_FUNCTIONS = (function(){
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
	const STRENGTH_TABLE = cyl_data_json.strTable;
	
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
			strTr.classList.remove(HIDDEN_CLASS);
			
			strIndex++; //Increment last
		}
	}
	
	function removeStrTarget(){
		
		if(strIndex > 1){
			strIndex--; //Decrement first
			
			const targetRow = STRENGTH_TABLE[strIndex];
			
			const visibleInput = document.getElementById(targetRow['labels']['visible']);
			visibleInput.value = 0;
			
			const strTr = document.getElementById(targetRow['name']);
			strTr.classList.add(HIDDEN_CLASS);
			
			//Reset inputs to ''
			const inputs = strTr.querySelectorAll('input[type="number"]'); //CSS Selector to select html inputs where type="number"
			
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
			strTr.classList.add(HIDDEN_CLASS); //Assign the cylHidden class to the table row to hide it, also reset inputs if set
			
			inputs.forEach(input => {
				input.value = '';
			});
			
		} else {
			strIndex++;
		}
		
	}
	
	//Export functions to be used externally
	return {addStrTarget, removeStrTarget};
 
 })();
 


(function(){
	/*
	Create an IIFE (Immediately Invoked Function Expression) to create a local scope and execute automatically using 
	the (function(){})(); syntax
	*/

	
	//Get data from the <script></script> tags passed from Python to Jinja
	const CONDITIONS_TABLE = cyl_data_json.conditionsTable;
	const IS_SCC = cyl_data_json.fieldTable.valData.isScc;
	const CYL_EDITING = cyl_editing_json;
	
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
			targetElement.classList.remove(HIDDEN_CLASS);
			
			//Hide only where the currentKey is false and different from other key
			if(!row[currentKey] && (row[currentKey] !== row[prevKey])){
				
				targetElement.classList.add(HIDDEN_CLASS);
				
				//Grab the inputs under the table row and clear the values
					//All inputs are text EXCEPT auto_id which is hidden, which we do not want to reset
				const inputs = targetElement.querySelectorAll('input[type="text"]');
				
			
				
			   inputs.forEach(input => {
					input.value = '';
				});
				
		
			}
		
		
		}
		
	}
	
})();



