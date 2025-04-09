from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


# Function to load posts from a JSON file
def load_posts():
    try:
        with open('posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist


# Function to save posts to a JSON file
def save_posts(posts):
    with open('posts.json', 'w') as file:
        json.dump(posts, file)


# Route to view all blog posts
@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


# Route to add a new blog post
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_post = {
            'id': len(load_posts()) + 1,  # Simple ID generation based on current length
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'likes': 0  # Initialize likes to 0
        }
        posts = load_posts()
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')


# Route to delete a blog post
@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    post_to_delete = next((p for p in posts if p['id'] == post_id), None)

    if post_to_delete:
        posts.remove(post_to_delete)
        save_posts(posts)

    return redirect(url_for('index'))


# Route to update a blog post
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('update.html', post=post)


# Route to increment the "likes" for a post
@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    post['likes'] += 1  # Increment the likes count
    save_posts(posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
