# RedditWeeklySpotifyPlaylist
![](https://res.cloudinary.com/toreckk/image/upload/v1562946657/SpotifyPlaylist.png)

A python script that updates a spotify playlist weekly, with the top 50 weekly posts on /r/listentothis.

Currently hosted on AWS Lambda function, and updating the following playlist: 



https://open.spotify.com/playlist/76Lp1VihCkH3lq0M2rwWtu?si=w9FecOS4RFyEJPbdHhAoJw

## Requirements

 - Python 3.7+


## Setup

### Locally

To run this project locally:

1. Clone this repo:

				# Clone this repository
                
				$ git clone https://github.com/Toreckk/RedditWeeklySpotifyPlaylist
        
2. Install the requests and PRAW packages

				$ pip install requests

                $ pip install praw
                
3. Fill in the exampleconfig.json and edit the name to config.json

	 3a. For the Spotify client ID and Secret, visit the [spotify developers web page](https://developer.spotify.com/) create an app, and fill in the required data. 
     
     3b. For the Reddit client ID and Secret,Visit the [following reddit page](https://www.reddit.com/prefs/apps/), create an app and fill in the required data.
     3c. Change your client's User-Agent string to something unique and descriptive, including the target platform, a unique application identifier, a version string, and your username as contact information, in the following format:
     
			<platform>:<app ID>:<version string> (by /u/<reddit username>)
            
     3d. If you don't have the access tokens and refresh token refer to the [usage](##usage) section.
     
   
            
### AWS Lambda

1. Clone this repo:

				# Clone this repository
                
				$ git clone https://github.com/Toreckk/RedditWeeklySpotifyPlaylist
                
2. Install the requests and PRAW packages on the same folder

				$ pip install requests -t .

                $ pip install praw -t .
                
                
3. Zip the file                 
4. Create a new [AWS Lambda](https://aws.amazon.com/lambda/) function
5. Configuration tab > Function code section > Code entry type > Change from edit code inline to Upload a .zip
6. Upload the .zip containing the project
7. Fill in the environment variables with the keys from the config.json file 

![Environment variables](https://res.cloudinary.com/toreckk/image/upload/v1562945167/Secrets.png)
             
             
             
## Usage

### Locally

1. Run the main.py script
2. If you don't have access + refresh tokens:

	 2a. You will be prompted with a link click it and give it permissions
     
     2b. Wait to be redirected and copy the link with the following format:
     
         http://localhost:8888/callback?code=NApCCg..BkWtQ&state=profile%2Factivity
         
     2c. Paste the link and hit enter, this will get the tokens for you
     
NOTE: You will only only have to do step 2 ONCE!


![](https://res.cloudinary.com/toreckk/image/upload/v1562946265/WithTokens.png)


### AWS Lambda

1. If you don't have access + refresh tokens follow the [local usage](##Usage), to obtain the tokens.
2. Fill in the environment variables as described in the [Setup](##Setup) section.
3. Press Test!

![](https://res.cloudinary.com/toreckk/image/upload/v1562946618/TestAWSLambda.png)

4. If you want the trigger script periodically follow this  [AWS Lambda guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html).



## Contributing


Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

How to get in contact


## License
This project is licensed under the MIT License - see the LICENSE.md file for details



         


