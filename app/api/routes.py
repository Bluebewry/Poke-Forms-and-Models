from flask import Blueprint, request
from ..models import Post,User
from ..apiauthhelper import basic_auth_required, token_auth_required, basic_auth, token_auth
from flask_cors import cross_origin


api = Blueprint('api', __name__ )

@api.route('/api/posts')
def getPosts():
    posts = Post.query.all()

    new_posts = []
    for p in posts:
        new_posts.append(p.to_dict())

    return {
        'status': 'ok',
        'totalResults': len(posts),
        'posts': [p.to_dict() for p in posts]
    }

@api.route('/api/posts/<int:post_id>')
def getPost(post_id):
    post = Post.query.get(post_id)

    if post: 
         return {
        'status': 'ok',
        'totalResults': 1,
        'posts': post.to_dict()
    }
    else:
        return {
            'status': 'not ok',
            'message': 'The post you are looking for does not exist.'
        }

@api.route('/api/posts/create', methods = ["POST"])
@basic_auth_required
def createPost(user):
    data = request.json

    title = data['title']
    caption = data['caption']
    img_url = data['img_url']



    post = Post(title, img_url, caption, user.id)
    post.saveToDB()
    return{
        'status': 'ok',
        'message': 'Succesfully created post!'
    }



@api.route("/api/signup", methods=["POST"])
def signUpPage():
    data = request.json

    username = data['username']
    email = data['email']
    password = data['password']

    user = User(username, email, password)
    print(user)

    user.saveToDB()

    return {
        'status': 'ok',
        'message': 'Successfully created an account'
    }


@api.route("/api/login", methods=["POST"])
@basic_auth.login_required
def getToken():
    user = basic_auth.current_user()
    return {
        'status': 'ok',
        'user': user.to_dict()
    }