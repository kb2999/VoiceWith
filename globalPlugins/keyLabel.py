import api
from scriptHandler import *
import globalPluginHandler
import ui
from . import _utils

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.messages = {'c': '복사', 'v': '붙여 넣기', 'x': '잘라내기', 'z': '되돌리기', 'a': '전체 선택'}
		self.vwConfig = _utils.loadVWConfig()


	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if self.vwConfig.get('keyLabel', True): 
				focus = api.getFocusObject()
				if focus.treeInterceptor and not focus.treeInterceptor.passThrough:
					self.removeGestureBinding("kb:control+c")
					self.removeGestureBinding("kb:control+a")
				else:
					self.bindGesture('kb:control+c'	, 'reportKeyLabel')
					self.bindGesture('kb:control+a'	, 'reportKeyLabel')
		except:
			pass


	@script(gestures=['kb:control+x', 'kb:control+v', 'kb:control+z', 'kb:control+a', 'kb:control+c'])
	def script_reportKeyLabel(self, gesture):
		if self.vwConfig.get('keyLabel', True):
			mainKey = gesture.mainKeyName
			msg = self.messages[mainKey]
			ui.message(msg)
		gesture.send()


