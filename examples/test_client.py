import codecs
import sys
import pyraknet
import gevent
from gevent import Greenlet
import struct
import timeit
from codecs import encode

CLIENT_PORT = 3000
SERVER_PORT = 4000

TYPE_CLIENT = 0
TYPE_SERVER = 1

ID_GAME_PACKET = pyraknet.ID_USER_PACKET_ENUM + 1

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def create_instance(host='127.0.0.1', port=4000):
    peer: pyraknet.RakPeerInterface = pyraknet.RakPeerInterface.GetInstance()
    
    socket_descriptor = pyraknet.SocketDescriptor(port, host)
    
    success = peer.Startup(1, socket_descriptor, 1)
    assert success == pyraknet.RAKNET_STARTED

    return peer

def send_data(peer: pyraknet.RakPeerInterface, address, ms_delay):
    # while True:
    for _ in range(20):
        gevent.sleep(0.030)
        packet = b''
        packet += struct.pack('<B', ID_GAME_PACKET)
        data = 'Hello! It\'s test message.'.encode('ascii').ljust(50, b'\x00')
        packet += struct.pack('<H', 50)
        packet += data
        peer.Send(packet, pyraknet.HIGH_PRIORITY, pyraknet.RELIABLE_ORDERED, 0, address, False)
        # print('send ret type is ', type(send_ret))

def listen_packet(peer: pyraknet.RakPeerInterface, peer_type):
    print('listening packets')
    if peer_type == TYPE_CLIENT:
        tag = bcolors.FAIL + '[CLIENT]'
    elif peer_type == TYPE_SERVER:
        tag = bcolors.OKBLUE + '[SERVER]'

    packet: pyraknet.Packet
    while True:
        packet = pyraknet.Receive(peer)
        if not packet:
            peer.DeallocatePacket(packet)
            gevent.sleep(0.030)
            continue
        id = pyraknet.get_packet_indentifier(packet)
        data = pyraknet.get_packet_payload(packet)

        print(tag, 'Got packet with id', id, 'of len', packet.length)
        
        # if id == ID_GAME_PACKET:
        #     print(tag, encode(data, 'hex'))
            # send_data(peer, pyraknet.AddressOrGUID(packet), 2000)

        peer.DeallocatePacket(packet)


client: pyraknet.RakPeerInterface = create_instance(port=CLIENT_PORT)
# server: pyraknet.RakPeerInterface = create_instance(port=SERVER_PORT)

client.SetMaximumIncomingConnections(1)
# server.SetMaximumIncomingConnections(10)

client_packet_thread = Greenlet.spawn(listen_packet, client, TYPE_CLIENT)
# server_packet_thread = Greenlet.spawn(listen_packet, server, TYPE_SERVER)

# print(server.GetSystemAddressFromGuid(server.GetMyGUID()).ToString())

# listen_packet(server, TYPE_SERVER)

success = client.Connect('127.0.0.1', SERVER_PORT, '', 0)

print(success, pyraknet.CONNECTION_ATTEMPT_STARTED)

addrguid = pyraknet.AddressOrGUID()

addrguid.systemAddress = pyraknet.SystemAddress('127.0.0.1', SERVER_PORT)

# send_data_thread = Greenlet.spawn(send_data, client, addrguid, 1500)
send_data(client, addrguid, 0)

threads = [client_packet_thread]

gevent.joinall(threads)

pyraknet.RakPeerInterface.DestroyInstance(client)
# pyraknet.RakPeerInterface.DestroyInstance(server)