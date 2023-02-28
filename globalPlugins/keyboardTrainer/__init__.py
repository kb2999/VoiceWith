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


# ��������
mainTitle = u"���̽����� Ÿ�� ����"
trainingDialog = None
mainPanel = None
subPanel = None
studyPanel = None
descriptions = {
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"������ ������ ��������.",
	u"��": u"������ ������ ��������.",
	u"��": u"������ ������ ��������.",
	u"��": u"������ ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"������ ������ ����ƮŰ�� �����鼭 �޼� ������ ��������.",
	u"��": u"������ ������ ����ƮŰ�� �����鼭 �޼� ������ ��������.",
	u"��": u"������ ������ ����ƮŰ�� �����鼭 �޼� ������ ��������.",
	u"��": u"������ ������ ����ƮŰ�� �����鼭 �޼� ������ ��������.",
	u"��": u"������ ������ ����ƮŰ�� �����鼭 �޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"�޼� ������ ��������.",
	u"��": u"������ ������ ��������.", 
	u"��": u"������ ������ ��������.",
	u"��": u"������ ������ ��������.",
	u"��": u"�� �� ������ ������ ��������.",
	u"��": u"�� �� ������ ������ ��������.",
	u"��": u"�� �� �޼� ������ ����ƮŰ�� �����鼭 ������ ������ ��������.",
	u"��": u"�� �� �޼� ������ ����ƮŰ�� �����鼭 ������ ������ ��������.", 
	u"��": u"������ ������ ��������.",
	u"��": u"������ ������ ��������.",
	u"��": u"������ ������ ��������.",

	"a": u"�޼� ������ ��������.", 
	"b": u"�޼� ������ ��������.", 
	"c": u"�޼� ������ ��������.", 
	"d": u"�޼� ������ ��������.", 
	"e": u"�޼� ������ ��������.", 
	"f": u"�޼� ������ ��������.", 
	"g": u"�޼� ������ ��������.", 
	"h": u"������ ������ ��������.", 
	"i": u"������ ������ ��������.", 
	"j": u"������ ������ ��������.", 
	"k": u"������ ������ ��������.", 
	"l": u"������ ������ ��������.", 
	"m": u"������ ������ ��������.", 
	"n": u"������ ������ ��������.", 
	"o": u"������ ������ ��������.", 
	"p": u"������ ������ ��������.", 
	"q": u"�޼� ������ ��������.", 
	"r": u"�޼� ������ ��������.", 
	"s": u"�޼� ������ ��������.", 
	"t": u"�޼� ������ ��������.", 
	"u": u"������ ������ ��������.", 
	"v": u"�޼� ������ ��������.", 
	"w": u"�޼� ������ ��������.", 
	"x": u"�޼� ������ ��������.", 
	"y": u"������ ������ ��������.", 
	"z": u"�޼� ������ ��������.", 

	"1": u"�޼� ������ ��������.", 
	"2": u"�޼� ������ ��������.", 
	"3": u"�޼� ������ ��������.", 
	"4": u"�޼� ������ ��������.", 
	"5": u"�޼� ������ ��������.", 
	"6": u"�޼� ������ ��������.", 
	"7": u"������ ������ ��������.", 
	"8": u"������ ������ ��������.", 
	"9": u"������ ������ ��������.", 
	"0": u"������ ������ ��������.", 

	"!": u"����ǥ ����ƮŰ�� ���� 1�� ���ÿ� ��������.", 
	"@": u"����� ����ƮŰ�� ���� 2�� ���ÿ� ��������.", 
	"#": u"�� ����ƮŰ�� ���� 3�� ���ÿ� ��������.", 
	"$": u"�޷� ����ƮŰ�� ���� 4�� ���ÿ� ��������.", 
	"%": u"�ۼ�Ʈ ����ƮŰ�� ���� 5�� ���ÿ� ��������.", 
	"^": u"ĳ�� ����ƮŰ�� ���� 6�� ���ÿ� ��������.", 
	"&": u"���ۼ��� ����ƮŰ�� ���� 7�� ���ÿ� ��������.", 
	"*": u"��Ÿ ����ƮŰ�� ���� 8�� ���ÿ� ��������.", 
	"(": u"��ȣ ���� ����ƮŰ�� ���� 9�� ���ÿ� ��������.", 
	")": u"��ȣ �ݰ� ����ƮŰ�� ���� 0�� ���ÿ� ��������.", 

	"`": u"�׷��̺� ���� 1 ���ʿ� �ֽ��ϴ�. �޼� ������ ��������.",
	"-": u"�뽬 ���� 0 �����ʿ� �ֽ��ϴ�. ������ ������ ��������.",
	"=": u"���� ���� 0 ������ �ι�°�� �ֽ��ϴ�. ������ ������ ��������.",
	"[": u"���ȣ ���� ���� p Ű�� �����ʿ� �ֽ��ϴ�. ������ ������ ��������.",
	"]": u"���ȣ �ݰ� ���� p Ű ������ �ι�°�� �ֽ��ϴ�. ������ ������ ��������.",
	"\\": u"�� ������ ���� 0 ������ ����°�� �ְų� ���� p Ű�� ������ ����°�� �ֽ��ϴ�. ������ ������ ��������.",
	";": u"�����ݷ� ���� l Ű �����ʿ� �ֽ��ϴ�. ������ ������ ��������.",
	"'": u"���۽�Ʈ���� ���� l Ű�� ������ �ι�°�� �ֽ��ϴ�. ������ ������ ��������.",
	",": u"�޸� ���� m �����ʿ� �ֽ��ϴ�. ������ ������ ��������.",
	".": u"�� ���� m Ű�� ������ �ι�°�� �ֽ��ϴ�. ������ ������ ��������.",
	"/": u"������ ���� m Ű�� ������ ����°�� �ֽ��ϴ�. ������ ������ ��������.",

	"~": u"���� ����Ʈ�� �׷��̺긦 �Բ� ��������.",
	"_": u"����� ����Ʈ�� �뽬�� �Բ� ��������.",
	"+": u"�÷��� ����Ʈ�� ������ �Բ� ��������.",
	"{": u"�߰�ȣ ���� ����Ʈ�� ���ȣ ���� �Բ� ��������.",
	"}": u"�߰�ȣ �ݰ� ����Ʈ�� ���ȣ �ݰ� �Բ� ��������.",
	"|": u"��Ƽ�ù� ����Ʈ�� �齽������ �Բ� ��������.",
	":": u"�ݷ� ����Ʈ�� �����ݷ��� �Բ� ��������.",
	'"': u"�����̼� ����Ʈ�� ���۽�Ʈ���Ǹ� �Բ� ��������.",
	"<": u"������ ����Ʈ�� �޸��� �Բ� ��������.",
	">": u"�׷����ʹ� ����Ʈ�� ���� �Բ� ��������.",
	"?": u"����ǥ ����Ʈ�� �������� �Բ� ��������.",

	wx.WXK_RETURN: u"����", 
	wx.WXK_SPACE: u"�����̽�", 
	wx.WXK_BACK: u"�� �����̽�", 
	wx.WXK_CONTROL: u"��Ʈ��", 
	wx.WXK_ALT: u"��Ʈ", 
	wx.WXK_SHIFT: u"����Ʈ", 
	wx.WXK_WINDOWS_LEFT: u"���� ������", 
	wx.WXK_PAGEUP: u"������ ��", 
	wx.WXK_PAGEDOWN: u"������ �ٿ�", 
	wx.WXK_HOME: u"Ȩ", 
	wx.WXK_END: u"����", 
	wx.WXK_INSERT: u"�μ�Ʈ", 
	wx.WXK_DELETE: u"����Ʈ", 
	wx.WXK_TAB: u"��", 
	wx.WXK_CAPITAL: u"ĸ�� ��", 
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
	"koreanBasic": [u"��", u"��", u"��", u"��", u"��", u"��", u"��", u"��", u"��"],
	"koreanLeftUpper": [u"��", u"��", u"��", u"��", u"��", u"��", u"��", u"��", u"��", u"��"], 
	"koreanLeftLower": [u"��", u"��", u"��", u"��"], 
	"koreanRightUpper": [u"��", u"��", u"��", u"��", u"��", u"��", u"��"], 
	"koreanRightLower": [u"��", u"��", u"��"], 

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
	"koreanBasic": [u"�̸�", u"�ϸ��", u"��Ӵ�", u"�ҸӴ�", u"���Ӹ�", u"����", u"����", u"ȣ��", u"�̳���", u"����", u"���", u"���", u"��", u"�ո�", u"����", u"����", u"����", u"����", u"����", u"��ӳ�", u"�󸶳�", u"����", u"�ѷ�", u"����", u"ȣ����", u"�㸮"], 
	"koreanLeftUpper": [u"����", u"�ƹ���", u"����", u"���", u"������", u"����", u"����", u"����", u"����", u"����", u"����", u"���", u"����", u"�ݴ�", u"�ݵ�", u"���", u"���", u"�ݴް�", u"����", u"�˻�", u"����", u"�Ѱ�", u"����", u"���ڱ�", u"�۾�", u"�մ�", u"����", u"����", u"���̴�", u"����", u"���", u"���", u"����", u"ȭ���", u"������", u"������", u"��ȸ��", u"ȯ��", u"��ȭ��", u"��ȸ", u"�ƺ�", u"�ǻǻ�", u"�ͳ���", u"����", u"�߻�", u"�о��о�", u"��½��½", u"¥���", u"¯��ġ", u"�˵��", u"�ʶ���", u"����", u"��������", u"����", u"����", u"����", u"����", u"�ļ�", u"������", u"��α�", u"�����", u"�����", u"�ֹֽ�", u"�ž�", u"����"], 
	"koreanLeftLower": [u"������", u"�ݶ�", u"Ŀ��", u"ĲĲ", u"ųų", u"�䳢", u"����", u"�н�", u"Ÿ��", u"Ƽ��"], 
	"koreanRightUpper": [u"����", u"�丮", u"ȿ��", u"ǥ����", u"��⵵", u"��ȭ", u"����", u"����", u"���", u"�Ѿ�", u"���б�", u"�����", u"���ʺ�", u"����", u"��ü", u"�Ը���", u"����", u"���", u"����"], 
	"koreanRightLower": [u"����", u"����", u"����", u"����", u"�Ҳ�", u"�ٳѱ�", u"�Ѹ�", u"����", u"����", u"����", u"���", u"���", u"���ο�", u"����", u"�Ʒü�", u"���ǽ�", u"����", u"���", u"ǳ��", u"ġ��", u"Ʃ��", u"����", u"�ֵ���", u"�巹��", u"�ǻ�", u"��ġ", u"�ͽ�", u"����", u"�䱸��Ʈ", u"", u"���", u"������", u"��ũ", u"Ʈ��", u"������", u"Ʈ����"],
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
		item = gui.mainFrame.sysTrayIcon.menu.Append(-1, u"Ÿ�� ����\tCtrl+&J")
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
		btnKoreanTraining = MenuButton(self, u"  �ѱ� ����", wx.Point(10, 10), self.onBtnKoreanTraining)
		btnEnglishTraining = MenuButton(self, u"  ���� ����", wx.Point(420, 10),  self.onBtnEnglishTraining)

		btnNumberSignTraining = MenuButton(self, u"  ���� �� ��ȣ ����", wx.Point(10, 100), self.onBtnNumberSignTraining)
		btnNotepad = MenuButton(self, u"  ������", wx.Point(420, 100), self.onBtnNotepad)

		self.btnPopupByGraave = wx.ToggleButton(self, -1, u"  �׷��̺긦 ������ �� �� ������ Ÿ�� ������ ����˴ϴ�.", (10, 190), (810, 100), style=wx.ALIGN_LEFT)
		self.btnPopupByGraave.SetFont(wx.Font(24, wx.MODERN, wx.NORMAL, wx.BOLD))
		if not "voiceWith" in config.conf:
			config.conf["voiceWith"] = {}
		if not "popupKeyboardTrainingByGraave" in config.conf["voiceWith"]:
			config.conf["voiceWith"]["popupKeyboardTrainingByGraave"] = "True"
		self.btnPopupByGraave.SetValue(eval(config.conf["voiceWith"]["popupKeyboardTrainingByGraave"]))
		self.btnPopupByGraave.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleButton)

		btnExit = MenuButton(self, u"  ����(&X)", wx.Point(10, 280), self.onBtnExit)



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

		# �ڷ� ���� ���� ��ư
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
		self.textCtrl = wx.TextCtrl(self, -1, '', (10, 10), (830, 530), style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB, name=u"������")
		self.textCtrl.SetBackgroundColour("#dddddd")

class KoreanPanel(SubPanel):
	def onInit(self):
		btnKRBasic = MenuButton(self, u"  �ѱ� �⺻ �ڸ�", wx.Point(10, 10), self.onBtnBasic)
		btnKRBasicWord = MenuButton(self, u"  �ѱ� �⺻ �ڸ� �ܾ�", wx.Point(420, 10), self.onBtnBasicWord)

		btnKRLeftUpper = MenuButton(self, u"  �ѱ� �޼� ����", wx.Point(10, 100), self.onBtnLeftUpper)
		btnKRLeftUpperWord = MenuButton(self, u"  �ѱ� �޼� ���� �ܾ�", wx.Point(420, 100), self.onBtnLeftUpperWord)

		btnKRLeftLower = MenuButton(self, u"  �ѱ� �޼� �Ʒ���", wx.Point(10, 190), self.onBtnLeftLower)
		btnKRLeftLowerWord = MenuButton(self, u"  �ѱ� �޼� �Ʒ��� �ܾ�", wx.Point(420, 190), self.onBtnLeftLowerWord)

		btnKRRightUpper = MenuButton(self, u"  �ѱ� ������ ����", wx.Point(10, 280), self.onBtnRightUpper)
		btnKRRightUpperWord = MenuButton(self, u"  �ѱ� ������ ���� �ܾ�", wx.Point(420, 280), self.onBtnRightUpperWord)

		btnKRRightLower = MenuButton(self, u"  �ѱ� ������ �Ʒ���", wx.Point(10, 370), self.onBtnRightLower)
		btnKRRightLowerWord = MenuButton(self, u"  �ѱ� ������ �Ʒ��� �ܾ�", wx.Point(420, 370), self.onBtnRightLowerWord)

		btnKRAllWord = MenuButton(self, u"  �ѱ� ��ü �ܾ�", wx.Point(10, 460), self.onBtnAllWord)

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
		btnEngBasic = MenuButton(self, u"  ���� �⺻ �ڸ�", wx.Point(10, 10), self.onBtnEngBasic)
		btnEngLeftUpper = MenuButton(self, u"  ���� �޼� ����", wx.Point(420, 10), self.onBtnEngLeftUpper)

		btnEngLeftLower = MenuButton(self, u"  ���� �޼� �Ʒ���", wx.Point(10, 100), self.onBtnEngLeftLower)
		btnEngRightUpper = MenuButton(self, u"  ���� ������ ����", wx.Point(420, 100), self.onBtnEngRightUpper)

		btnEngRightLower = MenuButton(self, u"  ���� ������ �Ʒ���", wx.Point(10, 190), self.onBtnEngRightLower)
		btnEngAllWord = MenuButton(self, u"  ���� �ܾ� ����", wx.Point(420, 190), self.onBtnEngAllWord)

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
		btnNumber = MenuButton(self, u"  ����", wx.Point(10, 10), self.onBtnNumber)
		btnShiftNumber = MenuButton(self, u"  ����Ʈ ���� ���� ��ȣ", wx.Point(420, 10), self.onBtnShiftNumber)

		btnOtherSign = MenuButton(self, u"  ��Ÿ ��ȣ", wx.Point(10, 100), self.onBtnOtherSign)
		btnShiftOtherSign = MenuButton(self, u"  ����Ʈ ���� ��Ÿ ��ȣ", wx.Point(420, 100), self.onBtnShiftOtherSign)

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

		# �ڷ� ���� ���� ��ư
		btnBack = wx.Button(self, wx.ID_CANCEL, u"")
		btnBack.Hide()
		btnBack.Bind(wx.EVT_BUTTON, self.onBtnBack)

		# �����̽� ��ư ����
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
		msg = u"���� Ƚ�� : %s\n���� �ð�: %s�� %s��\n1ȸ �� %.2f��" % (count, min, sec, ratio)
		wx.MessageBox(msg, u"�н� ���", parent=self, style=wx.OK)


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
