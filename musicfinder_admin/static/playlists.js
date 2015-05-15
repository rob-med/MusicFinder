
/**** START CONSTANTS****/
//True or False
var DEBUG = true,
COLLECTIONJSON = "application/vnd.collection+json",
HAL = "application/hal+json",
FORUM_USER_PROFILE = "http://atlassian.virtues.fi:8090/display/PWP/Exercise+4#Exercise4-Forum_User",
FORUM_MESSAGE_PROFILE = "http://atlassian.virtues.fi:8090/display/PWP/Exercise+4#Exercise4-Forum_Message",
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

function getPlaylists(nickname) {
	var apiurl = ENTRYPOINT + "users/"+nickname+"/playlists/";

	return $.ajax({
		url: apiurl,
		dataType:DEFAULT_DATATYPE
	}).always(function(){
		//Remove old list of users, clear the form data hide the content information(no selected)
		$("#playlists").empty();
		$("#songsinpl").empty();
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
				if (user_data[j].name=="name"){
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
    getUser(href);
	return false; //IMPORTANT TO AVOID <A> DEFAULT ACTIONS
}

function search() {
	nickname = processForm(); // Get the user's nickname passed as parameter through the page neme (/playlists.html?nickname). It takes the name after the question mark.
	playlistInput = $('#playlistInput').val();
	var apiurl = ENTRYPOINT + "users/"+nickname+"/playlists/"+playlistInput+"/";

	return $.ajax({
		url: apiurl,
		dataType:DEFAULT_DATATYPE
	}).always(function(){
		$("#playlists").empty();
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
    	playlist = data.name;
    	href = data._links.collection.href;
    	appendUserToList(href+playlist+"/", playlist);
    	

	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		//Inform user about the error using an alert message.
		alert ("Could not find the playlist.  Please, try again");
	});
}

// It get all the songs that will be visualize in the table of the right, in the user's playlist page.
function handleGetsongs() {
	if (DEBUG) {
		console.log ("Triggered handleGetSongs")
	}
	event.preventDefault();//Avoid default link behaviour
	// $(".selected").removeClass("selected");
 //    $(this).parent().addClass("selected");
 //    var href = $(this).attr("href");
    getUser();
	return false; //IMPORTANT TO AVOID <A> DEFAULT ACTIONS
}

function appendUserToList(url, nickname) {
	var $user = $('<tr>').html('<a class= "playlist_link" href="'+url+'">'+nickname+'</a>');
	//Add to the user list
	$("#playlists").append($user);
	return $user;
}

function getUser(apiurl) {
	return $.ajax({
		url: apiurl + "songs/",
		dataType:DEFAULT_DATATYPE,
		//headers: {"Authorization":"admin"}
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        $("#songsinpl").empty();
		var songs = data.collection.items;
		for(i = 0; i<songs.length; i++){
            var song = songs[i].data;
			appendSong(song);

        }

	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		//Show an alert informing that I cannot get info from the user.
		alert ("Cannot extract information about this user from the forum service.")
		//Deselect the user from the list.
		deselectUser()
	});
}

function getSongs() {
	return $.ajax({
		url: apiurl + "songs/",
		dataType:DEFAULT_DATATYPE,
		//headers: {"Authorization":"admin"}
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        $("#songsinpl").empty();
		var songs = data.collection.items;
		for(i = 0; i<songs.length; i++){
            var song = songs[i].data;
			appendSong(song);

        }

	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		//Show an alert informing that I cannot get info from the user.
		alert ("Cannot extract information about this user from the forum service.")
		//Deselect the user from the list.
		deselectUser()
	});
}


function appendSong(song) {
	var $user = $('<tr>').html('<p>'+ song[0]["value"]+'</p>' +
	'<p>' + song[2]["value"] + " (" + song[3]["value"]+ ")</p>");
	//Add to the user list
	$("#songsinpl").append($user);
	return $user;
}
/*
Sets the url to add a new user to the list.
*/
function setNewUserUrl(url){
	console.log("NEW URL, ", url)
   $("#addUser").attr("href", url);
}

function deselectUser() {
	$("#user_list li.selected").removeClass("selected");
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

/**
Transform a date given in a UNIX timestamp into a more user friendly string.
**/
function getDate(timestamp){
	// create a new javascript Date object based on the timestamp
	// multiplied by 1000 so that the argument is in milliseconds, not seconds
	var date = new Date(timestamp*1000);
	// hours part from the timestamp
	var hours = date.getHours();
	// minutes part from the timestamp
	var minutes = date.getMinutes();
	// seconds part from the timestamp
	var seconds = date.getSeconds();

	var day = date.getDate();

	var month = date.getMonth()+1;

	var year = date.getFullYear();

	// will display time in 10:30:23 format
	return day+"."+month+"."+year+ " at "+ hours + ':' + minutes + ':' + seconds;
}

// It takes parameters from the URL. The parameter is the nickname of the user
function processForm()
  {
    var parameters = location.search.substring(1).split("&");
    return parameters
  }

/*** END UI HELPERS***/

function addPlaylist(apiurl, userData){
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
		alert ("Playlist successfully added");

	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		alert ("Could not create new playlist");
	});
}

function handleCreatePlaylist() {
	nickname = processForm();
	url = '/musicfinder/api/users/'+nickname+'/playlists/'
		var envelope={'template':{
								'data':[]
	}}; 
	var data = {};
	data.name = "name";
	data.value = $("#newPlaylistName").val();
	envelope.template.data.push(data);

	var date = new Date().getTime(); // Eventually to put even the date of creation.
    addPlaylist(url, envelope);
}


/*** START ON LOAD ***/
//This method is executed when the webpage is loaded.
$(function(){
	nickname = processForm(); // Get the user's nickname passed as parameter through the page neme (/playlists.html?nickname). It takes the name after the question mark.
    $("#playlists").on("click", "tr a.playlist_link", handleGetUser);
	getPlaylists(nickname); // Show just the playlist of the chosen user.
	$("#nickShowed").text(nickname); // Put the nickname just next to the title (in the header with id=nickShowed).
    $("#artbutt").attr("href", "artists.html?" + nickname);
})
/*** END ON LOAD**/