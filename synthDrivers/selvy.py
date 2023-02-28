# -*- coding: UTF-8 -*-
#synthDrivers/selvy.py

import os
import sys
from collections import OrderedDict
from . import _selvy
import languageHandler
from synthDriverHandler import SynthDriver,VoiceInfo,synthIndexReached, synthDoneSpeaking #,BooleanSynthSetting
import speech
from logHandler import log
#import traceback


class SynthDriver(SynthDriver):
	name = "selvy"
	description = "Selvy TTS"
	
	# 마침표로 끝나는 문장을 플레이 할 경우 엔진에서 마지막 mark 이벤트를 보내지 않음
	lastIndexCommand = -1
	supportedSettings=(
		#SynthDriver.VoiceSetting(),
		#SynthDriver.VariantSetting(),
		SynthDriver.RateSetting(),
		#SynthDriver.RateBoostSetting(),
		SynthDriver.PitchSetting(),
		#SynthDriver.InflectionSetting(),
		SynthDriver.VolumeSetting(),
	)
	supportedCommands = {
		speech.commands.IndexCommand,
		speech.commands.CharacterModeCommand,
		speech.commands.LangChangeCommand,
		speech.commands.BreakCommand,
		speech.commands.PitchCommand,
		speech.commands.RateCommand,
		speech.commands.VolumeCommand,
		speech.commands.PhonemeCommand,
	}
	supportedNotifications = {synthIndexReached, synthDoneSpeaking}

	@classmethod
	def check(cls):
		return True

	def __init__(self):


		_selvy.initialize(self._onIndexReached)
		log.info("Using Selvy TTS version %s" % _selvy.info())
		lang=languageHandler.getLanguage()
		_selvy.setVoiceByLanguage(lang)
		self._language=lang
		self._variantDict=_selvy.getVariantDict()
		#self.variant="max"
		self.rate=30
		self.pitch=50
		self.volume=50
		#self.inflection=75

	def _get_language(self):
		return self._language

	PROSODY_ATTRS = {
		speech.commands.PitchCommand: "pitch",
		speech.commands.VolumeCommand: "volume",
		speech.commands.RateCommand: "rate",
	}

	IPA_TO_ESPEAK = {
		u"θ": u"T",
		u"s": u"s",
		u"ˈ": u"'",
	}

	def _processText(self, text):
		#text = str(text)
		# We need to make several replacements.
		return text.translate({
			0x1: None, # used for embedded commands
			0x3C: u"&lt;", # <: because of XML
			0x3E: u"&gt;", # >: because of XML
			0x5B: u" [", # [: [[ indicates phonemes
		})


	def speak(self, speechSequence):
#		log.info("[selvy] speak %s" % speechSequence)
#		log.info('\n'.join(str(item) for item in speechSequence))
		
#		callstack = ""
#		for line in traceback.format_stack():
#			callstack = callstack + line.strip() + "\n"
#		log.debugWarning(callstack)
		#log.info(callstack)
		
		
		defaultLanguage=self._language
		textList=[]
		langChanged=False
		prosody={}
		
		pitchCmd=False
		volumeCmd=False
		speedCmd=False
		
		# We output malformed XML, as we might close an outer tag after opening an inner one; e.g.
		# <voice><prosody></voice></prosody>.
		# However, eSpeak doesn't seem to mind.
		for item in speechSequence:
			#log.debugWarning("item:%s" % item)
			#log.info("item:%s" % item)
			if isinstance(item, str):
				textList.append(self._processText(item))
			elif isinstance(item, bytes):
				item = item.decode('mbcs', 'ignore')
				textList.append(self._processText(item))
			elif isinstance(item,speech.commands.IndexCommand):
				global lastIndexCommand
				lastIndexCommand = item.index
				textList.append("<mark=\"%d\" />"%item.index)
				#log.debugWarning("Unsupported speech command: %s"%item)
			elif isinstance(item,speech.commands.CharacterModeCommand):
				#textList.append("<say-as interpret-as=\"characters\">" if item.state else "</say-as>")
				log.debugWarning("Unsupported speech command: %s"%item)
			elif isinstance(item,speech.commands.LangChangeCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			elif isinstance(item,speech.commands.BreakCommand):
				#textList.append('<break time="%dms" />' % item.time)
				textList.append('<pause="%dms">' % item.time)
			elif isinstance(item,speech.commands.PitchCommand):
				if pitchCmd:
					textList.append("</pitch>")
				if item.multiplier == 1:
					pitchCmd = False
				else:
					pitchPercent = self._get_pitch() * item.multiplier
					if pitchPercent > 100:
						pitchPercent = 100
						
					pitchVal = self._percentToParam(pitchPercent, _selvy.minPitch, _selvy.maxPitch)
					textList.append('<pitch="%d">' % pitchVal)
					pitchCmd = True
			elif isinstance(item,speech.commands.VolumeCommand):
				if volumeCmd:
					textList.append("</volume>")
				if item.multiplier == 1:
					volumeCmd = False
				else:
					volumePercent = self._get_volume() * item.multiplier
					if volumePercent > 100:
						volumePercent = 100
						
					volumeVal = self._percentToParam(volumePercent, _selvy.minVolume, _selvy.maxVolume)
					textList.append('<volume="%d">' % volumeVal)
					volumeCmd = True
			elif isinstance(item,speech.commands.RateCommand):
				if speedCmd:
					textList.append("</speed>")
				if item.multiplier == 1:
					speedCmd = False
				else:
					speedPercent = self._get_rate() * item.multiplier
					if speedPercent > 100:
						speedPercent = 100
						
					speedVal = self._percentToParam(speedPercent, _selvy.minRate, _selvy.maxRate)
					textList.append('<speed="%d">' % speedVal)
					speedCmd = True
			elif isinstance(item,speech.commands.PhonemeCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			elif isinstance(item,speech.commands.SpeechCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			else:
				log.error("Unknown speech: %s"%item)
		# Close any open tags.
		if langChanged:
			textList.append("</voice>")
		if prosody:
			textList.append("</prosody>")
			
		if pitchCmd:
			textList.append("</pitch>")
		if volumeCmd:
			textList.append("</volume>")
		if speedCmd:
			textList.append("</speed>")
		
		text=u"".join(textList)
		_selvy.speak(text)
		#_selvy.speak(u'테스트<pause="3000">음성입니다.')
	

	def cancel(self):
		global lastIndexCommand
		lastIndexCommand = -1
		
#		callstack = ""
#		for line in traceback.format_stack():
#			callstack = callstack + line.strip() + "\n"
			
#		log.debugWarning(callstack)
		
		_selvy.stop()

	def pause(self,switch):
		_selvy.pause(switch)


	# default 100, 50~200
	def _get_rate(self):
		val=_selvy.getRate()
		return self._paramToPercent(val,_selvy.minRate,_selvy.maxRate)

	# default 100, 50~200
	def _set_rate(self,rate):
		val=self._percentToParam(rate, _selvy.minRate, _selvy.maxRate)
		_selvy.setRate(val)

	# default 100, 80~120
	def _get_pitch(self):
		val=_selvy.getPitch()
		return self._paramToPercent(val,_selvy.minPitch,_selvy.maxPitch)

	# default 100, 80~120
	def _set_pitch(self,pitch):
		val=self._percentToParam(pitch, _selvy.minPitch, _selvy.maxPitch)
		_selvy.setPitch(val)

	# default 100, 0~200
	def _get_volume(self):
		val=_selvy.getVolume()
		return self._paramToPercent(val,_selvy.minVolume, _selvy.maxVolume)

	# default 100, 0~200
	def _set_volume(self,volume):
		val=self._percentToParam(volume, _selvy.minVolume, _selvy.maxVolume)
		_selvy.setVolume(val)

	def _getAvailableVoices(self):

		return _selvy.getVoiceList()

	def _get_voice(self):
		curVoice=getattr(self,'_voice',None)
		if curVoice: return curVoice
		curVoice = _selvy.getCurrentVoice()
		if not curVoice:
			return ""
		# #5783: For backwards compatibility, voice identifies should always be lowercase
		return curVoice.identifier.split('+')[0].lower()

	def _set_voice(self, identifier):
		if not identifier:
			return
		# #5783: For backwards compatibility, voice identifies should always be lowercase
		identifier=identifier.lower()
		if "\\" in identifier:
			identifier=os.path.basename(identifier)
		self._voice=identifier
		try:
			_selvy.setVoiceAndVariant(voice=identifier,variant=self._variant)
		except:
			self._voice=None
			raise
		self._language=super(SynthDriver,self).language

	def _onIndexReached(self, index):		
		global lastIndexCommand
		
		log.debugWarning("[selvy] _onIndexReached index:%s, lastIndexCommand:%s" % (index, lastIndexCommand))
		
		if lastIndexCommand is not None and lastIndexCommand == index:
			lastIndexCommand = -1
			
		if index is not None:
			#log.debugWarning("[selvy] _onIndexReached calling synthIndexReached index:%s" % index)
			synthIndexReached.notify(synth=self, index=index)
		else:
			if lastIndexCommand >= 0:
				index = lastIndexCommand
				lastIndexCommand = -1
				synthIndexReached.notify(synth=self, index=index)
				
			synthDoneSpeaking.notify(synth=self)

	def terminate(self):
		_selvy.terminate()

	def _get_variant(self):
		return self._variant

	def _set_variant(self,val):
		if self._variantDict is not None:
			self._variant = val if val in self._variantDict else "max"
			_selvy.setVoiceAndVariant(variant=self._variant)
		else:
			self._variant = val

	def _getAvailableVariants(self):
		return OrderedDict((ID,VoiceInfo(ID, name)) for ID, name in self._variantDict.iteritems())
