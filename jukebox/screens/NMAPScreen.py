import os
from Button import Button
from RenderText import RenderText
import pygame
import pexpect
import os

class NMAPScreen:
    def __init__(self, parent):
        self.net_knowledge=[]    
        self.parent=parent

    def OnEnter(self):
        with open("knownmachines","r") as f:
            for l in f:
                print l
                arr=l.split(";")
                print arr
                self.net_knowledge.append((arr[0].rstrip().lstrip(), arr[1].rstrip().lstrip(), arr[2].rstrip().lstrip(),arr[3].rstrip().lstrip()))


    def OnDraw(self, screen):
        screen.fill((0,0,0))
        pos = RenderText(screen,"NMAP results", [0,200], {'align-center':"",'bold':"",'font':self.parent.font_big})
        try:
            o=open("logdone","r")
            d=self.Parser(o.read())
            message=""
            # print d
            lst = d.keys()
            lst.sort(key=lambda x:int(x.split(".")[-1]))
            
            for host in lst:
                message+=host+"   "
                if d[host].has_key("id_text") and len(d[host]["id_text"])>0:
                    message+=d[host]["id_text"]
                elif d[host].has_key("id_name"):
                    #message+=random.choice(("smells like ","feels like ", "looks like ", ""))+d[host]["id_name"]
                    message+=d[host]["id_name"]
                elif d[host].has_key("brand"):
                    message+=d[host]['brand']
                else:
                    message += "unknown"
                message+="\n"
            RenderText(screen, message, [150,pos[1]+50], {'font':self.parent.font_big})
        except IOError:
            pass
        try:
            o=open("log","r")
        except:
            print "Resuming scanning"
            os.system("touch log")
            os.system("sudo ./scan_net &")
        return
        
        
    def OnClick(self, event):
        os.system("sudo killall nmap")
        os.system("sudo rm log")
        self.parent.ChangeScreen("MainScreen")
        return
    
    def OnFlip(self):
        pygame.display.flip()
        

    def Parser(self, s):
        hosts={}
        host=None
        for l in s.split("\n"):
            if l.startswith("Nmap scan report"):
                host = l.split(" ")[-1].rstrip(")").lstrip("(")
                hosts[host]=dict()

            if l.startswith("MAC Address"):
                mac = l.split(" ")[2]
                brand = " ".join(l.split(" ")[3:]).rstrip(")").lstrip("(")
                hosts[host]["mac"] = mac
                hosts[host]["brand"] = brand
        for h in hosts.keys():
            for k in self.net_knowledge:
                if k[0]=='ip':
                    if k[1]==h:
                        hosts[h]['id_name']=k[2]
                        hosts[h]['id_text']=k[3]
                if k[0]=='mac' and hosts[h].has_key("mac"):
                    if k[1]==hosts[h]["mac"]:
                        hosts[h]['id_name']=k[2]
                        hosts[h]['id_text']=k[3]
        with open("log2","w") as l:
            l.write(str(self.net_knowledge))
            l.write('\n')
            l.write(str(hosts))
        return hosts
        
