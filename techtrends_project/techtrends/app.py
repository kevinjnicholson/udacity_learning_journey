import sqlite3
import logging
import sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Configure Handlers For STDOUT
stdout_handler = logging.StreamHandler(stream=sys.stdout)
file_handler = logging.FileHandler(filename='techtrends.log')
handlers = [file_handler, stdout_handler]

# Configure Logging
logging.basicConfig(handlers=handlers,
                    level=logging.DEBUG,
                    format='%(levelname)-8s | %(name)8s | %(asctime)s -  %(message)s',
                    datefmt='%d/%m/%Y | %H:%M:%S'
                   )

# Function to get a database connection.
# This function connects to database with the name `database.db`
# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global DBcount
    DBcount =+ 1
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('404 page not found')
      return render_template('404.html'), 404
    else:
      app.logger.info('Existing article "{}" retrieved'.format(post['title']))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Us page retrieved')
    return render_template('about.html')

# Define the /healthz end point
@app.route('/healthz')
def healthz():
    response = app.response_class(
        response=json.dumps({'result':'OK - healthy'}),
        status=200,
        mimetype='application/json'
    )
    return response

# Define the /metrics end point
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    DBpostcount = len(posts)
    connection.close()
    response = app.response_class(
           response=json.dumps({'db_connection_count': DBcount, 'post_count': DBpostcount}),
        status=200,
        mimetype='application/json'
    )
    return response

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        app.logger.info('%s article has been created', title)
        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
