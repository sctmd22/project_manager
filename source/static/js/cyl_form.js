const EDITING = cyl_editing_json;

let CYL_ID = cyl_id;

//Fetch additional data based on the cylinder ID
//Add the "XMLHttpRequest" header data to allow access
fetch(`/reports/cylinders/get_json_data/${CYL_ID}`, {
		headers: {
			"X-Requested-With": "XMLHttpRequest"
		}
})
	.then(response => response.json())
	.then(data => {
		 // Use the additional data
		FORM_FUNCTIONS(data);
});

const FORM_FUNCTIONS = function(data){
	let FORM_DATA_JSON = data;


	class FormElement {
		/*
			Used to define input element objects which contain info and methods related to form inputs
		*/
			constructor(inputID, errorID) {
				this.inputID = inputID;
				this.inputElement = this.getElement(this.inputID);
				
				if(errorID){
					this.errorID = errorID;
					this.errorElement = this.getElement(this.errorID);
					
				}
				
				this.valid = false;
				//this.updateVal();
				this.hideErr();
					
			}
			
			getElement(id){
				const elem = document.getElementById(id);
				
				if(!elem){
					return false;
				}
				
				return elem;
			}
			
			//Set this.val and the element value
			setVal(data){
				if(this.inputElement){
					this.inputElement.value = data;
					this.val = data;
				}
			}
				
			//Read the elements current value and update self.val. Call this inside eventlisteners
			updateVal(){
				if(this.inputElement){
					this.val = this.inputElement.value;
				} else {
					this.val = null;
				}
			}
			
			getVal(){
				if(this.inputElement){
					this.val = this.inputElement.value;
					return this.val;
				}
			}

			hideErr(){
				if(this.errorElement){
					this.errorElement.classList.add(HIDDEN_CLASS);	
				}
			}				
			
			showErr(msg){
				if(this.errorElement){
					this.errorElement.classList.remove(HIDDEN_CLASS);	
					this.errorElement.textContent = msg;
				}
			}
			
			
			disable(){
				if(this.inputElement){
					this.inputElement.disabled = true;
					this.hideErr();
				}
			}
			
			enable(){
				if(this.inputElement){
					this.inputElement.disabled = false;
					
					//Trigger an "input" event on enable
					this.triggerInput();
				}
			}

			triggerInput(){
				if(this.inputElement){
					//Trigger an input event 
					const event = new Event("input", { bubbles: true, cancelable: true });
					this.inputElement.dispatchEvent(event);
				}
			}
			
			triggerChange(){
				if(this.inputElement){
					//Trigger a change event
					const event = new Event("change", { bubbles: true, cancelable: true });
					this.inputElement.dispatchEvent(event);
				}
			}
			
			clear(){
				if(this.inputElement){
					this.inputElement.value = '';
				}
			}
			
		}
		
	class TextInput extends FormElement {
		constructor(inputID, errorID, maxSize = 255){
			super(inputID, errorID);
			this.maxSize = maxSize;
			
		}
		
		//No forward or back slashes, single or double quotes
		verifyNoSlashesNoQuotes(){
			this.inputElement.value = this.inputElement.value.replace(/[/\\'"]/g, ""); 
			this.verifySize();
		}
		
		//Upper and lower case letters AND digits 0-9
		verifyAlphaNumeric(){
			//[^...] in regex indicates negation, so replace anything that doesnt NOT match a-z, A-Z and 0-9
			this.inputElement.value = this.inputElement.value.replace(/[^a-zA-Z0-9]/g, ""); 
			this.verifySize();
		}
		
		//Upper and lowercase letters only
		verifyUpperLower(){
			this.inputElement.value = this.inputElement.value.replace(/[^a-zA-Z]/g, "");
			this.verifySize();
		
		}
		

		verifySize(){
			const val = this.inputElement.value;
			this.inputElement.value = val.slice(0, this.maxSize);
			
			if(val.length == 0){
				this.valid = false;
				this.val = null;
			} else {
				this.hideErr();
				this.valid = true;
				this.val = this.inputElement.value;
			}
			
		}
	}

	class DropInput extends FormElement {
		constructor(inputID){
			super(inputID);
		}
		
		decodeSetOptions(){
			//Get the latest value from the input element
			this.updateVal();
			
			if(this.val === 'none'){
				this.val = '';
			} else {
				this.val = this.val.toUpperCase();
			}
		}
		
		decodeSeparatorOptions(){
			this.updateVal();
			
			if(this.val === 'space'){
				this.val = ' ';
			}
		}
		
		
		//Don't read directly from the input - the values will be decoded by another function and this.val set directly
		getVal(){
			return this.val;
		}
	}

	class IntInput extends FormElement {
		
		constructor(inputID, errorID, minSize = 0, maxSize = 0){
			super(inputID, errorID);
		
			this.maxSize = maxSize;
			this.minSize = minSize;

		}
		
		verifySize(){
			const rawNum = this.inputElement.value;
			const num = parseInt(rawNum);
			
			const ERROR_NAN = "Not a valid number";
			const ERROR_SIZE = `Value must be between ${this.minSize} and ${this.maxSize}`;
		
			//Don't display an error for an empty string
			if(rawNum == ''){
				this.val = null;
				this.valid = false;
				this.hideErr();
				
			}else if(isNaN(num)){
				this.val = null;
				this.showErr(ERROR_NAN);
				this.valid = false;
				
			} else if (num < this.minSize){
				//this.inputElement.value = this.minSize;
				this.val = null;
				this.showErr(ERROR_SIZE);
				this.valid = false;
				
			} else if (num > this.maxSize) {
				//this.inputElement.value = this.maxSize;
				this.val = this.maxSize;
				this.showErr(ERROR_SIZE);
				this.valid = false;
			
			
			//Valid: Hide the error message
			} else {
				this.val = num;
				this.hideErr();
				this.valid = true;
			}
			
		}
		
		verifyPosInt() {
			// Regex to allow only integers (positive or negative)
			const regex = /^\d*$/;

			// If the input doesn't match the regex, remove invalid characters
			if (!regex.test(this.inputElement.value)) {
				this.inputElement.value = this.inputElement.value.replace(/[^\d]/g, ''); // Remove non-integer characters
			}
			
			this.verifySize();
					
		}
		
		getVal(){
			this.verifyPosInt();
			return this.val;
		}
	}

	class NumberInput extends FormElement {
		constructor(inputID, errorID){
			super(inputID, errorID);
			
		}
		
		verifyNumber(){
			let val = this.inputElement.value
			
			//Use regex to filter out invalid characters
			const regex = /^-?\d*\.?\d*$/; // Allows optional negative sign, digits, and optional decimal
			let newValue = '';

			//Build the new value character by character
				//Does not append any characters that do not pass the regex test
			for (let chara of val) {
				if (regex.test(newValue + chara)) {
					newValue += chara;
				}
			}

			//Update the input field value
			this.inputElement.value = newValue;
			this.val = newValue;
		}
		
		getVal(){
			this.verifyNumber();
			return this.val;
		}
		
	}

	class DateInput extends FormElement {

		constructor(inputID, errorID){
			super(inputID, errorID); //Call parent constructor
			this.val = null;
		}
		
					
		//Verifies a string can be parsed as a Date object.
			//Get the month and day to be used as part of the cylinder ID
			//Update the this.valid member
		verifyDate(){
			const errMsg = "Please enter a valid date.";
			
			let dateString = this.inputElement.value;
		
			if(!dateString){
				this.val = null;
				this.valid = false;
				this.showErr(errMsg);
				return;
			}


			//Parse the date as milliseconds and convert to a date object
			let parsedDate = Date.parse(`${dateString}`);
			
			if(isNaN(parsedDate)){
				this.val = null;
				this.valid = false;
				this.showErr(errMsg);
				return;
			}
			
			this.valid = true;
			this.val = new Date(parsedDate);
			this.hideErr();
			
		}
		
		//Convert the date object to a string 'MMDD' with padding
		toDayMonthStr(){
			if(!this.val){
				return '';
			}

			let day = this.val.getUTCDate();
			let month = this.val.getUTCMonth() + 1;
			
			let dayStr = day.toString().padStart(2, '0');
			let monthStr = month.toString().padStart(2, '0');

			let result = `${monthStr}${dayStr}`;

			return result;	
			
		}
	}

	class OutputElement {
		constructor(id){
			this.outputID = id;
			this.outputElement = document.getElementById(id);
			
		}
		
		getVal(){
			if(this.outputElement){
				return this.val;
			
			}
		}
		
		setVal(data){
			if(this.outputElement){
				this.val = data;
				this.outputElement.innerText = data;
			}
		}
		
		disable(){
			if(this.outputElement){
				this.outputElement.disabled = true;
			}
		}
		
		enable(){
			if(this.outputElement){
				this.outputElement.disabled = false;
			}
		}
			
		
	}

	const FIELD_FUNCTIONS = (function(){
		
		if(EDITING){
			FIELD_VALIDATION();
		}
		
		//Add event listeners to validate 'mix and field data' inputs
		function FIELD_VALIDATION(){
			
			const FIELD_TABLE = FORM_DATA_JSON.fieldTable;
			
			const volumeInput = new NumberInput(FIELD_TABLE.dataFields.volume.label, FIELD_TABLE.dataFields.volume.errorLabel);
			
			volumeInput.inputElement.addEventListener('input', ()=>{
				volumeInput.verifyNumber();
				
			});
		}
		
		
	})();

	const ITEMS_FUNCTIONS = (function(){
		
		const ITEMS_LIMIT = 30;
		
		const checkboxReceivedEqual = document.getElementById(FORM_DATA_JSON.fieldTable.dataFields.dateReceivedEqual.label);
		const checkboxSpecimenEqual = document.getElementById(FORM_DATA_JSON.fieldTable.dataFields.dateSpecimenEqual.label);
		const checkboxCustomID = document.getElementById('customIDCheck');
		
		const addButtonElement = document.getElementById('btnAddItems');	
		const addButtonRowElement = document.getElementById('btnAddItemsRow');	

		const exampleOutput = new OutputElement('itemsExampleID');

		const numItems = new IntInput('numItemsIn', 'numItemsErrorMsg', 1, ITEMS_LIMIT);
		
		const initials = new TextInput('itemsInitialsIn', 'itemsInitialsErrorMsg', 3);
		const customID = new TextInput('itemsCustomID', 'itemsCustomIDErr', 20);
		
		const dateCast = new DateInput(FORM_DATA_JSON.fieldTable.dataFields.castDate.label);
		const dateTransported = new DateInput(FORM_DATA_JSON.fieldTable.dataFields.dateTransported.label);
		
		const dateReceived = new DateInput(FORM_DATA_JSON.fieldTable.dataFields.dateReceived.label, 'itemsDateReceivedErr');
		const dateSpecimenID = new DateInput(FORM_DATA_JSON.fieldTable.dataFields.dateSpecimen.label, 'itemsDateSpecimenErr');

		const setDropdown = new DropInput('itemsSetSelect');
		const separatorDropdown = new DropInput('itemsSeparatorSelect');


		if(EDITING){
			ADD_ITEMS();
		}

		//Handle realtime functionality of the "Add Cylinders/Cubes/X" forms
		function ADD_ITEMS(){
			//Run toggleCheck to set the initial value
			toggleCheck(checkboxReceivedEqual, dateTransported.inputElement, dateReceived.inputElement);
			toggleCheck(checkboxSpecimenEqual, dateCast.inputElement, dateSpecimenID.inputElement);			
			
			
			//Disable the "Custom ID" input by default
			customID.disable();
			
			//Immediately call the varifyDate function as there may be a valid date initially
			dateSpecimenID.verifyDate();
			
			//Make sure the drop down values are set and decoded
			separatorDropdown.decodeSeparatorOptions();
			setDropdown.decodeSetOptions();
			
			//Event listener for the "Custom ID" checkbox
			customIDCheck.addEventListener("change", ()=>{
				customIDToggle();
			});
			
			//Event listener for Custom ID text input
			customID.inputElement.addEventListener("input", ()=>{
				customID.verifyNoSlashesNoQuotes();
				updateExample();
				checkValidity();
			
			});
			
			
			//Input event listener for "numItemsIn" input box
			numItems.inputElement.addEventListener("input", ()=>{
				numItems.verifyPosInt();
				checkValidity();

			});
			
			//Input event listener for Tech Initials input box
			initials.inputElement.addEventListener("input", ()=>{
				initials.verifyUpperLower();	
				updateExample();
				checkValidity();

			});

			//Input event listener for ID Date input box
			dateSpecimenID.inputElement.addEventListener("input", ()=>{
				dateSpecimenID.verifyDate();
				updateExample();
				checkValidity();

			});
			
			//Event listener for separator selection
			setDropdown.inputElement.addEventListener("change", ()=>{
				setDropdown.decodeSetOptions();
				updateExample();
				
			});
			
			//Event listener for separator selection
			separatorDropdown.inputElement.addEventListener("change", ()=>{
				separatorDropdown.decodeSeparatorOptions();
				updateExample();
				
			});
			
			//Need an event handler for the checkbox AND for dateTransported incase the value in dateTransported changes
				//Using an arrow functions " ()=> {}; " which executes toggleCheck() only when the event handler runs 
			checkboxReceivedEqual.addEventListener('change', ()=> {
				toggleCheck(checkboxReceivedEqual, dateTransported.inputElement, dateReceived.inputElement);	
			});
			
			dateTransported.inputElement.addEventListener('change', ()=>{
				toggleCheck(checkboxReceivedEqual, dateTransported.inputElement, dateReceived.inputElement);		
			
			});	
			
			//Specimen ID
			checkboxSpecimenEqual.addEventListener('change', ()=> {
				toggleCheck(checkboxSpecimenEqual, dateCast.inputElement, dateSpecimenID.inputElement);	
			});
			
			
			dateCast.inputElement.addEventListener('change', ()=>{
				toggleCheck(checkboxSpecimenEqual, dateCast.inputElement, dateSpecimenID.inputElement);		
			
			});	
			
			
			
			//Update the "Example Output" element text
			function updateExample(){
				if(initials.valid && dateSpecimenID.valid && !customIDCheck.checked){
					
					exampleOutput.setVal(`${initials.getVal()}${dateSpecimenID.toDayMonthStr()}${setDropdown.getVal()}${separatorDropdown.getVal()}1`);
					
				} else if(customID.valid && customIDCheck.checked) {
					exampleOutput.setVal(`${customID.getVal()}1`);
			
				} else {
					exampleOutput.setVal('');
				}
			}
			
			//Enable the 'Add x' button if various form fields are valid 
			function checkValidity(){
					
				if(numItems.valid && initials.valid && dateSpecimenID.valid && !customIDCheck.checked){
					addButtonElement.disabled = false;
					
				} else if(numItems.valid && customIDCheck.checked && customID.valid) {
					
					addButtonElement.disabled = false;
					
				} else {
					addButtonElement.disabled = true;
				}
				
			}
			
			//Enable or disable the 'customID' input and related inputs
			function customIDToggle(){
				if(checkboxCustomID.checked){
					initials.disable();
					dateSpecimenID.disable();
					separatorDropdown.disable();
					setDropdown.disable();
					
					checkboxSpecimenEqual.disabled = true;
					customID.enable();
					
				} else {
					initials.enable();
					dateSpecimenID.enable();
					
					checkboxSpecimenEqual.disabled = false;
					separatorDropdown.enable();
					setDropdown.enable();
					
					customID.disable();
					
					//Call toggleCheck to ensure the state of the inputs being controlled by the checkboxes
						//return to their previous value (might be disabled still)
					toggleCheck(checkboxSpecimenEqual, dateCast.inputElement, dateSpecimenID.inputElement);	

				}
			}
			
					
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
		};
		
		
		/*---------------------------------------------------------------------------------------------------------------------------------------------*/
			
			
		class ItemsTable {
			constructor(itemsData, template, tableID, maxItems){
				/*
					itemsData: 	An array of objects, each row corresponding to an items row. Will be empty if table has not yet been written to database
					template:	An object (dict) correpsond to HTML properties of each row (without values)
					tableID:	The HTML ID of the table to append data to
					maxItems:	The maximum number of rows the table will allow
				*/
				
				this.numRows = 0;
				this.tableBodyElement = null;
				this.itemsTableData = [];
				this.itemsTableDB = []; //Save a copy of itemsData incase the table needs to be reset
				this.rowLimit = 100;
				this.rowTemplate = {};
				
				
				//Control button ID's (Add Row, Reset, Delete)
				this.isBtnRow = false; //Whether the "Add Row" row has been added or not
				this.isDeleteBtnRow = false; //Whether or not the delete row icons have been set with eventlisteners
				this.addRowID = 'addItemsRow';
				this.addRowBtnID  = 'btnItemsAddRow'; //ID of the table row for the "Add Row" button
				this.resetBtnID = 'btnResetTable';
				this.deleteTableBtnID = 'btnDeleteTable';
				this.deleteBtnRowID = 'btnDeleteRow';
				
				
				if(maxItems){
					this.rowLimit = maxItems;
				}
				
				this.rowTemplate = template;
				
				//Get correct table row from table
				this.tableBodyElement = document.querySelector(`#${tableID} tbody`);
			
				if(itemsData){
					this.numRows = itemsData.length;
					this.itemsTableDB = structuredClone(itemsData); //Save a copy of the original table incase the table needs to be reset
					this.itemsTableData = itemsData; //Initially assign the database table to the object table
				}
				
				
			}
			
			
			//Add the bottom row controls (Add Row, Undo All, Delete Table)
			addControls(){
				if(!this.isBtnRow){
					const addBtnID = this.addRowBtnID;
					const resetBtnID = this.resetBtnID;
					const deleteBtnID = this.deleteTableBtnID;
					
					const tableRow = document.createElement('tr');	
					tableRow.id = this.addRowID;
					
					tableRow.innerHTML = `
						<td colspan="14">
							<button type="button" class="btn btn-primary" id="${addBtnID}">Add Row</button>
							<button type="button" class="btn btn-primary" id="${resetBtnID}">Undo All</button>
							<button type="button" class="btn btn-danger" id="${deleteBtnID}">Delete Table</button>
						</td>`;
					
					this.tableBodyElement.appendChild(tableRow);
					
					this.isBtnRow = true;
					
					//Get the element of the newly added buttons
					const addBtnElement = document.getElementById(addBtnID);
					const resetBtnElement = document.getElementById(resetBtnID);
					const deleteBtnElement = document.getElementById(deleteBtnID);

					//Add event listeners
					addBtnElement.addEventListener('click', ()=>{
						this.addRow();
					});
					
					
					resetBtnElement.addEventListener('click', ()=>{
						const userConfirmed = confirm("Warning - This will reset any changes made to the Cylinder Data table during this session.");
						
						if(userConfirmed){
							this.resetTable();
						}
						
					});
					
			
					deleteBtnElement.addEventListener('click', ()=>{
						const userConfirmed = confirm("Are you sure you want to delete the Cylinder Data table?");
						
						if(userConfirmed){
							this.deleteTable();
						}
						
					});
					
				}
		
			}
			
			
			//Remove only the changes from the table (not the data loaded from the database)
				//Any data entered or rows added/removed will be reset to the original state when the table was first loaded
			resetTable(){
				//Need to clear the display first as clearDisplay() reads elements to clear from the table
				this.clearDisplay();
				
				//Overwrite the current table with a copy the one from the database
				this.itemsTableData = structuredClone(this.itemsTableDB);
				
				this.updateSize();
				this.displayTable();
				
			}
			
			
			deleteTable(){
				this.clearDisplay();
				
				//Clear Table
				this.itemsTableData = []
				this.updateSize();
				
			}
			
			
			//Read through the table and remove all rows from the DOM
			clearDisplay(){
				for(let i = 0; i < this.numRows; i++){
					const rowID = this.itemsTableData[i].name;
					const rowElem = document.getElementById(rowID);
					
					//Remove form elements
					if(rowElem){
						rowElem.remove();
					}	
				}
			}
			
			//Display the contents of this.itemsTableData
			displayTable(){
				this.clearDisplay();
				this.addControls();
				
				for(let i = 0; i < this.numRows; i++){
					const rowData = this.itemsTableData[i].dataFields;
					const rowID = this.itemsTableData[i].name;
					
					const tableRow = document.createElement('tr');	
					tableRow.id = `${rowID}`;
					
					tableRow.innerHTML = this.populateTD(rowData, i);;

					//Select the btnRow <tr></tr> to insert the table rows before it
					const btnAddRow = document.getElementById(this.addRowID);

					this.tableBodyElement.insertBefore(tableRow, btnAddRow);
					
				}
				
				this.addDeleteControl();

			}
			
			
			//Add event listeners for the delete icons for each row
			addDeleteControl(){
				
				if(!this.isDeleteBtnRow){

					//The ID without an index suffix is the input boxes 'name' property
					const deleteBtnID = this.deleteBtnRowID;
					
					const deleteBtnElements = document.querySelectorAll(`i[name=${deleteBtnID}]`);
					
					console.log(deleteBtnElements);
					
					//ADD EVENT LISTENERS
					
					this.isDeleteBtnRow = true;
	
				}
				
			
			}
			
			
			//Populate the HTML template <td></td> with data
			populateTD(rowData, idIndex){
				let tableRow = '';
				
				for(let key in rowData){
					const maxLength = rowData[key].maxlength;
					const label = rowData[key].label;
					const val = rowData[key].val;
					const disabled = rowData[key].disabled;
					
					let td = '';
				
					const id = `${label}${idIndex}`
					
					
					let deleteBtn = '';
					let tdClass = '';
			
					if(key == 'itemID'){
						deleteBtn = `<i class="bi bi-trash3 itemsIcon" id="${this.deleteBtnRowID}${idIndex}" name="${this.deleteBtnRowID}" row="${idIndex}"></i>`;
						tdClass = 'itemsTD';
					}
			
					
					if(key == 'autoID'){
						td = `<input type="hidden" id="${id}" name="${label}" value="${val}">`;
						
					} else {
						td = `<td>${deleteBtn}<input type="text" maxlength="${maxLength}" class="form-control ${tdClass}" id="${id}" name="${label}" value="${val}" aria-describedby="textDesc" ${disabled}></td>`;
					}
					
					tableRow += td;
					
				}
				return tableRow;
			}
			
			//Add rows filled in with information from the 'Add Cylinders' form
			addTableRows(n, specimenID, dateReceived, dateTested){

				const startVal = this.numRows + 1;
				let endVal = n + startVal;
				
				//Ensure endVal is within the limits
				if(endVal > this.rowLimit){
					endVal = this.rowLimit + 1;
					
				}
				
				
				for(let i = startVal; i < endVal; i++){				
					
					let newRow = structuredClone(this.rowTemplate); //Creat a deep copy of the template row

					newRow.dataFields.itemID.val = `${specimenID}${i}`;

					this.itemsTableData.push(newRow);
					this.updateSize();
					
				}

				this.displayTable()
				
			}
			
			
			//Add an empty row to the end of the table
			addRow(){
				if(this.numRows < this.rowLimit){
					
					//Append the template to the table
					this.itemsTableData.push(this.rowTemplate);	
					
					//Update numRows
					this.updateSize()
	
					this.displayTable();
				}	
			}
			
			updateSize(){
				this.numRows = this.itemsTableData.length;
			}
			
			
			deleteRow(rowNum){
				
				
			}
			
			insertRow(){
				
			}
			
		}	
			
		//Items table declarations
		const ITEMS_TABLE = FORM_DATA_JSON.cylItemsTable;
		const ITEMS_TABLE_ID = 'cylItemsTable';		//Table to append elements to
		const itemsTableBody = document.querySelector(`#${ITEMS_TABLE_ID} tbody`); //Select <tbody> of ITEMS_TABLE_ID
		
		//Template to be used to fill the HTML properties such as id, maxlength, etc. of each input of the items row
		let ITEMS_TEMPLATE = FORM_DATA_JSON.cylItemsTableTemplate[0]; 
		
		//Create ItemsTable object
		itemsTable = new ItemsTable(ITEMS_TABLE, ITEMS_TEMPLATE, ITEMS_TABLE_ID, ITEMS_LIMIT);
		
		
		
		if(EDITING){
			itemsTable.displayTable();
			
			//Add event listener for "Add X" button
			addButtonElement.addEventListener('click', ()=>{
				const numRows = numItems.getVal();
				const specimenID = exampleOutput.getVal().slice(0,-1);
				const dateReceivedVal = dateReceived.getVal();
				const dateTestedVal = '';
				
				itemsTable.addTableRows(numRows, specimenID, dateReceivedVal, dateTestedVal);
			});
			
		}
		
		
	})();
	
	const STR_FUNCTIONS = (function(){
		const STRENGTH_TABLE = FORM_DATA_JSON.strTable;

		if(EDITING){
			STRENGTH_VALIDATION();
		}
		
		function STRENGTH_VALIDATION() {
			
			//Add event listeners for each day and strength input
			for (let row of STRENGTH_TABLE){
				const strengthInput = new IntInput(row.dataFields.strength.label, row.dataFields.strength.errorLabel, row.dataFields.strength.size.min, row.dataFields.strength.size.max);
				const daysInput = new IntInput(row.dataFields.days.label, row.dataFields.days.errorLabel, row.dataFields.days.size.min, row.dataFields.days.size.max);
				
				strengthInput.inputElement.addEventListener('input', ()=>{
					strengthInput.verifyPosInt();
				});
				
				daysInput.inputElement.addEventListener('input', ()=>{
					daysInput.verifyPosInt();
				});
			}
		};

		const SHOW_HIDE = (function(){
			/*
			-Implement the functionality for "Add Target" and "Remove Target" for cylinder strength table
			-How it works:
				1. Initially loop through the STRENGTH_TABLE to get the HTML ID's in order to read the values of the "visible" inputs.
					1 = visible 
					0 or empty = not visible
				2. Hide strength table rows where visible = 0 (or none) by assigning the classId "hidden"
				3. Count the number of inputs that are visible (value = 1) to get the index for the addStrTarget() and removeStrTarget() functions
			*/
			
						
			const numStrTargets = STRENGTH_TABLE.length;
			let strIndex = 0;

			if(EDITING){
				const ADD_TARGET_ID = "strAddTarget";
				const REMOVE_TARGET_ID = "strRemoveTarget";
				
				const addTargetBtn = document.getElementById(ADD_TARGET_ID);
				const removeTargetBtn = document.getElementById(REMOVE_TARGET_ID);

			
				//Add event listeners for the "Add Target" and "Remove Target" buttons
				addTargetBtn.addEventListener('click', ()=>{
					addStrTarget();
				});
				
							
				removeTargetBtn.addEventListener('click', ()=>{
					removeStrTarget();
				});

				
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

		})();
		
	 })();
	 
	const CONDITIONS_FUNCTIONS = (function(){
		//Get data from the <script></script> tags passed from Python to Jinja
		const CONDITIONS_TABLE = FORM_DATA_JSON.conditionsTable;
		
		
		if(EDITING){
			CONDITIONS_VALIDATION();
			NATURAL_AIR();
		}
		
		//Add event listeners to ensure only decimal numbers can be entered into the text boxes
		function CONDITIONS_VALIDATION() {
			//Add event listeners for each day and strength input
			for (let row of CONDITIONS_TABLE){
				const actualInput = new NumberInput(row.dataFields.actual.label, row.dataFields.actual.errorLabel);
				const minInput = new NumberInput(row.dataFields.min.label, row.dataFields.min.errorLabel);
				const maxInput = new NumberInput(row.dataFields.max.label, row.dataFields.max.errorLabel);

				actualInput.inputElement.addEventListener('input', ()=>{
					actualInput.verifyNumber();
				});
				
				minInput.inputElement.addEventListener('input', ()=>{
					minInput.verifyNumber();
				});
				
				maxInput.inputElement.addEventListener('input', ()=>{
					maxInput.verifyNumber();
				});
				
			}
		};
		
		//Disable the airMin and airMax inputs depending on the value of the Air Options dropdown box
		function NATURAL_AIR(){
			
			const airDropdown = document.getElementById(FORM_DATA_JSON.fieldTable.dataFields.airOptions.label);
			let airMin = null;
			let airMax = null;
			
			//Grab the MAX and MIN input box elements for the 'air' property
			for (let row of CONDITIONS_TABLE){
				if(row.property === 'air'){
					airMax = new FormElement(row.dataFields.max.label);
					airMin = new FormElement(row.dataFields.min.label);
				}
			}
		
			//Call to set initial value
			toggleAir();

			airDropdown.addEventListener('input', ()=>{
				toggleAir();
			});
					
			function toggleAir(){
				const val = airDropdown.value;
				
				if(airDropdown.value === 'custom'){
					airMax.enable();
					airMin.enable();
				} else if(val === 'natural') {
					airMax.disable();
					airMax.clear();
					
					airMin.disable();
					airMin.clear();

				} else if(val === 'none'){
					airMax.disable();
					airMax.clear();
					
					airMin.disable();
					airMin.clear();
				}
			}
		}
		
		
		//Hide/show conditions table elements depending on value of SCC Radio Button
		(function(){
			const IS_SCC = FORM_DATA_JSON.fieldTable.dataFields.isScc.val;
			const SCC_ID = FORM_DATA_JSON.fieldTable.dataFields.isScc.label;

			
			// Get references to the radio buttons and the target element
			const sccRadioButtons = document.querySelectorAll(`input[name="${SCC_ID}"]`);

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
				if(EDITING){
					//input[name="cylSCC"] is CSS selector syntax
					sccVal = document.querySelector(`input[name="${SCC_ID}"]:checked`).value;

				}
				
				//Reverse current and prev keys if sccVal set
				if (sccVal === 'yes'){
					currentKey = 'SCC';
					prevKey = 'CYL';
					
				}

				for (let row of CONDITIONS_TABLE){
					let targetElement = document.getElementById(row.name);
					
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
		
		
	})();



}

