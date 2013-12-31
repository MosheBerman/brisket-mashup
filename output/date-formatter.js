
/* Replaces all unix timestamps as formatted strings. */
function formatDates(){
	
	timestampDisplays = document.getElementsByClassName("tweet-timestamp");

	for (var i = timestampDisplays.length - 1; i >= 0; i--) {

		var element = timestampDisplays[i];

		var timestamp = parseInt(element.innerText);

		var date = new Date(timestamp * 1000);		
		
		var formattedDate = monthFromDate(date) + "/" + dayOfMonthFromDate(date) + "/" + fullYearFromDate(date) + " at " + hoursFromDate(date) + ":" + minutesFromDate(date) + " (UTC)";

		element.innerText = formattedDate;
		
	};
}

/* Returns the minutes, padded if necessary. */
function secondsFromDate(date){

	var seconds = date.getUTCSeconds();

	return paddedDigit(seconds);
}

/* Returns the minutes, padded if necessary. */
function minutesFromDate(date){

	var minutes = date.getUTCMinutes();

	return paddedDigit(minutes);
}

/* Returns the hours, padded if necessary. */
function hoursFromDate(date){

	var hours = date.getUTCHours();

	return paddedDigit(hours);
}

function AMOrPMFromDate(date){

	var hours = date.getUTCHours();

	return (hours >= 12) ? "PM" : "AM";

}

/* Day of the month from a date. */
function dayOfMonthFromDate(date){
	return date.getUTCDate();
}

/* Month from a date. */
function monthFromDate(date){
	return date.getUTCMonth();
}

/* Month from a date. */
function fullYearFromDate(date){
	return date.getUTCFullYear();
}


/* Returns a given digit padded with leading zero if necessary. */
function paddedDigit(digit) {
	
	if (digit < 10) {
		return "0" + digit;
	};

	return digit;
}