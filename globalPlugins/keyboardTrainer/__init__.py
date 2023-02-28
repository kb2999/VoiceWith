# coding: EUC-KR

from logHandler import log
import globalPluginHandler
import gui
import wx
import scriptHandler
import config
import random
import queueHandler
import speech
import winsound
import time
import os


# 전역변수
mainTitle = u"보이스위드 타자 연습"
trainingDialog = None
mainPanel = None
subPanel = None
studyPanel = None
descriptions = {
	u"ㄴ": u"왼손 약지로 누르세요.",
	u"ㄹ": u"왼손 검지로 누르세요.",
	u"ㅁ": u"왼손 소지로 누르세요.",
	u"ㅇ": u"왼손 중지로 누르세요.",
	u"ㅎ": u"왼손 검지로 누르세요.",
	u"ㅏ": u"오른손 중지로 누르세요.",
	u"ㅓ": u"오른손 검지로 누르세요.",
	u"ㅗ": u"오른손 검지로 누르세요.",
	u"ㅣ": u"오른손 약지로 누르세요.",
	u"ㅂ": u"왼손 소지로 누르세요.",
	u"ㅈ": u"왼손 약지로 누르세요.",
	u"ㄷ": u"왼손 중지로 누르세요.",
	u"ㄱ": u"왼손 검지로 누르세요.",
	u"ㅅ": u"왼손 검지로 누르세요.",
	u"ㅃ": u"오른손 소지로 쉬프트키를 누르면서 왼손 소지로 누르세요.",
	u"ㅉ": u"오른손 소지로 쉬프트키를 누르면서 왼손 약지로 누르세요.",
	u"ㄸ": u"오른손 소지로 쉬프트키를 누르면서 왼손 중지로 누르세요.",
	u"ㄲ": u"오른손 소지로 쉬프트키를 누르면서 왼손 검지로 누르세요.",
	u"ㅆ": u"오른손 소지로 쉬프트키를 누르면서 왼손 검지로 누르세요.",
	u"ㅋ": u"왼손 소지로 누르세요.",
	u"ㅌ": u"왼손 약지로 누르세요.",
	u"ㅊ": u"왼손 중지로 누르세요.",
	u"ㅍ": u"왼손 검지로 누르세요.",
	u"ㅛ": u"오른손 검지로 누르세요.", 
	u"ㅕ": u"오른손 검지로 누르세요.",
	u"ㅑ": u"오른손 중지로 누르세요.",
	u"ㅐ": u"아 이 오른손 약지로 누르세요.",
	u"ㅔ": u"어 이 오른손 소지로 누르세요.",
	u"ㅒ": u"야 이 왼손 소지로 쉬프트키를 누르면서 오른손 약지로 누르세요.",
	u"ㅖ": u"여 이 왼손 소지로 쉬프트키를 누르면서 오른손 소지로 누르세요.", 
	u"ㅠ": u"오른손 검지로 누르세요.",
	u"ㅜ": u"오른손 검지로 누르세요.",
	u"ㅡ": u"오른손 검지로 누르세요.",

	"a": u"왼손 소지로 누르세요.", 
	"b": u"왼손 검지로 누르세요.", 
	"c": u"왼손 중지로 누르세요.", 
	"d": u"왼손 중지로 누르세요.", 
	"e": u"왼손 중지로 누르세요.", 
	"f": u"왼손 검지로 누르세요.", 
	"g": u"왼손 검지로 누르세요.", 
	"h": u"오른손 검지로 누르세요.", 
	"i": u"오른손 중지로 누르세요.", 
	"j": u"오른손 검지로 누르세요.", 
	"k": u"오른손 중지로 누르세요.", 
	"l": u"오른손 약지로 누르세요.", 
	"m": u"오른손 검지로 누르세요.", 
	"n": u"오른손 검지로 누르세요.", 
	"o": u"오른손 약지로 누르세요.", 
	"p": u"오른손 소지로 누르세요.", 
	"q": u"왼손 소지로 누르세요.", 
	"r": u"왼손 검지로 누르세요.", 
	"s": u"왼손 약지로 누르세요.", 
	"t": u"왼손 검지로 누르세요.", 
	"u": u"오른손 검지로 누르세요.", 
	"v": u"왼손 검지로 누르세요.", 
	"w": u"왼손 약지로 누르세요.", 
	"x": u"왼손 약지로 누르세요.", 
	"y": u"오른손 검지로 누르세요.", 
	"z": u"왼손 소지로 누르세요.", 

	"1": u"왼손 소지로 누르세요.", 
	"2": u"왼손 약지로 누르세요.", 
	"3": u"왼손 중지로 누르세요.", 
	"4": u"왼손 검지로 누르세요.", 
	"5": u"왼손 검지로 누르세요.", 
	"6": u"왼손 검지로 누르세요.", 
	"7": u"오른손 검지로 누르세요.", 
	"8": u"오른손 중지로 누르세요.", 
	"9": u"오른손 약지로 누르세요.", 
	"0": u"오른손 소지로 누르세요.", 

	"!": u"느낌표 쉬프트키와 숫자 1을 동시에 누르세요.", 
	"@": u"골뱅이 쉬프트키와 숫자 2를 동시에 누르세요.", 
	"#": u"샵 쉬프트키와 숫자 3을 동시에 누르세요.", 
	"$": u"달러 쉬프트키와 숫자 4를 동시에 누르세요.", 
	"%": u"퍼센트 쉬프트키와 숫자 5를 동시에 누르세요.", 
	"^": u"캐럿 쉬프트키와 숫자 6을 동시에 누르세요.", 
	"&": u"앰퍼센드 쉬프트키와 숫자 7을 동시에 누르세요.", 
	"*": u"스타 쉬프트키와 숫자 8을 동시에 누르세요.", 
	"(": u"괄호 열고 쉬프트키와 숫자 9를 동시에 누르세요.", 
	")": u"괄호 닫고 쉬프트키와 숫자 0을 동시에 누르세요.", 

	"`": u"그레이브 숫자 1 왼쪽에 있습니다. 왼손 소지로 누르세요.",
	"-": u"대쉬 숫자 0 오른쪽에 있습니다. 오른손 소지로 누르세요.",
	"=": u"이퀄 숫자 0 오른쪽 두번째에 있습니다. 오른손 소지로 누르세요.",
	"[": u"대괄호 열고 영어 p 키의 오른쪽에 있습니다. 오른손 소지로 누르세ㅛ.",
	"]": u"대괄호 닫고 영어 p 키 오른쪽 두번째에 있습니다. 오른쪽 소지로 누르세요.",
	"\\": u"백 슬레시 숫자 0 오른쪽 세번째에 있거나 영어 p 키의 오른쪽 세번째에 있습니다. 오른손 소지로 누르세요.",
	";": u"세미콜론 영어 l 키 오른쪽에 있습니다. 오른손 소지로 누르세요.",
	"'": u"어퍼스트로피 영어 l 키의 오른쪽 두번째에 있습니다. 오른손 소지로 누르세요.",
	",": u"콤마 영어 m 오른쪽에 있습니다. 오른손 중지로 누르세요.",
	".": u"점 영어 m 키의 오른쪽 두번째에 있습니다. 오른손 약지로 누르세요.",
	"/": u"슬레시 영어 m 키의 오른쪽 세번째에 있습니다. 오른손 소지로 누르세요.",

	"~": u"물결 쉬프트와 그레이브를 함께 누르세요.",
	"_": u"언더바 쉬프트와 대쉬를 함께 누르세요.",
	"+": u"플러스 쉬프트와 이퀄을 함께 누르세요.",
	"{": u"중괄호 열고 쉬프트와 대괄호 열고를 함께 누르세요.",
	"}": u"중괄호 닫고 쉬프트와 대괄호 닫고를 함께 누르세요.",
	"|": u"버티컬바 쉬프트와 백슬레쉬를 함께 누르세요.",
	":": u"콜론 쉬프트와 세미콜론을 함께 누르세요.",
	'"': u"쿼테이션 쉬프트와 어퍼스트로피를 함께 누르세요.",
	"<": u"레스댄 쉬프트와 콤마를 함께 누르세요.",
	">": u"그레이터댄 쉬프트와 점을 함께 누르세요.",
	"?": u"물음표 쉬프트와 슬레쉬를 함께 누르세요.",

	wx.WXK_RETURN: u"엔터", 
	wx.WXK_SPACE: u"스페이스", 
	wx.WXK_BACK: u"백 스페이스", 
	wx.WXK_CONTROL: u"컨트롤", 
	wx.WXK_ALT: u"알트", 
	wx.WXK_SHIFT: u"쉬프트", 
	wx.WXK_WINDOWS_LEFT: u"왼쪽 윈도우", 
	wx.WXK_PAGEUP: u"페이지 업", 
	wx.WXK_PAGEDOWN: u"페이지 다운", 
	wx.WXK_HOME: u"홈", 
	wx.WXK_END: u"엔드", 
	wx.WXK_INSERT: u"인서트", 
	wx.WXK_DELETE: u"딜리트", 
	wx.WXK_TAB: u"탭", 
	wx.WXK_CAPITAL: u"캡스 록", 
	wx.WXK_F1: u"F1", 
	wx.WXK_F2: u"F2", 
	wx.WXK_F3: u"F3", 
	wx.WXK_F4: u"F4", 
	wx.WXK_F5: u"F5", 
	wx.WXK_F6: u"F6", 
	wx.WXK_F7: u"F7", 
	wx.WXK_F8: u"F8", 
	wx.WXK_F9: u"F9", 
	wx.WXK_F10: u"F10", 
	wx.WXK_F11: u"F11", 
	wx.WXK_F12: u"F12,",
	}

dKeys = {
	"koreanBasic": [u"ㅁ", u"ㄴ", u"ㅇ", u"ㄹ", u"ㅎ", u"ㅗ", u"ㅓ", u"ㅏ", u"ㅣ"],
	"koreanLeftUpper": [u"ㅂ", u"ㅈ", u"ㄷ", u"ㄱ", u"ㅅ", u"ㅃ", u"ㅉ", u"ㄸ", u"ㄲ", u"ㅆ"], 
	"koreanLeftLower": [u"ㅋ", u"ㅌ", u"ㅊ", u"ㅍ"], 
	"koreanRightUpper": [u"ㅛ", u"ㅕ", u"ㅑ", u"ㅐ", u"ㅔ", u"ㅒ", u"ㅖ"], 
	"koreanRightLower": [u"ㅠ", u"ㅜ", u"ㅡ"], 

	"englishBasic": ["a", "s", "d", "f", "g", "h", "j", "k", "l"], 
	"englishLeftUpper": ["q", "w", "e", "r", "t"], 
	"englishLeftLower": ["z", "x", "c", "v", "b"], 
	"englishRightUpper": ["y", "u", "i", "o", "p"], 
	"englishRightLower": ["m", "n"], 

	"number": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], 
	"shiftNumber": ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")"], 
	"otherSign": ["`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/"], 
	"shiftOtherSign": ["~", "_", "+", "{", "}", "|", ":", '"', "<", ">", "/"], 

	"modifier": [wx.WXK_RETURN, wx.WXK_SPACE, wx.WXK_BACK, wx.WXK_CONTROL, wx.WXK_ALT, wx.WXK_SHIFT, wx.WXK_WINDOWS_LEFT, wx.WXK_PAGEUP, wx.WXK_PAGEDOWN, wx.WXK_HOME, wx.WXK_END, wx.WXK_INSERT, wx.WXK_DELETE, wx.WXK_TAB, wx.WXK_CAPITAL, wx.WXK_F1, wx.WXK_F2, wx.WXK_F3, wx.WXK_F4, wx.WXK_F5, wx.WXK_F6, wx.WXK_F7, wx.WXK_F8, wx.WXK_F9, wx.WXK_F10, wx.WXK_F11, wx.WXK_F12], 
	}

dWords = {
	"koreanBasic": [u"이모", u"하모니", u"어머니", u"할머니", u"말머리", u"만남", u"망언", u"호미", u"미나리", u"난민", u"논어", u"농어", u"논리", u"넝마", u"낭만", u"난리", u"나리", u"남미", u"오리", u"어머나", u"얼마나", u"난로", u"롤러", u"나라", u"호랑이", u"허리"], 
	"koreanLeftUpper": [u"보리", u"아버지", u"반지", u"빈곤", u"조리사", u"전기", u"직선", u"도시", u"동시", u"독사", u"더미", u"담비", u"답장", u"반달", u"반디", u"곤란", u"고니", u"반달곰", u"거지", u"검사", u"감사", u"한강", u"공기", u"도자기", u"송어", u"손님", u"성대", u"선비", u"사이다", u"상인", u"상업", u"상어", u"시인", u"화장실", u"도서실", u"독서실", u"사회자", u"환자", u"도화지", u"조회", u"아빠", u"뽀뽀뽀", u"뽕나무", u"빵집", u"삐삐", u"쫑알쫑알", u"번쩍번쩍", u"짜장면", u"짱아치", u"똥덩어리", u"똘똘이", u"떡집", u"땅강아지", u"딱지", u"딸기", u"땀띠", u"꼴찌", u"꼼수", u"껌딱지", u"깍두기", u"쏘시지", u"눈썰미", u"쌍쌍바", u"씽씽", u"씨앗"], 
	"koreanLeftLower": [u"콩닥콩닥", u"콜라", u"커피", u"캉캉", u"킬킬", u"토끼", u"톱질", u"털실", u"타조", u"티코"], 
	"koreanRightUpper": [u"교실", u"요리", u"효도", u"표지판", u"경기도", u"영화", u"명작", u"형님", u"향수", u"한약", u"대학교", u"배신자", u"탱탱볼", u"생명", u"신체", u"게맛살", u"제사", u"얘기", u"옛날"], 
	"koreanRightLower": [u"감귤", u"율무", u"법률", u"석유", u"불꽃", u"줄넘기", u"둘리", u"땅굴", u"술병", u"문장", u"운동장", u"우산", u"눈싸움", u"마루", u"훈련소", u"쿨피스", u"퉁소", u"충고", u"풍선", u"치즈", u"튜브", u"본드", u"핫도그", u"드레스", u"의사", u"위치", u"귀신", u"의자", u"요구르트", u"", u"희망", u"지휘자", u"탱크", u"트럭", u"프랑스", u"트럼프"],
	"english": ["auto", "boot", "create", "data", "error", "file", "game", "hot", "if", "jump", "key", "link", "menu", "no", "open", "pass", "quit", "run", "start", "typ", "up", "volume", "window", "xp", "yes", "zip"],
	}


def play(file):
	soundPath = os.path.join(os.path.dirname(__file__), "sounds")
	filePath = os.path.join(soundPath, file)
	if os.path.exists(filePath):
		winsound.PlaySound(filePath, winsound.SND_FILENAME)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		item = gui.mainFrame.sysTrayIcon.menu.Append(-1, u"타자 연습\tCtrl+&J")
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onKeyboardTraining, item)

	def onKeyboardTraining(self, e):
		self.popupDialog()

	def script_popupDialog(self, gesture):
		if "voiceWith" in config.conf and "popupKeyboardTrainingByGraave" in config.conf["voiceWith"] and not eval(config.conf["voiceWith"]["popupKeyboardTrainingByGraave"]):
			gesture.send()
			return

		count = scriptHandler.getLastScriptRepeatCount()
		if count == 1:
			self.popupDialog()
		else:
			gesture.send()

	def popupDialog(self):
		global trainingDialog, mainPanel, subPanel, studyPanel
		if trainingDialog is None:
			trainingDialog = TrainingDialog()
			trainingDialog.Show()
		elif trainingDialog.IsIconized():
			trainingDialog.Iconize(False)
			trainingDialog.Show()
		trainingDialog.Raise()


	__gestures = {"kb:`": "popupDialog",}



class TrainingDialog(wx.Dialog):
	def __init__(self):
		global mainTitle, mainPanel
		super(TrainingDialog, self).__init__(None, -1, mainTitle, wx.DefaultPosition, wx.Size(930, 650))
		self.SetBackgroundColour("#dddddd")
		self.Bind(wx.EVT_CLOSE, self.onDestroy)
		mainPanel = MainPanel(self)
		play("start.wav")

	def onDestroy(self, e):
		global trainingDialog, mainPanel, subPanel, studyPanel
		trainingDialog = mainPanel = subPanel = studyPanel = None
		play("end.wav")
		self.Destroy()

class MenuButton(wx.Button):
	def __init__(self, parent, label, point, eventHandler=None):
		super(MenuButton, self).__init__(parent, -1, label, point, wx.Size(400, 80), wx.ALIGN_LEFT)
		self.SetBackgroundColour("#dddddd")
		font = wx.Font(22, wx.MODERN, wx.NORMAL, wx.BOLD)
		self.SetFont(font)
		if eventHandler:
			self.Bind(wx.EVT_BUTTON, eventHandler)


class MainPanel(wx.Panel):
	def __init__(self, parent):
		super(MainPanel, self).__init__(parent, -1, wx.Point(50, 50), wx.Size(830, 550))
		self.SetBackgroundColour("#bbbbbb")
		self.parent = parent
		btnKoreanTraining = MenuButton(self, u"  한글 연습", wx.Point(10, 10), self.onBtnKoreanTraining)
		btnEnglishTraining = MenuButton(self, u"  영어 연습", wx.Point(420, 10),  self.onBtnEnglishTraining)

		btnNumberSignTraining = MenuButton(self, u"  숫자 및 기호 연습", wx.Point(10, 100), self.onBtnNumberSignTraining)
		btnNotepad = MenuButton(self, u"  낙서장", wx.Point(420, 100), self.onBtnNotepad)

		self.btnPopupByGraave = wx.ToggleButton(self, -1, u"  그레이브를 빠르게 두 번 누르면 타자 연습이 실행됩니다.", (10, 190), (810, 100), style=wx.ALIGN_LEFT)
		self.btnPopupByGraave.SetFont(wx.Font(24, wx.MODERN, wx.NORMAL, wx.BOLD))
		if not "voiceWith" in config.conf:
			config.conf["voiceWith"] = {}
		if not "popupKeyboardTrainingByGraave" in config.conf["voiceWith"]:
			config.conf["voiceWith"]["popupKeyboardTrainingByGraave"] = "True"
		self.btnPopupByGraave.SetValue(eval(config.conf["voiceWith"]["popupKeyboardTrainingByGraave"]))
		self.btnPopupByGraave.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleButton)

		btnExit = MenuButton(self, u"  종료(&X)", wx.Point(10, 280), self.onBtnExit)



	def onToggleButton(self, e):
		state = not eval(config.conf["voiceWith"]["popupKeyboardTrainingByGraave"]) 
		config.conf["voiceWith"]["popupKeyboardTrainingByGraave"] = str(state)
		self.btnPopupByGraave.SetValue(state)

	def onBtnKoreanTraining(self, e):
		global subPanel
		subPanel = KoreanPanel(self.parent)
		play("in.wav")
		subPanel.SetFocus()

	def onBtnEnglishTraining(self, e):
		global subPanel
		subPanel = EnglishPanel(self.parent)
		play("in.wav")
		subPanel.SetFocus()

	def onBtnNumberSignTraining(self, e):
		global subPanel
		subPanel = NumberSignPanel(self.parent)
		play("in.wav")
		subPanel.SetFocus()


	def onBtnNotepad(self, e):
		global subPanel
		subPanel = NotepadPanel(self.parent)
		play("in.wav")
		subPanel.SetFocus()


	def onBtnExit(self, e):
		self.parent.onDestroy(None)


class SubPanel(wx.Panel):
	def __init__(self, parent):
		super(SubPanel, self).__init__(parent, -1, wx.Point(50, 50), wx.Size(830, 550))
		self.SetBackgroundColour("#bbbbbb")
		self.parent = parent
		try:
			mainPanel.Hide()
		except:
			pass

		# 뒤로 가기 숨김 버튼
		btnBack = wx.Button(self, wx.ID_CANCEL, u"")
		btnBack.Hide()
		btnBack.Bind(wx.EVT_BUTTON, self.onBtnBack)
		accelTable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_CANCEL), (wx.ACCEL_ALT, wx.WXK_LEFT, wx.ID_CANCEL)])
		self.SetAcceleratorTable(accelTable)

		self.onInit()

	def onBtnBack(self, e):
		global mainPanel, subPanel
		play("out.wav")
		mainPanel.Show()
		mainPanel.SetFocus()
		subPanel = None
		self.Destroy()

	def onInit(self):
		raise NotImplementedError


class NotepadPanel(SubPanel):
	def onInit(self):
		self.textCtrl = wx.TextCtrl(self, -1, '', (10, 10), (830, 530), style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB, name=u"낙서장")
		self.textCtrl.SetBackgroundColour("#dddddd")

class KoreanPanel(SubPanel):
	def onInit(self):
		btnKRBasic = MenuButton(self, u"  한글 기본 자리", wx.Point(10, 10), self.onBtnBasic)
		btnKRBasicWord = MenuButton(self, u"  한글 기본 자리 단어", wx.Point(420, 10), self.onBtnBasicWord)

		btnKRLeftUpper = MenuButton(self, u"  한글 왼손 윗줄", wx.Point(10, 100), self.onBtnLeftUpper)
		btnKRLeftUpperWord = MenuButton(self, u"  한글 왼손 윗줄 단어", wx.Point(420, 100), self.onBtnLeftUpperWord)

		btnKRLeftLower = MenuButton(self, u"  한글 왼손 아랫줄", wx.Point(10, 190), self.onBtnLeftLower)
		btnKRLeftLowerWord = MenuButton(self, u"  한글 왼손 아랫줄 단어", wx.Point(420, 190), self.onBtnLeftLowerWord)

		btnKRRightUpper = MenuButton(self, u"  한글 오른손 윗줄", wx.Point(10, 280), self.onBtnRightUpper)
		btnKRRightUpperWord = MenuButton(self, u"  한글 오른손 윗줄 단어", wx.Point(420, 280), self.onBtnRightUpperWord)

		btnKRRightLower = MenuButton(self, u"  한글 오른손 아랫줄", wx.Point(10, 370), self.onBtnRightLower)
		btnKRRightLowerWord = MenuButton(self, u"  한글 오른손 아랫줄 단어", wx.Point(420, 370), self.onBtnRightLowerWord)

		btnKRAllWord = MenuButton(self, u"  한글 전체 단어", wx.Point(10, 460), self.onBtnAllWord)

	def onBtnBasic(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["koreanBasic"], extra=None).SetFocus()

	def onBtnBasicWord(self, e):
		global dWords, studyPanel
		studyPanel = StudyPanel(self.parent, dWords["koreanBasic"], extra=None).SetFocus()

	def onBtnLeftUpper(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["koreanLeftUpper"], extra=dKeys["koreanBasic"]).SetFocus()

	def onBtnLeftUpperWord(self, e):
		global dWords, studyPanel, studyPanel
		studyPanel = studyPanel = StudyPanel(self.parent, dWords["koreanLeftUpper"], extra=dWords["koreanBasic"]).SetFocus()

	def onBtnLeftLower(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["koreanLeftLower"], extra=dKeys["koreanBasic"]+dKeys["koreanLeftUpper"]).SetFocus()

	def onBtnLeftLowerWord(self, e):
		global dWords, studyPanel
		studyPanel = StudyPanel(self.parent, dWords["koreanLeftLower"], extra=dWords["koreanBasic"]+dWords["koreanLeftUpper"]).SetFocus()

	def onBtnRightUpper(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["koreanRightUpper"], extra=dKeys["koreanBasic"]+dKeys["koreanLeftUpper"]+dKeys["koreanLeftLower"]).SetFocus()

	def onBtnRightUpperWord(self, e):
		global dWords, studyPanel
		studyPanel = StudyPanel(self.parent, dWords["koreanRightUpper"], extra=dWords["koreanBasic"]+dWords["koreanLeftUpper"]+dWords["koreanLeftLower"]).SetFocus()

	def onBtnRightLower(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["koreanRightLower"], extra=dKeys["koreanBasic"]+dKeys["koreanLeftUpper"]+dKeys["koreanLeftLower"]+dKeys["koreanRightUpper"]).SetFocus()

	def onBtnRightLowerWord(self, e):
		global dWords, studyPanel
		studyPanel = StudyPanel(self.parent, dWords["koreanRightLower"], extra=dWords["koreanBasic"]+dWords["koreanLeftUpper"]+dWords["koreanLeftLower"]+dWords["koreanRightUpper"]).SetFocus()


	def onBtnAllWord(self, e):
		global dWords, studyPanel
		koreanWords = [s for key in dWords.keys() if key.startswith('korean') for s in dWords[key]]
		studyPanel = StudyPanel(self.parent, koreanWords, extra=None).SetFocus()


class EnglishPanel(SubPanel):
	def onInit(self):
		btnEngBasic = MenuButton(self, u"  영어 기본 자리", wx.Point(10, 10), self.onBtnEngBasic)
		btnEngLeftUpper = MenuButton(self, u"  영어 왼손 윗줄", wx.Point(420, 10), self.onBtnEngLeftUpper)

		btnEngLeftLower = MenuButton(self, u"  영어 왼손 아랫줄", wx.Point(10, 100), self.onBtnEngLeftLower)
		btnEngRightUpper = MenuButton(self, u"  영어 오른손 윗줄", wx.Point(420, 100), self.onBtnEngRightUpper)

		btnEngRightLower = MenuButton(self, u"  영어 오른손 아랫줄", wx.Point(10, 190), self.onBtnEngRightLower)
		btnEngAllWord = MenuButton(self, u"  영어 단어 연습", wx.Point(420, 190), self.onBtnEngAllWord)

	def onBtnEngBasic(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["englishBasic"], extra=None).SetFocus()

	def onBtnEngLeftUpper(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["englishLeftUpper"], extra=dKeys["englishBasic"]).SetFocus()

	def onBtnEngLeftLower(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["englishLeftLower"], extra=dKeys["englishBasic"]+dKeys["englishLeftUpper"]).SetFocus()

	def onBtnEngRightUpper(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["englishRightUpper"], extra=dKeys["englishBasic"]+dKeys["englishLeftUpper"]+dKeys["englishLeftLower"]).SetFocus()

	def onBtnEngRightLower(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["englishRightLower"], extra=dKeys["englishBasic"]+dKeys["englishLeftUpper"]+dKeys["englishLeftLower"]+dKeys["englishRightUpper"]).SetFocus()

	def onBtnEngAllWord(self, e):
		global dWords, studyPanel
		studyPanel = StudyPanel(self.parent, dWords["english"], extra=None).SetFocus()


class NumberSignPanel(SubPanel):
	def onInit(self):
		btnNumber = MenuButton(self, u"  숫자", wx.Point(10, 10), self.onBtnNumber)
		btnShiftNumber = MenuButton(self, u"  쉬프트 숫자 조합 기호", wx.Point(420, 10), self.onBtnShiftNumber)

		btnOtherSign = MenuButton(self, u"  기타 기호", wx.Point(10, 100), self.onBtnOtherSign)
		btnShiftOtherSign = MenuButton(self, u"  쉬프트 조합 기타 기호", wx.Point(420, 100), self.onBtnShiftOtherSign)

	def onBtnNumber(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["number"], extra=None).SetFocus()

	def onBtnShiftNumber(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["shiftNumber"], extra=dKeys["number"]).SetFocus()

	def onBtnOtherSign(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["otherSign"], extra=dKeys["number"]+dKeys["shiftNumber"]).SetFocus()

	def onBtnShiftOtherSign(self, e):
		global dKeys, studyPanel
		studyPanel = StudyPanel(self.parent, dKeys["shiftOtherSign"], extra=dKeys["number"]+dKeys["shiftNumber"]+dKeys["otherSign"]).SetFocus()


class StudyPanel(wx.Panel):
	def __init__(self, parent, keys, extra=None):
		global mainPanel, subPanel, descriptions
		super(StudyPanel, self).__init__(parent, -1, wx.Point(50, 50), wx.Size(830, 550))
		self.SetBackgroundColour("#bbbbbb")
		self.parent = parent
		self.keys = keys
		self.extra = extra
		self.descriptions = descriptions
		self.startTime = int(time.time())
		self.quezCount = 0

		try:
			mainPanel.Hide()
			subPanel.Hide()
		except:
			pass

		play("in.wav")

		self.guide = wx.StaticText(self, -1, '', wx.Point(50, 150), wx.Size(730, 150), style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ALIGN_CENTRE_VERTICAL)
		self.guide.SetFont(wx.Font(36, wx.MODERN, wx.NORMAL, wx.BOLD))
		self.textCtrl = wx.TextCtrl(self, -1, "", wx.Point(100, 400), wx.Size(630, 50), wx.TE_PROCESS_ENTER | wx.TE_CENTRE)
		self.textCtrl.SetFont(wx.Font(36, wx.MODERN, wx.NORMAL, wx.BOLD))

		# 뒤로 가기 숨김 버튼
		btnBack = wx.Button(self, wx.ID_CANCEL, u"")
		btnBack.Hide()
		btnBack.Bind(wx.EVT_BUTTON, self.onBtnBack)

		# 스페이스 버튼 숨김
		idSpace = wx.NewId()
		btnSpace = wx.Button(self, idSpace, u"")
		btnSpace.Hide()
		btnSpace.Bind(wx.EVT_BUTTON, self.onBtnSpace)

		accelTable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_CANCEL), (wx.ACCEL_ALT, wx.WXK_LEFT, wx.ID_CANCEL), (wx.ACCEL_NORMAL, wx.WXK_SPACE, idSpace)])
		self.SetAcceleratorTable(accelTable)

		self.select()


	def onBtnBack(self, e):
		global mainPanel, subPanel, studyPanel
		self.endStudy()
		try:
			play("out.wav")
			subPanel.Show()
			subPanel.SetFocus()
		except:
			mainPanel.Show()
			mainPanel.SetFocus()
			subPanel = None
		finally:
			studyPanel = None
			self.Destroy()


	def endStudy(self):
		elapsedTime = int(time.time()) - self.startTime
		sec = elapsedTime % 60
		min = int(elapsedTime / 60)
		count = self.quezCount - 1
		ratio = 1.0 * elapsedTime / count if count else 0
		msg = u"연습 횟수 : %s\n연습 시간: %s분 %s초\n1회 당 %.2f초" % (count, min, sec, ratio)
		wx.MessageBox(msg, u"학습 결과", parent=self, style=wx.OK)


	def select(self):
		n = int(random.random()*100000000) % 3
		l = self.extra if n == 0 and self.extra else self.keys
		index = int(random.random()*100000000) % len(l)
		self.keyText = l[index]
		desc = u"%s:\n%s" % (self.keyText, self.descriptions[self.keyText]) if self.descriptions and self.descriptions.get(self.keyText, None) else self.keyText
		self.guide.SetLabel(desc)
		self.quezCount += 1
		if self.quezCount == 101:
			self.onBtnBack(None)
			return
		self.speakKeyText()



	def onBtnSpace(self, e):
		ans = self.textCtrl.GetValue()
		self.textCtrl.Clear()

		if ans and ans == self.keyText:
			play("right.wav")
			self.select()
		elif ans and ans != self.keyText:
			play("error.wav")
			self.speakKeyText()
		else:
			self.speakKeyText()


	def speakKeyText(self):
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakText, self.keyText)
		if self.keyText in self.descriptions:
			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, self.descriptions[self.keyText])
		else:
			locale = speech.getCurrentLanguage()
			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakSpelling, self.keyText, locale, False)
