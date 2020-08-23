# Project 2

#####  Web Programming with Python and JavaScript

This project is a chat application. It allows the user to create channels and send messages that any other user on the current channel can read. The application also gives user the option of deleting its own messages.

File contents:  
application.py - main code of flask application  
models.py - classes for channels and messages  
.gitignore - excludes unnecessary files/directories  
requirements.txt - required packages  
templates directory:  
 - base.html is jijna2 base template  
 - other .html files are children templates for all subpages of the application  

static directory:
 - app.js - display name, last visited channel, saving data in local storage
 - io.js - SocketIO features, adding and deleting messages
  - style.scss - application styling
 
For personal touch I have added possibility to delete one's own messages.
