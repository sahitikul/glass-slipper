# glass-slipper
SteelHacks Hackathon Project 2025

Team information:
Emily Bartell     egb87@pitt.edu
Raima Saha        ras709@pitt.edu
Sahiti Kulkarni
Lakshya Srinivasan

This app allows users to upload a picture of a celebrity they look up to and would like makeup advice from. 
Our app then takes that celebrity and detects some of there main traits including gender, age, and basic facial features.
Then, it provides the user with specified makeup products and tips similar to the style of their favorite celebrity.
This way, users can find products that their favorite celebs use and add them to their own routines. 
Thus, allowing them to have a similar routine to someone they look up to! This can lead to more confidence and inspire creativity. 

Frontend:
(frontend explanation)


Backend:

We first use Amazons Rekognition API to detect the celebrity from the user input.
Then, using this same API, it detects facial features and other basic information based off of the celebrity. 
It gathers features such as the persons gender, age, emotions, eyes, mouth, pose, etc. 
Then, using the OpenAI API, we take this information and curate makeup products and tips that closely match the ones the celebrity uses. 
In the end, users get recommendations based on the facial features of their favorite celebrity. 


Future Plans:

1. Address the API call issues: We will set it up so that each user have to create an account to track the usage by user. Additionally, we will incorporate a database (preferably PostgreSQL so it can scale) so we can track usage per user and it will be easier to keep track of which user has exceeded their limit and notify them when they have.

2. Update to suggest to users face rather than basing off celebrity: Include an option so that the user can upload a picture of their face so that makeup, hair, and jewelry suggestions can be tailored to the user.

3. Improve depth and quality of suggestions: With more work, we could implement more prompting to have the AI suggest with more detail, particularly in regards to undertone and hue of the skin so that makeup and jewelry suggestions can be even more specific.

