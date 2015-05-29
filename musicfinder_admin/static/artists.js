
/**** START CONSTANTS****/
//True or False
var DEBUG = true,
COLLECTIONJSON = "application/vnd.collection+json",
DEFAULT_DATATYPE = "json",
ENTRYPOINT = "/musicfinder/api/" //Entry point is getUsers()
ECHONEST_API = "http://developer.echonest.com/api/v4/artist/hotttnesss?api_key=F4AVFSUHXJALPX6NT&format=json&name="
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
			appendArtistToList(user.href, user_data);
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
		if (songs.length == 0)
		    alert("No songs by the selected artist");
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

	$(".selected .details").addClass("hideDetails");
	$(".selected").removeClass("selected");

    $(this).parent().parent().addClass("selected");
	$(".selected .details").removeClass("hideDetails");
    var href = $(this).attr("href");
    getSongs(href);






	return false; //IMPORTANT TO AVOID <A> DEFAULT ACTIONS
}

function search() {
	var apiurl = ENTRYPOINT + "artists/?";

	artistInput = $('#artist_input').val();
	countryInput = $('#country_input').val();
	languageInput = $('#language_input').val();
	genreInput = $('#genre_input').val();
    add = 0;
	if (artistInput){
	    apiurl+="name=" + artistInput;
	    add = 1;
	 }
	if (countryInput){
	        if (add)
	            apiurl += "&";
		    apiurl+="country=" + countryInput;
		    add = 1;
		}
    if (languageInput){
	        if (add)
	            apiurl += "&";
		    apiurl+="language=" + languageInput;
		    add = 1;
		    }
    if (genreInput){
	        if (add)
	            apiurl += "&";
		    apiurl+="genre=" + genreInput;
    }
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

            appendArtistToList(artist.href, artist_data);



		}
	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
		//Inform user about the error using an alert message.
		alert ("Could not fetch the list of users.  Please, try again");
	});
}

function appendArtistToList(url, data) {
    var toappend = '<h4><a class= "artist_link" href="'+url+'">'+data[0].value+'</a></h4><div class="details hideDetails">';
    if(data[1].value != null)
        toappend += '<h5>Genre: ' +
	data[1].value + '</h5>';
	if(data[2].value != null)
        toappend += '<h5>Country: ' +
	data[2].value + '</h5>';
	if(data[3].value != null)
        toappend += '<h5>Language: ' +
	data[3].value + '</h5>';
	if(data[4].value != null)
        toappend += '<h5>Active from: ' +
	data[4].value + '</h5>';

    return $.ajax({
		url: ECHONEST_API + data[0].value,
		jsonp: true,
		dataType:DEFAULT_DATATYPE,
		crossDomain: true,
		//headers: {"Authorization":"admin"}
	}).done(function (data, textStatus, jqXHR){
		if (DEBUG) {
			console.log ("RECEIVED RESPONSE: data:",data,"; textStatus:",textStatus)
		}
		var popularity = parseInt(data.response.artist.hotttnesss*100)
       	   if (popularity < 60)
            toappend += '<div class="c100 p'+popularity+' small orange">'+
                        '<span>' + popularity + '%</span>'+
                    '<div class="slice">'+
                        '<div class="bar"></div>' +
                        '<div class="fill"></div>'+
                    '</div></div>';
	       else if(popularity < 75)
            toappend += '<div class="c100 p'+popularity+' small">'+
                        '<span>' + popularity + '%</span>'+
                    '<div class="slice">'+
                        '<div class="bar"></div>' +
                        '<div class="fill"></div>'+
                    '</div></div>';
	       else
            toappend += '<div class="c100 p'+popularity+' small green">'+
                        '<span>' + popularity + '%</span>'+
                    '<div class="slice">'+
                        '<div class="bar"></div>' +
                        '<div class="fill"></div>'+
                    '</div></div>';



	}).fail(function (jqXHR, textStatus, errorThrown){
		if (DEBUG) {
			console.log ("RECEIVED ERROR: textStatus:",textStatus, ";error:",errorThrown)
		}
	})
	.always(function(){
	    toappend += "</div>"
		var $user = $('<tr>').html(toappend);
	    //Add to the user list
	    $("#artists").append($user);
	    return $user;

	});
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
	data.name = "byArtist";
	data.value = $("#artist").text();
	envelope.template.data.push(data);

    var data = {};
    data.name = "name";
    data.value = $("#song").text();
	envelope.template.data.push(data);

    addPlaylist(url, envelope);
});


	//Retrieve list of users from the server
})
/*** END ON LOAD**/