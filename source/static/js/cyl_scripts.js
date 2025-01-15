document.addEventListener('DOMContentLoaded', () => {
  const dateCastInput = document.getElementById('cylCastDate');
  const batchTimeInput = document.getElementById('cylBatchTime');
  const sampleTimeInput = document.getElementById('cylSampleTime');
  const castTimeInput = document.getElementById('cylCastTime');

  dateCastInput.addEventListener('input', () => {
    // Enable the time input if the date input has a value, otherwise disable it
    if (dateCastInput.value) {
		cylBatchTime.disabled = false;
		cylSampleTime.disabled = false;
		cylCastTime.disabled = false;
		

	  
    } else {
		cylBatchTime.disabled = true;
		cylSampleTime.disabled = true;
		cylCastTime.disabled = true;
		
		cylBatchTime.value = "";
		cylSampleTime.value = "";
		cylCastTime.value = "";
    }
  });
});





function clearTime() {

	const container = document.getElementById("table-body");
	const newInput = document.createElement("tr");



	
}