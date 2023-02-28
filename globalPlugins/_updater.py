import gui
import time
import os
import subprocess
from threading import Thread
import _requests
import wx
from _html.parser import HTMLParser
import globalPluginHandler
import tones
import _utils
from addonHandler import getAvailableAddons
import tempfile


class Parser(HTMLParser):
	result = None
	def handle_starttag(self, tag, attrs):
		if not self.result and tag == 'a':
			hrefList = [v for k, v in attrs if k == 'href' and v.startswith('/kb2999/VoiceWith/releases/tag/v')]
			if hrefList:
				self.result = hrefList[0]



class Updater(Thread):
	def __init__(self, isAuto):
		super().__init__()
		self.isAuto = isAuto
		self.run()

	def run(self):
		self.vwConfig = _utils.loadVWConfig()
		# 최초 실행이면 올드 타임을 이틀 전으로 만든다.
		curTime = time.time()
		oldTime = self.vwConfig.get('updateCheckTime', False)
		if not oldTime:
			oldTime = curTime - 86400*2
			###oldTime = 0
			self.vwConfig['updateCheckTime'] = oldTime
			_utils.saveVWConfig(self.vwConfig)

		if self.isAuto:
					# 자동 업데이트 체크가 되어 있으면, 3일에 한번만 업데이트 검사함.
			if self.vwConfig.get('autoUpdateCheck', True):
				if curTime - oldTime < (86400*3):
					return

		# 수동이거나 72시간이 지난 자동 업데이트의 경우
		r = _requests.get('https://github.com/kb2999/VoiceWith/releases/latest', timeout=10)
		if r is None or r.status_code//100 != 2:
			if not self.isAuto:
				gui.messageBox('업데이트 저장소에 접속할 수 없습니다.', '오류', parent=gui.mainFrame)
			return

		html = r.text
		parser = Parser()
		parser.feed(html)
		href = parser.result
		if href is None:
			if not self.isAuto:
				gui.messageBox('저장소에 업데이트 파일이 없습니다.', '알림', parent=gui.mainFrame)
			return

		# 버전 비교
		index = href.rfind('/')
		newVersion = float(href[index+2:])
		try:
			oldVersion = float([obj for obj in getAvailableAddons() if obj.name == 'VoiceWith'][0].version)
		except:
			if not self.isAuto:
				gui.messageBox('설치되어 있는 보이스위드 버전을 알 수 없습니다.', '오류', parent=gui.mainFrame)
			return

		# 업데이트 체크를 했으므로 업데이트 체크 타임을 현재 시점으로 옮긴다. 그러면 24시간 내에는 다시 물어 보지 않는다.
		self.vwConfig['updateCheckTime'] = curTime
		_utils.saveVWConfig(self.vwConfig)

		if newVersion <= oldVersion:
			if not self.isAuto:
				gui.messageBox(f'설치되어 있는 보이스위드는 최신 버전입니다.\n현재 버젼: {oldVersion}', '알림', parent=gui.mainFrame)
			return

		# 업데이트 묻기
		if gui.messageBox(f'새로운 보이스위드 업데이트가 발견되었습니다. 업데이트하시겠습니까?\n새로운 버젼: {newVersion}', '질문', parent=gui.mainFrame, style=wx.YES|wx.NO) == wx.NO:
			return

		# 파일 다운로드 링크 문자열 조립
		fileName = f'VoiceWith_v{newVersion}.nvda-addon'
		url = f'https://github.com/kb2999/VoiceWith/releases/download/v{newVersion}/{fileName}'
		filePath = os.path.join(os.environ['temp'], fileName)

		r = _requests.get(url, stream=True)
		if r is None or r.status_code//100 != 2:
			gui.messageBox('업데이트 파일에 접속할 수 없습니다.', '오류', parent=gui.mainFrame)
			return
		readSize = 0
		totalSize = int(r.headers.get('Content-Length', 0))
		if totalSize == 0:
			gui.messageBox('업데이트 파일 크기가 정확하지 않습니다.', '오류', parent=gui.mainFrame)
			return

		# 이미 다운로드 완료된 파일이 존재한다면 곧바로 설치함.
		if os.path.exists(filePath) and os.path.getsize(filePath) == totalSize:
			try:
				subprocess.call(f'nvda_slave.exe addons_installAddonPackage "{filePath}"')
			except:
				gui.messageBox('추가 기능 설치에 실패했습니다. 다시 다운로드 받아 보세요.', '오류', parent=gui.mainFrame)
			finally:
				return

		# 다운로드 시작
		with open(filePath, 'wb') as f:
			for chunk in r.iter_content(1024*1024*4):
				f.write(chunk)
				readSize += len(chunk)
				percent = readSize * 100 // totalSize
				tones.beep(percent*10 + 500, 100)

		# 최종 다운로드 파일 크기를 검사한 후 설치 시작
		try:
			subprocess.call(f'nvda_slave.exe addons_installAddonPackage "{filePath}"')
		except:
			gui.messageBox('추가 기능 설치에 실패했습니다. 다시 다운로드 받아 보세요.', '오류', parent=gui.mainFrame)
		finally:
			return
