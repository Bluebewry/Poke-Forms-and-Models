from app import app
from flask import render_template, request, redirect, url_for
from .forms import UserCreationForm, p_name, LoginForm, PostForm
from .models import User, Post
import requests as r
from flask_login import login_user, logout_user, current_user, login_required


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
   
@app.route("/login", methods=["GET", "POST"])
def loginPage():
    login = LoginForm()

    if request.method == "POST":
        if login.validate():
            username = login.username.data
            password = login.password.data

            user = User.query.filter_by(username = username).first()
            if user:
                if user.password == password:
                    login_user(user)

                else:

                    print(("wrong password"))

            else:
                print("user does not exist")



    return render_template("login.html", login = login) 

@app.route("/logout", methods=["GET"])
@login_required
def logoutRoute():
    logout_user()

    return redirect(url_for('loginPage'))
    
@app.route("/post/create", methods=["GET", "POST"])
def createPost():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)
            post.saveToDB()

    return render_template('createpost.html', form = form)

@app.route("/posts", methods=["GET"])
def getPosts():
    posts = Post.query.all()

    return render_template('feed.html', posts = posts)
    
@app.route("/posts/<int:post_id>", methods=["GET"])
def getPost(post_id):
    post = Post.query.get(post_id)

    return render_template('singlepost.html', post = post)

@app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def updatePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.author.id:
        return redirect(url_for('getPosts'))
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data
            post.title = title
            post.img_url = img_url
            post.caption = caption
            post.saveChanges()
            return redirect(url_for('getPost', post_id = post.id))
    return render_template('updatepost.html', post = post, form = form)

@app.route("/posts/<int:post_id>/delete", methods=["GET"])
@login_required
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.author.id:
        return redirect(url_for('getPosts'))

    post.deleteFromDB()
    
    return redirect(url_for('getPosts'))