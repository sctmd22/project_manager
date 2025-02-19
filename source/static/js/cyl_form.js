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
	
		
		
		//Determine if cbox is checked. Copy source value to destination if true and
			//trigger an "input" event
		function toggleCheck(cbox, source, destination){		
			//cbox:			Checkbox element Ooject
			//source:		Element object to obtain the value from
			//destination: 	Element object to write the source value to
		
			if(cbox.checked){
				destination.disabled = true;
				destination.value = source.value;
				
				//Trigger and event so the data validation functions work correctly. 
				const event = new Event("input", { bubbles: true, cancelable: true });
				destination.dispatchEvent(event);
			
			} else {
				destination.disabled = false;
			}
			
		};
		
		
	})();
	
	
	//Realtime validation for the "Add Cylinders" form members
	(function(){

		class InputElement {

			constructor(inputID, errorID, value = '', maxSize = 0, minSize = 0) {
				this.inputID = inputID;
				this.errorID = errorID;
				this.valid = false;
				this.val = value;
				this.maxSize = maxSize;
				this.minSize = 0;
				
				this.inputElement = this.getElement(this.inputID);
				this.errorElement = this.getElement(this.errorID);
				
				this.hideErr();
					
			}
			
			getElement(id){
				const elem = document.getElementById(id);
				
				if(!elem){
					return false;
				}
				
				return elem;
			}

			hideErr(){
				this.errorElement.classList.add(HIDDEN_CLASS);	
			}				
			
			showErr(msg){
				this.errorElement.classList.remove(HIDDEN_CLASS);	
				this.errorElement.textContent = msg;
			}
			
			
			//Verifies a string can be parsed as a Date object.
				//Get the month and day to be used as part of the cylinder ID
				//Update the this.valid memeber
			verifyDate(){
				const errMsg = "Please enter a valid date.";
				let dateString = this.inputElement.value;
			
		
				if(!dateString){
					this.valid = false;
					this.showErr(errMsg);
					return;
				}
				
				//Ensures the dateString is only 10 characters (YYYY-MM-DD)
				/*
				if(dateString.length > 10){
					dateString = dateString.slice(0,10);
					
				}
				*/
		
				//Parse the date as milliseconds and convert to a date object
				let parsedDate = Date.parse(`${dateString}`);
				
				if(isNaN(parsedDate)){
					this.valid = false;
					this.showErr(errMsg);
					return;
				}
				
				this.valid = true;
				this.hideErr();
				
				newDate = new Date(parsedDate);
				
				let day = newDate.getUTCDate();
				let month = newDate.getUTCMonth();

				console.log(day);
				console.log(month);
			
			}
			
			
		
		}
		
		const EXAMPLE_OUTPUT_ID = 'itemsExampleID'; //"Example Output" element
		
		const ADD_BUTTON_ID = 'btnAddItems';	//Add Cyl/Cube/Prism Button

		const numItems = new InputElement('numItemsIn', 'numItemsErrorMsg', '', 30, 1);
		
		const initials = new InputElement('itemsInitialsIn', 'itemsInitialsErrorMsg');
		const idDate = new InputElement('cylDateSpecimen', 'cylDateSpecimenErrorMsg');
		const dateReceived = new InputElement('cylDateReceived', 'cylDateReceivedErrorMsg');
	
		const addButtonElement = document.getElementById(ADD_BUTTON_ID);
		
		const exampleOutputElement = document.getElementById(EXAMPLE_OUTPUT_ID);
		
		
		//Input event listener for "numItemsIn" input box
		numItems.inputElement.addEventListener("input", ()=>{
			numItems.valid = HELPERS.verifyInt(numItems.minSize, numItems.maxSize, numItems.inputElement, numItems.errorElement);
			checkValidity();

		});
		
		//Input event listener for Tech Initials input box
		initials.inputElement.addEventListener("input", ()=>{
			initials.valid = HELPERS.verifyInitials(initials.inputElement, initials.errorElement);	
			updateExample();
			checkValidity();

		});

		//Immediately call the varifyDate function as there may be a valid date initially
		HELPERS.verifyDate(idDate.inputElement, idDate.errorElement);

		//Input event listener for ID Date input box
		idDate.inputElement.addEventListener("input", ()=>{
			idDate.verifyDate();
			updateExample();
			checkValidity();

		});
		
		
		//Update the "Example Output" element text
		function updateExample(){
			if(initials.valid && idDate.valid){
				
				initials.val = initials.inputElement.value;
				exampleOutputElement.textContent = `${idDate.val}${initials.val}-1`
			} else {
				initials.val = '';
				exampleOutputElement.textContent = '';
			}
		}
		
		//Enable the 'Add x' button if all form fields are valid
		function checkValidity(){
			if(numItems.valid && initials.valid){
				addButtonElement.disabled = false;
			} else {
				addButtonElement.disabled = true;
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
	const STRENGTH_TABLE = cyl_data_json.strTable;
	
	(function(){
		
		for (let row of STRENGTH_TABLE){
			console.log(row);
			
		}
		
		//const errorBoxStrength = document.getElementById(STRENGTH_TABLE.dataFields.strength.errorLabel);
		//const errorBoxDays = document.getElementByID(STRENGTH_TABLE.dataFields.strength.errorLabel);
		
		
	})();


	const SHOW_HIDE = (function(){
		/*
		-Implement the functionality for "Add Target" and "Remove Target" for cylinder strength table
		-How it works:
			1. Initially loop through the STRENGTH_TABLE to get the HTML ID's in order to read the values of the "visible" inputs.
				1 = visible 
				0 or empty = not visible
			2. Hide strength table rows where visible = 0 (or none) by assigning the classId "hidden"
			3. Count the number of inputs that are visible (value = 1) to get the index for the addStrTarget() and removeStrTarget() functions
		
		Assign the IIFE to a constant named STR_FUNCTIONS so any returned functions can be accessed 
		*/
		
		const numStrTargets = STRENGTH_TABLE.length;
		let strIndex = 0;
		
		function addStrTarget(){
			
			if(strIndex <= (numStrTargets - 1)){
				//Select the correct row based on the strIndex
				let targetRow = STRENGTH_TABLE[strIndex];
				
				//Get the hidden input which holds the 'visible' value and set to 1
				let visibleInput = document.getElementById(targetRow['dataFields']['visible']['label']);
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
				
				const visibleInput = document.getElementById(targetRow['dataFields']['visible']['label']);
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
			let visibleInput = document.getElementById(row['dataFields']['visible']['label']);
			
			let visibleInputVal;
			
			
			if(isNaN(visibleInput.value)){
				visibleInputVal = 0;

			} else {
				visibleInputVal = Number(visibleInput.value);
			}

			let strTr = document.getElementById(row['name']);

			const inputs = strTr.querySelectorAll('input[type="number"]'); //Select all inputs of number type from the table row

			//Change any non-zero values to zero
			if(!visibleInputVal){
				visibleInputVal.value = 0;
				strTr.classList.add(HIDDEN_CLASS); //Assign the HIDDEN_CLASS class to the table row to hide it, also reset inputs if set
				
				inputs.forEach(input => {
					input.value = '';
				});
				
			} else {
				strIndex++;
			}
			
		}
		
		return {addStrTarget, removeStrTarget};
		
	})();
	
	
	//Return addStrTarget and removeStrTarget without requiring additonal notation (ex: STR_FUNCTIONS.addStrTarget() instead of STR_FUNCTIONS.SHOW_HIDE.addStrTarget)
	return {
        addStrTarget: SHOW_HIDE.addStrTarget,
        removeStrTarget: SHOW_HIDE.removeStrTarget,
    };
 
 })();
 

//Show or hide Condition/Measurement Table rows corresponding to the state of the SCC radio buttons
(function(){
	/*
	Create an IIFE (Immediately Invoked Function Expression) to create a local scope and execute automatically using 
	the (function(){})(); syntax
	*/

	
	//Get data from the <script></script> tags passed from Python to Jinja
	const CONDITIONS_TABLE = cyl_data_json.conditionsTable;
	const IS_SCC = cyl_data_json.fieldTable.valueData.isScc;
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



