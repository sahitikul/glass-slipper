# glass-slipper
SteelHacks Hackathon Project 2025

(team information) 
Emily Bartell     egb87@pitt.edu

This app allows users to upload a picture of a celebrity they look up to and would like makeup advice from. 
Our app then takes that celebrity and detects some of there main traits including gender, age, and basic facial features.
Then, it provides the user with specified makeup products and tips similar to the style of their favorite celebrity.
This way, users can find products that their favorite celebs use and add them to their own routines. 
Thus, allowing them to have a similar routine to someone they look up to! This can lead to more confidence and inspire creativity. 

(frontend explanation)

Backend

We first use Amazons Rekognition API to detect the celebrity from the user input.
Then, using this same API, it detects facial features and other basic information based off of the celebrity. 
It gathers features such as the persons gender, age, emotions, eyes, mouth, pose, etc. 
Then, using the OpenAI API, we take this information and curate makeup products and tips that closely match the ones the celebrity uses. 
In the end, users get recommendations based on the facial features of their favorite celebrity. 

(future plans)

