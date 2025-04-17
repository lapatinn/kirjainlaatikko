import db

def create_user(username, password_hash):
    sql = """INSERT INTO users (username, password_hash) 
                VALUES (?, ?)
                ;"""
    
    db.execute(sql, [username, password_hash])

def get_hash(username): # lol
    sql = """SELECT id, password_hash 
                FROM users 
                WHERE username = ?
                ;"""
    res = db.query(sql, [username])

    return res[0] if res else "VIRHE: Kysely ei tuottanut tulosta. Annettua käyttäjänimeä ei ole tietokannassa."
    
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

    return res if res else None

def fetch_users():
    sql = """SELECT username, id
            FROM users
            ORDER BY username DESC"""
    
    res = db.query(sql)

    return res if res else None