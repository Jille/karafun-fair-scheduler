import unittest

from qmgr import QueueManager

class QueueManagerTest(unittest.TestCase):

	def applyQueueMutation(self, queue, cmd):
		self.assertEqual(cmd[0], 'queueMove')
		moveFrom = cmd[1]['from']
		moveTo = cmd[1]['to']
		self.assertLess(moveFrom, len(queue))
		self.assertTrue(moveTo < len(queue) or moveTo == 99999)
		s = queue[moveFrom]
		self.assertEqual(cmd[1]['queueId'], s['queueId'])
		queue[moveTo:moveTo] = [queue[moveFrom]]
		if moveTo < moveFrom:
			del queue[moveFrom+1]
		else:
			del queue[moveFrom]
		return self.reindexQueue(queue)
	
	def reindexQueue(self, queue):
		for i, s in enumerate(queue):
			s['id'] = i
		return queue

	def test_a(self):
		qm = QueueManager(False)
		queue = [
			{u'status': u'playing', u'queueId': u'D6E07CCEA252D728F08CA93EDD81C3BE', u'singer': u'Jille', u'artist': u'moonlight-kissed', u'title': u'moonlight-kissed', u'songId': 0, u'id': 0},
			{u'status': u'ready', u'queueId': u'982FDEB56480D79BA5081E2ADB534628', u'singer': u'Milka', u'artist': u'Avenged Sevenfold', u'title': u'Afterlife', u'songId': 29745, u'id': 1},
			{u'status': u'ready', u'queueId': u'3C69C3CF359C6B047813435166B67AE2', u'singer': u'Milka', u'artist': u'Avenged Sevenfold', u'title': u'Beast and the Harlot', u'songId': 53004, u'id': 2},
			{u'status': u'ready', u'queueId': u'AF805022EFB9356B802EE3A6977375C5', u'singer': u'Kevin', u'artist': u'code-in-go', u'title': u'code-in-go', u'songId': 0, u'id': 3},
			{u'status': u'ready', u'queueId': u'E66C02C7B8967B3F599E27682262CF2C', u'singer': u'Jille', u'artist': u'code-in-go', u'title': u'code-in-go', u'songId': 0, u'id': 4},
		]
		action = qm.reconcile(queue)
		print action
		queue = self.applyQueueMutation(queue, action)
		print queue
		self.assertEqual(queue, [
			{u'status': u'playing', u'queueId': u'D6E07CCEA252D728F08CA93EDD81C3BE', u'singer': u'Jille', u'artist': u'moonlight-kissed', u'title': u'moonlight-kissed', u'songId': 0, u'id': 0},
			{u'status': u'ready', u'queueId': u'982FDEB56480D79BA5081E2ADB534628', u'singer': u'Milka', u'artist': u'Avenged Sevenfold', u'title': u'Afterlife', u'songId': 29745, u'id': 1},
			{u'status': u'ready', u'queueId': u'AF805022EFB9356B802EE3A6977375C5', u'singer': u'Kevin', u'artist': u'code-in-go', u'title': u'code-in-go', u'songId': 0, u'id': 2},
			{u'status': u'ready', u'queueId': u'3C69C3CF359C6B047813435166B67AE2', u'singer': u'Milka', u'artist': u'Avenged Sevenfold', u'title': u'Beast and the Harlot', u'songId': 53004, u'id': 3},
			{u'status': u'ready', u'queueId': u'E66C02C7B8967B3F599E27682262CF2C', u'singer': u'Jille', u'artist': u'code-in-go', u'title': u'code-in-go', u'songId': 0, u'id': 4},
		])
		action = qm.reconcile(queue)
		print action
		queue = self.applyQueueMutation(queue, action)
		print queue
		self.assertEqual(queue, [
			{u'status': u'playing', u'queueId': u'D6E07CCEA252D728F08CA93EDD81C3BE', u'singer': u'Jille', u'artist': u'moonlight-kissed', u'title': u'moonlight-kissed', u'songId': 0, u'id': 0},
			{u'status': u'ready', u'queueId': u'982FDEB56480D79BA5081E2ADB534628', u'singer': u'Milka', u'artist': u'Avenged Sevenfold', u'title': u'Afterlife', u'songId': 29745, u'id': 1},
			{u'status': u'ready', u'queueId': u'AF805022EFB9356B802EE3A6977375C5', u'singer': u'Kevin', u'artist': u'code-in-go', u'title': u'code-in-go', u'songId': 0, u'id': 2},
			{u'status': u'ready', u'queueId': u'E66C02C7B8967B3F599E27682262CF2C', u'singer': u'Jille', u'artist': u'code-in-go', u'title': u'code-in-go', u'songId': 0, u'id': 3},
			{u'status': u'ready', u'queueId': u'3C69C3CF359C6B047813435166B67AE2', u'singer': u'Milka', u'artist': u'Avenged Sevenfold', u'title': u'Beast and the Harlot', u'songId': 53004, u'id': 4},
		])
		queue.pop(0)  # Song finished playing
		queue = self.reindexQueue(queue)
		action = qm.reconcile(queue)
		self.assertEqual(action, None)

if __name__ == '__main__':
	unittest.main()
