from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ← enable CORS on all routes

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///insights.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/ping')
def ping():
    return 'pong'

from flask import jsonify

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([
        {
            'id': p.id,
            'category': p.category,
            'subject': p.subject,
            'time': p.time,
            'author': p.author,
            'content': p.content
        } for p in posts
    ])

from flask import request

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    # ensure all required fields are present
    required = ['category', 'subject', 'time', 'author', 'content']
    if not data or any(field not in data for field in required):
        return jsonify({'error': 'Missing one or more fields'}), 400

    # build and save the new Post
    post = Post(
        category=data['category'],
        subject=data['subject'],
        time=data['time'],
        author=data['author'],
        content=data['content']
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({
        'id': post.id,
        'category': post.category,
        'subject': post.subject,
        'time': post.time,
        'author': post.author,
        'content': post.content
    }), 201

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'category': post.category,
        'subject': post.subject,
        'time': post.time,
        'author': post.author,
        'content': post.content
    })

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return '', 204

@app.route('/api/portfolios/<int:pid>', methods=['GET'])
def get_portfolio(pid):
    p = Portfolio.query.get_or_404(pid)
    return jsonify({
        'id':      p.id,
        'subject': p.subject,
        'time':    p.time,
        'author':  p.author,
        'content' : p.content
    })


@app.route('/api/portfolios', methods=['GET'])
def get_portfolios():
    items = Portfolio.query.all()
    return jsonify([{
        'id':      p.id,
        'subject': p.subject,
        'time':    p.time,
        'author':  p.author,
        'content': p.content
    } for p in items])

@app.route('/api/portfolios', methods=['POST'])
def create_portfolio():
    data = request.get_json() or {}
    # now require 'content' as well
    if any(f not in data for f in ('subject','time','author','content')):
        return jsonify({'error':'Missing fields'}), 400
    # include content when creating the Portfolio
    p = Portfolio(
        subject=data['subject'],
        time=   data['time'],
        author= data['author'],
        content=data['content']
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({
        'id':      p.id,
        'subject': p.subject,
        'time':    p.time,
        'author':  p.author,
        'content': p.content
    }), 201

@app.route('/api/portfolios/<int:pid>', methods=['DELETE'])
def delete_portfolio(pid):
    p = Portfolio.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return '', 204

# ─── Serve Portfolio Admin ───
@app.route('/secured/portfolios/<path:filename>')
def serve_portfolios_admin(filename):
    return send_from_directory('OurPortfolios/secured', filename)

@app.route('/secured/<path:filename>')
def serve_secured(filename):
    return send_from_directory('OurInsights/secured', filename)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

class Portfolio(db.Model):
    id      = db.Column(db.Integer,  primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    time    = db.Column(db.String(50),  nullable=False)
    author  = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text,        nullable=False)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=False)
