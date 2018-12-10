# English Chat Page
A chat application to teach basic English writing for non-native speakers.
Expected input is a single phrase.
App is multi-player and with a limit set on number of users
Ideal for classroom use or student practice
Messages are stored in text and json files for further analysis if required.

## UX
Home page gives user the option to read the Guidelines. 
Then they can create their own page by entering a username.
From own page user submits a phrase in a message box and that phrase is shown 
    in the main box with any spelling errors surrounded by [].
User can see messages from other users every 5 seconds.
User can see usernames of all other users.
User messages are scored as per the Guidelines.
User can see their own score and a Leaderboard of scores on their page.
On the right of the page is a seperate box (yellow box) to test phrase structure.
User can enter any line number from main box to test that phrase, selecting it 
    as either a statement or a question.
A specific error message is shown for any errors found.

## Features:
1. Each word is checked for correct spelling against a file of basic English words.
        Considered incorrect are contractions and most proper nouns
        Words found as correct will be printed normally
        Words not found will be printed in brackets.
2. A score is assigned as +1 for a word in the list, -1 if not in the list.
        Cumulative score is shown on user's page
3. A leaderboard, based on above score, is shown on each user page
4. A user selected line can additionally be checked for correct structure.
        This function is limited in scope to a basic check of correct verb positioning.
        Beyond this would be overly complex for this project.
        ? The challenge can be set in scoring or non-scoring mode
5. User Limit: set to 3 for testing purposes
6. New messages and leaderboard are updated every 5 secs to other users
7. Rest of user's page is only updated when user submits a valid form.
        Note: it takes 15 seconds and then 2 POSTs from other users 
                to record that a user has left the site.
8. Guidelines for users available from sign-in page

## Technology:
- [Flask] (http://flask.pocoo.org/)
    - microframework used for this project
- [Python 3] ( https://www.python.org/ )
    - This project is python driven.
- [Bootstrap 3] ( https://getbootstrap.com/ )
   - The styling library
- [JQuery] (https://jquery.com)
    - updates chat messages every 5 secs.
- Multi-threading used for most file writes and read

## Testing:
- The main messaging section (blue box) is tested manually.
- The structure analysis ( yellow box) uses atomated testing at /chat/test
- Structural tests are limited to the single phrases that the app can currently handle.

### Main Section Tests:
- Submit a message with correct spelling results in phrase appearing in main box 
       without any brackets and scored correctly.
- Submit a message with incorrect spelling results in phrase appearing in main box 
       with incorrect words in brackets and scored correctly.
- Submitting messages from other user pages results in correct scoring on Leaderboard.
- Submitting blank message prevented by required attribute

### Structure Section Tests:
- Submitting blanks prevented by required attribute
- Submitting non-existant line (x) produces result "x>Challenges must have at least three words"
- Automated test page at /chat/test. All tests produce expected results.
- Automated test data files stored at /data/tests


### Devices
    - Tested on google inspect for different screen sizes. No issues found.
    - Tested on browsers Chrome, Edge, Opera.

### Issues:
1. Bugs:
    1. 
    
    

## Deployment:

1. App deployed on Heroku :https://project3-chat.herokuapp.com/
2. Files created for this deployment: Procfile, requirements.txt.
3. GitHub:https://github.com/saor48/project3