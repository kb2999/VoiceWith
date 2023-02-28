# coding: EUC-KR

from logHandler import log
import appModuleHandler
import api
import queueHandler
import speech
import re

class AppModule(appModuleHandler.AppModule):

	__gestures = {"kb:l": "reportPosition",}

	def script_reportPosition(self, gesture):
		obj = api.getForegroundObject()
		if len(obj.children) <= 1:
			self.say(u"��ü ȭ�鿡���� ��� ��ġ ������ ��� �� �� �����ϴ�. ��Ʈ+���͸� ���� �� �ٽ� �õ��� �ּ���.")
			return

		for inx in range(len(obj.children)):
			s = obj.children[inx].name
			if not isinstance(s, basestring):
				continue

			ptn1 = re.compile(r'(\d+):(\d+):(\d+)\s*/\s*(\d+):(\d+):(\d+)')
			ptn2 = re.compile(r'(\d+):(\d+)\s*/\s*(\d+):(\d+)')

			m = ptn1.search(s)
			if m is not None:
				msg = u'���� ��ġ %s�ð� %s�� %s�� ��ü �ð� %s�ð� %s�� %s��' % tuple([int(n) for n in m.groups()])
				if inx + 1 < len(obj.children) and isinstance(obj.children[inx+1].name, basestring):
					msg += obj.children[inx+1].name
				self.say(msg)
				return

			m = ptn2.search(s)
			if m is not None:
				msg = u'���� ��ġ %s�� %s�� ��ü �ð� %s�� %s��' % tuple([int(n) for n in m.groups()])
				if inx + 1 < len(obj.children) and isinstance(obj.children[inx+1].name, basestring):
					msg += obj.children[inx+1].name
				self.say(msg)
				return


	def say(self, text):
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, text)
