//Allow multiple strength targets to be added for cylinder data
const ROW_LIMIT = 5;
const ROW_START_LIMIT = 2;

const CYL_ROW_CLASS = 'cylStrRow';
const LABEL_CLASS = 'cylStrLabel';
const DATA_CLASS = 'cylStrData'; 

const strTotalRows = document.getElementById('cyl_str_total_rows'); //Grab the number the number of strength rows from the hidden ID
const ROW_START = strTotalRows.value;

let rowCount = ROW_START;

function addInput() {

	
	const container = document.getElementById("table-body");
	const newInput = document.createElement("tr");
	

	
	if(rowCount < ROW_LIMIT){
		rowCount++;
		newInput.id = CYL_ROW_CLASS + '-' + rowCount;
		newInput.className = CYL_ROW_CLASS;
		newInput.innerHTML = `
			<td><label class="col-sm-2 col-form-label cylStrLabel">Target ${rowCount}:</label></td>
			<td><input type="number" class="form-control cylStrData" id="str_table_str${rowCount}" name="str_table_strength"  value="0" aria-describedby="textDesc"></td>
			<td><input type="number" class="form-control cylStrData" id="str_table_days${rowCount}" name="str_table_days"  value="0" aria-describedby="textDesc"></td>
		`;
		
		container.appendChild(newInput);
		
		
		/*
		const myTd = document.getElementById("testing");
		
		console.log("td: " + myTd);
		
		const newContainer = document.getElementById("rootTable");
		const strInput = document.createElement("input");
		strInput.name = 'customStr';
		strInput.value = 5;
		
		newContainer.appendChild(strInput)
		
		console.log("Created Container=" + rowCount);
		*/

	}
	
}


function removeCylStrInput() {
	if(rowCount > 1){
		let rowId = CYL_ROW_CLASS + '-' + (rowCount);

		const tag = document.getElementById(rowId);
		
		if(tag){
			tag.remove();
			console.log("Removed Container=" + (rowCount));
			rowCount--;
	
		}
	}
	
}

