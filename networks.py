import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    

     bonuscoin=math.Object(
        P2P_PREFIX='FBB0D742'.decode('hex'), 
        P2P_PORT=65000, 
        ADDRESS_VERSION=0x19,
        RPC_PORT=65001, 
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue( 
            'bonusaddress' in (yield bitcoind.rpc_help()) and 
            not (yield bitcoind.rpc_getinfo())['testnet'] 
        )), 
        SUBSIDY_FUNC=lambda nBits, height: __import__('bonuscoin_subsidy').GetBlockValue(nBits, height),
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=120, 
        SYMBOL='BNS', 
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Bonus') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Bonus/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bonus'), 'bonus.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.bonuscoin.net/block/', 
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.bonuscoin.net/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.bonuscoin.net/tx/',
        SANE_TARGET_RANGE=(2**256//2**32 - 1, 2**256//2**32 - 1), 
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    )

   
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
