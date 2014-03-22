from threading import Thread
import socket
import datetime
from pydispatch import dispatcher
import wx


########################################################################
class SniffDHCPThread(Thread):
    
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Init Worker Thread Class."""
        self.listen = True 
        self.parent = parent
        Thread.__init__(self)
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        
        try:
            port = 67
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind(("", port))
            
        except:
            # something has already blocked the port, multiple instances can run without error because we used SO_REUSEADDR
            self.parent.portError = True 
            while True:
                pass 
        
        dispatcher.connect(self.stop, signal="start_stop_dhcp", sender=dispatcher.Any) #listen for pubsub to stop this thread
        #dispatcher.send(signal="tray_status", sender="dhcp_listen_true")
        
        while True:
            
            ''' receive packets from port 67
            msg is the data part of the packet
            addr is the from address and port number (not used)'''
            msg, addr = self.s.recvfrom(1024)
            
            # check if it is a DHCP "request" message 
            if ((msg[240]=="\x35" and msg[241]=="\x01" and msg[242]=="\x03")):  
                
                # extract the sending mac address
                mac_address = ((msg[28].encode("hex") + ":" + 
                                msg[29].encode("hex") + ":" + 
                                msg[30].encode("hex") + ":" + 
                                msg[31].encode("hex") + ":" + 
                                msg[32].encode("hex") + ":" +
                                msg[33].encode("hex") 
                              )) 

                #process only the DHCP options portion of the packet
                self.dhcp_options = msg[243:]
                ip_address = ''
                hostname = ''
                
                while self.dhcp_options:        
                        
                    opt = self.dhcp_options[0]
                    
                    #end of packet 
                    if opt == '\xff':
                        self.dumpByte() #move to the next byte
                        break
                    
                    # padding in packet
                    if opt == '\x00':
                        self.dumpByte() #move to the next byte
                        continue
                    
                    # requested IP
                    if opt == '\x32':
                        
                        #We need to move to the data, and read the length of it                        
                        ip_address = '.'.join(str(ord(c)) for c in (self.readData(self.getToData())))  # convert what we got from hex to decimal and put into string with dots   
                        continue
                    
                    # hostname 
                    if opt == '\x0c':
                                                
                        hostname = ''.join((c) for c in (self.readData(self.getToData()))) # convert what we got to a string    
                        continue
                    
                    # if we have made it this far this is an dhcp_option we can skip
                   
                    #print " ".join(hex(ord(n)) for n in opt)
                    #print " ".join(hex(ord(n)) for n in self.dhcp_options)
                    
                    self.readData(self.getToData())
                    
                    #continue
            
                           
                # lets pack that information into a dictionary
                
                info = {}
                
                info['ip'] = ip_address
                if ip_address == '':
                    continue
                
                if hostname != []:
                    info['hostname'] = hostname    
                else:
                    info['hostname'] = ''
                
                info['serial'] = ''
                info['firmware'] = ''
                info['device'] = ''
                info['model'] = ''
                info['mac'] = mac_address
                info['time'] = datetime.datetime.now()
                info['ip_type'] = ''
                info['gateway'] = ''
                info['subnet'] = ''
                info['master'] = ''
                info['ip_type'] = ''
                info['gateway'] = ''
                info['subnet'] = ''
                info['system'] = ''
                
                # check if we have been told to stop listening
                if self.listen == True:
                    
                    #send it processed packet to the main loop
                    wx.CallAfter(self.postTime, info)
             
    def readData(self, data_length):
        
        read_data = []
                
        for i in range(0, data_length):
            read_data.append(self.dhcp_options[0])
            self.dhcp_options = self.dhcp_options[1:]
        return(read_data)    
    
    def dumpByte(self):
        
        self.dhcp_options = self.dhcp_options[1:] #move one byte   
        
    def getToData(self):
        
        self.dumpByte() # move to data length
                        
        data_length = ord(self.dhcp_options[0]) # get data length
        
        self.dumpByte() #move to start of data  
        
        return(data_length)     
                    
    def stop(self, sender):

        if sender == "start":
            self.listen = True
            #dispatcher.send(signal='tray_status', sender='dchp_listen_true')
            
        if sender == "stop":
            self.listen = False
            #dispatcher.send(signal='tray_status', sender='dchp_listen_false')            
           
             
    #----------------------------------------------------------------------
    def postTime(self, info):
        """
        Send data to GUI
        """   
        #dispatcher.send(signal="tray_status", sender="dhcp_incoming")     
        dispatcher.send( signal="Incoming Packet", sender=info )
 
########################################################################
