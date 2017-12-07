# Mozilla Scripts version 1.4 (Dec-2017)
# Shared code for both appmodules
# Author Javi Dominguez <fjavids@gmail.com>
# License GNU GPL

from datetime import datetime, timedelta
from threading import Timer
from tones import beep
import speech
import controlTypes
import api
import ui
import addonHandler

addonHandler.initTranslation()

def focusAlertPopup(alertPopup, SETFOCUS = True):
	if alertPopup.role != controlTypes.ROLE_ALERT:
		return False
	obj = alertPopup.firstChild
	while obj and not obj.isFocusable:
		obj = obj.next
	if obj:
		if api.getFocusObject() == obj:
			return True
		if SETFOCUS: # Else returns True to indicate that popup is focusable but does not perform the action.
			obj.scrollIntoView()
			obj.setFocus()
			api.setFocusObject(obj)
		speech.speakObject(alertPopup)
		Timer(0.05, speech.cancelSpeech)
		return True
	return False

def elapsedFromTimestamp(timestamp):
	delta = datetime.now()-timestamp
	d = delta.days
	if d == 1:
		return _("Yesterday")
	if d > 1:
		return _("%d days ago") % d
	h, r = divmod(delta.seconds, 3600)
	m, s = divmod(r, 60)
	if h == 1:
		return _("About an hour ago")
	elif h > 1:
		return _("About %d hours ago") % h
	if m == 1:
		return _("About a minute ago")
	elif m > 1:
		return _("About %d minutes ago") % m
	if s == 1:
		return _("a second ago")
	elif s > 1:
		return _("%d seconds ago") % s

def getAlertText(alertPopup):
	alertText = alertPopup.name if alertPopup.name else alertPopup.description if alertPopup.description else alertPopup.displayText if alertPopup.displayText else ""
	for obj in alertPopup.recursiveDescendants:
		objText = obj.name if obj.name else obj.description if obj.description else obj.displayText if obj.displayText else ""
		if not obj.isFocusable and objText not in alertText:
			alertText = "%s %s" % (alertText, objText)
	return alertText

def showDebugMessage(obj):
	clsList = []
	obj.findOverlayClasses(clsList)
	debug = "Please copy this report and paste it in https://github.com/javidominguez/MozillaScripts/issues\n\
	Unexpected object in event_alert\n\
	appModule: %s\nRole: %s\nName: %s\nDescription: %s\n IA2Attributes:%s%s%s\nClasses: %s"\
	% (obj.appModule.appName,
	controlTypes.roleLabels[obj.role],
	obj.name, obj.description.replace("\n", "\\n"),
	" id:%s" % obj.IA2Attributes["id"] if "id" in obj.IA2Attributes.keys() else "",
	" tag:%s" % obj.IA2Attributes["tag"] if "tag" in obj.IA2Attributes.keys() else "",
	" class:%s" % obj.IA2Attributes["class"] if "class" in obj.IA2Attributes.keys() else "",
	" ".join([str(c) for c in clsList]))
	beep(200, 150)
	ui.browseableMessage(debug, "MozillaScripts appModule debug")
