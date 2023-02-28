# coding: utf-8

from scriptHandler import script
from logHandler import *
from controlTypes import *
from NVDAObjects.UIA import UIA

import api
import appModuleHandler
import globalCommands
import queueHandler
import threading
import time
import ui
import winsound


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if hasattr(obj, 'name') and isinstance(obj.name, str) and obj.name in ('친구 목록', '채팅') and obj.role == ROLE_LIST:
			clsList.insert(0, MainList)
		elif obj.role == ROLE_WINDOW and hasattr(obj, 'name') and isinstance(obj.name, str) and obj.name.startswith('ChatDlg'):
			clsList.insert(0, ChatDialog)
		elif obj.role == ROLE_LIST and obj.parent.name.startswith('ChatDlg '):
			clsList.insert(0, ChatList)

class MainList(UIA):

	def script_leftRight(self, gesture):
		winsound.Beep(1000, 100)

	def script_upDown(self, gesture):
		gesture.send()
		api.processPendingEvents(False)
		itemList = [child.name for child in self.children if STATE_SELECTED in child.states and getattr(child, 'name', '')]
		if not itemList:
			itemList = ['선택 항목 없음']
		ui.message(itemList[0])




	__gestures = {"kb:leftArrow": "leftRight", 
		"kb:rightArrow": "leftRight",
		"kb:upArrow": "upDown", 
		"kb:downArrow": "upDown",
		}


class ChatDialog(UIA):
	def event_foreground(self):
		th = threading.Thread(target=CheckNewMessage, args=(self,))
		th.start()

	def _get_chatList(self):
		if not getattr(self, '_chatList', None):
			itemList = [child for child in self.recursiveDescendants if child.role == ROLE_LIST] 
			self._chatList = itemList[0] if itemList else None
		return self._chatList

class CheckNewMessage(threading.Thread):
	def __init__(self, parent):
		itemList = [child for child in parent.recursiveDescendants if child.role == ROLE_LIST]
		if not itemList:
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, '채팅 내용 목록을 찾지 못했습니다.')
			return

		chatList = itemList[0]
		chatCount = len(chatList.children)

		while api.getForegroundObject() is parent:
			count = len(chatList.children) 
			if count > chatCount:
				chatCount = count
				queueHandler.queueFunction(queueHandler.eventQueue, ui.message, chatList.children[-1].name)
			time.sleep(0.1)


class ChatList(UIA):

	index = 1

	def event_gainFocus(self):
		super(ChatList, self).event_gainFocus()
		if not self.children:
			queueHandler.queueFunction(queueHandler.eventQueue, ui.message, '채팅 내용이 없습니다.')
			return
		api.setNavigatorObject(self.children[-1])
		obj = api.getNavigatorObject()
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, obj.name)


	def script_move(self, gesture):
		count = len(self.children)
		key = gesture.mainKeyName
		if key == "downArrow":
			self.index = self.index - 1 if self.index > 1 else 1
		elif key == "upArrow":
			self.index = self.index + 1 if self.index < count else count
		elif key == "home":
			self.index = count
		elif key == "end":
			self.index = 1
		elif key == "pageUp":
			self.index = self.index + 5 if self.index + 5 <= count else count
		elif key == "pageDown":
			self.index = self.index - 5 if self.index - 5 >= 1 else 1

		api.setNavigatorObject(self.children[self.index*-1])
		obj = api.getNavigatorObject()
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, obj.name)


	__gestures = {"kb:upArrow": "move",
		"kb:downArrow": "move",
		"kb:home": "move",
		"kb:end": "move",
		"kb:pageUp": "move",
		"kb:pageDown": "move",
		}
