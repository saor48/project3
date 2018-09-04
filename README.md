A chat application to teach basic English writing for non-native speakers.
Expected input is a single phrase.
App is multi-player and with a limit set on number of users
Ideal for in classroom use or student practice

Features:
1. Each word is checked for correct spelling against a file of basic English words.
        Words found as correct will be printed normally
        Words not found will be printed in brackets.
2. A score is assigned as +1 for a word in the list, -1 if not in the list.
        Cumulative score is shown on user's page
3. A leaderboard, based on above score, is shown on each user page
4. A user selected line can additionally be checked for correct structure.
        This function is limited in scope to a basic check of correct verb positioning.
        Beyond this would be overly complex for this project.
        The challenge can be set in scoring or non-scoring mode

Technology:
1. Python with jQuery to update chat messages every 5 secs.
2. Multi-threading used for most file writes and read
3. considered queue to update vars in main from thread
        but using thread globals to return values to decrement was simpler
4. considered asyncio for checking words in wordlist 
        but cloud 9 has py3.4 and most asyncio modules are py3.5