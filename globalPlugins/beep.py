import globalPluginHandler
import tones
from scriptHandler import script

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(gesture="kb:control+k")
	def script_beepBeep(self, gesture):
		tones.beep(1500, 2000)

