# Hospitality50 - CS50 Final Project
#### Video Demo:  https://www.youtube.com/watch?v=VGjxhvUBFHw
#### Description:
The project is a webpage where staff teams of hospitality services can create tasks to either maintenance or housekeeping. It's implementation is fairly simple, to keep the project scope in check. It provides the user with simple interface and tools to keep track of tasks and their completion.

#### Technologies used:

 - Flask
 - JavaScript
 - Jinja
 - CSS
 - HTML
 - SQL

### Detailing:
#### Layout:
In the Layout template, I've made use of a navbar and made adjustments to better fit the needs of my website. I have created links to functions in app.py that render other templates. The navbar behaves in two different ways, one is if no user_id is detected in session, showing links to login and register, and the other is by detecting an user_id logged an showing links to log out, index, new task, closed tasks and reports.
The template also lays Jinja blocks for the bodies of the other templates used, and the footer for all other templates.


#### Login:
The login template is pretty simple, it asks the user for a username and password, it calls for @app.route "/login" which accepts POST and GET methods. If the method is GET it will render the template with the forms asking for the user's information, when the user fills this and send a POST request, it will check the users table in the tasks.db database for compatible username and password, if everything is provided correctly it will redirect the user to @app.route "/" the index of the website.
If no valid information is provided it will return to the user with an apology informing of the problem it encountered.
The @app.route "register" is also only accessible through the navbar presented at the login screen.

#### Index:
In the index when getting a GET request the website shows the user a table with all the current open tasks, meaning unresolved issues in some room. The table is dynamically generated using a Jinja for loop that gets it's data from a query in it's app.py back-end. The user can also close a task by clicking the close button, informing other users that the task is done, when the close button is clicked a POST request is sent to app.py,  which will change the status of the task to closed and it will no longer show in the index page.
The table can also be sorted by team making it easier to identify which tasks someone should be looking to complete, the sorting mechanism works via a Javascript in the page, that rearranges rows by switching them until no switching of rows is done.
The Navbar here is the same as other pages except register and login, meaning a user can access the New Task, Closed Tasks and Reports, as well as log out from the website.

#### New Task:
When accessing the New Task page via a GET request the user will be prompted to provide a Room Number, a Location in the Room, a Team to resolve the task and some Details to briefly describe what needs attention. After providing all this information the user will click the Create Task button that will send a POST request to app.py, which will check the information in the forms and provide an apology if anything is not properly filled, if everything is in order it will record the information as well as the user_id in the tasks table in the tasks.db database, which will timestamp the new entry as well as providing an id to the task and the open status, it will also redirect the user to the index page.

#### Closed Tasks:
The closed tasks will only take GET requests and will generate a dynamic table like the one from the index except it will only show closed tasks.

#### Reports / Reported:
These pages work for the same end, to provide the user with a report of activity during a certain time period and if needed a certain team. The Reports page when receiving a GET request prompts the user to provide a time period in From Date and To Date, it also asks the user for a team however that being optional. After the user provides the information and clicks the Create Report button it will send a POST request to app.py where it will verify and validate the time period provided, if the information provided is valid it will query the tasks.db for all the information that fits the time period and team (if provided). After which it will render the Reported template, that will show the information provided by the query in a dinamic table similar to the ones in index and closed tasks, except that it will be able to be sorted by Id, Time, User id, Team, Room Number and Status, using the same script used in index.html.

#### Register:
In the register page when receiving a GET request the user will be asked to provide an username, a team to be a part of, a password and its confirmation, after filling the forms and clicking the Register button, it will send a POST request to app.py, which will verify if the username is available in the users table in the tasks.db database, it will also verify the password and confirmation making sure it matches, after validating all the information it will save the username, the team, and it hash the password and store it's hash, and create a unique user id, in the users table in tasks.db.