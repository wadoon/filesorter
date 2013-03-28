#!/usr/bin/python

from gi.repository import Gtk
from pprint import pprint
import multiprocessing as mp

def _get_builder(ctx):
    builder = Gtk.Builder()
    builder.add_from_file("MainFrame.glade")
    builder.connect_signals(ctx)
    return builder

RULES = []

def Deamon():
    pass #run deamon in seperate process

class DeamonMP(object):
    def __init__(self):
        pass

    def run(self):
        pass

    def on_update(self):
        pass

class IconoTray:
    def __init__(self, iconname):
        self.menu = Gtk.Menu()
        
        APPIND_SUPPORT = 1
        try: 
            from gi.repository import AppIndicator3
        except: 
            APPIND_SUPPORT = 0
            
        if APPIND_SUPPORT == 1:
            self.ind = AppIndicator3.Indicator.new("rhythmbox", iconname, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            self.ind.set_status (AppIndicator3.IndicatorStatus.ACTIVE)
            self.ind.set_menu(self.menu)
        else:
            self.myStatusIcon = Gtk.StatusIcon()
            self.myStatusIcon.set_from_icon_name(iconname)
            self.myStatusIcon.connect('popup-menu', self.right_click_event_statusicon)
	
	def add_menu_item(self, command, title):
		aMenuitem = Gtk.MenuItem()
		aMenuitem.set_label(title)
		aMenuitem.connect("activate", command)

		self.menu.append(aMenuitem)
		self.menu.show_all()

	def add_seperator(self):
		aMenuitem = Gtk.SeparatorMenuItem()
		self.menu.append(aMenuitem)
		self.menu.show_all()

	def get_tray_menu(self):
		return self.menu		

	def right_click_event_statusicon(self, icon, button, time):
		self.get_tray_menu()

		def pos(menu, aicon):
			return (Gtk.StatusIcon.position_menu(menu, aicon))

		self.menu.popup(None, None, pos, icon, button, time)




class Window(object):
    def __init__(self,rules=[]):
        self.builder = _get_builder(self)
        self.window = self.builder.get_object("window")
        self.rules = rules

        self.statusicon = Gtk.StatusIcon()
        self.statusicon.set_from_stock(Gtk.STOCK_HOME)
        self.statusicon.connect("popup-menu", lambda *x: pprint(x))
        self.statusicon.set_visible(True)

        print self.window.set_focus_chain((self.builder.get_object("actionBox"),))
        self.fc = []

        for r in rules:
            self.showRule(r)

    def showRule(self, rule):
        a = ActionPanel()
        a.set_model(rule)
        panel = self.builder.get_object("actionBox")
        panel.pack_end(a.view,False,False,0)        
        self.window.set_focus_chain(self.fc+[a.view]+a.view.get_focus_chain())
        print self.window.get_focus_chain()
        a.view.grab_focus()
        print self.window.get_focus()
        print a.view.get_focus_chain()
        
    def show(self):
        self.window.show_all()
        dir(self.builder.get_object("statusicon"))
        Gtk.main()

    def addRule(self, obj=None):
        self.showRule({})

    #handle onSettings
    #save model 
    

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

class ActionPanel(object):
    def __init__(self, onChange = lambda:True):
        self.model = {}
        self.builder = _get_builder(self)
        self.view = self.builder.get_object("gridAction")

        go = self.builder.get_object

        go("expander1").set_expanded(True)
        
        self.txt_folder  = go("fileChooserButtonFolder")
        self.txt_pattern = go("txtPattern")
        self.txt_script  = go("txtScript")
        self.cbo_ptype   = go("cboPatternType")
        self.txt_target = go("fileChooserButtonTarget")
        self.lbl_head = go("lblHead")
        self.txt_hint = go("txtHint")

        self.notifyMainFrame = onChange

        self.view.set_focus_chain((go("expander1"),
            self.txt_hint, self.txt_folder, self.txt_pattern,self.cbo_ptype,
            self.txt_target))

        self.set_model({'folder':'~', 'target':'~', 'pattern':'',
                      'ptype':'', 'script':'','hint':"newrule"})


    #TODO handle events onDelete, onCopy

    def set_model(self,rule, updateUi = False):
        if not self.model: self.model = dict()
        self.model.update(rule)
        print self.model
        
        self.lbl_head.set_label(self.model['hint'])

        self.notifyMainFrame()

        if updateUi:
            self.txt_hint.set_text(self.model['hint'])
            self.txt_pattern.set_text(self.model['pattern'])
            self.txt_script.get_text(self.model['script'])            
            self.txt_target.get_filename(self.model['target'])
            self.txt_folder.get_filename(self.model['folder'])       
            self.cbo_ptype.set_active_text(self.model['ptype'])
        
    def get_model(self):
        return self.model

    def _get_view(self):
        return self.view

    def updateModel(self,obj):
        print "update model"
        
        h = self.txt_hint.get_text()
        p = self.txt_pattern.get_text()
        s = self.txt_script.get_text()
        
        t = self.txt_target.get_filename()
        f = self.txt_folder.get_filename()
        
        pt = self.cbo_ptype.get_active_text()

        self.set_model({"folder":f, 'target':t, 'pattern':p, 'ptype':pt, 'script':s, 'hint':h})


if __name__ == "__main__":
    Window().show()
