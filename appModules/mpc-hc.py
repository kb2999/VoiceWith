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
			self.say(u"전체 화면에서는 재생 위치 정보를 얻어 올 수 없습니다. 알트+엔터를 누른 후 다시 시도해 주세요.")
			return

		for inx in range(len(obj.children)):
			s = obj.children[inx].name
			if not isinstance(s, basestring):
				continue

			ptn1 = re.compile(r'(\d+):(\d+):(\d+)\s*/\s*(\d+):(\d+):(\d+)')
			ptn2 = re.compile(r'(\d+):(\d+)\s*/\s*(\d+):(\d+)')

			m = ptn1.search(s)
			if m is not None:
				msg = u'현재 위치 %s시간 %s분 %s초 전체 시간 %s시간 %s분 %s초' % tuple([int(n) for n in m.groups()])
				if inx + 1 < len(obj.children) and isinstance(obj.children[inx+1].name, basestring):
					msg += obj.children[inx+1].name
				self.say(msg)
				return

			m = ptn2.search(s)
			if m is not None:
				msg = u'현재 위치 %s분 %s초 전체 시간 %s분 %s초' % tuple([int(n) for n in m.groups()])
				if inx + 1 < len(obj.children) and isinstance(obj.children[inx+1].name, basestring):
					msg += obj.children[inx+1].name
				self.say(msg)
				return


	def say(self, text):
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, text)
