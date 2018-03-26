# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Mar 18 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import wx.dataview
import wx.propgrid as pg

ID_NEW = 1000
ID_OPEN = 1001
ID_SAVE = 1002
ID_SAVE_AS = 1003
ID_EXIT = 1004
ID_CUT = 1005
ID_COPY = 1006
ID_PASTE = 1007
ID_SELECT = 1008
ID_SELECT_ALL = 1009
ID_BUILD = 1010
ID_CLEAN = 1011
ID_SHOW_FILES = 1012
ID_OPTIONS = 1013
ID_CONTENT = 1014
ID_ABOUT = 1015

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"UMLToCode", pos = wx.DefaultPosition, size = wx.Size( 648,569 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.FRAME_FLOAT_ON_PARENT|wx.ICONIZE|wx.MAXIMIZE|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.m_mgr = wx.aui.AuiManager()
		self.m_mgr.SetManagedWindow( self )
		self.m_mgr.SetFlags(wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE|wx.aui.AUI_MGR_ALLOW_FLOATING|wx.aui.AUI_MGR_DEFAULT|wx.aui.AUI_MGR_HINT_FADE|wx.aui.AUI_MGR_LIVE_RESIZE)
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.file = wx.Menu()
		self.new = wx.MenuItem( self.file, ID_NEW, u"New"+ u"\t" + u"Ctrl+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.new )
		
		self.open = wx.MenuItem( self.file, ID_OPEN, u"Open..."+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.open )
		
		self.file.AppendSeparator()
		
		self.save = wx.MenuItem( self.file, ID_SAVE, u"Save"+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.save )
		
		self.saveAs = wx.MenuItem( self.file, ID_SAVE_AS, u"Save As", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.saveAs )
		
		self.file.AppendSeparator()
		
		self.exit = wx.MenuItem( self.file, ID_EXIT, u"Exit"+ u"\t" + u"Alt+X", wx.EmptyString, wx.ITEM_NORMAL )
		self.file.Append( self.exit )
		
		self.m_menubar1.Append( self.file, u"File" ) 
		
		self.edit = wx.Menu()
		self.cut = wx.MenuItem( self.edit, ID_CUT, u"Cut"+ u"\t" + u"Ctrl+X", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.Append( self.cut )
		
		self.copy = wx.MenuItem( self.edit, ID_COPY, u"Copy"+ u"\t" + u"Ctrl+C", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.Append( self.copy )
		
		self.paste = wx.MenuItem( self.edit, ID_PASTE, u"Paste"+ u"\t" + u"Ctrl+V", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.Append( self.paste )
		
		self.edit.AppendSeparator()
		
		self.select = wx.MenuItem( self.edit, ID_SELECT, u"Select", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.Append( self.select )
		
		self.selectAll = wx.MenuItem( self.edit, ID_SELECT_ALL, u"Select All"+ u"\t" + u"Ctrl+A", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit.Append( self.selectAll )
		
		self.m_menubar1.Append( self.edit, u"Edit" ) 
		
		self.run = wx.Menu()
		self.build = wx.MenuItem( self.run, ID_BUILD, u"Build"+ u"\t" + u"Ctrl+B", wx.EmptyString, wx.ITEM_NORMAL )
		self.run.Append( self.build )
		
		self.clean = wx.MenuItem( self.run, ID_CLEAN, u"Clean", wx.EmptyString, wx.ITEM_NORMAL )
		self.run.Append( self.clean )
		
		self.showFiles = wx.MenuItem( self.run, ID_SHOW_FILES, u"Show Files", wx.EmptyString, wx.ITEM_NORMAL )
		self.run.Append( self.showFiles )
		
		self.m_menubar1.Append( self.run, u"Run" ) 
		
		self.tools = wx.Menu()
		self.options = wx.MenuItem( self.tools, ID_OPTIONS, u"Options..."+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.tools.Append( self.options )
		
		self.m_menubar1.Append( self.tools, u"Tools" ) 
		
		self.windows = wx.Menu()
		self.m_menubar1.Append( self.windows, u"Windows" ) 
		
		self.help = wx.Menu()
		self.content = wx.MenuItem( self.help, ID_CONTENT, u"Content", wx.EmptyString, wx.ITEM_NORMAL )
		self.help.Append( self.content )
		
		self.about = wx.MenuItem( self.help, ID_ABOUT, u"About", wx.EmptyString, wx.ITEM_NORMAL )
		self.help.Append( self.about )
		
		self.m_menubar1.Append( self.help, u"Help" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.m_panel_tools = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL, u"tools_pane" )
		self.m_mgr.AddPane( self.m_panel_tools, wx.aui.AuiPaneInfo() .Left() .Caption( u"Tools" ).PinButton( True ).Gripper().Dock().Resizable().FloatingSize( wx.Size( 100,250 ) ).BottomDockable( False ).TopDockable( False ).BestSize( wx.Size( 100,-1 ) ).MaxSize( wx.Size( 200,-1 ) ).Layer( 2 ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panel_tools.SetSizer( bSizer2 )
		self.m_panel_tools.Layout()
		bSizer2.Fit( self.m_panel_tools )
		self.m_toolBar_main = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.m_tool_new = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"New", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/new.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, u"Create new file", None ) 
		
		self.m_tool_open = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"Open", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/open.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBar_main.AddSeparator()
		
		self.m_tool_save = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"Save", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/save.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBar_main.AddSeparator()
		
		self.m_tool_undo = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"Undo", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/undo.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_tool_redo = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"Redo", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/redo.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBar_main.AddSeparator()
		
		self.m_tool_cut = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"Cut", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/cut.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_tool_copy = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"Copy", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/copy.xpm", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_tool_paste = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"Paste", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/paste.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBar_main.AddSeparator()
		
		self.m_tool_build = self.m_toolBar_main.AddLabelTool( wx.ID_ANY, u"Build", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/events.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBar_main.Realize()
		self.m_mgr.AddPane( self.m_toolBar_main, wx.aui.AuiPaneInfo() .Top() .CaptionVisible( False ).CloseButton( False ).Gripper().Dock().Resizable().FloatingSize( wx.DefaultSize ).BottomDockable( False ).Layer( 10 ).ToolbarPane() )
		
		self.m_auinotebook_editor = wx.aui.AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_NB_CLOSE_BUTTON|wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB|wx.aui.AUI_NB_DEFAULT_STYLE|wx.aui.AUI_NB_TAB_EXTERNAL_MOVE|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_TAB_SPLIT|wx.aui.AUI_NB_WINDOWLIST_BUTTON )
		self.m_mgr.AddPane( self.m_auinotebook_editor, wx.aui.AuiPaneInfo() .Center() .Caption( u"Editor" ).PinButton( True ).Gripper().Dock().Resizable().FloatingSize( wx.DefaultSize ).BottomDockable( False ).CentrePane().DefaultPane() )
		
		self.m_scrolledWindow_designer = wx.ScrolledWindow( self.m_auinotebook_editor, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow_designer.SetScrollRate( 5, 5 )
		self.m_auinotebook_editor.AddPage( self.m_scrolledWindow_designer, u"Designer", True, wx.NullBitmap )
		self.m_scrolledWindow_code = wx.ScrolledWindow( self.m_auinotebook_editor, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow_code.SetScrollRate( 5, 5 )
		self.m_auinotebook_editor.AddPage( self.m_scrolledWindow_code, u"Code", False, wx.NullBitmap )
		
		self.m_panel_messages = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_mgr.AddPane( self.m_panel_messages, wx.aui.AuiPaneInfo() .Bottom() .Caption( u"Messages" ).PinButton( True ).Gripper().Dock().Resizable().FloatingSize( wx.Size( -1,100 ) ).TopDockable( False ).LeftDockable( False ).RightDockable( False ).BestSize( wx.Size( -1,100 ) ).MaxSize( wx.Size( -1,100 ) ) )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_dataViewListCtrl_messages_dv = wx.dataview.DataViewListCtrl( self.m_panel_messages, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_HORIZ_RULES|wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		self.m_dataViewListColumn_name = self.m_dataViewListCtrl_messages_dv.AppendTextColumn( u"Name" )
		self.m_dataViewListColumn_desc = self.m_dataViewListCtrl_messages_dv.AppendTextColumn( u"Description" )
		self.m_dataViewListColumn_type = self.m_dataViewListCtrl_messages_dv.AppendIconTextColumn( u"Type" )
		self.m_dataViewListColumn_location = self.m_dataViewListCtrl_messages_dv.AppendTextColumn( u"Location" )
		bSizer4.Add( self.m_dataViewListCtrl_messages_dv, 100, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 1 )
		
		
		self.m_panel_messages.SetSizer( bSizer4 )
		self.m_panel_messages.Layout()
		bSizer4.Fit( self.m_panel_messages )
		self.m_panel_properties = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_mgr.AddPane( self.m_panel_properties, wx.aui.AuiPaneInfo() .Right() .Caption( u"Properties" ).PinButton( True ).Gripper().Dock().Resizable().FloatingSize( wx.Size( 150,-1 ) ).BottomDockable( False ).TopDockable( False ).BestSize( wx.Size( 150,-1 ) ).MaxSize( wx.Size( 150,-1 ) ) )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_propertyGridManager_main = pg.PropertyGridManager(self.m_panel_properties, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PGMAN_DEFAULT_STYLE|wx.propgrid.PG_ALPHABETIC_MODE|wx.propgrid.PG_AUTO_SORT|wx.propgrid.PG_BOLD_MODIFIED|wx.propgrid.PG_DESCRIPTION|wx.propgrid.PG_TOOLBAR|wx.propgrid.PG_TOOLTIPS)
		self.m_propertyGridManager_main.SetExtraStyle( wx.propgrid.PG_EX_HELP_AS_TOOLTIPS|wx.propgrid.PG_EX_MODE_BUTTONS ) 
		
		self.m_propertyGridPage_default = self.m_propertyGridManager_main.AddPage( u"Default", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/properties.png", wx.BITMAP_TYPE_ANY ) );
		self.m_propertyGridItem_name = self.m_propertyGridPage_default.Append( pg.StringProperty( u"Name", u"Name" ) ) 
		self.m_propertyGridItem_desc = self.m_propertyGridPage_default.Append( pg.StringProperty( u"Description", u"Description" ) ) 
		
		self.m_propertyGridPage_events = self.m_propertyGridManager_main.AddPage( u"Events", wx.Bitmap( u"../../wxFormBuilder/output/resources/icons/events.png", wx.BITMAP_TYPE_ANY ) );
		self.m_propertyGridItem_on_loaded = self.m_propertyGridPage_events.Append( pg.StringProperty( u"OnLoaded", u"OnLoaded" ) ) 
		self.m_propertyGridItem_on_unloaded = self.m_propertyGridPage_events.Append( pg.StringProperty( u"OnUnloaded", u"OnUnloaded" ) ) 
		bSizer3.Add( self.m_propertyGridManager_main, 100, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 1 )
		
		
		self.m_panel_properties.SetSizer( bSizer3 )
		self.m_panel_properties.Layout()
		bSizer3.Fit( self.m_panel_properties )
		self.m_statusBar_main = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_panel_project = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel_project.Hide()
		
		self.m_mgr.AddPane( self.m_panel_project, wx.aui.AuiPaneInfo() .Left() .Caption( u"Project" ).PinButton( True ).Gripper().Dock().Resizable().FloatingSize( wx.Size( 150,250 ) ).BottomDockable( False ).TopDockable( False ).Row( 0 ).Position( 1 ).BestSize( wx.Size( 150,-1 ) ).MaxSize( wx.Size( 200,-1 ) ).Layer( 2 ) )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_genericDirCtrl_project = wx.GenericDirCtrl( self.m_panel_project, wx.ID_ANY, u".", wx.DefaultPosition, wx.DefaultSize, wx.DIRCTRL_3D_INTERNAL|wx.DIRCTRL_EDIT_LABELS|wx.DIRCTRL_MULTIPLE|wx.DIRCTRL_SELECT_FIRST|wx.DIRCTRL_SHOW_FILTERS|wx.SUNKEN_BORDER, wx.EmptyString, 0 )
		
		self.m_genericDirCtrl_project.ShowHidden( False )
		bSizer5.Add( self.m_genericDirCtrl_project, 100, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 1 )
		
		
		self.m_panel_project.SetSizer( bSizer5 )
		self.m_panel_project.Layout()
		bSizer5.Fit( self.m_panel_project )
		
		self.m_mgr.Update()
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		self.m_mgr.UnInit()
		
	

