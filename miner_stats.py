import pool_db, requests, json, re, datetime
user_info = pool_db.get_user('rick')
url = 'http://ckpool.org/users/' + user_info[1]

def get_miner_data():
    response = requests.get(url)
    response.raise_for_status()
    miner_data = json.loads(response.text)
    return miner_data

def get_miner_stats(miner_data):
    hr1m = miner_data['hashrate1m']
    hr5m = miner_data['hashrate5m']
    hr1hr = miner_data['hashrate1hr']
    hr1d = miner_data['hashrate1d']
    hr7d = miner_data['hashrate7d']
    lastshare = miner_data['lastshare']
    workers = miner_data['workers']
    shares = miner_data['shares']
    bestshare = miner_data['bestshare']
    lns = miner_data['lns']
    luck = miner_data['luck']
    accumulated = miner_data['accumulated']
    postponed = miner_data['postponed']
    herp = miner_data['herp']
    derp = miner_data['derp']
    last_check = datetime.datetime.now()
    return (hr1m, hr5m, hr1hr, hr1d, hr7d, lastshare, workers, shares, bestshare, lns, luck, accumulated, postponed, herp, derp, last_check)

#miner_data = get_miner_data()
#stats = get_miner_stats(miner_data)
#print stats
