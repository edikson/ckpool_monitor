import sqlite3

def push_stats(user, block_count, derp, last_check, over_time, postponed):
    conn = sqlite3.connect('pool_db.db')
    c = conn.cursor()
    c.execute('UPDATE mining_stats SET block_count = %s, derp = "%s", last_check = "%s", 
              over_time = "%s", postponed = "%s" WHERE user = "%s"' % (block_count, derp, last_check, over_time, postponed, user,))
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
