import db

def get_user(user_id):
    sql = """SELECT id, username
            FROM users
            WHERE id = ?
            ;"""
    
    res = db.query(sql, [user_id])

    return res[0] if res else None

def get_users_reviews(user_id):
    sql = """SELECT R.movie, R.id
            FROM users U, reviews R
            WHERE U.id = R.user_id
            AND U.id = ?
            ;"""
    
    res = db.query(sql, [user_id])
    print(res)

    return res if res else None

def fetch_users():
    sql = """SELECT username, id
            FROM users
            ORDER BY username DESC"""
    
    res = db.query(sql)

    return res if res else None