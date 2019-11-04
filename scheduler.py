import argparse
import functools
import os
import socketio
import threading

from qmgr import QueueManager


parser = argparse.ArgumentParser(description='Karafun fair scheduler.')
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
										help='enable logging')
parser.add_argument('--hide-singers', action='store_true',
										help='hide who queued each song')
parser.add_argument('channel',
										help='karafun session id')
args = parser.parse_args()


sio = socketio.Client(logger=args.verbose)
mtx = threading.Lock()
qm = QueueManager(args.hide_singers)

def mlock(f):
	@functools.wraps(f)
	def inner(*args, **kwargs):
		with mtx:
			return f(*args, **kwargs)
	return inner

@sio.event
@mlock
def connect():
	if args.verbose:
		print('connection established')
	sio.emit('authenticate', {
		'login': 'fair scheduler',
		'channel': args.channel,
		'role': 'participant',
		'app': 'karafun',
		'socket_id': None,
	})

@sio.event
@mlock
def loginAlreadyTaken():
	if args.verbose:
		print('loginAlreadyTaken')
	sio.emit('authenticate', {
		'login': 'fair scheduler %d' % os.getpid(),
		'channel': args.channel,
		'role': 'participant',
		'app': 'karafun',
		'socket_id': None,
	})

@sio.event
@mlock
def permissions(data):
	if args.verbose:
		print('permissions received ', data)

@sio.event
@mlock
def preferences(data):
	if args.verbose:
		print('preferences received ', data)
	if not data['askSingerName']:
		print('You must turn on "Ask singer\'s name when adding to queue" in the Karafun remote control settings in order for the scheduler to work.')
		sio.disconnect()

@sio.event
@mlock
def status(data):
	if args.verbose:
		print('status received ', data)

queue_handle_timer = threading.Timer(999.0, lambda: None)

@sio.event
@mlock
def queue(data):
	if args.verbose:
		print('queue received ', data)
	@mlock
	def handle():
		action = qm.reconcile(data)
		if action:
			print('sending ', action)
			sio.emit(action[0], action[1])
	global queue_handle_timer
	queue_handle_timer.cancel()
	queue_handle_timer = threading.Timer(0.3, handle)
	queue_handle_timer.start()

@sio.event
@mlock
def serverUnreacheable():
	print('Server unreachable. Try restarting the Karafun App?')
	sio.disconnect()

@sio.event
@mlock
def disconnect():
	print('Disconnected from server.')

sio.connect('https://www.karafun.com/?remote=kf%s' % args.channel)
sio.wait()
