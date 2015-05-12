
/**** START CONSTANTS****/
//True or False
var DEBUG = true,
COLLECTIONJSON = "application/vnd.collection+json",
DEFAULT_DATATYPE = "json",
ENTRYPOINT = "/musicfinder/api/" //Entry point is getUsers()
/**** END CONSTANTS****/

/**** START RESTFUL CLIENT****/
/*
getUsers is the entrypoint of the application.

Sends an AJAX request to retrive the list of all the users of the application
ONSUCCESS=> Show users in the UI list. It uses appendUserToList for that purpose. 
The list contains the url of the users.
ONERROR => Show an alert to the user
*/

function getUsers() {
	var apiurl = ENTRYPOINT + "users/";

	return $.ajax({
		url: apiurl,
		dataType:DEFAULT_DATATYPE
	}).always(function(){
		//Remove old list of users, clear the form data hide the content information(no selected)
		$("#users").empty();
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
		//Extract the users
    	users = data.collection.items;
		for (var i=0; i < users.length; i++){
			var user = users[i];
			//Extract the nickname by getting the data values. Once obtained
			// the nickname use the method appendUserToList to show the user
			// information in the UI.
			//Data format example:
			//  [ { "name" : "nickname", "value" : "Mystery" },
			//    { "name" : "registrationdate", "value" : "2014-10-12" } ]
			var user_data = user.data;
			for (var j=0; j<user_data.length;j++){
				if (user_data[j].name=="nickname"){
					appendUserToList(user.href, user_data[j].value);
				}			
			} 
		}
		//Set the href of #addUser for creating a new user
		setNewUserUrl(data.collection.href)
	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		//Inform user about the error using an alert message.
		alert ("Could not fetch the list of users.  Please, try again");
	});
}

function handleGetUser(event) {
	if (DEBUG) {
		console.log ("Triggered handleGetUser")
	}
	event.preventDefault();//Avoid default link behaviour
	$(".selected").removeClass("selected");
    $(this).parent().addClass("selected");
    var href = $(this).attr("href");
    getUsers(href);
	return false; //IMPORTANT TO AVOID <A> DEFAULT ACTIONS
}

/*
Sets the url to add a new user to the list.
*/
function setNewUserUrl(url){
	console.log("NEW URL, ", url)
   $("#addUser").attr("href", url);
}

/**
 Creates User resource representation using the data from the form showed in the screen.
 Calls the method addUser to upload the new User resource to the Web service.
 TRIGGER: Submit button with value Create from form #create_user_form 
**/

function appendUserToList(url, nickname) {
	//var $user = $('<tr>').html('<a class= "user_link" href="'+url+'">'+nickname+'</a>');
	var $user = $('<tr>').html('<a class= "user_link" href=playlists.html?'+nickname+'>'+nickname+'</a>');
	//Add to the user list
	$("#users").append($user);
	return $user;
}

function deselectUser() {
	$("#user li.selected").removeClass("selected");
	$("#mainContent").hide();
}

/*
Helper method to reloadUserData. Internally it makes click on the href of the 
selected user.
*/
function reloadUserData() {
	var selected = $("#user_list li.selected a");
	selected.click();
}


/*** START ON LOAD ***/
//This method is executed when the webpage is loaded.
$(function(){

	$("#artists").on("click","tr a.artist_link", handleGetUser);
	getUsers();
	//Retrieve list of users from the server
	

})
/*** END ON LOAD**/

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
