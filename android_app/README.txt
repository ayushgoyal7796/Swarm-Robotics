										********SWARM ROBOTICS MOBILE APPLICATION********

***We are using this application for interfacing swarm bots with mobile over wifi networking communication system***

Firstly,a server-client network is created by creating a server with the help of a router and bots as client.
After succesfully setting up the server, and configuring mobile application as client All corresponding codes & algorithms are uploaded on devices.


                  ANDROID APP setup
				  
				  The app comprises of three activities:
			MainActivity
			First activity
			Second activity
		
MainActivity    : MainActivity consists of shapes and manual operation buttons.
				   when shapes button is pressed it transfers the control to first activity.
				   when shapes button is pressed it transfers the control to second activity.
				   MainActivity over.

First activity  : It consists of buttons with names of different shapes and other functions.
				   When a button is pressed,the particular command signal is loaded as JSON format for transfer through HTTP request to the server
				   In this way,the command for different shapes is being sent.
				  
Second activity : It consists a blank screen mapped with the arena of display of bots.
				  So we are able to move bots to respective locations pressed on the screen,mapped with arena.
				  

The data is being sent to server in JSON format through HTTPRequest.
