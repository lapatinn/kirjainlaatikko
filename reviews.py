import sqlite3, db

def add_review(user_id, movie_title, movie_rating, movie_review, genre, director, year):
    sql = """INSERT INTO reviews (user_id, movie, rating, review) 
            VALUES (?, ?, ?, ?)"""
    
    db.execute(sql, [user_id, movie_title, movie_rating, movie_review])

    rev_id = db.last_insert_id()

    sql1 = """INSERT INTO movie_info (review_id, genre, director, year)
            VALUES (?, ?, ?, ?)"""

    db.execute(sql1, [rev_id, genre, director, year])

def fetch_reviews():
    sql = """SELECT id, user_id, movie, rating, review
            FROM reviews
            ORDER BY id DESC
            ;"""
    
    return db.query(sql)

def get_review(item_id):
    sql = """SELECT R.id, R.movie, R.rating, R.review, R.user_id, U.username
    FROM reviews R, users U
    WHERE R.user_id = U.id
    AND R.id = ?
    ;"""

    return db.query(sql, [item_id])[0]

def update_review(review_id, movie_title, movie_rating, movie_review, genre, director, year):
    sql = """UPDATE reviews SET movie = ?,
                                rating = ?,
                                review = ?
            WHERE id = ?
            ;"""
    
    db.execute(sql, [movie_title, movie_rating, movie_review, review_id])

    sql1 = """UPDATE movie_info SET genre = ?,
                                    director = ?,
                                    year = ?
            WHERE review_id = ?
            ;"""
    
    db.execute(sql1, [genre, director, year, review_id])

def remove_review(item_id):
    sql = "DELETE FROM reviews WHERE id = ?"

    db.execute(sql, [item_id])

def find_reviews(query):
    sql = """SELECT id, movie FROM reviews
            WHERE movie LIKE ?
            ORDER BY id DESC
            ;"""
    
    return db.query(sql, ["%" + query + "%"])

def get_info(item_id):
    sql = """SELECT genre, director, year
            FROM movie_info
            WHERE review_id = ?
            ORDER BY id DESC
            ;"""
    
    return db.query(sql, [item_id])

def add_comment(user_id, review_id, comment):
    sql = """INSERT INTO comments (user_id, review_id, content)
            VALUES (?, ?, ?)
            ;"""
    

    db.execute(sql, [user_id, review_id, comment])

def fetch_comments(review_id):
    sql = """SELECT C.id, C.content, C.user_id, U.username
            FROM comments C, reviews R, users U
            WHERE R.id = ? 
            AND C.review_id = R.id
            AND U.id = C.user_id
            ORDER BY C.id
            ;"""

    res = db.query(sql, [review_id])

    return res

def get_comment(comment_id):
    sql = """SELECT C.content, C.id, C.user_id, C.review_id
            FROM comments C, users U
            WHERE C.id = ?
            AND C.user_id = U.id"""

    return db.query(sql, [comment_id])[0]

def remove_comment(comment_id):
    sql = """DELETE FROM comments
            WHERE id = ?
            ;"""

    db.execute(sql, [comment_id])