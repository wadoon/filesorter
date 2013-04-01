#!/usr/bin/python

from gi.repository import Gtk
from pprint import pprint
from uuid import uuid1 as uuid
#from pyyaml import dump,load
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


def Rule(dict):
    def __init__(self,*args):
        super(dict).__init__(*args)

    def __str__(self):
        return self['hint']


from see import see
class Window(object):    
    def __init__(self,rules=[]):
        self.builder = _get_builder(self)
        self.window = self.builder.get_object("window")
        self.rules = rules

        self.statusicon = Gtk.StatusIcon()
        self.statusicon.set_from_stock(Gtk.STOCK_HOME)
        self.statusicon.connect("popup-menu", lambda *x: pprint(x))
        self.statusicon.set_visible(True)

        go = self.builder.get_object

        self.ruleStore = Gtk.ListStore(object)        
        self.treeview = go('treeview')        
        self.treeview.set_model(self.ruleStore)

        def func(column,cell,model,ite,user_data):
            value = model.get_value(ite,0)
            x = value['hint']                
            cell.set_property('text', str(x))
            return 

        cr = Gtk.CellRendererText()
        self.treeColumn = Gtk.TreeViewColumn("Rules",cr,text=0)
        self.treeColumn.set_cell_data_func(cr, func)

        self.treeview.append_column(self.treeColumn)
        
        self.txt_folder  = go("fileChooserButtonFolder")
        self.txt_pattern = go("txtPattern")
        self.txt_script  = go("txtScript")
        self.cbo_ptype   = go("cboPatternType")
        self.txt_target = go("fileChooserButtonTarget")
        self.lbl_head = go("lblHead")
        self.txt_hint = go("txtHint")
        
        self.model = {}
        for r in rules:
            self.showRule(r)

    def showRule(self, rule):
        self.ruleStore.append([rule])
        print "rule appended", rule
        self.treeview
        #select new entry
        
        
    def show(self):
        self.window.show_all()
        dir(self.builder.get_object("statusicon"))
        Gtk.main()

    def addRule(self, obj=None):
        self.showRule({'hint':'new entry'})


    def storeRules(self):
        pass

    
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)


    def ruleSelectionChanged(self,*args):
        (model,sel) = self.treeview.get_selection().get_selected()
        value = model.get_value(sel,0)
        self.set_model(value,True)
    
    def set_model(self,rule, updateUi = False):
        if not self.model: self.model = dict()
        self.model.update(rule)
                
        if updateUi:
            self.txt_hint.set_text(self.model['hint'])
            self.txt_pattern.set_text(self.model['pattern'])
            self.txt_script.get_text(self.model['script'])            
            self.txt_target.get_filename(self.model['target'])
            self.txt_folder.get_filename(self.model['folder'])       
            self.cbo_ptype.set_active_text(self.model['ptype'])
        
    def get_model(self):
        return self.model

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
    r = {"folder":'~', 'target':'~/tmp', 'pattern':'abc', 'ptype':'Regex', 'script':None, 'hint':'TestRule'}
    Window([r]).show()
