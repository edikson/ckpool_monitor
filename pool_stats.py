import pool_db, requests, json, re, datetime

url = 'http://ckpool.org/pool/pool.status'

def get_pool_data(url = url):
    response = requests.get(url)
    response.raise_for_status()
    pool_stuff = response.text
    split_list = [pos for pos, char in enumerate(pool_stuff) if char == '{']
    first_part = pool_stuff[split_list[0]:split_list[1]]
    second_part = pool_stuff[split_list[1]:split_list[2]]
    third_part = pool_stuff[split_list[2]:split_list[3]]
    last_part = pool_stuff[split_list[3]:]
    first_part = json.loads(first_part)
    second_part = json.loads(second_part)
    third_part = json.loads(third_part)
    last_part = json.loads(last_part)
    return first_part, second_part, third_part, last_part

def get_pool_stats(first_part, second_part, third_part, last_part):
    users = first_part['Users']
    workers = first_part['Workers']
    idle = first_part['Idle']
    disconnected = first_part['Disconnected']
    sps1m = third_part['SPS1m']
    sps5m = third_part['SPS5m']
    sps15m = third_part['SPS15m']
    sps1h = third_part['SPS1h']
    hr5m = second_part['hashrate5m']
    hr15m = second_part['hashrate15m']
    hr1h = second_part['hashrate1hr']
    hr6h = second_part['hashrate6hr']
    hr1d = second_part['hashrate1d']
    hr7d = second_part['hashrate7d']
    diff = last_part['diff']
    reward = last_part['reward']
    herp = last_part['herp']
    lns = last_part['lns']
    accepted = last_part['accepted']
    rejected = last_part['rejected']
    last_check = datetime.datetime.now()
    return (users, workers, idle, disconnected, sps1m, sps5m, sps15m, sps1h, hr5m, hr15m, hr1h, hr6h, hr1d, hr7d, diff, reward, herp, lns, accepted, rejected, last_check)

first_part, second_part, third_part, last_part = get_pool_data()
stats = get_pool_stats(first_part, second_part, third_part, last_part)
print stats
