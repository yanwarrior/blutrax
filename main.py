import pythoncom, pyHook
import sys
import blutrax.app as blutrax
import thread

def run_blutrack():
	# create a hook manager
	hm = pyHook.HookManager()
	# watch for all keyboard events
	hm.KeyDown = blutrax.keyboard_tracking
	# set the hook
	hm.HookKeyboard()
	# watch for all mouse events
	#hm.MouseAll = blutrax.mouse_tracking
	# set the hook
	#hm.HookMouse()
	# wait forever
	pythoncom.PumpMessages()

if __name__ == '__main__':
	try:
		run_blutrack()
	except:
		print "Error"
