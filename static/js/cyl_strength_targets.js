//Allow multiple strength targets to be added for cylinder data
const ROW_START = 2;
const ROW_LIMIT = 5;

const CYL_ROW_CLASS = 'cylStrRow';


let rowCount = ROW_START;

function addInput() {

	const container = document.getElementById("table-body");
	const newInput = document.createElement("tr");
	
	if(rowCount <= ROW_LIMIT){
				
		newInput.className = CYL_ROW_CLASS;

		newInput.id = CYL_ROW_CLASS + '-' + rowCount;
		newInput.innerHTML = `

				<td><label class="col-sm-2 col-form-label cylStrLabel">Target ${rowCount}:</label></td>
				<td><input type="number" class="form-control cylStrData" id="str_table_str${rowCount}" name="str_table_str${rowCount}"  value="{{ data.a }}" aria-describedby="textDesc"></td>
				<td><input type="number" class="form-control cylStrData" id="str_table_days${rowCount}" name="str_table_days${rowCount}"  value="{{ data.a }}" aria-describedby="textDesc"></td>

		`;
		
		

		container.appendChild(newInput);
		rowCount++;
		
		
	}

}



function removeCylStrInput() {
	//rowCount will be 1 greater than limit
	if(rowCount > ROW_LIMIT){
		rowCount = ROW_LIMIT;
	}
	
	let rowId = CYL_ROW_CLASS + '-' + rowCount;
	

	const tag = document.getElementById(rowId);
	
	if(tag){
		tag.remove();
		//Ensure rowCount doesn't count down below start value
		if(rowCount > ROW_START){
			rowCount--;
		}
	}
}


		
		