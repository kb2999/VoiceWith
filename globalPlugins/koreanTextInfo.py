# coding: UTF-8

import re
import globalPluginHandler
import ui
import textInfos
import controlTypes
from textInfos.offsets import *
import NVDAObjects
from NVDAObjects.window.edit import Edit, EditTextInfo
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.UIA import UIA
from . import _utils



class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# 단순 편집창
		if obj.role == controlTypes.ROLE_EDITABLETEXT and obj.windowClassName == "Edit" and not isinstance(obj, NVDAObjects.inputComposition.InputComposition):
			clsList.insert(0, KoreanEdit)
		
		# IAccessible 고정 텍스트 
		elif obj.role == controlTypes.ROLE_STATICTEXT and isinstance(obj, IAccessible):
			clsList.insert(0, KoreanStaticTextIAccessible)
		# 목록 아이템
		elif  obj.role == controlTypes.ROLE_LISTITEM:
			clsList.insert(0, KoreanStaticTextIAccessible if isinstance(obj, IAccessible) else KoreanStaticTextUIA)


class KoreanEditTextInfo(EditTextInfo):
	def _getWordOffsets(self, offset):
		paraStart, paraEnd = self._getParagraphOffsets(offset)
		paraText = self._getTextRange(paraStart, paraEnd)
		start = findStartOfWord(paraText, offset - paraStart) + paraStart
		end = findEndOfWord(paraText, offset - paraStart) + paraStart
		return start, end


class KoreanEdit(Edit):
	TextInfo = KoreanEditTextInfo
	vwConfig = _utils.loadVWConfig()


	def script_caret_moveByWord(self, gesture):
		if self.vwConfig.get('moveByWord', False):
			info = self.makeTextInfo(position=textInfos.POSITION_CARET)
			direction = 1 if gesture.mainKeyName == 'rightArrow' else -1
			info.move(unit=textInfos.UNIT_WORD, direction=direction)
			info._setCaretOffset(info._startOffset)
			info.expand(unit=textInfos.UNIT_WORD)
			ui.message(info.text)
		else:
			gesture.send()
			info = self.makeTextInfo(position=textInfos.POSITION_CARET)
			lineStart, lineEnd = info._getLineOffsets(info._startOffset)
			text = info._getTextRange(info._startOffset, lineEnd)
			m = re.match(r'([^\s\r\n\t]+)', text)
			word = m.group(1) if m is not None else text
			ui.message(word)



class KoreanNVDAObjectTextInfo(NVDAObjects.NVDAObjectTextInfo):
	def _getWordOffsets(self, offset):
		paraStart, paraEnd = self._getParagraphOffsets(offset)
		paraText = self._getTextRange(paraStart, paraEnd)
		start = findStartOfWord(paraText, offset - paraStart) + paraStart
		end = findEndOfWord(paraText, offset - paraStart) + paraStart
		return start, end


class KoreanStaticTextIAccessible(IAccessible):
	TextInfo = KoreanNVDAObjectTextInfo


class KoreanStaticTextUIA(UIA):
	TextInfo = KoreanNVDAObjectTextInfo

