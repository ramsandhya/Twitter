from flask import Flask, redirect, session, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import pg

db = pg.DB(dbname = 'twitter')

app = Flask('TwitterApp')

@app.route('/')
def login():
    session.clear()
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def signin_submit():
    if request.method == 'GET':
        return render_template('login.html', title = "Login")
    else:
        username = request.form['username']
        password = request.form['password']
        query = db.query("select id, name, password from twitter_user where name = '%s'" % username)
        result = query.namedresult()
        session['name'] = ''
        print result
        if len(result) > 0:
            check_password = check_password_hash(result[0].password, password)
            print password
            print check_password
            if check_password:
                session['name'] = username
                return redirect('/timeline')
            else:
                return render_template('login.html', title='Login', error='The username or password does not match. Please try again.')
            # return redirect ('/user/%s' % session['name'])
        else:
            return render_template('login.html', title='Login', error='The username or password does not match. Please try again.')
app.secret_key = 'NTOEU0948375980CTH9EO893'

@app.route('/timeline', methods=['GET'])
def listings():
    query = db.query('''
    select
    	twitter_user.id,
        tweet.message,
        twitter_user.name
    from
        tweet
    left outer join
    	twitter_user on tweet.user_id = twitter_user.id
    where
        tweet.user_id = 9 or
        tweet.user_id in
            (select
                followee_id
            from
                follow
            where
                follower_id = 9)
    ''')

    tweets = query.namedresult()
    # print tweets

    return render_template('timeline.html', title='My timeline', tweets=tweets)

@app.route('/user/<username>', methods=['GET','POST'])
def my_profile(username):
    # name = request.form['name']
    print 'Hello'
    query = db.query('''
    select
        twitter_user.name,
        tweet.message
    from
        tweet
    left outer join
        twitter_user on tweet.user_id = twitter_user.id
    where
        twitter_user.name = $1
    ''', username)
    tweets = query.namedresult()
    print tweets
    return render_template('profile.html', title='My profile', tweets=tweets)

@app.route('/addTweet', methods=['POST'])
def add_tweet():
    new_post = request.form['tweet_name']
    db.insert('tweet', message=new_post, user_id=9)
    return redirect('/timeline')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', title = "Register")
    else:
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        # insert user into the database
        db.insert('twitter_user', name=username, password=hashed_password)

        return redirect('/login')

app.debug = True

if __name__ == "__main__":
    app.run(debug=True)

# app.secret_key = 'NTOEU0948375980CTH9EO893'
#
# @app.route('/timeline', methods=['GET'])
# def listings():
#     query = db.query('''
#     select
#     	twitter_user.id,
#         tweet.message,
#         twitter_user.name
#     from
#         tweet
#     left outer join
#     	twitter_user on tweet.user_id = twitter_user.id
#     where
#         tweet.user_id = 9 or
#         tweet.user_id in
#             (select
#                 followee_id
#             from
#                 follow
#             where
#                 follower_id = 9)
#     ''')
#
#     tweets = query.namedresult()
#     # print tweets
#
#     return render_template('timeline.html', title='My timeline', tweets=tweets)
# re
    # print tweets

# Trial for the list of all users in the timeline page

# select
#         tweet.message,
#         tweet.user_id
#     from
#         tweet,
#         follow
# toby--        follow on tweet.user_id = follow.followee_id
#     where
#     	tweet.user_id = 9 -- or
# toby--    	(tweet.user_id = follow.followee_id and
# toby--    	follow.follower_id = 9)


# Profile page query for usernme 'Sandhya'

# select
# 		twitter_user.name,
#       	tweet.message
# # --    tweet.user_id
#     from
#         tweet
#    	left outer join
#         twitter_user on tweet.user_id = twitter_user.id
#     where
#         twitter_user.name = 'Sandhya';

# select
#     *
# from
#     tweet
# where
#     tweet.user_id = $1 or
#     tweet.user_id in
#         (select
#             followee_id
#         from
#             follow
#         where
#             follower_id = $1
#         )
#
# # Query for the id, names, messages
#     my messages
#     others messages who I am following
#
#
# select
# 	twitter_user.id,
#     tweet.message,
#     twitter_user.name
# from
#     tweet
# left outer join
# 	twitter_user on tweet.user_id = twitter_user.id
# where
#     tweet.user_id = 9 or
#     tweet.user_id in
#         (select
#             followee_id
#         from
#             follow
#         where
#             follower_id = 9
#         )
