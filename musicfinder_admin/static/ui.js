
var DEBUG = true,
COLLECTIONJSON = "application/vnd.collection+json",
DEFAULT_DATATYPE = "json",
ENTRYPOINT = "/musicfinder/api/" //Entry point is getUsers()

function authenticate() {

	nickInput = $("#nickInput").val();
	passInput = $("#passInput").val();
	if (nickInput == "admin" && passInput == "admin") {
		document.location.href = "admin.html";
	}
    if(nickInput == "" || nickInput == null || passInput == null || passInput == ""){
        alert("Please provide nickname and password.");
        return;
     }
	var apiurl = ENTRYPOINT + "users/" + nickInput + "?password=" + passInput; // Get directly the desired user. Avoided the use of getUsers (getting all the users), because it would be
													// neccessary to loop between all of them. Doing like this the load is on the database.
	return $.ajax({
		url: apiurl,
		dataType:DEFAULT_DATATYPE
	}).always(function(){

	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}

		if (data.nickname == nickInput) {
			document.location.href = "playlists.html?"+nickInput; // Jump the the playlist page of the chosen user (/playsists.html?user)
		}

	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		//Inform user about the error using an alert message.
		alert ("Wrong nickname or password.  Please, try again");
	});

}

function addUser(apiurl, userData){
	userData = JSON.stringify(userData);
	return $.ajax({
		url: apiurl,
		type: "POST",
		//dataType:DEFAULT_DATATYPE, 
		data:userData,
		processData:false,
		contentType: COLLECTIONJSON+";",
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
		alert ("User successfully added");
		//Add the user to the list and load it.
		// $user = appendUserToList(jqXHR.getResponseHeader("Location"),nickname);
		// $user.children("a").click();

	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		alert ("Could not create new user");
	});
}

function handleCreateUser() {
	url = '/musicfinder/api/users/'
		var envelope={'template':{
								'data':[]
	}}; 
	var data = {};
	data.name = "nickname";
	data.value = $("#newNickname").val();
	envelope.template.data.push(data);

    var data = {};
    data.name = "password";
    data.value = $("#newPassword").val();
	envelope.template.data.push(data);
   
    if ($("#newAge").val()) {
    	var data = {};
    	data.name = "age";
    	data.value = $("#newAge").val();
    	envelope.template.data.push(data);
    }
    if ($("#newCountry").val()) {
    	var data = {};
    	data.name = "country";
    	data.value = $("#newCountry").val();
    	envelope.template.data.push(data);

    }
    if ($("#newGender").val()) {
    	var data = {};
    	data.name = "gender";
    	data.value = $("#newGender").val();
    	envelope.template.data.push(data);

    }
    addUser(url, envelope);
}