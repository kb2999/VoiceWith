# NVDA Add-on: Speech Review
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# See the file LICENSE for more details.
# _historyOn:   True 출력내용 대화상자가 팝업된 경우


from . import _utils
import api
from collections import deque
import wx
from globalCommands import SCRCAT_SPEECH
import globalPluginHandler
from queueHandler import eventQueue, queueFunction
import speech
import speechViewer
from scriptHandler import script



class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		vwConfig = _utils.loadVWConfig()
		maxLength = vwConfig.get('speechReviewerCount', 100)
		self._history=deque(maxlen=maxLength)
		self._reviewObj = None
		self.oldSpeak = speech.speech.speak
		speech.speech.speak = self.mySpeak

	def append_to_history(self, text):
		self._history.append(text)

	def mySpeak(self, sequence, *args, **kwargs):
		self.oldSpeak(sequence, *args, **kwargs)
		if self._reviewObj:
			return
		text = speechViewer.SPEECH_ITEM_SEPARATOR.join([x for x in sequence if isinstance(x, str)])
		if text.strip():
			queueFunction(eventQueue, self.append_to_history, text)


	@script(gesture='kb:f12', description='음성 출력 내용을 확인합니다. 한번 더 누르면 출력 내용 대화상자가 닫힙니다.', category=SCRCAT_SPEECH)
	def script_viewReview(self, gesture):
		if self._reviewObj:
			self._reviewObj.onClose(None)
		else:
			self._reviewObj = ReviewDialog(self)


class ReviewDialog(wx.Dialog):
	def __init__(self, plugin):
		super().__init__(None, -1, '출력 내용', wx.DefaultPosition, (500, 500), name='speechReviewer')
		self.plugin = plugin
		self.Bind(wx.EVT_CLOSE, self.onClose)
		text = '\n'.join(self.plugin._history)
		self.tc = wx.TextCtrl(self, -1, text, (10, 10), (480, 480), style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.tc.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.Show()
		self.Raise()
		self.tc.SetFocus()
		self.tc.SetInsertionPointEnd()
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.onTimer, self.timer)
		self.timer.Start(500)
		self.tcWindowHandle  = self.tc.GetHandle()


	def onTimer(self, e):
		if self.tcWindowHandle != api.getFocusObject().windowHandle:
			self.onClose(e)


	def onClose(self, e):
		self.plugin._reviewObj = None
		self.Destroy()

	def onKeyDown(self, e):
		if e.GetKeyCode() == wx.WXK_ESCAPE:
			self.onClose(e)
		else:
			e.Skip()

