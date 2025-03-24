import sqlite3, db

def add_review(user_id, movie_title, movie_rating, movie_review):
    sql = """INSERT INTO reviews (user_id, movie, rating, review) 
            VALUES (?, ?, ?, ?)"""
    db.execute(sql, [user_id, movie_title, movie_rating, movie_review])

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

def update_review(review_id, movie_title, movie_rating, movie_review):
    sql = """UPDATE reviews SET movie = ?,
                                rating = ?,
                                review = ?
            WHERE id = ?
            ;"""
    
    db.execute(sql, [movie_title, movie_rating, movie_review, review_id])