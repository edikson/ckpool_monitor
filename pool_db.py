import sqlite3

pool = 'pool.db'

def create_db(pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('CREATE TABLE IF NOT EXISTS "user_info" ("username" TEXT, "pb_key" TEXT, "btc_addy" TEXT)')
    db.execute("CREATE TABLE IF NOT EXISTS 'pool_stats' ('users' INTEGER, 'workers' INTEGER, 'idle' INTEGER, 'disconnected' INTEGER, 'sps1m' REAL, 'sps5m' REAL, 'sps15m' REAL, 'sps1h' REAL, 'hr5m' TEXT, 'hr15m' TEXT, 'hr1h' TEXT, 'hr6h' TEXT, 'hr1d' TEXT, 'hr7d' TEXT, 'diff' REAL, 'reward' REAL, 'herp' REAL, 'lns' REAL, 'accepted' INTEGER, 'rejected' INTEGER,'last_check' TEXT, UNIQUE(pool))")
    db.execute("CREATE TABLE IF NOT EXISTS 'miner_stats' ('username' TEXT, 'hr1m' TEXT, 'hr5m' TEXT, 'hr1hr' TEXT, 'hr1d' TEXT, 'hr7d' TEXT, 'lastshare' INTEGER, 'workers' INTEGER, 'shares' INTEGER, 'bestshare' INTEGER, 'lns' REAL, 'luck' REAL, 'accumulated' REAL, 'postponed' INTEGER, 'herp' REAL, 'derp' REAL, 'last_check' TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS 'block_stats' ('pool' TEXT, 'height' INTEGER, 'reward' REAL, 'solvedby' TEXT, 'date' TEXT, 'diff' REAL, 'shares' INTEGER, 'hash' TEXT)")
    conn.commit()
    conn.close()

def create_user(keys, pool = pool):
    user = (keys[0],)
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute("select exists(select 1 from pool_stats where pool='ck_pool')")
    exists = db.fetchall()
    db.execute("INSERT INTO user_info (username, pb_key, btc_addy) VALUES (?,?,?)", keys)
    db.execute("INSERT INTO miner_stats (username) VALUES (?)", user)
    if  exists[0][0] == 0:
        db.execute("INSERT INTO pool_stats (pool) VALUES ('ck_pool')")
    conn.commit()
    conn.close()

def get_user_list(pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('SELECT username FROM user_info')
    users = db.fetchall()
    conn.close()
    user_list = []
    for each in users:
        user_list.append(each[0])
    return user_list

def check_user(username):
    users = get_user_list()
    if username in users:
        return True
    else:
        return False

def get_user(username, pool = pool):
    user = (username,)
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('SELECT pb_key, btc_addy FROM user_info Where username = ?', user)
    users = db.fetchall()
    conn.close()
    return users[0]

def update_user(user_info_keys_first, pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('UPDATE user_info SET pb_key = ?, btc_addy = ? WHERE username = ?', user_info_keys_first)
    conn.commit()
    conn.close()

def push_pool_stats(pool_numbers, pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('UPDATE pool_stats SET users = ?, workers = ?, idle = ?, disconnected = ?, sps1m = ?, sps5m = ?, sps15m = ?, sps1h = ?, hr5m = ?, hr15m = ?, hr1h = ?, hr6h = ?, hr1d = ?, hr7d = ?, diff = ?, reward = ?, herp = ?, lns = ?, accepted = ?, rejected = ?, last_check = ? WHERE pool = "ck_pool"', pool_numbers)
    conn.commit()
    conn.close()

def push_block_stats(block_info, pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('INSERT INTO block_stats (height, reward, solvedby, date, diff, shares, hash) VALUES (?, ?, ?, ?, ?, ?, ?)', block_info)
    conn.commit()
    conn.close()

def push_miner_stats(miner_numbers,username, pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('UPDATE miner_stats SET hr1m = ?, hr5m = ?, hr1hr = ?, hr1d = ?, hr7d = ?, lastshare = ?, workers = ?, shares = ?, bestshare = ?, lns = ?, luck = ?, accumulated = ?, postponed = ?, herp = ?, derp = ?, last_check = ? WHERE username = "%s"', miner_numbers % (username))
    conn.commit()
    conn.close()

def pull_pool_stats(pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute("SELECT users, workers, idle, disconnected, sps1m, sps5m, sps15m, sps1h, hr5m, hr15m, hr1h, hr6h, hr1d, hr7d, diff, reward, herp, lns, accepted, rejected FROM pool_stats, last_check = ? WHERE pool = 'ck_pool'")
    pool_stats = db.fetchall()
    conn.close()
    return pool_stats[0]

def pull_block(height, pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute("SELECT reward, solvedby, date, diff, shares, hash FROM block_stats WHERE height = '%s'" % (height))
    block = db.fetchall()
    conn.close()
    return block[0]

def pull_block_list(pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('SELECT height FROM block_stats')
    blocks = db.fetchall()
    conn.close()
    block_list = []
    for each in blocks:
        block_list.append(each[0])
    return block_list

def pull_block_diffs(pool = pool):
    conn = sqlite3.connect(pool)
    db = conn.cursor()
    db.execute('SELECT diff FROM block_stats')
    diffs = db.fetchall()
    conn.close()
    return diffs[0]

