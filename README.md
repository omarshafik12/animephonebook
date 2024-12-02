Project Infrastructure  (it is much easier to read the google doc: https://docs.google.com/document/d/1VlozW9tYYSw_XpVS8576VWqZtZbD-sZqz7sHOZ1nV6M/edit?usp=sharing)
This is my first time doing this so I have no idea what to write. 

Prerequisites
Amazon S3: 

	The images used for each character were placed into S3 to allow organization as placing many separate folders or placing all images into one would be confusing. Secondly, I was going to have added profile pictures be uploaded to S3 but the removal process with os.remove() was simpler and seemed more practical as this was all temporary. 

MySQL: 

Before any code towards the application, I constructed the base table that would be copied. Though my original iteration was changed multiple times due to necessary additions such as tm_tokens. 

Fakeyou:

	As I originally planned to train models on the characters' voices using Tacotron 2. I happened to find Fakeyou, which has other people’s models already trained. Using their $25 a month subscription, I was allowed to use their API. 

Main Website Template:
	
Every page you see other than the call page and the profile pages used the “Responsive Halloween Website” (https://github.com/bedimcode/responsive-halloween-website) created by bedimcode as the template I altered. 

Profile Pages Template:

	Both the View and Edit profile originated from this one template named “User Profile Page” (https://www.creative-tim.com/bits/bootstrap/user-profile-page-argon-dashboard) by Creative Tim. 

Call page Website Template:

	As for specifically the call page, the template used was “Video Calling Website UI Design”(https://codepen.io/vkive/pen/gOGZezV?fbclid=IwAR0Pgt5pTXSaofdWUoQYhhgwqnhepH3gWQOeqH2neNhkMzaMHJn5hgJJh5o) by Vanessa. 

Database closure and file deletion:

	I simply started a thread that is practically a countdown that when reached, deletes all user saved images and closes the connection to the database.
Home Page
As for the home page, the only main logic that was incorporated was the search bar and transfering user input to the query page.

The remainder consists of simple html and css adjustments with the addition of audio clips for each swipe of the slider. 
List Page
The List Page presented much more sophistication as I had to correctly transfer data pulled from MySQL to the correct location on the front end. It is simple to me nowadays but the learning curve of the correct SQL script and Python in html was a notable amount.

Secondly, The incorporation of the add profile was complex as adjusting in the zoom in effect and slide feature was constantly accidentally changing margins and or other elements.

Other than that the development took me two days and was relatively simple.
Querying Page
The Query page was relatively a copy and paste of the list page and the only difference was who was presented based on certain conditions, other than that it was all the same.

The only difficulty was building a query that searched each category with the user’s query. First I incorporated all the categories in the search and then in SQL language to my database to retrieve each row with that query in any category. This is apparent as if you search “Goku” both Goku and Gohan show up as I believe it mentions that he is Goku’s Son which has “Goku in it. 

I recognize that that query logic is incorrect especially with large tables and databases, but since in this use case, only a few users will ever use it and the tables are refreshed every couple hours. I thought it would be practical due to the scale of traffic.
Viewing Profile Page
This was the second hardest page and took me about a month. The incorporation of WTForms into the front end caused plenty of issues in the translation aspect as due to me originally using default values kept the values equal to the default values no matter the user input. 

After using data Filerequired and datarequired, it allowed me to remove default values which in turn allowed for the translation to occur. The only remaining issue that I spent around 2 weeks on but couldn’t resolve was that uploaded images would show on the list and query page, but not show on the profile image page though they were there. 

Simply the backend uses WTForms and a post request to update current data in the temporary table. While using SQL and placeholders to show the user the current data in the front end. \
Adding Profile Page
Copying the structure and html of the viewing page, I simply altered the SQL statement to insert the new data and since I knew the user had to input data into data fields I was able to just paste %s the correct number of times. 

Then I simply set the placeholder values to example data to give the user an idea of what to type in.
Call Page
This aspect of the project was the most painstaking due to Fakeyou, my incompetence, and multiple iterations. I believe it took me 2-3 months to complete.

Starting with user_input_and_gpt_processor.py, This was rather simple as I had to incorporate APIs from Google and OpenAI who practically wrote the code for you and provided excellent documentation. After initializing the speech recognizer, I simply set it to record and remove ambient noise. Then sent the audio data to Google’s tts(text to speech). With the new string I added pretty much conditions on ChatGPT to fabricate the result in a key way. I needed Romaji(Japanese written in english text), the translation to show the user what was said, and for the model to impersonate the character.

A problem that I could not change was the recognizer, either my mic is bad or the software is not as great as I thought. It messes up your words many times.

As for gpt_processer, I simply used their streaming methodology as it was faster. The second change was that I set the max_tokens to 100 so that my $5 goes a long way, click here(https://platform.openai.com/tokenizer) to quickly see how much 100 tokens is. This causes issues as the GPT just cuts off the response, but since this is a small project and I am financially limited, it made sense. Lastly, I used gpt 3.5 and not the latest gpt-4.

Another problem that leads to the result of “unable to translate” is when the GPT has a response to a question that is over 100 tokens in just romaji so it never produces the english translation causing an error. Though this is just a financial problem so the code is fine. 

As for the voice_encoder.py, This is the file that worked with the fakeyou api and provided the most difficulty. For some reason, I really couldn’t understand the documentation(https://docs.fakeyou.com/#/) provided by Fakeyou, it was probably my lack of experience. I decided to look in the packages and look through their code instead and just learn what I didn’t know. The two main files of importance were objects.py and fakeyou.py.

After understanding how fakeyou structured the way it delivered its package which could be found in the functions: “make_tts_job” and “tts_poll” in the fakeyou.py. I saw that it sent the wav file to the destination folder and also sent hjson package with key info, mainly the name of the file. I was able to extract that name since I believe it was built like a dictionary if I remember correctly, which then I put that name into the folder path variable.

Upon that I first used playsound, but that was conflicting with os.remove(). So I switched to pygame mixer since it was wonderful in that it had a stop method that only allowed progress upon the completion of it playing the sound. Upon that I had it close after playing and had it delete the file with os.remove().

As for the route in main.py and the html, This aspect went through many iterations from an initial while loop, a recursive function, threading, threading and recursive, threading and recursive with a txt file, to finally Javascript. I was confused at why it wasn’t working, until I read somewhere that you have to follow a request response cycle and that web applications weren’t the best at looping while threading. So I adjusted to JS to build the loop, and it worked.
