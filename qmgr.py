import collections

class QueueManager(object):

	def __init__(self, hideSingers):
		self.singerRotation = []
		self.song2singer = {}
		self.hideSingers = hideSingers
	
	def getSinger(self, s):
		if s['songId'] == 0:
			return s['singer']
		if s['songId'] not in self.song2singer:
			self.song2singer[s['songId']] = s['singer']
		return self.song2singer[s['songId']]
	
	def getParsedSinger(self, s):
		singer = self.getSinger(s)
		if singer.endswith('!'):
			return singer[:-1], True
		return singer, False
	
	def reconcile(self, queue):
		if not queue:
			self.singerRotation = []
			self.song2singer = {}
			return

		# Clean up old entries in self.song2singer.
		unseen = set(self.song2singer.keys()) - {s['songId'] for s in queue}
		for qid in unseen:
			del self.song2singer[qid]

		singerQueues = collections.defaultdict(list)
		for s in queue[1:]:
			singer, bang = self.getParsedSinger(s)
			if singer not in self.singerRotation:
				self.singerRotation.append(singer)
			if bang and singerQueues[singer]:
				singerQueues[singer][-1].append(s)
			else:
				singerQueues[singer].append([s])

		if self.singerRotation and self.getParsedSinger(queue[0])[0] == self.singerRotation[0]:
			self.singerRotation = self.singerRotation[1:] + self.singerRotation[:1]

		# If you don't have anything queued, you lose your place in the scheduler.
		self.singerRotation = filter(lambda singer: singer in singerQueues, self.singerRotation)

		if self.hideSingers:
			# Deduplicate songs, keeping the first.
			seen = set()
			for s in queue[1:]:
				if s['songId'] > 0 and s['songId'] in seen:
					return ('queueRemove', s['queueId'])
				seen.add(s['songId'])

		idx = 1
		while idx < len(queue):
			if singerQueues['_next']:
				r = ['_next']
			elif singerQueues['']:
				r = ['']
			else:
				r = self.singerRotation
			for singer in r:
				if not singerQueues[singer]:
					continue
				for s in singerQueues[singer].pop(0):
					if s['id'] != idx:
						return ('queueMove', {'queueId': s['queueId'], 'from': s['id'], 'to': idx})
					idx += 1

		if self.hideSingers:
			for s in queue[1:]:
				if s['songId'] > 0 and s['singer'] != '':
					return ('queueAdd', {'songId': int(s['songId']), 'pos': s['id'], 'singer': ''})

		return None
