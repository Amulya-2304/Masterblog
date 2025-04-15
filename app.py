from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def load_posts():
    """Load blog posts from JSON file."""
    try:
        with open('posts.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    """Save blog posts to JSON file."""
    with open('posts.json', 'w', encoding='utf-8') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()
        new_post = {
            'id': len(posts) + 1,
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'likes': 0
        }
        posts.append(new_post)
        save_posts(posts)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()
    post_to_delete = next((p for p in posts if p['id'] == post_id), None)

    if post_to_delete:
        posts.remove(post_to_delete)
        save_posts(posts)

    return redirect(url_for('index'))


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


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)

    if post is None:
        return "Post not found", 404

    post['likes'] += 1
    save_posts(posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
