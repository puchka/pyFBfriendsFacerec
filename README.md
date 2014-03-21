Facebook Friends Facial Recognition Script
=============================================

It's a script intending to perform facial recognition.
The script constantly process through pictures on facebook and twitter logging the names and pictures that correlate to them.
The information is placed into an SQL database where it will be accessed as needed.
At a later date, we should be able to find all references to an individuals based upon what the script has catalogued,
if we type in a name or if we have a match to the facial recognition algorithm. The script is written in Python.

Installation in short
---------------------

- Register as a Facebook Developer
- Change the access token from the Graph API Exlorer [https://developers.facebook.com/tools/explorer/]
  in the variable **"oauth_access_token"** in *facerec.py* 
- Change the values of **"user"** and **"passwd"** variable in *dict_app.py* to
  your database settings
- Create a database named "facerec" in PhpMyAdmin : http://localhost/phpmyadmin
- Execute the *create_tables.py* for creating the table necessary for
  the script
- Execute *facerec.py* which is the main script.
  It will grab all names and photos of your buddies and store it in the
  "friends" MySQL table in the *facerec* database.

For more details about the installation and prerequisites libraries, see the Wiki.
