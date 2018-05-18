import hashlib
import json
import sys
import random


def hash_me(msg=""):

    # For convenience, this is a helper function that wraps our hashing alogirthm
    if type(msg) != "str":
        msg = json.dumps(msg, sort_keys=True)  # If we don't sort keys, we can't guarantee repeatablity!

    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(), 'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()


def make_transaction(max_value=3):
    
    # This will create valid transactions in the range of (1, max_value)
    sign = int(random.getrandbits(1)) * 2 -1  # This will randomly choose -1 or 1

    amount = random.randint(1, max_value)
    alice_pays = sign * amount
    bobs_pays = -1 * alice_pays

    # By construction, this will always return transactions that respect the conversations of tokens.
    # However, note that we have not done anything to check whether these overdraft an account

    return {
        u'Alice': alice_pays,
        u'Bob':  bobs_pays
    }

txt_buffer = [make_transaction() for i in range(30)]


def update_state(txn, state):
    """
    :params txn: <dict> keyed with account names, holding numeric values for transfer amount
    :params state: <dict> keyed with account names, holding numeric values for account balance
    :return: <dict> Updated state, with additional users added to state if necessary
    This doesn't validate the transaction - just updates the states!
    """

    # If transaction is valid, then update the state
    state = state.copy()  # As dictionaries are mutable, let's avoid any confusion by creating a working copy of the data

    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]

    return state


def is_valid_txn(txn, state):
    """
    :params txn: <dict> keyed with account names, holding numeric values for transfer amount
    :params state: <dict> keyed with account names, holding numeric values for account balance
    :return: <bool> True if transaction doesn not cause an overdraft, if not False
    """

    # Check that the sum of the deposits and withdrawals is 0
    if sum(txn.values()) is not 0:
        return False

    # Check that the transaction does not cause an overdraft
    for key in txn.keys():
        if key in state.keys():
            account_balance = state[key]
        else:
            account_balance = 0
        
        if (account_balance + txn[key]) < 0:
            return False

    return True


state = {
    u'Alice': 50,
    u'Bob': 50
}  # Define the initial state

genesis_block_txns = [state]
genesis_block_contents = {
    u'blockNumber': 0,
    u'parentHash': None,
    u'txnCount': 1,
    u'txns': genesis_block_txns
}

genesis_hash = hash_me(genesis_block_contents)
genesis_block = {
    u'hash': genesis_hash,
    u'contents': genesis_block_contents
}

genesis_block_str = json.dumps(genesis_block, sort_keys=True)

chain = [genesis_block]





