# coding: EUC-KR
####################################################################
#
# 독서기 재생 관련 플러그인
#
####################################################################

import appModuleHandler
from NVDAObjects.window.edit import *
import api

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.name in (u"정지", u"재생"):
			clsList.insert(0, TextBox)

class TextBox(Edit):
	def _caretScriptPostMovedHelper(self, speakUnit, gesture, info=None):
		if self.name == u"재생":
			return
		super(TextBox, self)._caretScriptPostMovedHelper(speakUnit, gesture, info)
