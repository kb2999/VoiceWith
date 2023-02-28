# coding: EUC-KR
####################################################################
#
# ������ ��� ���� �÷�����
#
####################################################################

import appModuleHandler
from NVDAObjects.window.edit import *
import api

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.name in (u"����", u"���"):
			clsList.insert(0, TextBox)

class TextBox(Edit):
	def _caretScriptPostMovedHelper(self, speakUnit, gesture, info=None):
		if self.name == u"���":
			return
		super(TextBox, self)._caretScriptPostMovedHelper(speakUnit, gesture, info)
