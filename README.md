Facebook Friends Facial Recognition Script
=============================================

- Register as a Facebook Developer
- Change the access token from the Graph API Exlorer [https://developers.facebook.com/tools/explorer/]
  in the variable **"oauth_access_token"** in *facerec.py* 
- Change the values of **"user"** and **"passwd"** variable in *dict_app.py* to
  your database seetings
- Create a database named "facerec" in PhpMyAdmin : http://localhost/phpmyadmin
- Execute the *create_tables.py* for creating the table necessary for
  the script
- Execute *facerec.py* which is the main script.
  It will grab all names and photos of your buddies and store it in the
  "friends" MySQL table in the *facerec* database.
