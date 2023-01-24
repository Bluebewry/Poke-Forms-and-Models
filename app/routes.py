from app import app
from flask import render_template, request, redirect, url_for
from .forms import UserCreationForm, p_name
from .models import User
import requests as r


@app.route("/")
def homePage():
    welcome = "Welcome"
    return render_template("index.html", welcome = welcome)

@app.route("/signup", methods=["GET", "POST"])
def signUpPage():
    form = UserCreationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username, email, password)
            print(user)

            user.saveToDB()

            return redirect(url_for('loginPage'))

    return render_template("signup.html", form = form)

@app.route("/login")
def loginPage():
    return render_template("login.html")

@app.route("/search", methods=["GET", "POST"])
def searchPage():
    form = p_name()
    print(request.method)
    if request.method == 'POST':
        input = form.search_input.data
        print(input)
            # return redirect(url_for('homePage'))
            # dont need to redirect

    # import requests as r
    # def findpokemon(pokemon):
        url = f'https://pokeapi.co/api/v2/pokemon/{input}'
        response = r.get(url)
        # print(response)
        if response.ok:
            my_dict = response.json()
            # print(my_dict)
            pokemon_dict = {}
            pokemon_dict["Name"] = my_dict["name"]
            pokemon_dict["Ability"] = my_dict["abilities"][0]["ability"]["name"]
            pokemon_dict["Base XP"] = my_dict["base_experience"]
            pokemon_dict["Front Shiny"] = my_dict["sprites"]["front_shiny"]
            pokemon_dict["Base ATK"] = my_dict["stats"][1]["base_stat"]
            pokemon_dict["Base HP"] = my_dict["stats"][0]["base_stat"]
            pokemon_dict["Base DEF"] = my_dict["stats"][2]["base_stat"]
            print(pokemon_dict)
            return render_template("search.html", form = form, pokemon_dict = pokemon_dict)
        else:
            return "The pokemon you're looking for does not exist."


    return render_template("search.html", form = form)
   
  

    
    

