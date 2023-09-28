# Common Workflow

    # views.py

    from components.BookDetails import Book

    @app.route("/books", methods=["GET"])
    def getBooks():
        """ Returns a json with all the books in the database """
        # Query
        all_books = Book.query.all()

        result = Book.products_schema.dump(all_books)

        # Returns all the DB items as json
        return jsonify(result)
