from logHandler import log
from speech import sayAll
import inputCore
import review
import globalPluginHandler
import controlTypes
import config
import globalCommands
import winKernel
import api
import speech
import textInfos
import eventHandler
from NVDAObjects.inputComposition import InputComposition
from scriptHandler import script, getLastScriptRepeatCount
from os.path import join, dirname
import ui
import speech
from . import _utils


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.vwConfig = _utils.loadVWConfig()

		try:
			inputCore.manager.userGestureMap.load(join(dirname(__file__), 'extraGestures1.ini'))
		except:
			log.info('extraGestures1.ini 파일을 읽어 오지 못했습니다.')

		nCompetitable = self.vwConfig.get('competitableMode', 0)
		if nCompetitable == 0:
			globalCommands.commands = KoreanCommands()
		elif nCompetitable == 1:
			globalCommands.commands = KoreanCommandsWithSenseReaderKeys()
			try:
				inputCore.manager.userGestureMap.load(join(dirname(__file__), 'extraGestures2.ini'))
			except:
				log.info('extraGestures2.ini 파일을 읽어 오지 못했습니다.')


class KoreanCommands(globalCommands.commands.__class__):

	def checkInputComposition(self):
		obj = api.getNavigatorObject()
		if isinstance(obj, InputComposition):
			api.setNavigatorObject(obj.parent, isFocus=False)

	def focusSilently(self, obj):
		oldSpeechMode=speech.getState().speechMode
		speech.setSpeechMode(speech.SpeechMode.off)
		eventHandler.executeEvent("gainFocus", obj)
		speech.setSpeechMode(oldSpeechMode)

	@script(
		description=_(
			# Translators: Input help mode message for report current line command.
			"Reports the current line under the application cursor. "
			"Pressing this key twice will spell the current line. "
			"Pressing three times will spell the line using character descriptions."
		),
		category=globalCommands.SCRCAT_SYSTEMCARET,
		gestures=("kb(desktop):NVDA+upArrow", "kb(laptop):NVDA+l")
	)
	def script_reportCurrentLine(self,gesture):
		focus = api.getFocusObject()
		if isinstance(focus, InputComposition):
			self.focusSilently(focus.parent)
			super(KoreanCommands, self).script_reportCurrentLine(gesture)
			self.focusSilently(focus)
		else:
			super(KoreanCommands, self).script_reportCurrentLine(gesture)

	@script(
		# Translators: Input help mode message for move review cursor to top line command.
		description=_("Moves the review cursor to the top line of the current navigator object and speaks it"),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:shift+numpad7", "kb(laptop):NVDA+control+home")
	)
	def script_review_top(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_top(gesture)

	@script(
		# Translators: Input help mode message for move review cursor to previous line command.
		description=_("Moves the review cursor to the previous line of the current navigator object and speaks it"),
		resumeSayAllMode=sayAll.CURSOR.REVIEW,
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad7", "kb(laptop):NVDA+upArrow", "ts(text):flickUp")
	)
	def script_review_previousLine(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_previousLine(gesture)

	@script(
		description=_(
			# Translators: Input help mode message for read current line under review cursor command.
			"Reports the line of the current navigator object where the review cursor is situated. "
			"If this key is pressed twice, the current line will be spelled. "
			"Pressing three times will spell the line using character descriptions."
		),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad8", "kb(laptop):NVDA+shift+.")
	)
	def script_review_currentLine(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_currentLine(gesture)

	@script(
		# Translators: Input help mode message for move review cursor to next line command.
		description=_("Moves the review cursor to the next line of the current navigator object and speaks it"),
		resumeSayAllMode=sayAll.CURSOR.REVIEW,
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad9", "kb(laptop):NVDA+downArrow", "ts(text):flickDown")
	)
	def script_review_nextLine(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_nextLine(gesture)

	@script(
		# Translators: Input help mode message for move review cursor to bottom line command.
		description=_("Moves the review cursor to the bottom line of the current navigator object and speaks it"),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:shift+numpad9", "kb(laptop):NVDA+control+end")
	)
	def script_review_bottom(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_bottom(gesture)

	@script(
		# Translators: Input help mode message for move review cursor to previous word command.
		description=_("Moves the review cursor to the previous word of the current navigator object and speaks it"),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad4", "kb(laptop):NVDA+control+leftArrow", "ts(text):2finger_flickLeft")
	)
	def script_review_previousWord(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_previousWord(gesture)

	@script(
		description=_(
			# Translators: Input help mode message for report current word under review cursor command.
			"Speaks the word of the current navigator object where the review cursor is situated. "
			"Pressing twice spells the word. "
			"Pressing three times spells the word using character descriptions"
		),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad5", "kb(laptop):NVDA+control+.", "ts(text):hoverUp")
	)
	def script_review_currentWord(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_currentWord(gesture)

	@script(
		# Translators: Input help mode message for move review cursor to next word command.
		description=_("Moves the review cursor to the next word of the current navigator object and speaks it"),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad6", "kb(laptop):NVDA+control+rightArrow", "ts(text):2finger_flickRight")
	)
	def script_review_nextWord(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_nextWord(gesture)

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to start of current line command.
			"Moves the review cursor to the first character of the line "
			"where it is situated in the current navigator object and speaks it"
		),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:shift+numpad1", "kb(laptop):NVDA+home")
	)
	def script_review_startOfLine(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_startOfLine(gesture)

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to previous character command.
			"Moves the review cursor to the previous character of the current navigator object and speaks it"
		),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad1", "kb(laptop):NVDA+leftArrow", "ts(text):flickLeft")
	)
	def script_review_previousCharacter(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_previousCharacter(gesture)

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to next character command.
			"Moves the review cursor to the next character of the current navigator object and speaks it"
		),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpad3", "kb(laptop):NVDA+rightArrow", "ts(text):flickRight")
	)
	def script_review_nextCharacter(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_nextCharacter(gesture)

	@script(
		description=_(
			# Translators: Input help mode message for move review cursor to end of current line command.
			"Moves the review cursor to the last character of the line "
			"where it is situated in the current navigator object and speaks it"
		),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:shift+numpad3", "kb(laptop):NVDA+end")
	)
	def script_review_endOfLine(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_endOfLine(gesture)

	@script(
		description=_(
			# Translators: Input help mode message for say all in review cursor command.
			"Reads from the review cursor up to the end of the current text,"
			" moving the review cursor as it goes"
		),
		category=globalCommands.SCRCAT_TEXTREVIEW,
		gestures=("kb:numpadPlus", "kb(laptop):NVDA+shift+a", "ts(text):3finger_flickDown")
	)
	def script_review_sayAll(self,gesture):
		self.checkInputComposition()
		super(KoreanCommands, self).script_review_sayAll(gesture)
	@script(
		# Translators: Input help mode message for say all with system caret command.
		description=_("Reads from the system caret up to the end of the text, moving the caret as it goes"),
		category=globalCommands.SCRCAT_SYSTEMCARET,
		gestures=("kb(desktop):NVDA+downArrow", "kb(laptop):NVDA+a")
	)
	def script_sayAll(self,gesture):
		focus = api.getFocusObject()
		if isinstance(focus, InputComposition):
			self.focusSilently(focus.parent)
		super(KoreanCommands, self).script_sayAll(gesture)




class KoreanCommandsWithSenseReaderKeys(KoreanCommands):

	@script(description='키보드 입력 읽기 방식을 변경합니다.', category=globalCommands.SCRCAT_INPUT, gesture='kb:control+shift+c')
	def script_changeInputReport(self, gesture):
		if config.conf['keyboard']['speakTypedCharacters'] and config.conf['keyboard']['speakTypedWords']:
			config.conf['keyboard']['speakTypedCharacters'] = False 
			config.conf['keyboard']['speakTypedWords'] = False
			msg = '키보드 입력 읽지 않기'

		elif config.conf['keyboard']['speakTypedCharacters'] and not config.conf['keyboard']['speakTypedWords']:
			config.conf['keyboard']['speakTypedCharacters'] = False 
			config.conf['keyboard']['speakTypedWords'] = True
			msg = '입력한 단어 읽기'

		elif not config.conf['keyboard']['speakTypedCharacters'] and config.conf['keyboard']['speakTypedWords']:
			config.conf['keyboard']['speakTypedCharacters'] = True
			msg = '입력한 글자 및 단어 읽기'

		else:
			config.conf['keyboard']['speakTypedCharacters'] = True
			msg = '입력한 글자 읽기'

		ui.message(msg)



	@script(description='현재 윈도우 좌표를 알려 줍니다.', category=globalCommands.SCRCAT_FOCUS, gesture='kb:nvda+w')
	def script_reportWindowPosition(self, gesture):
		fg = api.getForegroundObject()
		lect = fg.location
		msg = f"좌상단: ({lect.left}, {lect.top}), 우하단: ({lect.right}, {lect.bottom})"
		ui.message(msg)


	@script(description='브라우저 모드로 전환합니다. 센스리더에서는 가상커서 모드 선택과 같습니다.', 		category=inputCore.SCRCAT_BROWSEMODE, gesture='kb:control+shift+f11')
	def script_browseMode(self, gesture):
		focus = api.getFocusObject()
		vbuf = focus.treeInterceptor
		try:
			if vbuf.passThrough:
				ui.message('브라우저 모드')
				super(KoreanCommandsWithSenseReaderKeys, self).script_toggleVirtualBufferPassThrough(gesture)
		except:
			pass


	@script(description='포커스 모드로 전환됩니다. 센스리더에서 가상 커서 모드를 해제한 것과 같습니다.', 		category=inputCore.SCRCAT_BROWSEMODE, gesture='kb:control+shift+f12')
	def script_focusMode(self, gesture):
		focus = api.getFocusObject()
		vbuf = focus.treeInterceptor
		try:
			if not vbuf.passThrough:
				ui.message('포커스 모드')
				super(KoreanCommandsWithSenseReaderKeys, self).script_toggleVirtualBufferPassThrough(gesture)
		except:
			pass


	@script(description='화면 탐색 모드 등 리뷰  모드를 변경합니다.', category=globalCommands.SCRCAT_TEXTREVIEW, gestures=('kb:numpadMinus', 'kb:shift+numpadMinus', 'kb:alt+shift+[', 'kb(laptop):alt+shift+-'))
	def script_changeReviewMode(self,gesture):
		label=review.nextMode()
		if not label:
			label = review.nextMode(prev=True)
		ui.reviewMessage(label)


	# 캐럿 다음 줄 일기
	@script(description='캐럿 다음 줄 읽기', category=globalCommands.SCRCAT_SYSTEMCARET, gesture='kb:control+shift+o')
	def script_reportNextLine(self, gesture):
		info = self._getTIAtCaret(True)
		info.collapse()
		beforeMark = info.bookmark
		info.move(textInfos.UNIT_LINE, 1)
		info.collapse()
		afterMark = info.bookmark
		if beforeMark == afterMark:
			speech.speakMessage('맨 아래')
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)


	# 캐럿 이전 줄 읽기
	@script(description='캐럿 이전 줄 읽기', category=globalCommands.SCRCAT_SYSTEMCARET, gesture='kb:control+shift+u')
	def script_reportPreviousLine(self, gesture):
		info = self._getTIAtCaret(True)
		info.collapse()
		beforeMark = info.bookmark
		info.move(textInfos.UNIT_LINE, -1)
		info.collapse()
		afterMark = info.bookmark
		if beforeMark == afterMark:
			speech.speakMessage('맨 위')
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)


	# 캐럿 다음 단어 일기
	@script(description='캐럿 다음 단어 읽기', category=globalCommands.SCRCAT_SYSTEMCARET, gesture='kb:control+shift+l')
	def script_reportNextWord(self, gesture):
		info = self._getTIAtCaret(True)
		info.collapse()
		beforeMark = info.bookmark
		info.move(textInfos.UNIT_WORD, 1)
		info.collapse()
		afterMark = info.bookmark
		if beforeMark == afterMark:
			speech.speakMessage('맨 끝')
		info.expand(textInfos.UNIT_WORD)
		speech.speakTextInfo(info, unit=textInfos.UNIT_WORD, reason=controlTypes.OutputReason.CARET)


	# 캐럿 단어 읽기
	@script(description='캐럿 이전 단어 읽기', category=globalCommands.SCRCAT_SYSTEMCARET, gesture='kb:control+shift+j')
	def script_reportPreviousWord(self, gesture):
		info = self._getTIAtCaret(True)
		info.collapse()
		beforeMark = info.bookmark
		info.move(textInfos.UNIT_WORD, -1)
		info.collapse()
		afterMark = info.bookmark
		if beforeMark == afterMark:
			speech.speakMessage('맨 앞')
		info.expand(textInfos.UNIT_WORD)
		speech.speakTextInfo(info, unit=textInfos.UNIT_WORD, reason=controlTypes.OutputReason.CARET)


	# 캐럿 현재 단어 일기
	@script(description='캐럿 현재 단어 읽기', category=globalCommands.SCRCAT_SYSTEMCARET, gesture='kb:control+shift+k')
	def script_reportCurrentWord(self, gesture):
		info = self._getTIAtCaret(True)
		info.expand(textInfos.UNIT_WORD)
		scriptCount=getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info, reason=controlTypes.OutputReason.CARET, unit=textInfos.UNIT_WORD)
		else:
			speech.spellTextInfo(info,useCharacterDescriptions=scriptCount>1)


	# 캐럿 다음글자 일기
	@script(description='캐럿 다음 글자 읽기', category=globalCommands.SCRCAT_SYSTEMCARET, gesture='kb:control+shift+.')
	def script_reportNextCharacter(self, gesture):
		info = self._getTIAtCaret(True)
		info.collapse()
		beforeMark = info.bookmark
		info.move(textInfos.UNIT_CHARACTER, 1)
		info.collapse()
		afterMark = info.bookmark
		if beforeMark == afterMark:
			speech.speakMessage('맨 끝')
		info.expand(textInfos.UNIT_CHARACTER)
		speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)


	# 캐럿 이전 글자 읽기
	@script(description='캐럿 이전 글자 읽기', category=globalCommands.SCRCAT_SYSTEMCARET, gesture='kb:control+shift+m')
	def script_reportPreviousCharacter(self, gesture):
		info = self._getTIAtCaret(True)
		info.collapse()
		beforeMark = info.bookmark
		info.move(textInfos.UNIT_CHARACTER, -1)
		info.collapse()
		afterMark = info.bookmark
		if beforeMark == afterMark:
			speech.speakMessage('맨 앞')
		info.expand(textInfos.UNIT_CHARACTER)
		speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)


	# 캐럿 현재 글자 읽기
	@script(description='캐럿 현재 글자 읽기', category=globalCommands.SCRCAT_SYSTEMCARET, gesture='kb:control+shift+,')
	def script_reportCurrentCharacter(self, gesture):
		info = self._getTIAtCaret(True)
		info.collapse()
		info.expand(textInfos.UNIT_CHARACTER)
		scriptCount= getLastScriptRepeatCount()
		if scriptCount==0:
			speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)
		elif scriptCount==1:
			speech.spellTextInfo(info,useCharacterDescriptions=True)
		else:
			try:
				c = ord(info.text)
			except TypeError:
				c = None
			if c is not None:
				speech.speakMessage("%d," % c)
				speech.speakSpelling(hex(c))
			else:
				log.debugWarning("Couldn't calculate ordinal for character %r" % info.text)
				speech.speakTextInfo(info, unit=textInfos.UNIT_CHARACTER, reason=controlTypes.OutputReason.CARET)

	# 리뷰커서를 캐럿으로 이동
	@script(description='리뷰커서를 캐럿으로이동합니다.', category=globalCommands.SCRCAT_TEXTREVIEW, gestures=('kb:control+numpadPlus', 'kb:nvda+numpadPlus'))
	def script_review_toCaret(self, gesture):
		tIAtCaret = self._getTIAtCaret(True)
		if tIAtCaret.obj.role != controlTypes.ROLE_EDITABLETEXT:
			speech.speakMessage('캐럿이 없습니다.')
			return
		api.setReviewPosition(tIAtCaret)
		speech.speakMessage('캐럿으로 이동')

	# 이동줄 아래로
	@script(description='이동 줄 아래로 리뷰 커서를 이동시키고 그 줄을 읽습니다.', category=globalCommands.SCRCAT_TEXTREVIEW, gestures=('kb:numpad3', 'kb(laptop):alt+shift+h'))
	def script_review_nextMovingLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		movingLine = int(config.conf['general'].get('movingLine', 5))
		res=info.move(textInfos.UNIT_LINE,movingLine)
		if res==0:
			# Translators: a message reported when review cursor is at the top line of the current navigator object.
			ui.reviewMessage(_("Bottom"))
		else:
			api.setReviewPosition(info)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)


	# 이동줄 위로
	@script(description='이동 줄 위로 리뷰 커서를 이동시키고 그 줄을 읽습니다.', category=globalCommands.SCRCAT_TEXTREVIEW, gestures=('kb:numpad9', 'kb(laptop):alt+shift+y'))
	def script_review_previousMovingLine(self,gesture):
		info=api.getReviewPosition().copy()
		info.expand(textInfos.UNIT_LINE)
		info.collapse()
		movingLine = int(config.conf['general'].get('movingLine', 5))
		res=info.move(textInfos.UNIT_LINE,-1 *movingLine)
		if res==0:
			# Translators: a message reported when review cursor is at the top line of the current navigator object.
			ui.reviewMessage(_("Top"))
		else:
			api.setReviewPosition(info)
		info.expand(textInfos.UNIT_LINE)
		speech.speakTextInfo(info, unit=textInfos.UNIT_LINE, reason=controlTypes.OutputReason.CARET)


	# 현재 시각
	@script(description='현재 날짜를 알려 줍니다.', category=globalCommands.SCRCAT_SYSTEM, gesture="kb:alt+shift+t")
	def script_time(self,gesture):
		text=winKernel.GetTimeFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.TIME_NOSECONDS, None, None)
		ui.message(text)

	# 현재 날짜
	@script(description='현재 시각을 알려 줍니다.', category=globalCommands.SCRCAT_SYSTEM, gesture="kb:alt+shift+d")
	def script_date(self,gesture):
		text=winKernel.GetDateFormatEx(winKernel.LOCALE_NAME_USER_DEFAULT, winKernel.DATE_LONGDATE, None, None)
		ui.message(text)

	# 기존 단축키 정지 및 센스리더 단축키 지정
	__gestures = {
		# 기존 단축키 차단
		"kb(desktop):NVDA+control+upArrow": None,
		"kb(laptop):NVDA+shift+control+upArrow": None,
		"kb(desktop):NVDA+control+downArrow": None,
		"kb(laptop):NVDA+shift+control+downArrow": None,
		"kb(desktop):NVDA+control+leftArrow": None,
		"kb(laptop):NVDA+control+leftArrow": None,
		"kb(laptop):NVDA+control+rightArrow": None,
		"kb(laptop):NVDA+shift+control+leftArrow": None,
		"kb(desktop):NVDA+control+rightArrow": None,
		"kb(laptop):NVDA+shift+control+rightArrow": None,
		"kb(desktop):NVDA+upArrow": None, 
		"kb(laptop):NVDA+upArrow": None, 
		"kb(laptop):NVDA+l": None,
		"kb:numpad1": None,
		"kb:numpad2": None,
		"kb:numpad4": None,
		"kb:numpad5": None,
		"kb:numpad6": None,
		"kb:numpad7": None,
		"kb:numpad8": None,
		"kb(laptop):NVDA+downArrow": None, 
		"kb(desktop):NVDA+downArrow": None, 
		"kb(laptop):NVDA+a": None,
		"kb(laptop):NVDA+leftArrow": None,
		"kb(laptop):NVDA+rightArrow": None,
		"kb(laptop):nvda+.": None,
		"kb(laptop):nvda+control+.": None,
		"kb(laptop):nvda+shift+.": None,
		"kb(laptop):nvda+shift+o": None,
		"kb:NVDA+numpad7": None, 
		'kb:nvda+p': None,
		"kb(laptop):NVDA+pageUp": None, 
		"kb:NVDA+numpad1": None, 
		"kb(laptop):NVDA+pageDown": None, 
		"kb:nvda+f2": None,
		'kb:nvda+f12': None,
		'kb:nvda+shift+b': None,
		'kt:nvda+t': None,
		'kb:nvda+b': None,
		"kb:shift+numpad1": None,
		"kb:shift+numpad3": None,
		"kb:shift+numpad7": None,
		"kb:shift+numpad9": None,
		"kb(desktop):NVDA+end": None, 
		"kb(laptop):NVDA+shift+end": None, 
		"kb(laptop):NVDA+control+home": None,
		"kb(laptop):NVDA+control+end": None,
		"kb(laptop):nvda+home": None, 
		"kb(laptop):nvda+end": None, 
		"kb:nvda+tab": None,
		"kb:nvda+t": None,
		"kb(desktop):NVDA+shift+upArrow": None, 
		"kb(laptop):NVDA+shift+upArrow": None, 
		"kb(laptop):NVDA+shift+downArrow": None, 
		"kb(laptop):NVDA+shift+leftArrow": None, 
		"kb(laptop):NVDA+shift+rightArrow": None, 
		"kb(laptop):NVDA+shift+s": None,
		"kb:NVDA+numpadEnter": None, 
		"kb(laptop):NVDA+enter": None, 
		"kb:NVDA+shift+numpadMinus": None, 
		"kb(laptop):NVDA+shift+backspace": None,
		"kb:NVDA+numpadDelete": None, 
		"kb(laptop):NVDA+delete": None,
		"kb:NVDA+numpadMinus": None, 
		"kb(laptop):NVDA+backspace": None,
		"kb:NVDA+numpadDivide": None, 
		"kb(laptop):NVDA+shift+m": None,
		"kb:NVDA+numpadMultiply": None, 
		"kb(laptop):NVDA+shift+n": None,

		# NVDA 메뉴 활성화
		'kb:control+\\': 'showGui',
		'kb:nvda+f4': 'quit',
				# 텍스트 리뷰 읽기
		'kb:numpad4': 'review_previousCharacter',
		'kb:alt+shift+m': 'review_previousCharacter',
		'kb:alt+numpad5': 'review_currentCharacter',
		'kb:alt+shift+,': 'review_currentCharacter',
		'kb:numpad6': 'review_nextCharacter',
		'kb:alt+shift+.': 'review_nextCharacter',
		'kb:control+numpad4': 'review_previousWord',
		'kb:nvda+numpad4': 'review_previousWord',
		'kb:alt+shift+j': 'review_previousWord',
		'kb:control+numpad5': 'review_currentWord',
		'kb:nvda+numpad5': 'review_currentWord',
		'kb:alt+shift+k': 'review_currentWord',
		'kb:control+numpad6': 'review_nextWord',
		'kb:nvda+numpad6': 'review_nextWord',
		'kb:alt+shift+l': 'review_nextWord',
		'kb:numpad8': 'review_previousLine',
		'kb:alt+shift+u': 'review_previousLine',
		'kb:numpad5': 'review_currentLine',
		'kb:alt+shift+i': 'review_currentLine',
		'kb:numpad2': 'review_nextLine',
		'kb:alt+shift+o': 'review_nextLine',
		'kb:control+numpad8': 'review_top',
		'kb:nvda+numpad8': 'review_top',
		'kb:alt+shift+p': 'review_top',
		'kb:control+numpad2': 'review_bottom',
		'kb:nvda+numpad2': 'review_bottom',
		'kb:alt+shift+;': 'review_bottom',
		'kb:numpad7': 'review_startOfLine',
		'kb:alt+shift+n': 'review_startOfLine',
		'kb:numpad1': 'review_endOfLine',
		'kb:alt+shift+/': 'review_endOfLine',
		# 객체 읽기
		'kb:nvda+control+numpad4': 'navigatorObject_previous',
		'kb:nvda+control+leftArrow': 'navigatorObject_previous',
		'kb:nvda+control+numpad5': 'navigatorObject_current',
		'kb:nvda+control+numpad6': 'navigatorObject_next',
		'kb:nvda+control+rightArrow': 'navigatorObject_next',
		'kb:nvda+control+numpad8': 'navigatorObject_parent',
		'kb:nvda+control+upArrow': 'navigatorObject_parent',
		'kb:nvda+control+numpad2': 'navigatorObject_firstChild',
		'kb:nvda+control+downArrow': 'navigatorObject_firstChild',
		'kb:nvda+control+numpadEnter': 'review_activate', 
		'kb:nvda+control+enter': 'review_activate', 
		'kb:nvda+control+numpadPlus': 'navigatorObject_moveFocus', 
		'kb:nvda+control+space': 'navigatorObject_moveFocus', 

		# 포커스, 탐색 객체 등 이동하기
		'kb:numpadPlus': 'navigatorObject_toFocus', 
		'kb:alt+shift+numpadPlus': 'moveNavigatorObjectToMouse', 
		'kb:control+shift+numpadPlus': 'moveMouseToNavigatorObject',
		'kb:control+shift+i': 'reportCurrentLine',
		# 포커스 관련 단축키
		'kb:control+shift+t': 'title',
		'kb:control+shift+s': 'readStatusLine',
		'kb:control+shift+f': 'reportCurrentFocus', 
		'kb:control+shift+w': 'speakForeground', 
		'kb:control+shift+b': 'reportCurrentSelection', 
		'kb:nvda+control+c': 'reportCaretLocation', 
		'kb:nvda+leftArrow': 'previousSynthSetting', 
		'kb:nvda+rightArrow': 'nextSynthSetting', 
		'kb:nvda+upArrow': 'increaseSynthSetting',
		'kb:nvda+downArrow': 'decreaseSynthSetting',
		'kb:alt+shift+z': 'cycleSpeechSymbolLevel', 
		'kb:nvda+a': 'reportOrShowFormattingAtCaret', 
		'kb:f11': 'sayAll', 
		'kb:control+shift+n': 'passNextKeyThrough', 
		'kb:nvda+b': 'say_battery_status', 
		'kb:alt+shift+backSpace': 'speechMode',
		}

