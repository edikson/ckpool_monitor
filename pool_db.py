import sqlite3

def check_db():
    db = sqlite3.connect('pool_db.db')
    db.execute('CREATE TABLE IF NOT EXISTS "mining_stats" ( `block_count` INTEGER, `derp` TEXT, `last_check` TEXT, `over_time` TEXT, `postponed` TEXT, `user` TEXT )')
    db.execute('CREATE TABLE IF NOT EXISTS `user_stats` ( `user` TEXT, `pb_key` TEXT, `btc_addy` TEXT )')
    db.close()

def check_user(username):
    users = get_user_list()
    if username in users:
        return True
    else:
        return False

def create_user(username, pb_key, btc_addy):
    conn = sqlite3.connect('pool_db.db')
    c = conn.cursor()
    c.execute('INSERT INTO user_stats (user, pb_key, btc_addy) VALUES ("%s", "%s", "%s")' % (username, pb_key, btc_addy, ))
    conn.commit()
    conn.close()

def update_user(username, pb_key, btc_addy):
    conn = sqlite3.connect('pool_db.db')
    c = conn.cursor()
    c.execute('UPDATE user_stats SET pb_key = "%s", btc_addy = "%s" WHERE user = "%s"' % (pb_key, btc_addy, username, ))
    conn.commit()
    conn.close()

def get_user_list():
    conn = sqlite3.connect('pool_db.db')
    c = conn.cursor()
    c.execute('SELECT user FROM user_stats')
    user_list = c.fetchall()
    conn.close()
    new_list = []
    for each in user_list:
        new_list.append(each[0])
    return new_list

def push_stats(user, block_count, derp, last_check, over_time, postponed):
    conn = sqlite3.connect('pool_db.db')
    c = conn.cursor()
    c.execute('UPDATE mining_stats SET block_count = %s, derp = "%s", last_check = "%s", over_time = "%s", postponed = "%s" WHERE user = "%s"' % (block_count, derp, last_check, over_time, postponed, user,))
    conn.commit()
    conn.close()

def get_user(user):
    conn = sqlite3.connect('pool_db.db')
    c = conn.cursor()
    c.execute('SELECT pb_key, btc_addy FROM user_stats WHERE user = "%s"' % (user))
    user_stats = c.fetchall()
    conn.close()
    pb_key, btc_addy = user_stats[0]
    return pb_key, btc_addy

def pull_stats(user):
    conn = sqlite3.connect('pool_db.db')
    c = conn.cursor()
    c.execute('SELECT block_count, derp, last_check, over_time, postponed FROM mining_stats WHERE user = "%s"' % (user))
    user_stats = c.fetchall()
    conn.close()
    block_count, derp, last_check, over_time, postponed = user_stats[0]
    return block_count, derp, last_check, over_time, postponed

