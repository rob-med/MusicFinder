
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

function getArtists() {
	var apiurl = ENTRYPOINT + "artists/";

	return $.ajax({
		url: apiurl,
		dataType:DEFAULT_DATATYPE
	}).always(function(){
		//Remove old list of users, clear the form data hide the content information(no selected)
		$("#artists").empty();
		$("#songs").empty();
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
					appendArtistToList(user.href, user_data[j].value);
				}			
			} 
		}
	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		//Inform user about the error using an alert message.
		alert ("Could not fetch the list of users.  Please, try again");
	});
}

function getSongs(apiurl) {
	return $.ajax({
		url: apiurl + "songs/",
		dataType:DEFAULT_DATATYPE, 
		//headers: {"Authorization":"admin"}
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
        $("#songs").empty();
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
		alert ("Cannot retrieve songs.")
		//Deselect the user from the list.
		deselectArtist()
	});
}

function handleGetArtist(event) {
	if (DEBUG) {
		console.log ("Triggered handleGetUser")
	}
	event.preventDefault();

	$(".selected").removeClass("selected");
    $(this).parent().addClass("selected");
    var href = $(this).attr("href");
    getSongs(href);






	return false; //IMPORTANT TO AVOID <A> DEFAULT ACTIONS
}

function search() {
	var apiurl = ENTRYPOINT + "artists/";

	artistInput = $('#artist_input').val();
	countryInput = $('#country_input').val();
	languageInput = $('#language_input').val();
	genreInput = $('#genre_input').val();

	return $.ajax({
		url: apiurl,
		dataType:DEFAULT_DATATYPE
	}).always(function(){
		$("#artists").empty();
		$("#songs").empty();
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
		//Extract the users
    	artists = data.collection.items;
		for (var i=0; i < artists.length; i++){
			artist = artists[i];
			artist_data = artist.data; 
			for (var j=0; j<artist_data.length;j++){
				if (artist_data[j].name=="name"){        
					artistName = artist_data[j].value;      // Get the name of the artist in the form
				}
				if (artist_data[j].name=="genre"){
					artistGenre = artist_data[j].value;     // Get the genre of the artist in the form
				}
				if (artist_data[j].name=="country"){
					artistCountry = artist_data[j].value;   // Get the country of the artist in the form
				}
				if (artist_data[j].name=="language"){
					artistLanguage = artist_data[j].value;  // Get the language of the artist in the form
				}			
			}

			if (!artistName) {

			} else if ((artistInput && artistName.toLowerCase().indexOf(artistInput.toLowerCase())>-1) || !artistInput) {
				if (!artistCountry) {

				} else if ((countryInput && artistCountry.toLowerCase().indexOf(countryInput.toLowerCase())>-1) || !countryInput) {
					if (!artistLanguage) {

					} else if ((languageInput && artistLanguage.toLowerCase().indexOf(languageInput.toLowerCase())>-1) || !languageInput) {
						if (!artistGenre) {

						} else if ((genreInput && artistGenre.toLowerCase().indexOf(genreInput.toLowerCase())>-1) || !genreInput) {
							appendArtistToList(artist.href, artistName);
						}
					}
				}
			}
		}
	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		//Inform user about the error using an alert message.
		alert ("Could not fetch the list of users.  Please, try again");
	});
}

function appendArtistToList(url, nickname) {
	var $user = $('<tr>').html('<a class= "artist_link" href="'+url+'">'+nickname+'</a>');
	//Add to the user list
	$("#artists").append($user);
	return $user;
}

function appendUserToList(url, nickname) {
	var $user = $('<tr>').html('<a class= "artist_link" href="'+url+'">'+nickname+'</a>');
	//Add to the user list
	$("#users").append($user);
	return $user;
}

function appendSong(song) {
	var $user = $('<tr>').html('<td><p>'+ song[0]["value"]+'</p>' +
	'<p>' + song[2]["value"] + '(' + song[3]["value"]+ ')</p></td>' +
	'<td><button type="button" class="hooks btn btn-primary btn-lg" data-toggle="modal" data-target="#chooseModal" data-song="' + song[0]["value"] +'" data-artist="'+ song[1]["value"] + '">+</button></td>');
	//Add to the user list
	$("#songs").append($user);
	return $user;
}

function choosePlaylist(nickname){

    var apiurl = ENTRYPOINT + "users/"+nickname+"/playlists/";

	return $.ajax({
		url: apiurl,
		dataType:DEFAULT_DATATYPE
	}).always(function(){
		//Remove old list of users, clear the form data hide the content information(no selected)
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
		//Extract the users
    	users = data.collection.items;
		for (var i=0; i < users.length; i++){
			var user = users[i];
			var user_data = user.data;
			for (var j=0; j<user_data.length;j++){
				if (user_data[j].name=="name"){
					$(".dropdown-menu").append('<li role="presentation"><a id="boh" role="menuitem" tabindex="-1" href="#">'+ user_data[j].value + '</a></li>');
				}
			}
		}

});
}

function deselectArtist() {
	$("#artists li.selected").removeClass("selected");
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
		alert ("Song successfully added!");
		//Add the user to the list and load it.
		// $user = appendUserToList(jqXHR.getResponseHeader("Location"),nickname);
		// $user.children("a").click();

	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		alert ("Could not add the song.");
	});
}

function processForm()
  {
    var parameters = location.search.substring(1).split("&");
    return parameters
  }

/*** START ON LOAD ***/
//This method is executed when the webpage is loaded.
$(function(){
    nickname = processForm();
	$("#artists").on("click","tr a.artist_link", handleGetArtist);
	getArtists();

    choosePlaylist(nickname);
    $('#chooseModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var song = button.data('song') // Extract info from data-* attributes
  var artist = button.data('artist')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('#artist').text(artist)
  modal.find('#song').text(song)
})


$(".dropdown").on("click",".dropdown-menu li a", function(){
url = '/musicfinder/api/users/' + nickname + '/playlists/' + $(this).text() + "/"
		var envelope={'template':{
								'data':[]
	}};
	var data = {};
	data.name = "artist";
	data.value = $("#artist").text();
	envelope.template.data.push(data);

    var data = {};
    data.name = "title";
    data.value = $("#song").text();
	envelope.template.data.push(data);

    addPlaylist(url, envelope);
});


	//Retrieve list of users from the server
})
/*** END ON LOAD**/