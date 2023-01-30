from app import app
from flask import render_template, request, redirect, url_for
from .forms import UserCreationForm, p_name, LoginForm, PostForm, EditProfileForm
from .models import User, Post, Pokemon
import requests as r
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
def homePage():
    
    return render_template("index.html")

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
        pokemon = Pokemon.query.filter(Pokemon.name==input).first()
        if pokemon:
            return render_template("search.html", form = form, pokemon = pokemon)

        url = f'https://pokeapi.co/api/v2/pokemon/{input}'
        response = r.get(url)
        # print(response)
        if response.ok:
            my_dict = response.json()
            # print(my_dict)
            pokemon_dict = {}
            
            name = my_dict["name"]
            ability = my_dict["abilities"][0]["ability"]["name"]
            base_xp = my_dict["base_experience"]
            front_shiny = my_dict["sprites"]["front_shiny"]
            base_atk = my_dict["stats"][1]["base_stat"]
            base_hp = my_dict["stats"][0]["base_stat"]
            base_def = my_dict["stats"][2]["base_stat"]
            print(pokemon_dict)

            print(pokemon_dict)
            pokemon = Pokemon(name, ability, base_xp, front_shiny, base_atk, base_hp, base_def)
            pokemon.saveToDB()
            return render_template("search.html", form = form, pokemon = pokemon)
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

@app.route("/profile", methods=["GET", "POST"])
def profile():
    form = EditProfileForm()
    user = User.query.filter_by(id = current_user.id).first()
    return render_template("profile.html", form = form, current_user = current_user)

@app.route("/editprofile", methods=["GET", "POST"])
@login_required
def editProfileForm():
    form = EditProfileForm()
    user = User.query.filter_by(id = current_user.id).first()
    print("Hi")
    if request.method == "POST":
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if username != "":
            user.username = username
        if email != "":
            user.email = email
        if password != "":
            user.password = password
        user.saveChanges()
        return render_template('editdelete.html', form = form, current_user = current_user )
    return render_template('editdelete.html', form = form, current_user = current_user )


@app.route("/profile/editdelete", methods=["GET", "POST"])
@login_required
def delProfile():
    user = User.query.filter_by(id = current_user.id).first()
    if request.method == "POST":
        if user:
            user.deleteFromDB()
            return redirect(url_for("loginPage"))
    return render_template("editdelete.html") 