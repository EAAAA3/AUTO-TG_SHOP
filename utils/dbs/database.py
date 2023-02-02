import sqlite3


name_1 = 'users.db'
name_2 = 'stats.db'
name_3 = 'promo.db'
item_1 = 'neflix.db'
item_2 = 'vk-instagram.db'


def create_db_users():
    conn = sqlite3.connect(name_1, check_same_thread=False) #check_same можно и не указывать
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        user_id INT UNIQUE,
        balance INT,
        total_purchases INT);''') # если че вставлять NULL
    conn.commit()
    conn.close()

def create_db_stats(): # мб поиграюсь с таблицей (пока что она пустая)
    conn = sqlite3.connect(name_2, check_same_thread=False)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS stats (
        total_users INT,
        total_products INT,
        total_sales INT);''')
    conn.commit()
    conn.close()

def create_db_promo():
    conn = sqlite3.connect(name_3, check_same_thread=False)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS promo (
        name_promo TEXT UNIQUE,
        price INT,
        amount INT);''')
    conn.commit()
    conn.close()

def create_db_netflix():
    conn = sqlite3.connect(item_1, check_same_thread=False)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS netflix (
        name TEXT,
        price INT,
        login TEXT,
        passwd TEXT);''')
    conn.commit()
    conn.close()

def create_db_vk_inst():
    conn = sqlite3.connect(item_2, check_same_thread=False)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS vk_instagram (
        name TEXT,
        price INT,
        login TEXT,
        passwd TEXT);''')
    conn.commit()
    conn.close()


class Database():

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()

    def add_user(self, data):
        self.cur.execute('INSERT INTO users VALUES (NULL,?,?,?);', (data))
        self.conn.commit()

    def get_all_users_for_stats(self):
        all_users = self.cur.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1").fetchone()
        return all_users[0]

    def upload_promo(self, data):
        self.cur.execute('INSERT INTO promo VALUES (?,?,?)', (data,))
        self.conn.commit()

    def upload_netflix(self, data):
        self.cur.execute('INSERT INTO netflix VALUES (?,?,?,?)', (data))
        self.conn.commit()
        
    def upload_vk_inst(self, data):
        self.cur.execute('INSERT INTO vk_instagram VALUES (?,?,?,?)', (data))
        self.conn.commit()

    def get_netflix_items(self):
        amount = len(self.cur.execute('SELECT * FROM netflix').fetchall())
        result = self.cur.execute('SELECT name, price FROM netflix').fetchone()
        name, price = result[0], result[1]
        return name, price, amount

    def get_vk_instagram_items(self):
        amount_vk = len(self.cur.execute('SELECT * FROM vk_instagram WHERE name = "Авторег VK"').fetchall())
        amount_inst = len(self.cur.execute('SELECT * FROM vk_instagram WHERE name = "Instagram Авторег"').fetchall())
        result_vk = self.cur.execute('SELECT name, price FROM vk_instagram WHERE name = "Авторег VK"').fetchone()
        result_inst = self.cur.execute('SELECT name, price FROM vk_instagram WHERE name = "Instagram Авторег"').fetchone()
        name_vk, price_vk = result_vk[0], result_vk[1]
        name_inst, price_inst = result_inst[0], result_inst[1]
        return name_vk, price_vk, amount_vk, name_inst, price_inst, amount_inst

    def get_vk_login_pass(self):
        login_pass = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Авторег VK"').fetchone()
        login_pass_2 = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Авторег VK" LIMIT 2').fetchall()
        login_pass_3 = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Авторег VK" LIMIT 3').fetchall()
        login_pass_4 = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Авторег VK" LIMIT 4').fetchall()
        login_pass_5 = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Авторег VK" LIMIT 5').fetchall()
        return login_pass, login_pass_2, login_pass_3, login_pass_4, login_pass_5

    def get_inst_login_pass(self):
        login_pass = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Instagram Авторег"').fetchone()
        login_pass_2 = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Instagram Авторег" LIMIT 2').fetchall()
        login_pass_3 = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Instagram Авторег" LIMIT 3').fetchall()
        login_pass_4 = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Instagram Авторег" LIMIT 4').fetchall()
        login_pass_5 = self.cur.execute('SELECT login, passwd FROM vk_instagram WHERE name = "Instagram Авторег" LIMIT 5').fetchall()
        return login_pass, login_pass_2, login_pass_3, login_pass_4, login_pass_5

    def get_id_n_balance(self, id):
        result = self.cur.execute('SELECT id, balance FROM users WHERE user_id = ?', (id,)).fetchone()
        id_, balance_ = result[0], result[1]
        return id_, balance_

    def get_purchases(self, id):
        result = self.cur.execute('SELECT total_purchases FROM users WHERE user_id = ?', (id,)).fetchone()
        purcahses = result[0]
        return purcahses

    def read(self):
        l = []
        self.cur.execute('SELECT * FROM users')
        records = self.cur.fetchall()
        for row in records:
            l.append(row[1])
        return l

    def close(self):
        self.conn.close()
