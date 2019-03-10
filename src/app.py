# update post keeps having error on 'done'
import json
from flask import Flask
from flask import request

app = Flask(__name__)
post_id_conunter = 3
posts = {
    0: {
        'id':0,
        'score': 0,
        'text': 'My First Post!',
        'username': 'Young'
    },
    1:{
        'id':1,
        'score': 0,
        'text': 'My Second Post!',
        'username': 'Young'
    },
    2:{
        'id':1,
        'score': 0,
        'text': 'My Third Post!',
        'username': 'Young'
    }
}
@app.route('/')
def root():
    return 'Hello world!'

@app.route('/api/posts/')
def get_posts():
    res = {'success':True, 'data':list(posts.values())}
    return json.dumps(res), 200
#create post
#key not found due to not sending data use ""
@app.route('/api/posts/', methods = ['POST'])
def create_post():
    global post_id_conunter
    post_body = json.loads(request.data)
    text = post_body['text']
    username = post_body['username']
    post = {
         'id': post_id_conunter,
         'score': 0,
         'text': text,
         'username': username
    }
    posts[post_id_conunter] = post
    post_id_conunter += 1
    return json.dumps({'success':True,'data':post}),201
# check specific post
@app.route('/api/post/<int:post_id>/')
def get_post(post_id):
    if post_id in posts:
        post = posts[post_id]
        return json.dumps({'success':True,'data':post}),200
    return json.dumps({'success':False,'error':'Post not found!'}),404
# edit a post
# get the posts before test
@app.route('/api/post/<int:post_id>/', methods = ['POST'])
def update_post(post_id):
    if post_id in posts:
        post = posts[post_id]
        post_body = json.loads(request.data)
        post['text'] = post_body['text']
        return json.dumps({'success':True,'data':post}),200
    return json.dumps({'success':False,'error':'Post not found!'}),404
#delete post
@app.route('/api/post/<int:post_id>/', methods = ['DELETE'])
def delete_post(post_id):
    if post_id in posts:
        post = posts[post_id]
        del posts[post_id]
        return json.dumps({'success':True,'data':post}),200
    return json.dumps({'success':False,'error':'Post not found!'}),404
# update the dict by assigning new dict
comments = {
    0: [
            {'id':0,   
            'score':0,
            'text': 'My First Word!',
            'username': 'Young'
            },
            {'id':1,   
            'score':0,
            'text': 'My First Comment!',
            'username': 'Young'
        }
        ],
    1: [
            {'id':0,  
            'score':0, 
            'text': 'My First Comment!',
            'username': 'Young'
            }
        ]
    }
# get comments    
@app.route('/api/post/<int:post_id>/comments/')
def get_comments(post_id):
    if post_id in comments:
        res = {'success':True, 'data':comments[post_id]}
        return json.dumps(res), 200
    return json.dumps({'success':False,'error':'Comments not found!'}),404
#post comments
@app.route('/api/post/<int:post_id>/comment/', methods = ['POST'])
def create_comment(post_id):
    comment_body = json.loads(request.data)
    text = comment_body['text']
    username = comment_body['username']
    #No comment
    # if else 
    if post_id not in comments:
        if post_id in posts:
            comment= {
             'id':0,
             'score':0,
             'text': text,
             'username': username
             }
            comments.update({post_id:[comment]})
            return json.dumps({'success':True,'data':comment}),201
        return json.dumps({'success':False,'error':'Comment not found!'}),404
    #Has comment
    else:
        comment_id = len(comments[post_id])
        comment= {
             'id':comment_id,
             'score':0,
             'text': text,
             'username': username
             }
        comments[post_id].append(comment)
        return json.dumps({'success':True,'data':comment}),201
    return json.dumps({'success':False,'error':'Comment not found!'}),404
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)