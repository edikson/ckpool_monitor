import requests, pool_db, json, datetime
from HTMLParser import HTMLParser

blockurl = 'http://ckpool.org/blocks/'
links = []

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    if'.confirmed' in value:
                        links.append(value)

def get_block_addys(links = links):
    response = requests.get(blockurl)
    response.raise_for_status()
    raw_page = response.text
    parser = MyHTMLParser()
    parser.feed(raw_page)
    return links

def create_link(link, blockurl = blockurl):
    block_URL = blockurl + link
    return block_URL

def get_block_stats(block_URL):
    response = requests.get(block_URL)
    response.raise_for_status()
    json_bits = response.text
    block = json.loads(json_bits)
    return block

def get_block_info(block):
    block_number = block["height"]
    reward = block["reward"]
    solved_by = block["solvedby"]
    block_stamp = block["date"]
    block_stamp = block_stamp[1:-5]
    solve_hash = block["hash"]
    block_shares = block["shares"]
    diff = block["diff"]
    return (block_number, reward, solved_by, block_stamp, diff, block_shares, solve_hash)

def get_block_numbers(links):
    block_numbers = []
    for each in links:
        block_numbers.append(each[:-10])
    return block_numbers

def blocks_to_get():
    links = get_block_addys()
    blocks = get_block_numbers(links)
    db_blocks = pool_db.pull_block_list()
    final_list = [set(blocks) - set(db_blocks)]
    return final_list

def push_blocks():
    final_list = blocks_to_get()
    final_list = list(final_list[0])
    print len(final_list)
    for each in final_list:
        confirm = each + '.confirmed'
        blockURL = create_link(confirm)
        block = get_block_stats(blockURL)
        pool_db.push_block_stats(get_block_info(block))

def get_payout(username, height):
    user_info = pool_db.get_user(username)
    block = blockurl + height + '.confirmed'
    block_stats = get_block_stats(block)
    payouts = block_stats['payouts']
    if user_info[1] in payouts:
        return payouts[user_info[1]]
    else:
        return False

def get_postponed(username, height):
    user_info = pool_db.get_user(username)
    block = blockurl + height + '.confirmed'
    block_stats = get_block_stats(block)
    postponed = block_stats['postponed']
    if user_info[1] in postponed:
        return postponed[user_info[1]]
    else:
        return False

