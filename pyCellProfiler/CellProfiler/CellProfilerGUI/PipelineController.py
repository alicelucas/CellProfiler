"""PipelineController.py - controls (modifies) a pipeline

   $Revision$
"""
import CPFrame
import CellProfiler.Pipeline
from CellProfiler.CellProfilerGUI.AddModuleFrame import AddModuleFrame
import wx
import os
import scipy.io.matlab.mio
import cPickle

class PipelineController:
    """Controls the pipeline through the UI
    
    """
    def __init__(self,pipeline,frame):
        self.__pipeline =pipeline
        self.__frame = frame
        self.__add_module_frame = AddModuleFrame(frame,-1,"Add modules")
        self.__add_module_frame.AddListener(self.__OnAddToPipeline) 
        wx.EVT_MENU(frame,CPFrame.ID_FILE_LOAD_PIPELINE,self.__OnLoadPipeline)
        wx.EVT_MENU(frame,CPFrame.ID_FILE_SAVE_PIPELINE,self.__OnSavePipeline)
    
    def AttachToPipelineListView(self,pipeline_list_view):
        """Glom onto events from the list box with all of the module names in it
        
        """
        self.__pipeline_list_view = pipeline_list_view
    
    def AttachToModuleControlsPanel(self,module_controls_panel):
        """Attach the pipeline controller to the module controls panel
        
        Attach the pipeline controller to the module controls panel.
        In addition, the PipelineController gets to add whatever buttons it wants to the
        panel.
        """
        self.__module_controls_panel = module_controls_panel
        self.__mcp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__help_button = wx.Button(self.__module_controls_panel,-1,"?",(0,0),(15,15))
        self.__mcp_text = wx.StaticText(self.__module_controls_panel,-1,"Adjust modules:")
        self.__mcp_add_module_button = wx.Button(self.__module_controls_panel,-1,"+",(0,0),(15,15))
        self.__mcp_remove_module_button = wx.Button(self.__module_controls_panel,-1,"-",(0,0),(15,15))
        self.__mcp_module_up_button = wx.Button(self.__module_controls_panel,-1,"^",(0,0),(15,15))
        self.__mcp_module_down_button = wx.Button(self.__module_controls_panel,-1,"v",(0,0),(15,15))
        self.__mcp_sizer.AddMany([(self.__help_button,0,wx.EXPAND),
                                  (self.__mcp_text,0,wx.EXPAND),
                                  (self.__mcp_add_module_button,0,wx.EXPAND),
                                  (self.__mcp_remove_module_button,0,wx.EXPAND),
                                  (self.__mcp_module_up_button,0,wx.EXPAND),
                                  (self.__mcp_module_down_button,0,wx.EXPAND)])
        self.__module_controls_panel.SetSizer(self.__mcp_sizer)
        self.__module_controls_panel.Bind(wx.EVT_BUTTON, self.__OnHelp, self.__help_button)
        self.__module_controls_panel.Bind(wx.EVT_BUTTON, self.__OnAddModule,self.__mcp_add_module_button)
        self.__module_controls_panel.Bind(wx.EVT_BUTTON, self.__OnRemoveModule,self.__mcp_remove_module_button)
        self.__module_controls_panel.Bind(wx.EVT_BUTTON, self.__OnModuleUp,self.__mcp_module_up_button)
        self.__module_controls_panel.Bind(wx.EVT_BUTTON, self.__OnModuleDown,self.__mcp_module_down_button)
        
    def __OnLoadPipeline(self,event):
        dlg = wx.FileDialog(self.__frame,"Choose a pipeline file to open",wildcard="*.mat")
        if dlg.ShowModal()==wx.ID_OK:
            pathname = os.path.join(dlg.GetDirectory(),dlg.GetFilename())
            try:
                handles=scipy.io.matlab.mio.loadmat(pathname)
            except Exception,instance:
                self.__frame.DisplayError('Failed to open %s'%(pathname),instance)
                return
            try:
                self.__pipeline.CreateFromHandles(handles)
            except Exception,instance:
                self.__frame.DisplayError('Failed during loading of %s'%(pathname),instance)

    def __OnSavePipeline(self,event):
        dlg = wx.FileDialog(self.__frame,"Save pipeline",wildcard="*.mat",style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            pathname = os.path.join(dlg.GetDirectory(),dlg.GetFilename())
            handles = self.__pipeline.SaveToHandles()
            try:
                scipy.io.matlab.mio.savemat(pathname,handles,format='5')
            except:
                print 'foo'
            
    def __OnHelp(self,event):
        print "No help yet"
        
    def __OnAddModule(self,event):
        self.__add_module_frame.Show()
    
    def __GetSelectedModules(self):
        return self.__pipeline_list_view.GetSelectedModules()
    
    def __OnRemoveModule(self,event):
        selected_modules = self.__GetSelectedModules()
        for module in selected_modules:
            self.__pipeline.RemoveModule(module.ModuleNum())
            
    def __OnModuleUp(self,event):
        selected_modules = self.__GetSelectedModules()
        for module in selected_modules:
            self.__pipeline.MoveModule(module.ModuleNum(),CellProfiler.Pipeline.DIRECTION_UP);
        
    def __OnModuleDown(self,event):
        selected_modules = self.__GetSelectedModules()
        selected_modules.reverse()
        for module in selected_modules:
            self.__pipeline.MoveModule(module.ModuleNum(),CellProfiler.Pipeline.DIRECTION_DOWN);
    
    def __OnAddToPipeline(self,caller,event):
        selected_modules = self.__GetSelectedModules()
        ModuleNum = 1
        if len(selected_modules):
            ModuleNum=selected_modules[-1].ModuleNum()+1
        self.__pipeline.AddModule(event.ModulePath,ModuleNum)
            
