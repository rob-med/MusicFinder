
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



/*
Sends an AJAX request to retrive the template to create a new user.
	ONSUCCESS=> Show in #mainContent the form to create a new user (create_user_form).
	            a)The necessary input names are read from the response template element.
	            b)The Form is created using the helper methods createFormFromTemplate.
	            c)The Form is added using the helper method showNewUserForm
	ONERROR => a)Show an alert to the user
	           b) Go back to initial state by calling deselect user.
*/

/*
Sends an AJAX request to retrieve information related to a user(Resource name = User. See Appendix1)
INPUT: apiurl => The URL of the target user

ONSUCCESS =>
             a)Extract basic user information (nickname and registereddate)
               from the response and show it in the #user_public_form
             b)Add the url of the current user (self) to the action attribute
               of user_public_form. In that way we can Delete the current user
               by pressing #deleteUser button.
             c)Extract the URL of the user restricted_profile (User_restricted resource)
               and user history (History resource).
    		 d)Get the previous resources in parallel by calling getRestrictedProfile()
    		   and getUserHistory()
    		 e) The handlers of the previous methods will show the required
    		    information to the user.
ONERROR =>   a)Alert the user
             b)Unselect the user from the list and go back to initial state
*/




/*
Sends an AJAX request to retrieve the restricted profile information
(Resource name = User_restricted. See Appendix1)
It must be an authorized request so it must include Authorization header with value "admin".
INPUT: apiurl => The URL of the public profile
ONSUCCESS =>
	a)Create and fill the form (#user_restricted_form) with the information received on
	  the data parameter.
	  a.1) Call the method createFormFromTemplate in order to create such form.
	       The template is obtained from the response data.
	  a.2) Fill it with with the properties received in the respnse data.
	       Accordding to appendix 1 a template of a restricted profile have
	       the following properties:
			* "address"
            * "birthday"
            * "email"
            * "familyName"
            * "gender"
            * "givenName"
            * "website"
            * "telephone"
            * "skype"
            * "image"
       a.3) Append the form to the #userRestrictedInfo container
ONERROR =>
  	a)Show an alert informing the restricted profile could not be retrieved and
  	  that the data shown in the screen is not complete.
    b)Unselect current user and go to initial state by calling deselectUser .
*/
/*
Sends an AJAX request to retrieve information related to user history.
INPUT: apiurl => The URL of the History resource
ONSUCCESS =>
	a)Check the number of messages received (data.items) and add this value to the #messageNumber span element.
	b)Iterate through all messages. For each message in the history, call the function getMessage(messageurl). You
	  can extract the url of each message from the response object.
ONERROR =>
  	a)Show an alert informing the user that the target user history could not be retrieved
  	b)Deselect current user and go to the initial state by calling the deselectUser() method.

*/
/*
Sends an AJAX request to create a new user (POST).
INPUT: apiurl => The URL of the new User
	   userData => The template object to be returned as a Javascript object
	   nickname => The nickname of the user.
ONSUCCESS =>
	a)Show an alert informing the user that the user information has been modified
	b)Append the user to the list of users (call appendUserToList)
	  * The url of the resource is in the Location header
	  * appendUserToList returns the li element that has been added.
	c)Make a click() on the added li element. To show the information.
ONERROR =>
  	a)Show an alert informing the user that the new information was not stored in the databse

*/

/*
Sends an AJAX request to modify the restricted profile of a user (PUT)
INPUT: apiurl => The URL of the restricted profile to modify
	   template => The Javascript object containing the Collecton+JSON template
	   with the existing data.
	   Check the format from Appendix1 (Resource name = User_restricted)
ONSUCCESS =>
	a)Show an alert informing the user that the user information has been modified
ONERROR =>
  	a)Show an alert informing the user that the new information was not stored in the databse
  	b)Unselect current user and go to the initial state by calling deselectUser

*/
/*
Sends an AJAX request to delete an user from the system (DELETE)
INPUT: apiurl => The URL of the user to remove

ONSUCCESS =>
	a)Show an alert informing the user that the user has been deleted
	b)Reload the list of users: getUsers().
ONERROR =>
  	a)Show an alert informing the user could not been deleted
*/
/*
Sends an AJAX request to retrive a message resource (GET)
ONSUCCESS=> a)Create a new form of class .message with the content of this response
	  a.1) Call the helper method appendMessageToList
	  a.2) Get the title and the body of the message from the HTTP response
ONERROR => Show an alert to the user
*/
/*
Sends an AJAX request to remove a message resource (DELETE)
ONSUCCESS=>
      a) Inform the user with an alert.
      b) Go to the initial state by calling the reloadUserData function.
ONERROR => Show an alert to the user
*/

/**** END RESTFUL CLIENT****/


/**** BUTTON HANDLERS ****/

/*
	Handler for the user_list li a.user_link element.
	This function modify the selected user in the user_list (using the .selected
	class) and call the getUser to retrieve user information.
	TRIGGER: Pressing the a.user_link  inside #user_list
*/
function handleGetUser(event) {
	if (DEBUG) {
		console.log ("Triggered handleGetUser")
	}
	event.preventDefault();//Avoid default link behaviour
	//TODO 2
	// This event is triggered by the a.user_link element. Hence, $(this)
	// is the <a> that the user has pressed. $(this).parent() is the li element
	// containing such anchor.
	//
	// Use the method event.preventDefault() in order to avoid default action
	// for anchor links.
	//
	// Remove the class "selected" from the previous #user_list li element and
	// add it to the current #user_list li element. Remember, the current
	// #user_list li element is $(this).parent()
    //
	//
	// Finally extract the href attribute from the current anchor ($(this)
	// and call the  method getUser(url) to make the corresponding HTTP call
	// to the RESTful API. You can extract an HTML attribute using the
	// attr("attribute_name") method  from JQuery.
	//
	//

	$(".selected").removeClass("selected");
    $(this).parent().addClass("selected");
    var href = $(this).attr("href");
    getUser(href);






	return false; //IMPORTANT TO AVOID <A> DEFAULT ACTIONS
}


/**
 Creates User resource representation using the data from the form showed in the screen.
 Calls the method addUser to upload the new User resource to the Web service.
 TRIGGER: Submit button with value Create from form #create_user_form
**/
/**
 Modifies current User_restricted resource representation using the data from the form showed in the screen.
 Calls the method editRestrictedUserProfile to upload the new user information to the Web service.
 TRIGGER: Submit button with Edit value from form #user_restricted_form
**/


/**
Calls the function deleteUser to remove the current user from the Web service.
TRIGGER: Delete user button.
**/

/**
Calls the function deleteMessage to remove the current message from the Web service.
TRIGGER: Delete message button.
**/
/*
Calls to getUsersForm in order to extract the template and create the form.
TRIGGER This method is called when #addUser is clicked
*/
/**** END BUTTON HANDLERS ****/

/**** UI HELPERS ****/
/*
Add a new li element in the #user_list using the information received as parameter
	PARAMETERS: nickname => nickname of the new user shown in the screen.
	            url=> url of the new user.

*/
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
/*
Creates a form with the values coming from the template.

INPUT:
 * url=Value that will be writtn in the action attribute.
 * template=Collection+JSON template which contains all the attributes to be shown.
 * id = unique id assigned to the form.
 * button_name = the text written on associated button. It can be null;
 * handler= function executed when the button is pressed. If button_name is null
   it must be null.

 OUTPUT:
  The form as a jquery element.
*/

/*

Serialize the input values from a given form into a Collection+JSON template.

INPUT:
A form jquery object. The input of the form contains the value to be extracted.

OUPUT:
A Javascript object containing each one of the inputs of the form serialized
following  the Collection+JSON template format.
*/

/*
Add a new .message element to the #list in #messages
	PARAMETERS: url=> url of the new message. It is stored in the action attribute of the corresponding form
				tite=>The title of the message
				body=> The body of the message.
*/

/*Helper method to show the ExistingUserData. It purges the old data.

*/
/*
Helper method to purge and show the newUserData form.
*/
/**
Helper method that unselect any user from the User_list and go back to the
initial state by hiding the "#mainContent".
**/
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

/*** START ON LOAD ***/
//This method is executed when the webpage is loaded.
$(function(){

	//TODO 1: Add corresponding click handler to #deleteUser and #addUser buttons.
	//The handlers are:
	// #deleteUser -> handleDeleteUser
	// #addUser -> handleCreateUserForm
	// Check http://api.jquery.com/on/ for more help.




	//TODO 1: Add corresponding click handlers for #deleteMessage button and
	// anchor elements with class .user_link from #user_list
	//Since these elements are generated programmatically
	// (they are not in the initial HTML code), you must use delegated events.
	//Recommend delegated elements are #messages for #deleteMessage button and
	// #user_list for  "li a.user_link"
	//The handlers are:
	// #deleteMessage => handleDeleteMessage
	// li a.user_link => handleGetUser
	// Direct and delegated events from http://api.jquery.com/on/
	nickname = processForm();
    $("#playlists").on("click", "tr a.playlist_link", handleGetUser);
	getPlaylists(nickname);
	//Retrieve list of users from the server
})
/*** END ON LOAD**/