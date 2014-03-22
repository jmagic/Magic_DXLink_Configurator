import wx
from pydispatch import dispatcher

from ObjectListView import ObjectListView, ColumnDefn
import time


class MultiSendCommandConfig ( wx.Dialog ):
    
    def __init__( self, parent, device_list, dxlink_model ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, 
                            pos = wx.DefaultPosition, size = wx.Size( 740,550 ), 
                            style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer121 = wx.BoxSizer( wx.VERTICAL )
        
        self.deviceOlv = ObjectListView(self, wx.ID_ANY, size = wx.Size( -1,200), 
                                        style=wx.LC_REPORT|
                                               wx.SUNKEN_BORDER|
                                               wx.RESIZE_BORDER )
        self.deviceOlv.SetColumns([ColumnDefn("Model", "center", 130, "model"),
                                        ColumnDefn("IP", "center", 100, "ip"),
                                        ColumnDefn("Device", "center", 80, "device")])
        bSizer121.Add( self.deviceOlv, 1, wx.ALL|wx.EXPAND, 5 )
        bSizer1.Add ( bSizer121, 0, wx.EXPAND, 5)
        
        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        self.send_query = wx.RadioButton(self, wx.ID_ANY, u"Query",
                                             wx.DefaultPosition, wx.DefaultSize, 0 ) #wx.RB_GROUP sets the radio buttons as a group. Makes windows work 
        self.Bind(wx.EVT_RADIOBUTTON, self.onQuery, self.send_query)
        bSizer11.Add( self.send_query, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        self.send_command = wx.RadioButton(self,  wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.DefaultSize,0 )
        self.send_command.SetValue( True )
        self.Bind(wx.EVT_RADIOBUTTON, self.onQuery, self.send_command)
        bSizer11.Add( self.send_command, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        command_comboChoices = []
        self.command_combo = wx.ComboBox( self, wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.DefaultSize, 
                                        command_comboChoices, 0 )
        bSizer11.Add( self.command_combo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.command_combo.Bind(wx.EVT_COMBOBOX, self.onCommandCombo)
        
        action_comboChoices = []
        self.action_combo = wx.ComboBox( self, wx.ID_ANY, u"Action", 
                                        wx.DefaultPosition, wx.DefaultSize, 
                                        action_comboChoices, 0 )
        bSizer11.Add( self.action_combo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.action_combo.Bind(wx.EVT_COMBOBOX, self.onActionCombo)
        
        self.get_all = wx.CheckBox( self, wx.ID_ANY, u"Send All Query's", 
                                        wx.DefaultPosition, wx.DefaultSize, 0 )
        self.get_all.SetValue(False)
        self.get_all.Bind(wx.EVT_CHECKBOX, self.onGetAll)
        bSizer11.Add( self.get_all, 0, wx.ALL, 5 )
        
        
        bSizer1.Add( bSizer11, 0, wx.EXPAND, 5 )
        
        
        #send_command 5317:6:1 , "'AUDOUT_FORMAT-HDMI'"
        
        
        bSizer13 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer20 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.static_text = wx.StaticText(self, wx.ID_ANY, 
                                        u"send_command <DEVICE>:", 
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_text.Wrap( -1 )
        bSizer20.Add( self.static_text, 0,  wx.ALIGN_CENTER_VERTICAL|
                                            wx.TOP|wx.BOTTOM|wx.LEFT, 5)
        
        self.string_port = wx.TextCtrl(  self, wx.ID_ANY, wx.EmptyString, 
                                        wx.DefaultPosition, wx.Size( 20,-1 ), 0 )
        
        bSizer20.Add( self.string_port, 0, wx.TOP|wx.BOTTOM, 5  )
        
        self.static_text2 = wx.StaticText(self, wx.ID_ANY, u":<SYSTEM>, \" \' ",
                                          wx.DefaultPosition, wx.DefaultSize, 0 )
        self.static_text2.Wrap( -1 )
        bSizer20.Add( self.static_text2, 0, wx.ALIGN_CENTER_VERTICAL|
                                                wx.TOP|wx.BOTTOM, 5)
        
        self.stringcommand = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, 
                                        wx.DefaultPosition, wx.Size( 280,-1 ), 0)
        bSizer20.Add( self.stringcommand, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 5)
        
        self.static_text3 = wx.StaticText(self, label="\' \" ")
        bSizer20.Add( self.static_text3, 1, wx.ALL, 5)
        
        self.send = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, 
                                wx.DefaultSize, 0 )
        bSizer20.Add( self.send, 0, wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.onSend, self.send)
        
        self.exit = wx.Button( self, wx.ID_ANY, u"Exit", 
                                    wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer20.Add( self.exit, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
        self.Bind(wx.EVT_BUTTON, self.OnExit, self.exit)
        
        bSizer13.Add( bSizer20, 0, wx.EXPAND, 5 )
        bSizer1.Add( bSizer13, 0, wx.EXPAND, 5 )
 
        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer16 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer16.SetMinSize( wx.Size( 260,-1 ) ) 
        self.description = wx.TextCtrl( self, wx.ID_ANY, u"Command", 
                                        wx.DefaultPosition, wx.Size( -1,-1 ), 
                                        style=wx.TE_MULTILINE|wx.TE_READONLY|
                                            wx.HSCROLL )
        self.description.SetMaxLength( 0 ) 
        bSizer16.Add( self.description, 1, wx.ALL|wx.EXPAND, 5 )
        
        bSizer15.Add( bSizer16, 0, wx.EXPAND, 5 )
        
        bSizer17 = wx.BoxSizer( wx.VERTICAL )
        
        self.syntax = wx.TextCtrl( self, wx.ID_ANY, u"Description", 
                                    wx.DefaultPosition, wx.DefaultSize, 
                                    style=wx.TE_MULTILINE|wx.TE_READONLY|
                                        wx.HSCROLL )
        self.syntax.SetMaxLength( 0 ) 
        bSizer17.Add( self.syntax, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer15.Add( bSizer17, 1, wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer15, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )


        #------------------------------ Done with wxFormBuilder  
           
        self.parent = parent
        #self.obj = obj
        self.parent.actionItems = []  #cleared out so progress will work.
        #dispatcher.connect(self.onResult, signal="send_command result", sender=dispatcher.Any)
        self.SetTitle("Multiple Send Command") # to %s" %obj.ip)
        self.rx_tx_commands = {'rx':
                                    {'?VIDOUT_SCALE':(6,[''],
                                    '?VIDOUT_SCALE \n\nRequests the current Scaling Mode\nthat the Receiver is set to. The\nmodes are AUTO (SmartScale)\nMANUAL, and BYPASS.',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'?VIDOUT_SCALE\'\"\n\nExample:\nSEND_COMMAND dvRX,\"\'?VIDOUT_SCALE\'\"\nReturns a COMMAND of the form:\nVIDOUT_SCALE-<AUTO/MANUAL/BYPASS>'),                             
                                    'VIDOUT_SCALE':(6,['AUTO','MANUAL','BYPASS'],
                                    'VIDOUT_SCALE \n\nSets the Scaling Mode on the \nReceiver to AUTO (SmartScale),\nMANUAL, or BYPASS',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'VIDOUT_SCALE-<scaling mode>\'\"\nVariable:\nscaling mode = AUTO, MANUAL, BYPASS\n\nExample:\nSEND_COMMAND dvRX,\"\'VIDOUT_SCALE-MANUAL\'\"'),
                                    
                                    '?VIDOUT_RES_REF':(6,[''],
                                    '?VIDOUT_RES_REF \n\nRequests the resolution and refresh\nrate of the video through the\nReceiver.\n\nNote: If the Scaling Mode is set to\nBypass, the response will be\n\"BYPASS.\"',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'?VIDOUT_RES_REF\'\"\nVariables:\n horizontal = An integer value representing the horizontal.\n  vertical = An integer value representing the vertical. May have an additional\nqualifier such as \'i\' or \'p\'.\n rate = An integer value representing the refresh rate.\n\nExample:\nSEND_COMMAND dvRX,\"\'?VIDOUT_RES_REF\'\"\nReturns a COMMAND of the form:\nVIDOUT_RES_REF-<horizontal>x<vertical>,<rate>'),
                                    
                                    'VIDOUT_RES_REF':(6,['640x480, 60','640x480, 72','640x480, 75','800x600, 60','800x600, 72','800x600, 75','1024x768, 60','1024x768,70','1024x768, 75','1280x720p, 50','1280x720p, 60','1280x768, 60','1280x800, 60','1280x1024, 60','1360x768, 60','1440x900, 60','1600x1200, 60','1680x1050, 60','1920x1080, 60','1920x1080p, 50','1920x1080p, 60','1920x1200, 60'],
                                    'VIDOUT_RES_REF \n\nSets the resolution and refresh rate \nof the video through the Receiver.\nImportant: The variables used must \ncome from the Resolution Names \nlisted in the table in the \"Supported \nOutput Resolutions\" appendix on \npage 129.\nNote: The default for Manual Mode \nis 1280x1024,60.',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,"\'VIDOUT_RES_REF- \n<horizontal>x<vertical>,<rate>\'"\n\nVariables:\n horizontal = An integer value representing the horizontal.\n vertical = An integer value representing the vertical. May have an \nadditional qualifier such as \'p\' or \'i\'.\n rate = An integer value representing the refresh rate.\n\nExample:\nSEND_COMMAND dvRX,\"\'VIDOUT_RES_REF-1920x1080p,60\'\"'),
                                    
                                    '?VIDOUT_RES':(6,[''],
                                    '?VIDOUT_RES \n\nRequests the resolution and refresh\nrate of the video through the\nReceiver.\n\nNote: If the Scaling Mode is set to\nBypass, the response will be\n\"BYPASS.\"',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'?VIDOUT_RES\'\"\nVariables:\n horizontal = An integer value representing the horizontal.\n  vertical = An integer value representing the vertical. May have an additional\nqualifier such as \'i\' or \'p\'.\n rate = An integer value representing the refresh rate.\n\nExample:\nSEND_COMMAND dvRX,\"\'?VIDOUT_RES\'\"\nReturns a COMMAND of the form:\nVIDOUT_RES-<horizontal>x<vertical>,<rate>'),
                                    
                                    '?VIDOUT_ASPECT_RATIO':(6,[''],
                                    '?VIDOUT_ASPECT_RATIO \n\nRequests the aspect ratio\npreference of the video\nthrough the Receiver.\n(For explanations of the ratio\noptions, see page 82.)',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'?VIDOUT_ASPECT_RATIO\'\"\nVariables:\nratio = STRETCH (default after FACTORYAV), MAINTAIN, ZOOM, ANAMORPHIC\n\nExample:\nSEND_COMMAND dvRX,\"\'?VIDOUT_ASPECT_RATIO\'\"\nReturns a COMMAND of the form:\nVIDOUT_ASPECT_RATIO-<ratio>'),
                                    
                                    'VIDOUT_ASPECT_RATIO':(6,['STRETCH', 'MAINTAIN', 'ZOOM', 'ANAMORPHIC'],
                                    'VIDOUT_ASPECT_RATIO\n\nSets the aspect ratio \npreference of the video \nthrough the Receiver to \nStretch, Maintain, Zoom, or \nAnamorphic. \n(For explanations of the ratio \noptions, see page 82.)',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'VIDOUT_ASPECT_RATIO-<ratio>\'\"\nVariables:\nratio = STRETCH, MAINTAIN, ZOOM, ANAMORPHIC \n\nExample:\nSEND_COMMAND dvRX,\"\'VIDOUT_ASPECT_RATIO-ZOOM\'\"'),
                                    
                                    '?VIDOUT_TESTPAT':(6,[''],
                                    '?VIDOUT_TESTPAT \n\nRequests the test pattern\nsetting on the Receiver.',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'?VIDOUT_TESTPAT\'\"\nVariables:\npattern = OFF, COLOR BAR, GRAY RAMP, SMPTE BAR, HILOTRAK, PLUGE,\nX-HATCH\n\nExample:\nSEND_COMMAND dvRX,\"\'?VIDOUT_TESTPAT\'\" Returns a COMMAND of the form:\nVIDOUT_TESTPAT-<pattern>'),
                                    
                                    'VIDOUT_TESTPAT':(6,['OFF', 'COLOR BAR', 'GRAY RAMP', 'SMPTE BAR', 'HILOTRAK', 'PLUGE', 'X-HATCH'],
                                    'VIDOUT_TESTPAT \n\nSets the test pattern to \ndisplay (will not display if an \ninput signal is not present). \nCan be sent in any Scaling \nMode.',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'VIDOUT_TESTPAT-<pattern>\'\"\nVariables:\npattern = OFF, COLOR BAR, GRAY RAMP, SMPTE BAR, HILOTRAK, PLUGE, \nX-HATCH\n\nExample:\nSEND_COMMAND dvRX,\"\'VIDOUT_TESTPAT-COLOR BAR\'\"'),
                                    
                                    '?VIDOUT_MUTE':(6,[''],
                                    '?VIDOUT_MUTE \n\nRequests the setting for the\nMute preference applied to\nthe image from the Receiver\n(Enable or Disable).',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'?VIDOUT_MUTE\'\"\nExample:\nSEND_COMMAND dvRX,\"\'?VIDOUT_MUTE\'\"\nReturns a COMMAND of the form:\nVIDOUT_MUTE-<ENABLE|DISABLE>'),
                                    
                                    'VIDOUT_MUTE':(6,['ENABLE','DISABLE'],
                                    'VIDOUT_MUTE \n\nSets the Mute preference of \nthe image from the Receiver \nto Enable (displays a blank \nscreen) or Disable.',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'VIDOUT_MUTE-<ENABLE|DISABLE>\'\"\n\nExample:\nSEND_COMMAND dvRX,\"\'VIDOUT_MUTE-ENABLE\'\"'),
                                    
                                    '?AUDOUT_MUTE':(6,[''],
                                    '?AUDOUT_MUTE \n\nRequests the setting for the\nMute preference of the audio\nfrom the Receiver (Enable or\nDisable).',
                                    'Syntax:\nSEND_COMMAND <DEV>,\"\'?AUDOUT_MUTE\'\"\nExample:\nSEND_COMMAND dvRX,\"\'?AUDOUT_MUTE\'\"\nReturns a COMMAND of the form:\nAUDOUT_MUTE-<ENABLE|DISABLE>'),
                                                   
                                    'AUDOUT_MUTE':(6,['ENABLE','DISABLE'],
                                    'AUDOUT_MUTE \n\nSets the Mute preference of\nthe audio from the Receiver\nto Enable (no sound) or\nDisable.',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'AUDOUT_MUTE-<ENABLE|DISABLE>\'\"\n\nExample:\nSEND_COMMAND dvRX,\"\'AUDOUT_MUTE-ENABLE\'\"'),
                                    
                                    '?AUDOUT_FORMAT':(6,[''],
                                    'AUDOUT_FORMAT \n\nRequests the audio format on\nthe Receiver.',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'?AUDOUT_FORMAT\'\"\nVariable:\nformat = HDMI, ANALOG, ALL\nExample:\nSEND_COMMAND dvRX,\"\'?AUDOUT_FORMAT\'\"\nReturns a COMMAND of the form:\nAUDOUT_FORMAT-<format>'),
                                    
                                    'AUDOUT_FORMAT':(6,['HDMI','ANALOG','ALL'],
                                    'AUDOUT_FORMAT \n\nSets the audio format on the\nReceiver (default is ALL).',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'AUDOUT_FORMAT-<format>\'\"\n\nVariable:\nformat = HDMI, ANALOG, ALL\n\nExample:\nSEND_COMMAND dvRX,\"\'AUDOUT_FORMAT-ANALOG\'\"'),
                                    
                                    '?USB_HID_ROUTE':(5,[''],
                                    '?USB_HID_ROUTE \n\nRequests the IP address\nor hostname of the host\ndevice (Transmitter)\nsending USB keyboard/\nmouse data to the\nReceiver.',
                                    'Syntax:\nSEND_COMMAND <DEV>,\"\'?USB_HID_ROUTE\'\"\nExample:\nSEND_COMMAND dvRX,\"\'?USB_HID_ROUTE\'\"\nReturns a COMMAND of the form:\nUSB_HID_ROUTE-<IP address or hostname>'),
                                    
                                    'USB_HID_ROUTE':(5,['0.0.0.0'],
                                    'USB_HID_ROUTE \n\nSet the IP address or \nhostname of the host \ndevice (Transmitter) that \nwill be sending USB \nkeyboard/mouse data to \nthe Receiver.\nNote: When a hostname is specified, a maximum of 50 characters can be used.)',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'USB_HID_ROUTE-<IP address or hostname>\'\"\n\nExample:\nSEND_COMMAND dvRX,\"\'USB_HID_ROUTE-<192.168.1.5>\'\"\n\nNote: To eliminate the connection, specify 0.0.0.0 as the IP address. To redirect to a new \nhost device (Transmitter), send the new IP address or hostname.'),
                                    },
                                'tx':
                                    {'?VIDIN_AUTO_SELECT':(1,[''],
                                    '?VIDIN_AUTO_SELECT \n\nRequests setting for the Auto Select mode\nfor the video input signal on the\nMulti-Format TX, Wallplate TX, or Decor\nWallplate TX (Enable or Disable).\nNote: This command applies to all DXLink\nTransmitters except the HDMI TX.',
                                    'Important: This command must be sent to Port 1.\nSyntax:\n\nSEND_COMMAND <DEV>,\"\'?VIDIN_AUTO_SELECT\'\"\nExample:\nSEND_COMMAND dvMFTX,\"\'?VIDIN_AUTO_SELECT\'\"\nReturns a COMMAND of the form:\nVIDIN_AUTO_SELECT-ENABLE'),
                                    
                                    'VIDIN_AUTO_SELECT':(1,['ENABLE','DISABLE'],
                                    'VIDIN_AUTO_SELECT \n\nEnables or disables the Auto Select mode \nfor the video input signal on the \nMulti-Format TX, Wallplate TX, or Decor \nWallplate TX.\nNote: This command applies to all DXLink \nTransmitters except the HDMI TX.',
                                    'Syntax: \n\nSEND_COMMAND <DEV>,\"\'VIDIN_AUTO_SELECT-<ENABLE|DISABLE>\'\"\n\nVariable:\nvalue = ENABLE | DISABLE\n\nExample:\nSEND_COMMAND dvMFTX,\"\'VIDIN_AUTO_SELECT-ENABLE\'\"'),
                                    
                                    '?INPUT-VIDEO,6':(1,[''],
                                    '?INPUT-VIDEO,6 \n\nRequests the video input being used on\nthe Multi-Format TX, Wallplate TX, or\nDecor Wallplate TX: either the digital video\n(Input 7) or the analog video (Input 8). The\noutput is always 6.\nNote: This command applies to all DXLink\nTransmitters except the HDMI TX.',
                                    'Important: This command must be sent to Port 1.\nSyntax:\nSEND_COMMAND <DEV>,\"\'?INPUT-VIDEO,6\'\"\nExample:\nSEND_COMMAND dvMFTX,\"\'?INPUT-VIDEO,6\'\"\nReturns a COMMAND of the form:\nSWITCH-LVIDEOI8O6'),
                                    
                                    'VI8O6':(1,[''],
                                    'VI<input>O<output>\n\nSets the Multi-Format TX, Wallplate TX, or \nDecor Wallplate TX to route either the \ndigital video (Input 7) or the analog video \n(Input 8) to the output (which is always \noutput 6).\nNote: This command applies to all DXLink \nTransmitters except the HDMI TX.',
                                    'Important: This command must be sent to Port 1. \n\nSyntax:\nSEND_COMMAND <DEV>,\"\'VI<input>O<output>\'\"\n\nVariables:\ninput = 7 for digital video; 8 for analog video\noutput = 6\n\nExample: \nSEND_COMMAND dvMFTX,\"\'VI8O6\'\"'),
                                     
                                    'VI7O6':(1,[''],
                                    'VI<input>O<output>\n\nSets the Multi-Format TX, Wallplate TX, or \nDecor Wallplate TX to route either the \ndigital video (Input 7) or the analog video \n(Input 8) to the output (which is always \noutput 6).\nNote: This command applies to all DXLink \nTransmitters except the HDMI TX.',
                                    'Important: This command must be sent to Port 1. \n\nSyntax:\nSEND_COMMAND <DEV>,\"\'VI<input>O<output>\'\"\n\nVariables:\ninput = 7 for digital video; 8 for analog video\noutput = 6\n\nExample: \nSEND_COMMAND dvMFTX,\"\'VI8O6\'\"'),
                                     
                                    '?VIDIN_STATUS':(7,[''],
                                    '?VIDIN_STATUS \n\nRequests the status of the video\ninput on the Transmitter.\nImportant: In the case of the\nMulti-Format TX, Wallplate TX,\nor Decor Wallplate TX this will\nonly specify the status of the\ncurrently routed input port.\nImportant: Send to Port 7 for digital video or to Port 8 for analog video.',
                                    'Syntax:\nSEND_COMMAND <DEV>,\"\'?VIDIN_STATUS\'\"\nVariable:\nstatus = NO SIGNAL, UNKNOWN SIGNAL, VALID SIGNAL\nExample:\nSEND_COMMAND dvMFTX,\"\'?VIDIN_STATUS\'\"\nReturns a COMMAND of the form:\nVIDIN_STATUS-<status>'),
                                    
                                    '?VIDIN_FORMAT':(7,[''],
                                    '?VIDIN_FORMAT \n\nRequests the video format on the\nTransmitter.\nNote: All DXLink Transmitters\nexcept the HDMI TX support\ncomponent, S-Video,\ncomposite, and VGA signals.',
                                    'Note: Send to Port 7 or Port 8.\nSyntax:\nSEND_COMMAND <DEV>,\"\'?VIDIN_FORMAT\'\"\nVariable:\nformat (port 8) = COMPONENT, S-VIDEO, COMPOSITE, VGA\nformat (port 7) = HDMI, DVI\nExample:\nSEND_COMMAND dvMFTX,\"\'?VIDIN_FORMAT\'\"\nReturns a COMMAND of the form:\nVIDIN_FORMAT-<format>'),
                                     
                                    'VIDIN_FORMAT':(7,['HDMI','DVI','COMPONENT', 'S-VIDEO', 'COMPOSITE', 'VGA'],
                                    'VIDIN_FORMAT \n\nSets the video format on the \nTransmitter (prior to sending, \nVIDIN_AUTO_SELECT must be \nset to DISABLE).\nNote: All DXLink Transmitters \nexcept the HDMI TX support \ncomponent, S-Video, \ncomposite, and VGA signals\nNote: Send to Port 7 or Port 8.',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'VIDIN_FORMAT-<format>\'\"\n\nVariable:\nformat (port 8) = COMPONENT, S-VIDEO, COMPOSITE, VGA\nformat (port 7) = HDMI, DVI\n\nExample:\nSEND_COMMAND dvMFTX,\"\'VIDIN_FORMAT-COMPONENT\'\"'),
                                     
                                    '?VIDIN_RES_AUTO':(7,[''],
                                    '?VIDIN_RES_AUTO \n\nRequests the setting for the Auto\nmode on the Transmitter (Enable\nor Disable).',
                                    'Note: Send to Port 7 or Port 8.\nSyntax:\nSEND_COMMAND <DEV>,\"\'?VIDIN_RES_AUTO\'\"\nExample:\nSEND_COMMAND dvMFTX,\"\'?VIDIN_RES_AUTO\'\"\nReturns a COMMAND of the form:\nVIDIN_RES_AUTO-<ENABLE|DISABLE>'),
                                    
                                    'VIDIN_RES_AUTO':(7,['ENABLE','DISABLE'],
                                    'VIDIN_RES_AUTO \n\nEnables or disables the Auto \nmode (for automatically \ndetermining the resolution) on \nthe Transmitter.\nNote: Send to Port 7 or Port 8.',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'VIDIN_RES_AUTO-<ENABLE|DISABLE>\'\"\n\nExample:\nSEND_COMMAND dvMFTX,\"\'VIDIN_RES_AUTO-ENABLE\'\"'),
                                     
                                    '?VIDIN_RES_REF':(7,[''],
                                    '?VIDIN_RES_REF \n\nRequests the resolution and\nrefresh rate of the video through\nthe Transmitter.',
                                    'Note: Send to Port 7 or Port 8.\nSyntax:\nSEND_COMMAND <DEV>,\"\'?VIDIN_RES_REF\'\"\nVariables:\n horizontal = An integer value representing the horizontal.\n vertical = An integer value\nrepresenting the vertical. May have an additional\nqualifier such as \'i\' or \'p\'.\n rate = An integer value representing the refresh rate.\nExample:\nSEND_COMMAND dvMFTX,\"\'?VIDIN_RES_REF\'\"\nReturns a COMMAND of the form:\nVIDIN_RES_REF-<horizontal>x<vertical>,<rate>'),

                                    'VIDIN_RES_REF':(7,[''],
                                    'VIDIN_RES_REF Sets the resolution and\nrefresh rate of the video\nthrough the Transmitter\n(disable VIDIN_RES_AUTO\nprior to sending).',
                                    'Important: Send to Port 7 or Port 8.\nSyntax:\nSEND_COMMAND <DEV>,\"\'VIDIN_RES_REF- <horizontal>x<vertical>,<rate>\'\"\nVariables:\n horizontal = An integer value representing the horizontal.\n vertical = An integer value representing the vertical. May have an additional qualifier\nsuch as \'i\' or \'p\'.\n rate = An integer value representing the refresh rate.'),

                                    '?VIDIN_PREF_EDID':(8,[''],
                                    'VIDIN_PREF_EDID \nRequests the preferred\nresolution of the EDID source\nfor the VGA video input.\nNote: This command applies\nto all DXLink Transmitters\nexcept the HDMI TX.',
                                    'Important: Send to Port 8.\nSyntax:\nSEND_COMMAND <DEV>,\"\'?VIDIN_PREF_EDID\'\"\nExample:\nSEND_COMMAND dvMFTX,\"\'?VIDIN_PREF_EDID\'\"\nReturns a COMMAND of the form:\nVIDIN_PREF_EDID-<resolution,refresh>'),
                                    
                                    'VIDIN_PREF_EDID':(8,['640x480, 60','640x480, 72','640x480, 75','800x600, 60','800x600, 72','800x600, 75','1024x768, 60','1024x768,70','1024x768, 75','1280x720p, 50','1280x720p, 60','1280x768, 60','1280x800, 60','1280x1024, 60','1360x768, 60','1440x900, 60','1600x1200, 60','1680x1050, 60','1920x1080, 60','1920x1080p, 50','1920x1080p, 60','1920x1200, 60'],
                                    'VIDIN_PREF_EDID \n\nSets the preferred resolution\nof the EDID source for the\nVGA video input.\nNote: This command applies\nto all DXLink Transmitters\nexcept the HDMI TX.',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,\"\'VIDIN_PREF_EDID - <resolution,refresh>\'\"\nVariable:\n resolution,refresh = <for supported input resolutions and refresh rates, see the tables\nstarting on page 126.>\nExamples:\nSEND_COMMAND dvMFTX,\"\'VIDIN_PREF_EDID-1920x1080p,60\'\"'),
                                    
                                    '?VIDIN_EDID':(8,[''],
                                    '?VIDIN_EDID \nRequests which EDID is\nbeing presented to the source\non the video port addressed\nby the D:P:S.',
                                    'Important: Send to Port 8.\nSyntax:\nSEND_COMMAND <DEV>, \"\'?VIDIN_EDID\'\"\nExample:\nSEND_COMMAND VIDEO_INPUT_1,\"\'?VIDIN_EDID\'\"\nReturns a COMMAND of the form:\nVIDIN_EDID-<source>\nSee the\nVIDIN_EDID command for the potential sources.'),
                                    
                                    'VIDIN_EDID':(8,[''],
                                    'VIDIN_EDID \nSets the EDID to be\npresented to the source on\nthe video input port\naddressed by the D:P:S.',
                                    'Important: Send to Port 8 (or Port 7 - only for the last variable listed).\nSyntax:\nSEND_COMMAND <DEV>,\"\'VIDIN_EDID-<source>\'\"\nVariables:\nsource = ALL RESOLUTIONS, USER EDID 1* (Port 8\nonly)\nMIRROR OUT 1** (Port 7 only)\nExample:\nSEND_COMMAND VIDEO_INPUT_1,\"\'VIDIN_EDID-ALL RESOLUTIONS\'\"\n* \"USER EDID 1\" must be written to the TX using DGX Configuration\nSoftware (see\npage 140).\n** The HDMI port mirrors downstream EDID of the connected DXLink device.\nTip: For troubleshooting purposes, \"MIRROR OUT 1\" can be sent to Port 7 of the TX\n(or Port 6 of\n the RX), which effectively acts like a hotplug and refreshes the EDID.'),
                                    
                                    '?VIDIN_HDCP':(7,[''],
                                    '?VIDIN_HDCP \nRequests the video HDCP\ncompliance of the video input\nport addressed by the D:P:S.',
                                    'Important: Send to Port 7.\nSyntax:\nSEND_COMMAND <DEV>,\"\'?VIDIN_HDCP\'\"\nExample:\nSEND_COMMAND dvTX,\"\'?VIDIN_HDCP\'\"\nReturns a COMMAND of the form:\nVIDIN_HDCP-<ENABLE|DISABLE>'),
                                    
                                    'VIDIN_HDCP':(7,['ENABLE','DISABLE'],
                                    'VIDIN_HDCP \n\nSets the video input HDCP \ncompliance setting of the \nvideo input port addressed by \nthe D:P:S. \n\nCaution: For sources (such\n as DVD and Blu-Ray players)\nthat do not support\nnon-compliant displays,\ndisabling the HDCP\ncompliance is not\nrecommended and may\naffect DXLink performance.',
                                    'Important: Send to Port 7.\nNote: When VIDIN_HDCP is disabled, the addressed video input will appear\nto any source as not being HDCP compliant. For PC sources that encrypt all\nvideo when connected to an HDCP compliant display, disabling HDCP\ncompliance on the input will cause the PC to send non-encrypted video which\ncan then be routed to non-compliant displays and video conferencing systems.\nThis command is not applicable to the analog video port.\nNote: After changing this setting, it may be necessary to disconnect and\nre-connect PC sources.\n\nSyntax:\nSEND_COMMAND <DEV>,\"\'VIDIN_HDCP-<ENABLE|DISABLE>\'\"\nExample:\nSEND_COMMAND dvTX,\"\'VIDIN_HDCP-ENABLE\'\"\nEnables the HDCP Compliance of video input port (#1 based on D:P:S).'),
                                    
                                    '?AUDIN_FORMAT_AUTO':(7,[''],
                                    '?AUDIN_FORMAT_AUTO \nRequests the setting (Enable\nor Disable) for automatically\ndetecting the audio source\nformat through the TX.',
                                    'Syntax:\nSEND_COMMAND <DEV>,\"\'?AUDIN_FORMAT_AUTO\'\"\nExample:\nSEND_COMMAND dvTX,\"\'?AUDIN_FORMAT_AUTO\'\"\nReturns a COMMAND of the form:\nAUDIN_FORMAT-AUTO<ENABLE|DISABLE>'),
                                    
                                    'AUDIN_FORMAT_AUTO':(7,['ENABLE','DISABLE'],
                                    'AUDIN_FORMAT_AUTO \n\nSets audio source format to \nautomatically detect the audio \nthrough the TX.',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,"\'AUDIN_FORMAT_AUTO-<ENABLE|DISABLE>\'"\n\nExample:\nSEND_COMMAND dvTX,"\'AUDIN_FORMAT_AUTO-ENABLE\'"'),
                                    
                                    '?AUDIN_FORMAT':(7,[''],
                                    '?AUDIN_FORMAT \nRequests the setting for the\naudio source format.',
                                    'Syntax:\nSEND_COMMAND <DEV>,\"\'?AUDIN_FORMAT\'\"\nVariable:\nformat = HDMI, SPDIF, ANALOG\nExample:\nSEND_COMMAND dvTX,\"\'?AUDIN_FORMAT\'\"\nReturns a COMMAND of the form:\nAUDIN_FORMAT-<format>'),
                                    
                                    'AUDIN_FORMAT':(7,['HDMI', 'SPDIF', 'ANALOG'],
                                    'AUDIN_FORMAT  \n\nSelects the audio input source \nthat will be embedded on the \nHDMI signal through the TX.\n\nNote: When the Multi-Format \nTX is set to route digital video \n(input 7), you can select from \nthe HDMI, SPDIF, or ANALOG \naudio inputs. When it is set to \nroute analog video (input 8), \nyou can only select the SPDIF \nor ANALOG audio input \n(see the VI<input>O<output> \ncommand).',
                                    'Syntax:\n\nSEND_COMMAND <DEV>,"\'AUDIN_FORMAT-<format>\'"\nVariable:\n\nformat = HDMI, SPDIF, ANALOG\n\nExample:\nSEND_COMMAND dvTX,\"\'AUDIN_FORMAT-ANALOG\'\"\n\nImportant: The order of precedence (HDMI embedded audio, S/PDIF, analog) can be \noverridden with this command; however, you must first send AUDIN_FORMAT_AUTODISABLE to disable the auto format function, or the audio format will automatically switch \nback anytime the order of precedence is violated.\nNote: S/PDIF signals are not available over the Wallplate TX or Decor Wallplate TX.'),

                                    '?USB_HID_SERVICE':(5,[''],
                                    '?USB_HID_SERVICE \nRequests the status for\nthe USB HID pass\nthrough setting (Enable or\nDisable).',
                                    'Syntax:\nSEND_COMMAND <DEV>,\"\'?USB_HID_SERVICE\'\"\nExample:\nSEND_COMMAND dvTX,\"\'?USB_HID_SERVICE\'\"\nReturns a COMMAND of the form:\nUSB_HID_SERVICE-<ENABLE/DISABLE>'),

                                    'USB_HID_SERVICE':(5,['ENABLE','DISABLE'],
                                    'USB_HID_SERVICE \n\nSets the USB HID pass \nthrough to Enable or \nDisable.)',
                                    'Note: When enabled, the USB port addressed by D:P:S is running in auto switching mode.\n\nSyntax:\nSEND_COMMAND <DEV>,\"\'USB_HID_SERVICE-<ENABLE|DISABLE>\'\"\n\nExample:\nSEND_COMMAND dvTX,\"\'USB_HID_SERVICE-ENABLE\'\"\n\nNote: This command persists through power cycling.'),

                                    
                                    }}
       
        
        self.obj = []
        self.result_string = ''
        self.send.Disable()       
        self.dxlink_model = dxlink_model
        self.onQuery(None)
        self.deviceOlv.SetColumns([ColumnDefn("Model", "center", 130, "model"),
                                   ColumnDefn("IP", "center", 100, "ip"),
                                   ColumnDefn("Device", "center", 80, "device")])
        self.deviceOlv.CreateCheckStateColumn()
        self.deviceOlv.SetObjects(device_list)
        objects = self.deviceOlv.GetObjects()
        for obj in objects:
            self.deviceOlv.ToggleCheck(obj)
        self.deviceOlv.RefreshObjects(objects)
        self.waiting_result = True
        dispatcher.connect(self.result, signal="send_command result", 
                            sender = dispatcher.Any)
        self.time_out = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimeOut, self.time_out) 
    #----------------------------------------------------------------------
    def onCommandCombo(self, event):

        self.action_combo.SetValue('Actions')
        self.updateActionCombo(self.command_combo.GetValue())
        self.send.Enable()
        
    def onActionCombo(self, event):
       
        self.updateString()
        pass
        
    def onQuery(self, event):
        
        old = self.command_combo.GetValue()
        self.command_combo.Clear()
        self.description.Clear()
        self.syntax.Clear()
        if self.send_query.GetValue():
            self.command_combo.SetValue('Query')
        else:
            self.command_combo.SetValue('Commands')
        
        for item in sorted(self.rx_tx_commands[self.dxlink_model]):  #sorting by second dimension 
            if self.send_query.GetValue():
                if item[:1] == '?': # only add query
                
                    self.command_combo.Append(item)
            else:
                if item[:1] != '?': # only add commands
                    
                    self.command_combo.Append(item)
        
        if self.send_query.GetValue():
            self.action_combo.Enable(False)
            for item in self.command_combo.GetItems():
                if item[1:] == old:
                    self.command_combo.SetValue(item)
                    self.onCommandCombo(None)
                    break
                else:
                    self.string_port.Clear()
                    self.stringcommand.Clear()
        else:
            self.action_combo.Enable(True)
            for item in self.command_combo.GetItems():
                if item == old[1:]:
                    self.command_combo.SetValue(item)
                    self.onCommandCombo(None)
                    break
                else:
                    self.string_port.Clear()
                    self.stringcommand.Clear()
    
    def updateActionCombo(self, selection):
        #phasesList = {"rx": self.rxList , "tx": self.txList , "mftx": self.mftxList }
        self.action_combo.Clear()
        for item in self.rx_tx_commands[self.dxlink_model][selection][1]:
            #print item
            self.action_combo.Append(item)
            self.port = self.rx_tx_commands[self.dxlink_model][selection][0]
            self.description.SetValue(self.rx_tx_commands[self.dxlink_model][selection][2])
            self.syntax.SetValue(self.rx_tx_commands[self.dxlink_model][selection][3])
        self.action_combo.SetValue("Actions")
        self.updateString()


    def updateString(self, Data=None):
        
        if self.action_combo.GetValue() == "Actions":
            action = ""
        elif self.action_combo.GetValue() == "":
                action = ''
        else:
            action = "-" + self.action_combo.GetValue()
        output = self.command_combo.GetValue() + action 
        self.string_port.SetValue(str(self.port))
        self.stringcommand.SetValue(output)

    def onGetAll(self, event):
        if self.get_all.GetValue():
            
            self.send.Enable(True)
            self.action_combo.Enable(False)
            self.command_combo.Enable(False)
            self.send_command.Enable(False)
            self.send_query.SetValue(True)
            self.onQuery(None)
        else:
            self.action_combo.Enable(True)
            self.command_combo.Enable(True)
            self.send_command.Enable(True)
            self.send.Enable(False)
        
    def onResult(self, sender):
        
        self.results.SetLabel('Result:   ' + sender)

    def onSend(self, event):
        
        objects = self.deviceOlv.GetObjects()
        for obj in objects:
            if self.deviceOlv.IsChecked(obj):
                #self.updateString(obj)
                if obj.device == " ":
                    device = 0
                else:
                    device = obj.device
                if obj.system == " ":
                    system = 0
                else:
                    system = obj.system
                
                if self.get_all.GetValue():
                    total = len(self.command_combo.GetItems())
                    #print total
                    dlg = wx.ProgressDialog("Sending command to selected device with results listed below ",'Sending command to selected device',
                            maximum = total,
                            parent = self.parent,
                            style =  wx.PD_APP_MODAL
                             | wx.PD_CAN_ABORT
                             | wx.PD_AUTO_HIDE
                             | wx.PD_SMOOTH
                             #| wx.PD_ELAPSED_TIME 
                             )
            
                            
                    count = 0 
                    abort = False
                    for item in self.command_combo.GetItems():
                        count += 1
                        #print count
                        #self.command_combo.SetValue(item)
                        #print item
                        #self.onCommandCombo(None)
                        
                        #print self.command_combo.GetValue()
                        
                        output = "send_command " + str(device) + ":" + str(self.rx_tx_commands[self.dxlink_model][item][0]) + ":" + str(system) + ", " + "\"\'" + str(item) + "\'\""
                        #print output
                        info = ['SendCommand', obj, self.parent.telnet_timeout_seconds, output, str(self.rx_tx_commands[self.dxlink_model][item][0])]
                        #print info
                        self.parent.actionItems.append(obj)
                        self.parent.telnetjobqueue.put(['SendCommand', obj, self.parent.telnet_timeout_seconds, output , str(self.rx_tx_commands[self.dxlink_model][item][0])])
                        #time_out = 0
                        self.time_out.Start(5000)
                        while self.waiting_result:
                            
                                   
                             
                            time.sleep(.5)
                            #time_out += 1
                            #if time_out >= 5:
                            #    self.waiting_result = False
                            (abort, skip) = dlg.Update (count,("Sending command %s of %s to device %s \n" + self.result_string) % (count,total,device))
                            #print abort
                        if not abort:
                            #self.parent.displayProgress()
                            abort = False
                            self.time_out.Stop()
                            self.waiting_result = True
                            break
                        self.time_out.Stop()
                        self.waiting_result = True
                        
                    #self.parent.actionItems = []
                    #self.completionlist = []
                    #self.errorlist = []
                    self.parent.displayProgress()
                    self.result_string = ''
                    dlg.Destroy()
                        
                        
                
                else:
                    output = "send_command " + str(device) + ":" + str(self.string_port.GetValue()) + ":" + str(system) + ", " + "\"\'" + str(self.stringcommand.GetValue()) + "\'\""
                    #print output
                    info = ['SendCommand', obj, self.parent.telnet_timeout_seconds, output , str(self.port)]
                    self.parent.actionItems.append(obj)
                    self.parent.telnetjobqueue.put(['SendCommand', obj, self.parent.telnet_timeout_seconds, output , str(self.port)])
                
                    self.parent.displayProgress()
    
    def onTimeOut(self, event):
        self.waiting_result = False
        #print 'timeout'
    
    def result(self, sender):
    
        self.waiting_result = False
        self.result_string = sender
        #print sender
        #time.sleep(1)
        #print result maybe
        
    def OnExit(self, event):

        self.Destroy()
        
    def OnAbort(self, event):
        
        self.parent.abort = True
        self.Destroy()
            
    def getModelandDevice(self):
        
        if self.obj.model == ' ' or self.obj.model == '' or self.obj.device == ' ' or self.obj.device == '':
            self.parent.jobqueue.put(['GetTelnetInfo', self.obj,  self.parent.telnet_timeout_seconds])
            self.parent.actionItems.append(self.obj)
            self.parent.displayProgress()         
        if self.obj.model[12:14] == 'TX' or self.obj.model[12:14] == 'WP'or self.obj.model[12:15] == 'DWP'or self.obj.model[12:16] == 'MFTX':
            self.dxlink_model = 'tx'
        elif self.obj.model[12:14] == 'RX':
            self.dxlink_model = 'rx'
        else:
            self.NotDXLink()  

    def NotDXLink(self):
        
        dlg = wx.MessageDialog(parent=self, message= 'This does not appear to be a DXLink Device \n Do you want to continue?', 
                                   caption = 'Do you want to continue?',
                                   style = wx.OK | wx.CANCEL
                                   )
        if  dlg.ShowModal() == wx.CANCEL:
            self.parent.abort = True
            dlg.Destroy()
            self.Destroy()
        else:
            dlg.Destroy()
            self.dxlink_model = 'tx'
            self.obj.device = '0'
        '''self.lblname = wx.StaticText(self, label="This is not a DXLink Device", pos=(20,40))

        self.cancel = wx.Button(self, label="Cancel", pos=(225, 40))
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel)
        
        self.SetSize((220,220))'''
    
     
        






























































































