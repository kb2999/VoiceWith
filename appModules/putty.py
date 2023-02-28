from nvdaBuiltin.appModules.putty import *
from scriptHandler import script
import tones
import re
from keyboardHandler import KeyboardInputGesture
import ui
import inputCore
import api
import textInfos


class AppModule(AppModule):
	TERMINAL_WINDOW_CLASS = "iPuTTY"
	_numList = []


	@script(gestures=["kb(desktop):nvda+numpadDivide", "kb(laptop):nvda+["], description='Putty 텔넷 프로그램을 쓸 때 게시물에 진입합니다.', category=inputCore.SCRCAT_MISC)
	def script_enterLeftNumberReturn(self, gesture):
		sNumber = self.getLeftNumber()
		if not sNumber:
			return
		api.copyToClip(sNumber)
		if self.sendKey("shift+insert") and self.sendKey("enter"):
			self._numList = []
			tones.beep(1000, 100)


	@script(gestures=["kb(desktop):nvda+numpadMultiply", "kb(laptop):nvda+]"], description='Putty 텔넷 프로그램을 쓸 때 저장된 번호를 입력합니다.', category=inputCore.SCRCAT_MISC)
	def script_enterNumListReturn(self, gesture):
		if not self._numList: return
		s = ' '.join(self._numList)
		api.copyToClip(s)
		if self.sendKey("shift+insert") and self.sendKey("enter"):
			self._numList = []
			tones.beep(1000, 100)


	@script(gestures=["kb(desktop):control+numpadDivide", "kb(laptop):control+nvda+["], description='Putty 텔넷 프로그램을 쓸 때 게시물 번호를 기억합니다.', category=inputCore.SCRCAT_MISC)
	def script_addLeftNumber(self, gesture):
		sNumber = self.getLeftNumber()
		if not sNumber:
			return
		self._numList.append(sNumber)
		ui.message(sNumber +" "  + u"추가")


	@script(gestures=["kb(desktop):control+numpadMultiply", "kb(laptop):control+nvda+]"], description='Putty 텔넷 프로그램을 쓸 때 저장된 게시물 번호를 일괄 삭제합니다.', category=inputCore.SCRCAT_MISC)
	def script_clearNumList(self, gesture):
		self._numList = []
		ui.message(u"기억 된 숫자 모두 삭제")


	def sendKey(self, keyName):
		try:
			ges = KeyboardInputGesture.fromName(keyName)
			ges.send()
			return True
		except:
			return False

	def getLeftNumber(self):
		info = api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		#s = info.getTextWithFields()[1]
		s = info.text
		m = re.match(r'\s*(\d+)\.?\s+', s)
		if m is None:
			return False
		return m.group(1)

