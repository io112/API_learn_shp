books = [{
    'name': 'book1',
    'pagenum': 17,
    'price': 256.6
}, {
    'name': 'book2',
    'pagenum': 47,
    'price': 450
}, {
    'name': 'book3',
    'pagenum': 376,
    'price': 753.5
}]

from flask import Flask, jsonify, abort

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello():
    return '<h1>Hello world</h1>'


@app.route('/api/v1/books', methods=['GET'])
def get_all_books():
    return jsonify(books)


@app.route('/api/v1/books/<int:book_id>', methods=["GET"])
def get_book_by_id(book_id):
    return jsonify(books[book_id])


if __name__ == '__main__':
    app.run(debug=True)
