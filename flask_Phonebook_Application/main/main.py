from flask import Flask, render_template, request, redirect, url_for, session, request
from datetime import datetime, timedelta
from forms import QueryForm, ProfileForm
from voice_encoder import Talk
from user_input_and_gpt_processor import speech_reader, gpt_processor
import mysql.connector
import boto3
import os
import threading


app = Flask(__name__, static_folder='assets', template_folder='templates')
app.config["SECRET_KEY"] = os.environ.get("ANIMEPHONE-APP-SECRET-KEY")  # remember to change

#This is to make sure that the user's changes only last 8 hours at most
app.permanent_session_lifetime = timedelta(hours=8)

# Keep in mind that you will have to host the MySQL server on AWS
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password= os.environ.get('MYSQL-ANIMEPHONEBOOK-PASS'), ###os.environ
    database="animephonebook",
)

#creating a temporary table for user interaction during their session, table terminates the moment the connection with MySQL ends
with mydb.cursor() as mycursor:
        mycursor.execute("CREATE TEMPORARY TABLE temp_tbl SELECT * FROM anime_table;")

#to close the connection to mysql and delete all user profile images
def close_database():
    folder_path = 'flask_Phonebook_Application/main/assets/user_saved_images'

    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)
        os.remove(file_path)

    mydb.close()####remember to do that page that just lets you click and return back to the main page. 
    

def db_closing():
    start_time = datetime.now()
    
    closing_time = start_time + timedelta(hours=7)
    
    delay = (closing_time - start_time).total_seconds()
    
    timer = threading.Timer(delay, close_database)
    timer.start()

db_closing()


@app.route("/", methods=['GET', 'POST'])
def home():
    session['method'] = 'GET'
    session.permanent = True
    form = QueryForm(request.form)

    if request.method == 'POST' and form.validate():
        search_query = form.search.data

        return redirect(url_for('query', search_query=search_query))

    return render_template("home.html", form=form)

@app.route("/list")
def list():
    form_search = QueryForm(request.form)

    if request.method == 'POST' and form_search.validate():
        search_query = form_search.search.data

        return redirect(url_for('query', search_query=search_query))
    
    all_query = "SELECT * FROM temp_tbl"

    with mydb.cursor() as mycursor:
        mycursor.execute(all_query)
        results = mycursor.fetchall()

    return render_template("list.html", results=results)

@app.route("/query", methods=['GET', 'POST'])
def query():
    search_query = request.args.get('search_query', '')

    if request.method == 'POST':
        search_query = request.form.get('search')

    table_name = "temp_tbl"

    with mydb.cursor() as mycursor:
        mycursor.execute(f"SHOW COLUMNS FROM {table_name}")
        column_names = [column[0] for column in mycursor.fetchall()]

        conditions = " OR ".join([f"{column} LIKE %s" for column in column_names])

        query = f"SELECT * FROM {table_name} WHERE {conditions}"
        mycursor.execute(query, tuple([f"%{search_query}%" for _ in range(len(column_names))]))

        results = mycursor.fetchall()

    return render_template("querying.html", search_query=search_query, results=results)

@app.route("/view/<character_abilities>", methods=['GET', 'POST'])
def profile(character_abilities):
    view_query = "SELECT * FROM temp_tbl WHERE abilities = %s"
    queryform = QueryForm(request.form)

    with mydb.cursor() as mycursor:
        mycursor.execute(view_query, (character_abilities,))
        view_results = mycursor.fetchone()
    
    form = ProfileForm()
    if request.method == "POST":
        if form.submit.data:
            if form.validate_on_submit:
                first_name = form.firstname.data
                last_name = form.lastname.data
                phone_number = form.phonenumber.data
                anime_show = form.show.data
                abilities = form.abilities.data
                email = form.email.data
                address = form.address.data
                city = form.city.data
                country = form.country.data
                post = form.post.data

                #image being saved
                file = request.files['photo']
                file.save(f"flask_Phonebook_Application/main/assets/user_saved_images/{file.filename}")
                user_img_path = f"assets/user_saved_images/{file.filename}"

                
                #editing the temporary table with the new data
                with mydb.cursor() as mycursor:
                    mycursor.execute(f"UPDATE temp_tbl SET first_name = '{first_name}', last_name = '{last_name}', phone_number = '{phone_number}', anime_show = '{anime_show}', abilities = '{abilities}', email = '{email}', Address = '{address}', City = '{city}', Country = '{country}', Post_Code = '{post}', image_url = '{user_img_path}' WHERE abilities = '{character_abilities}';")
                return redirect(url_for('list'))

        elif form.delete_image.data:
            with mydb.cursor() as mycursor:
                #make the image url equal to the basic profile one
                mycursor.execute(f"UPDATE temp_tbl SET image_url = 'assets/img/gojo_placeholder.jpg' WHERE abilities = '{character_abilities}';")
        
        elif form.delete_profile.data:
            with mydb.cursor() as mycursor:
                #make everything be equal to ''
                mycursor.execute(f"DELETE FROM temp_tbl WHERE abilities = '{character_abilities}';")
            return redirect(url_for('list'))


    return render_template("view_profile.html", view_results=view_results, form = form, queryform = queryform)

@app.route("/add", methods=['GET', 'POST'])
def add_profile():
    
    form = ProfileForm()

    if request.method == 'POST':
        if form.submit.data:
            if form.validate_on_submit():
                first_name = form.firstname.data
                last_name = form.lastname.data
                phone_number = form.phonenumber.data
                anime_show = form.show.data
                email = form.email.data
                character_abilities = form.abilities.data
                address = form.address.data
                city = form.city.data
                country = form.country.data
                post = form.post.data
                tm_token = None

                #This is for the image upload
                file = request.files['photo']
                file = request.files['photo']
                file.save(f"flask_Phonebook_Application/main/assets/user_saved_images/{file.filename}")
                user_img_path = f"assets/user_saved_images/{file.filename}"
                
                with mydb.cursor() as mycursor:
                    sql = "INSERT INTO temp_tbl VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (first_name, last_name, phone_number, character_abilities, anime_show, email, address, city, country, post, user_img_path, tm_token)
                    mycursor.execute(sql, values)
                return redirect(url_for('list'))
        else:
            print("Form validation failed")
            
    return render_template("add_profile.html", form = form)

def template_rendering(tm_tokens, charac, english):
    with mydb.cursor() as mycursor:
        mycursor.execute(f"SELECT image_url FROM temp_tbl WHERE first_name = '{charac}' OR last_name = '{charac}';")
        talk_to_img = mycursor.fetchone()

        #this is beacuse fetchone returns a tuple and I just want the first url it returns
        if talk_to_img:
            talk_to_img = talk_to_img[0]
    
    #did it this way because I was worried that changing the names in the db might mess something up.
    if charac == "Rorarona Zoro":
        talk_to_img = 'https://anime-phonebook.s3.amazonaws.com/one_piece/Zoro.png'
    elif "D." in charac:
        talk_to_img = 'https://anime-phonebook.s3.amazonaws.com/one_piece/Luffy_new_1.png'

    return render_template("call.html", talk_to_img=talk_to_img, tm_tokens = tm_tokens, charac = charac, english = english)

def continuous_processing(tm_tokens, charac):
    english = "Processing..."
    status = ''
    user_said = speech_reader(charac)
    if 'hey' in user_said:
        final = gpt_processor(user_said)
        split_text = final.split("English:")

        if len(split_text) > 1:
            romaji = split_text[0].strip()
            english = split_text[1].strip()
        else:
            romaji = final.strip()
            english = "Unable to Translate."

        talker = Talk(os.environ.get('FAKEYOU-USERNAME'), os.environ.get('FAKEYOU-PASS'), 'Buzz Lightyear (New)') ##username and password for fakeyou here
        status = talker.generate_audio(text=str(romaji), tm_tokens=tm_tokens)
        if status == 'complete':
            return english
        else:
            english = f"{charac} is unable to speak, please reload the page."
            return english

    elif 'stop' in user_said:
        print("I'm here")
        english = "Conversation ended"
        return english
    else:
        english = "Unable to detect... please speak and start with 'hey'."
        return english
    

@app.route("/call/<tm_tokens>/<charac>", methods=['GET', 'POST'])
def call(tm_tokens, charac):
    if request.method == 'POST':
        english = continuous_processing(tm_tokens, charac)
        return english 
    return template_rendering(tm_tokens, charac, english = '')

if __name__ == "__main__":
    app.run(debug=True, port=5000)