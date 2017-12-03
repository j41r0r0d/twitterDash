# -*- coding: utf-8 -*-
# Created by : Jairo J. Rodriguez
# email Address : rodriguezjfz@gmail.com
# Description : Twitter Dash Board Implementation 
# Last MOdificatio : Nov 21, 2017

import xml.dom.minidom
import urllib, os, tinyurl
import datetime,time, codecs, tweepy, xml.etree.cElementTree as et
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
import twitterbot, twCountryId as twCId


class TwErrorLog(object):
    def CreateErrLog(self,fileName):
        LogFileName=fileName
        logfile=codecs.open(LogFileName,'w',encoding='utf8')
        logfile.write("Twitter Dash Board Started")
        logfile.close()
        
    def WriteInLog(self,fileName,message):
        logfile=codecs.open(fileName,'a', encoding='utf8')
        logfile.write("\n\r" + str(datetime.datetime.now())\
                      +"   "+ message + "\n\r")
        logfile.close()
    
class TwitterActions:
    
    def AuthTwCredentials(self,Obj):
       
        global twapi, myUser
        
        Obj.actionTwitter_Bot_Settings.setEnabled(True)           
        Obj.widget_UserInfo.show()
                                             
        twd_ck = Obj.pTE_ConKey.toPlainText()         
        twd_cs = Obj.pTE_ConSec.toPlainText()        
        twd_ak = Obj.pTE_AccKey.toPlainText()       
        twd_as = Obj.pTE_AccSec.toPlainText()
               
        auth = tweepy.OAuthHandler(twd_ck,
                                   twd_cs)       
        auth.set_access_token(twd_ak,twd_as)
        
        try:
            TwErrorLog.WriteInLog(self,'twitterDash.log', 
                                 "Authenticating user with consumer key : "
                                 +twd_ck)
            twapi = tweepy.API(auth)
            myUser=twapi.me()
            
            TwErrorLog.WriteInLog(self,'twitterDash.log', 
                                 "User "+ "@" + str(myUser.screen_name)\
                                 + " authenticated")                       
            
            Obj.pTE_UsrInf_FollowersCount.show()
            
            Obj.Lbl_UserInfo_FollowersCount.setText("Followers")
            Obj.Lbl_UserInfo_FollowersCount_2.setText("Following")
            Obj.Lbl_UserInfo_UserName.setText("User Name")
            Obj.Lbl_UserInfo_Name.setText("Name")
            Obj.Lbl_UserInfo_GeoEna.setText("Geo Enabled")
            Obj.Lbl_UserInfo_Location.setText("Location")
            Obj.Lbl_UserInfo_CreatedAt.setText("Created at")
            Obj.Lbl_UserInfo_StatusCount.setText("Status Count")
            Obj.Lbl_UserInfo_Description.setText("Description")
            
            Obj.pTE_UsrInf_FollowersCount.setPlainText(
                    str(myUser.followers_count))
            
            
            Obj.pTE_UsrInf_FriendsCount.setPlainText(
                    str(myUser.friends_count))
            Obj.pTE_UsrInf_UserName.setPlainText(myUser.screen_name)
            Obj.pTE_UsrInf_Name.setPlainText(myUser.name)
            Obj.pTE_UsrInf_GeoEnabled.setPlainText(str(myUser.geo_enabled))
            Obj.pTE_UsrInf_Location.setPlainText(myUser.location)
            Obj.pTE_UsrInf_StatusCount.setPlainText(
                    str(myUser.statuses_count))
            Obj.pTE_UsrInf_Description.setPlainText(myUser.description)
            Obj.pTE_UsrInf_CreatedAt.setPlainText(
                    str(myUser.created_at))
            
            Obj.pTE_UsrInf_FollowersCount.setPlainText(
                    str(myUser.followers_count))
            
            url=myUser.profile_image_url

            data = urllib.request.urlopen(url).read()

            Obj.label.pixmap=QPixmap()            
            image = QtGui.QImage()         
            image.loadFromData(data)

            scaled_image = image.scaled( Obj.label.size(),\
                                        QtCore.Qt.KeepAspectRatio)

            Obj.label.setPixmap(QtGui.QPixmap(scaled_image))
                    


        except Exception as err:
            errMsg = str(err)
            TwErrorLog.WriteInLog(self,'twitterDash.log', errMsg) 
            self.msgBox(errMsg,"Error Message","Information")
            Obj.actionTwitter_Bot_Settings.setEnabled(False) 
            Obj.widget_UserInfo.hide()
            pass
       
    def SaveTwCredentials(self,Obj):
        
        twd_ck=Obj.pTE_ConKey.toPlainText()
        twd_cs=Obj.pTE_ConSec.toPlainText()
        twd_ak=Obj.pTE_AccKey.toPlainText()
        twd_as=Obj.pTE_AccSec.toPlainText()
        twd_un=Obj.pTE_UserName.toPlainText()

   
        root = et.Element("root")
        doc = et.SubElement(root,"doc")
        
        
        user = et.SubElement(doc,"user",name=twd_un)
        et.SubElement(user,"credential",name="consumer key", value=twd_ck)
        et.SubElement(user,"credential",name="consumer secret", value=twd_cs)
        et.SubElement(user,"credential",name="access key", value=twd_ak)
        et.SubElement(user,"credential",name="access secret", value=twd_as)
        
        tree = et.ElementTree(root)
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(caption="Save Credential file",
                                                  options=options, filter="XML Files (*.xml)\
                                                  ;;All (*.*)")
        tree.write(fileName)
        
    
    def msgBox(self,messageText,msgWindowTitle,msgType):
        global msg
        msg = QMessageBox()
        if msgType == "warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        elif msgType == "information":            
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
        elif msgType == "timed":
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.NoButton)
            self.timer = QtCore.QTimer()
            self.timer.singleShot(5000,self.msgCloseSlot)
                               
        msg.setWindowTitle(msgWindowTitle)
        msg.setText(messageText)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()
        return retval
    
    def msgbtn(self,i):
        return i.text()
    
    def msgCloseSlot(self):
        msg.destroy()
    
    
    def DeleteTwCredentials(self,Obj):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(caption="Delete Credential file",
                                                  options=options, filter="XML Files (*.xml)\
                                                  ;;All (*.*)")
        if fileName != "":
            retval=self.msgBox(
                    "File "+fileName+" will be deleted !!!",\
                    "Delete Credentials File","warning")                       
            if retval == QMessageBox.Ok :
                os.remove(fileName)
            else :
                pass
        else :
            pass
        
        
    def LoadTwCredentials(self,xmlFile,Obj):
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(caption="Open Credential file",
                                                  options=options, filter="XML Files (*.xml)\
                                                  ;;All (*.*)")
        xmlFile=fileName
                
        try: 
            doc=xml.dom.minidom.parse(xmlFile)           
            for node in doc.getElementsByTagName("user"):
                user=node.getAttribute("name")
                Obj.pTE_UserName.setPlainText(str(user))
                for i in node.childNodes:
                    credential=i.getAttribute("name")
                
                    key = i.getAttribute("value")
                    if "consumer key" in credential :
                        Obj.pTE_ConKey.setPlainText(key)
                    if "consumer secret" in credential :
                        Obj.pTE_ConSec.setPlainText(key)
                    if "access key" in credential :
                        Obj.pTE_AccKey.setPlainText(key)
                    if "access secret" in credential :
                        Obj.pTE_AccSec.setPlainText(key)
        except Exception as err:
            errMsg = str(err)
            TwErrorLog.WriteInLog(self,'twitterDash.log', errMsg) 
            self.msgBox(errMsg,"Error Message","Information")  
            pass  
        
    def itemSelectionHandler(self):
        global TTLocal, TTGlobal
        
        CidAux=(str(ui.cBox_BotTTLocal.currentText()))
        Cid=CidAux.split("-")
        
        trendsLocal = twapi.trends_place(int(Cid[1]))
        trendsGlobal = twapi.trends_place(1)
        dataLocal=trendsLocal[0]
        dataGlobal = trendsGlobal[0]
        trendsLocal=dataLocal['trends']
        trendsGlobal=dataGlobal['trends']

        TTLocal=[trendLocal['name'] for trendLocal in trendsLocal]
        TTGlobal=[trendGlobal['name'] for trendGlobal in trendsGlobal]        
        
        ui.lW_GlobalTrending.clear()
        ui.lW_LocalTrending.clear()
        
        for indx in range (len(TTLocal)):
            ui.lW_LocalTrending.addItem(TTLocal[indx])
        
        
        for indx in range (len(TTGlobal)):
            ui.lW_GlobalTrending.addItem(TTGlobal[indx])
    
    def LoadBotFile(self):
        
        global Botfile,f
               
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        BotfileName, _ = QFileDialog.getOpenFileName(
                caption="Load Bot Setting",options=options,\
                filter="Bot Setting File(*.bsf);;All (*.*)")
        ui.pTE_BotFileName.setPlainText(BotfileName)        
        
        Botfile=codecs.open(BotfileName,'r',encoding='utf8')
        f=Botfile.readlines()
        Botfile=codecs.open(BotfileName,'r',encoding='utf8')
        BottextFile=Botfile.read()
        ui.pTE_BotFileEditt.setPlainText(BottextFile)
    
    def MediaLocation(self):
        
        global MediaFile
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        BotMediaLocation = QFileDialog.getExistingDirectory()
        ui.pTE_BotMediaLocation.setPlainText(BotMediaLocation)        

    
    def SaveBotFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        BotfileName, _ = QFileDialog.getSaveFileName(
                caption="Save Bot Setting",options=options,\
                filter="Bot Setting File(*.bsf);;All (*.*)")
        Botfile=codecs.open(BotfileName,'w',encoding='utf8')
        Bottext=ui.pTE_BotFileEditt.toPlainText()
        Botfile.write(Bottext)
        
    def OpenBotWithExternal(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        BotfileName, _ = QFileDialog.getOpenFileName(
                caption="Load Bot Setting",options=options,\
                filter="Bot Setting File(*.bsf);;All (*.*)")
        os.system('start '+ BotfileName)

    def destroyStatuses(self,Obj):
        statusCount=0
        sBar=ui.pBarDestroyingStatuses
        sBar.setValue(0)
        ui.widget_StatusBar.show()        
        retval=self.msgBox(               
                "Twitter Statuses will be deleted !!!",\
                "Delete Previous Statuses",\
                "warning")


        if retval == QMessageBox.Ok :
                #myUser=twapi.me()
                statusescount=myUser.statuses_count
                sBar.setMaximum(statusescount-31)

                if ((statusescount-31)==0):
                            self.msgBox(               
                            "No Statuses to be destroyed",\
                            "Delete Previous Statuses",\
                            "information")

                            pass
                        
                for status in tweepy.Cursor(twapi.user_timeline).items():
                    try:
                        statusCount=statusCount+1
                        time.sleep(5)
                        sBar.setValue(statusCount)
                        sBar.show()
                        twapi.destroy_status(status.id)
                        TwErrorLog.WriteInLog(self,'twitterDash.log',\
                                              "Status ID "+str(status.id) + " destroyed")
                    except Exception as errMsg:
                        TwErrorLog.WriteInLog(self,'twitterDash.log', str(errMsg))
                        self.msgBox(errMsg,"Error Message","Information")
                        pass                   
                TwErrorLog.WriteInLog(self,'twitterDash.log',\
                              str(statusescount-31) +" Previous statuses destroyed")
                ui.widget_StatusBar.hide()
        else :
            pass
             
    
    def executeBot(self,Obj):
        Sline=""
        twline=""
        TwErrorLog.WriteInLog(self,'twitterDash.log', "Twitter Dash Bot initiated")
        num_lines = ui.pTE_BotFileEditt.document().blockCount()
        namesLoc=TTLocal
        namesGlo=TTGlobal
        print(num_lines)
        try:
            twtime=int(ui.pTE_BotPubFreq.toPlainText())
        except:
            pass
        
        #f=Botfile.readlines()
        mediaFile=ui.pTE_BotMediaLocation.toPlainText()

        for line in f:
           try:
               self.itemSelectionHandler()
               if line.find("[media]") >= 0:
                    MSline=line.split(" ")
                    mediaFile="images/" + str(MSline[1])
                    text=MSline[2]
                    twapi.update_with_media(mediaFile,text+namesLoc[1]+" "+ namesLoc[2])
                    TwErrorLog.WriteInLog(self,'twitterDash.log',"Media file "+ mediaFile + " published")                   
                    time.sleep(twtime)

               elif line.find("[ttl]") >=0:
                   twitTrendingsLocal ="Trending Topics Venezuela (" + str(datetime.datetime.now()
                		 ) + " GMT): " +\
                        "\n[1]" + namesLoc[0] +\
                        "\n[2]"+ namesLoc[1]+\
                        "\n[3]"+ namesLoc[2]+\
                        "\n[4]"+ namesLoc[3]+\
                        "\n[5]"+ namesLoc[4]+\
                        "\n[6]"+ namesLoc[5]+\
                        "\n[7]"+ namesLoc[6]+\
                        "\n[8]"+ namesLoc[7]+\
                        "\n[9]"+ namesLoc[8]+\
                        "\n[10]"+ namesLoc[9]
                   #print(twitTrendingsLocal)
                   try:
                       twapi.update_status(twitTrendingsLocal)
                       TwErrorLog.WriteInLog(self,'twitterDash.log',twitTrendingsLocal)
                   except Exception as err:
                       errMsg = str(err)
                       TwErrorLog.WriteInLog(self,'twitterDash.log', errMsg) 
                       self.msgBox(errMsg,"Error Message","timed")  
                       pass  

                   
               elif line.find("[ttg]") >=0:
                   twitTrendingsGlobal ="World Trending Topics (" + str(datetime.datetime.now()
                		 ) + " GMT): " +\
                        "\n[1]" + namesGlo[0] +\
                        "\n[2]"+ namesGlo[1]+\
                        "\n[3]"+ namesGlo[2]+\
                        "\n[4]"+ namesGlo[3]+\
                        "\n[5]"+ namesGlo[4]+\
                        "\n[6]"+ namesGlo[5]+\
                        "\n[7]"+ namesGlo[6]+\
                        "\n[8]"+ namesGlo[7]+\
                        "\n[9]"+ namesGlo[8]+\
                        "\n[10]"+ namesGlo[9]
                   #print(twitTrendingsGlobal)
                   try:
                       twapi.update_status(twitTrendingsLocal)
                       TwErrorLog.WriteInLog(self,'twitterDash.log',twitTrendingsGlobal)
                   except Exception as err:
                       errMsg = str(err)
                       TwErrorLog.WriteInLog(self,'twitterDash.log', errMsg) 
                       self.msgBox(errMsg,"Error Message","timed")  
                       pass 

               else :
                    Sline=line.split(" ")
                    Sline = [w.replace ('^ttl1',namesLoc[0]) for w in Sline]
                    Sline = [w.replace ('^ttl2',namesLoc[1]) for w in Sline]
                    Sline = [w.replace ('^ttl3',namesLoc[2]) for w in Sline]
                    Sline = [w.replace ('^ttl4',namesLoc[3]) for w in Sline]
                    Sline = [w.replace ('^ttl5',namesLoc[4]) for w in Sline]
                    Sline = [w.replace ('^ttl6',namesLoc[5]) for w in Sline]
                    Sline = [w.replace ('^ttg1',namesGlo[0]) for w in Sline]
                    Sline = [w.replace ('^ttg2',namesGlo[1]) for w in Sline]
                    Sline = [w.replace ('^ttg3',namesGlo[2]) for w in Sline]
                    Sline = [w.replace ('^ttg4',namesGlo[3]) for w in Sline]
                    Sline = [w.replace ('^ttg5',namesGlo[4]) for w in Sline]
                    Sline = [w.replace ('^ttg6',namesGlo[5]) for w in Sline]
                    for n,i in enumerate(Sline):
                        if i.find("http")>=0:
                            Sline[n]=tinyurl.create_one(Sline[n])
                    
                    line=" ".join(Sline)
                    nline=round(len(line)/280)
                    Delta=float(len((line)))/280-nline
                   
                    if Delta > 0.01:
                        nline+1
                        wordC=len(Sline)
                        sentS=int(round(wordC/2))
                   
                    if nline > 1 :
                        for j in range (0,int(nline)):
                            ind=j*sentS
                            twline=" ".join(Sline[ind:(j+1)*sentS])
                           
                            if j > 0 :
                               twline=" ".join(Sline[ind:(j+1)*(sentS+1)])
                        twline=str(j+1)+"/"+str(int(nline))+". "+twline
                       
                        TwErrorLog.WriteInLog(self,'twitterDash.log',"".join(twline))
                        #print("".join(twline))
                        try:
                            twapi.update_status("".join(twline))
                            #time.sleep(15)
                        except Exception as err:
                            errMsg = str(err)
                            TwErrorLog.WriteInLog(self,'twitterDash.log', str(errMsg)) 
                            self.msgBox(str(errMsg),"Error Message","timed")  
                            pass    
                    else:
                        try:
                            twapi.update_status("".join(line))
                            #print("".join(line))
                            TwErrorLog.WriteInLog(self,'twitterDash.log',"".join(line))
                        except Exception as err:
                            errMsg = str(err)
                            TwErrorLog.WriteInLog(self,'twitterDash.log', str(errMsg)) 
                            self.msgBox(str(errMsg),"Error Message","timed")  
                            pass
                        
               time.sleep(twtime*60)        
                                           
           except Exception as errMsg :
               TwErrorLog.WriteInLog(self,'twitterDash.log',str(errMsg))
               self.msgBox(str(errMsg),"Error Message","Information") 
            
        TwErrorLog.WriteInLog(self,'twitterDash.log',"Twitter Dash Bot Finished")
        self.msgBox("Twitter Dash Bot Finished","Information Message","Information")
        if ui.ckBoxBotStatByEmail.isChecked():
            twapi.send_direct_message(
                    myUser.screen_name,text=\
                    'Twitter Publishing has been completed')
    

    
    
    def CloseBotForm(self,Obj):
        self.FormTwitterBot.close()
        
    def showBotForm(self,Obj):
        global ui
               
        self.FormTwitterBot = QtWidgets.QWidget()
        ui =twitterbot.Ui_FormTwitterBot()
        ui.setupUi(self.FormTwitterBot)
        # this for loop sets the twitter country ID for local TT in a Combo boxcls
        
      
        for country in range (len(twCId.Twitter_TTLocationID)):
              cindx=twCId.Twitter_TTLocationID[country][
                      "name"] + "-" +str(twCId.Twitter_TTLocationID[country]\
                      ["woeid"])
              ui.cBox_BotTTLocal.addItem(cindx)
        
        ui.widget_StatusBar.hide()
        ui.cBox_BotTTLocal.activated.connect(self.itemSelectionHandler)  
        ui.pB_BotLdFile.clicked.connect(self.LoadBotFile)
        ui.pB_BotSaveFile.clicked.connect(self.SaveBotFile)
        ui.pB_BotEditFile.clicked.connect(self.OpenBotWithExternal)
        ui.pB_BotDestroy.clicked.connect(self.destroyStatuses)
        ui.pB_BotClose.clicked.connect(self.CloseBotForm)
        ui.pB_BotExecute.clicked.connect(self.executeBot)
        ui.pB_MediaSelect.clicked.connect(self.MediaLocation)

        self.FormTwitterBot.show()
        

                                                    
class XmlFileMngr():
    
    
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
                self,"QFileDialog.getOpenFileName()", "",\
                "All Files (*);;XML Files (*.xml)", options=options)
 
    def openFileNamesDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
                self,"QFileDialog.getOpenFileNames()", ""\
                ,"All Files (*);;XML Files (*.xml)", options=options)
 
    def saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
                self,"QFileDialog.getSaveFileName()",""\
                ,"All Files (*);;XML Files (*.xml)", options=options)

class Ui_Mw_TwitteDash(object):
        
    def setupUi(self, Mw_TwitteDash):
        Mw_TwitteDash.setObjectName("Mw_TwitteDash")
        Mw_TwitteDash.setEnabled(True)
        Mw_TwitteDash.resize(1260, 699)
        self.centralwidget = QtWidgets.QWidget(Mw_TwitteDash)
        
        self.centralwidget.setObjectName("centralwidget")
        self.widget_ReadCredentials = QtWidgets.QWidget(self.centralwidget)
        self.widget_ReadCredentials.setGeometry(QtCore.QRect(20, 50, 821, 311))
        self.widget_ReadCredentials.setObjectName("widget_ReadCredentials")
       
        # Hide Read Credentials Widget untill called#####################
        self.widget_ReadCredentials.hide()
        #################################################################
        
        self.Label_ConKey = QtWidgets.QLabel(self.widget_ReadCredentials)
        self.Label_ConKey.setGeometry(QtCore.QRect(52, 79, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Label_ConKey.setFont(font)
        self.Label_ConKey.setObjectName("Label_ConKey")
        self.Label_ConSec = QtWidgets.QLabel(self.widget_ReadCredentials)
        self.Label_ConSec.setGeometry(QtCore.QRect(49, 120, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Label_ConSec.setFont(font)
        self.Label_ConSec.setObjectName("Label_ConSec")
        self.Label_AccKey = QtWidgets.QLabel(self.widget_ReadCredentials)
        self.Label_AccKey.setGeometry(QtCore.QRect(50, 160, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Label_AccKey.setFont(font)
        self.Label_AccKey.setObjectName("Label_AccKey")
        self.Label_AccKey_2 = QtWidgets.QLabel(self.widget_ReadCredentials)
        self.Label_AccKey_2.setGeometry(QtCore.QRect(50, 200, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Label_AccKey_2.setFont(font)
        self.Label_AccKey_2.setObjectName("Label_AccKey_2")
        self.pTE_ConKey = QtWidgets.QPlainTextEdit(self.widget_ReadCredentials)
        self.pTE_ConKey.setGeometry(QtCore.QRect(190, 80, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pTE_ConKey.setFont(font)
        self.pTE_ConKey.setObjectName("pTE_ConKey")
        self.pTE_ConSec = QtWidgets.QPlainTextEdit(self.widget_ReadCredentials)
        self.pTE_ConSec.setGeometry(QtCore.QRect(190, 120, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pTE_ConSec.setFont(font)
        self.pTE_ConSec.setObjectName("pTE_ConSec")
        self.pTE_AccKey = QtWidgets.QPlainTextEdit(self.widget_ReadCredentials)
        self.pTE_AccKey.setGeometry(QtCore.QRect(190, 160, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pTE_AccKey.setFont(font)
        self.pTE_AccKey.setObjectName("pTE_AccKey")
        self.pTE_AccSec = QtWidgets.QPlainTextEdit(self.widget_ReadCredentials)
        self.pTE_AccSec.setGeometry(QtCore.QRect(190, 200, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pTE_AccSec.setFont(font)
        self.pTE_AccSec.setObjectName("pTE_AccSec")
        self.pB_LdCred = QtWidgets.QPushButton(self.widget_ReadCredentials)
        self.pB_LdCred.setGeometry(QtCore.QRect(190, 260, 111, 28))
        self.pB_LdCred.setObjectName("pB_LdCred")
        ########## Load Credentials Button Event <JJRU>#####################
        self.pB_LdCred.clicked.connect(lambda: twactions.LoadTwCredentials(
             "AuthCred.xml",ui))
        ###################################################################
        self.pB_AutCred = QtWidgets.QPushButton(self.widget_ReadCredentials)
        self.pB_AutCred.setGeometry(QtCore.QRect(640, 260, 111, 28))
        self.pB_AutCred.setObjectName("pB_AutCred")
        
        ########## Button Event Authenticate CRedentials <JJRU>###############
        self.pB_AutCred.clicked.connect(lambda: twactions.AuthTwCredentials(ui))     
        ###################################################################
        
        self.pB_SvCred = QtWidgets.QPushButton(self.widget_ReadCredentials)
        self.pB_SvCred.setGeometry(QtCore.QRect(310, 260, 111, 28))
        self.pB_SvCred.setObjectName("pB_SvCred")
        ########## Save Credentials Button Event <JJRU>#####################
        self.pB_SvCred.clicked.connect(lambda: twactions.SaveTwCredentials(ui))
        ###################################################################
        self.pB_DeCred = QtWidgets.QPushButton(self.widget_ReadCredentials)
        self.pB_DeCred.setGeometry(QtCore.QRect(430, 260, 121, 28))
        self.pB_DeCred.setObjectName("pB_DeCred")
        ########## Delete Credentials Button Event <JJRU>#####################
        self.pB_DeCred.clicked.connect(lambda: twactions.DeleteTwCredentials(ui))
        ###################################################################
        self.Label_UserName = QtWidgets.QLabel(self.widget_ReadCredentials)
        self.Label_UserName.setGeometry(QtCore.QRect(52, 39, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Label_UserName.setFont(font)
        self.Label_UserName.setObjectName("Label_UserName")
        self.pTE_UserName = QtWidgets.QPlainTextEdit(self.widget_ReadCredentials)
        self.pTE_UserName.setGeometry(QtCore.QRect(190, 40, 561, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pTE_UserName.setFont(font)
        self.pTE_UserName.setObjectName("pTE_UserName")
        
        ######################################################################
        # User Info WIdget 
        ######################################################################
        self.widget_UserInfo = QtWidgets.QWidget(self.centralwidget)
        self.widget_UserInfo.hide()
        #self.widget_UserInfo.setEnabled(False)
        self.widget_UserInfo.setGeometry(QtCore.QRect(850, 30, 371, 531))
        self.widget_UserInfo.setObjectName("widget_UserInfo")
        self.label = QtWidgets.QLabel(self.widget_UserInfo)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 101))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        
       
        self.label.setObjectName("label")
        self.Lbl_UserInfo_UserName = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_UserName.setGeometry(QtCore.QRect(20, 130, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_UserName.setFont(font)
        self.Lbl_UserInfo_UserName.setObjectName("Lbl_UserInfo_UserName")
        self.Lbl_UserInfo_Name = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_Name.setGeometry(QtCore.QRect(21, 171, 91, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_Name.setFont(font)
        self.Lbl_UserInfo_Name.setObjectName("Lbl_UserInfo_Name")
        self.Lbl_UserInfo_GeoEna = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_GeoEna.setGeometry(QtCore.QRect(20, 210, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_GeoEna.setFont(font)
        self.Lbl_UserInfo_GeoEna.setObjectName("Lbl_UserInfo_GeoEna")
        self.Lbl_UserInfo_Location = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_Location.setGeometry(QtCore.QRect(20, 250, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_Location.setFont(font)
        self.Lbl_UserInfo_Location.setObjectName("Lbl_UserInfo_Location")
        self.Lbl_UserInfo_CreatedAt = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_CreatedAt.setGeometry(QtCore.QRect(20, 290, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_CreatedAt.setFont(font)
        self.Lbl_UserInfo_CreatedAt.setObjectName("Lbl_UserInfo_CreatedAt")
        self.Lbl_UserInfo_StatusCount = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_StatusCount.setGeometry(QtCore.QRect(20, 330, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_StatusCount.setFont(font)
        self.Lbl_UserInfo_StatusCount.setObjectName("Lbl_UserInfo_StatusCount")
        self.Lbl_UserInfo_Description = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_Description.setGeometry(QtCore.QRect(20, 370, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_Description.setFont(font)
        self.Lbl_UserInfo_Description.setObjectName("Lbl_UserInfo_Description")
        self.Lbl_UserInfo_FollowersCount = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_FollowersCount.setGeometry(QtCore.QRect(130, 30, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_FollowersCount.setFont(font)
        self.Lbl_UserInfo_FollowersCount.setObjectName("Lbl_UserInfo_FollowersCount")
        self.Lbl_UserInfo_FollowersCount_2 = QtWidgets.QLabel(self.widget_UserInfo)
        self.Lbl_UserInfo_FollowersCount_2.setGeometry(QtCore.QRect(130, 70, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Lbl_UserInfo_FollowersCount_2.setFont(font)
        self.Lbl_UserInfo_FollowersCount_2.setObjectName("Lbl_UserInfo_FollowersCount_2")
        self.pTE_UsrInf_UserName = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_UserName.setGeometry(QtCore.QRect(120, 130, 231, 31))
        self.pTE_UsrInf_UserName.setObjectName("pTE_UsrInf_UserName")
        self.pTE_UsrInf_Name = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_Name.setGeometry(QtCore.QRect(120, 170, 231, 31))
        self.pTE_UsrInf_Name.setObjectName("pTE_UsrInf_Name")
        self.pTE_UsrInf_GeoEnabled = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_GeoEnabled.setGeometry(QtCore.QRect(120, 210, 231, 31))
        self.pTE_UsrInf_GeoEnabled.setObjectName("pTE_UsrInf_GeoEnabled")
        self.pTE_UsrInf_Location = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_Location.setGeometry(QtCore.QRect(120, 250, 231, 31))
        self.pTE_UsrInf_Location.setObjectName("pTE_UsrInf_Location")
        self.pTE_UsrInf_CreatedAt = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_CreatedAt.setGeometry(QtCore.QRect(120, 290, 231, 31))
        self.pTE_UsrInf_CreatedAt.setObjectName("pTE_UsrInf_CreatedAt")
        self.pTE_UsrInf_StatusCount = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_StatusCount.setGeometry(QtCore.QRect(120, 330, 231, 31))
        self.pTE_UsrInf_StatusCount.setObjectName("pTE_UsrInf_StatusCount")
        self.pTE_UsrInf_Description = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_Description.setGeometry(QtCore.QRect(20, 400, 331, 121))
        self.pTE_UsrInf_Description.setObjectName("pTE_UsrInf_Description")
        self.pTE_UsrInf_FollowersCount = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_FollowersCount.setGeometry(QtCore.QRect(210, 30, 91, 31))
        self.pTE_UsrInf_FollowersCount.setObjectName("pTE_UsrInf_FollowersCount")
        self.pTE_UsrInf_FriendsCount = QtWidgets.QPlainTextEdit(self.widget_UserInfo)
        self.pTE_UsrInf_FriendsCount.setGeometry(QtCore.QRect(210, 70, 91, 31))
        self.pTE_UsrInf_FriendsCount.setObjectName("pTE_UsrInf_FriendsCount")
        #######################################################################
        Mw_TwitteDash.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Mw_TwitteDash)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1260, 26))
        self.menubar.setObjectName("menubar")
        self.menuTwitter_Dash = QtWidgets.QMenu(self.menubar)
        self.menuTwitter_Dash.setObjectName("menuTwitter_Dash")
        self.menuFriends = QtWidgets.QMenu(self.menubar)
        self.menuFriends.setObjectName("menuFriends")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        Mw_TwitteDash.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Mw_TwitteDash)
        self.statusbar.setObjectName("statusbar")
        Mw_TwitteDash.setStatusBar(self.statusbar)
        self.actionRead_Authentication_File = QtWidgets.QAction(Mw_TwitteDash)
        self.actionRead_Authentication_File.setObjectName("actionRead_Authentication_File")       
        #Show Read Credentials Widgets After Click Option ###################               
        self.actionRead_Authentication_File.triggered.connect(lambda: self.widget_ReadCredentials.show()) 
        #####################################################################
        self.actionTwitter_Bot_Settings = QtWidgets.QAction(Mw_TwitteDash)     
        self.actionTwitter_Bot_Settings.setObjectName("actionTwitter_Bot_Settings")
        #Show Read Bot Excecution Widgets After Click Option ###################               
        self.actionTwitter_Bot_Settings.triggered.connect(lambda: twactions.showBotForm(ui))
        #####################################################################
        self.actionTwitter_Auto_Follow_Request = QtWidgets.QAction(Mw_TwitteDash)
        self.actionTwitter_Auto_Follow_Request.setObjectName("actionTwitter_Auto_Follow_Request")
        self.actionTrending_Topics_Settings = QtWidgets.QAction(Mw_TwitteDash)
        self.actionTrending_Topics_Settings.setObjectName("actionTrending_Topics_Settings")
        self.actionSecurity = QtWidgets.QAction(Mw_TwitteDash)
        self.actionSecurity.setObjectName("actionSecurity")
        self.actionExit = QtWidgets.QAction(Mw_TwitteDash)
        self.actionExit.setObjectName("actionExit")
        #Exit TwitterDAsh Click Option ###################               
        self.actionExit.triggered.connect(lambda: QApplication.quit())
        #####################################################################
        self.actionBot_File_Keys = QtWidgets.QAction(Mw_TwitteDash)
        self.actionBot_File_Keys.setObjectName("actionBot_File_Keys")
        self.actionAbout = QtWidgets.QAction(Mw_TwitteDash)
        self.actionAbout.setObjectName("actionAbout")
        self.actionCreate_Followers_File = QtWidgets.QAction(Mw_TwitteDash)
        self.actionCreate_Followers_File.setObjectName("actionCreate_Followers_File")
        self.actionCreate_Following_Files = QtWidgets.QAction(Mw_TwitteDash)
        self.actionCreate_Following_Files.setObjectName("actionCreate_Following_Files")
        self.actionRead_Followers_File = QtWidgets.QAction(Mw_TwitteDash)
        self.actionRead_Followers_File.setObjectName("actionRead_Followers_File")
        self.actionRead_Following_File = QtWidgets.QAction(Mw_TwitteDash)
        self.actionRead_Following_File.setObjectName("actionRead_Following_File")
        self.actionStatistics = QtWidgets.QAction(Mw_TwitteDash)
        self.actionStatistics.setObjectName("actionStatistics")
        self.actionBot_File_Keys_2 = QtWidgets.QAction(Mw_TwitteDash)
        self.actionBot_File_Keys_2.setObjectName("actionBot_File_Keys_2")
        self.actionAbout_2 = QtWidgets.QAction(Mw_TwitteDash)
        self.actionAbout_2.setObjectName("actionAbout_2")
        self.menuTwitter_Dash.addAction(self.actionRead_Authentication_File)
        self.menuTwitter_Dash.addAction(self.actionTwitter_Bot_Settings)
        self.menuTwitter_Dash.addAction(self.actionTwitter_Auto_Follow_Request)
        self.menuTwitter_Dash.addAction(self.actionTrending_Topics_Settings)
        self.menuTwitter_Dash.addAction(self.actionSecurity)
        self.menuTwitter_Dash.addSeparator()
        self.menuTwitter_Dash.addAction(self.actionExit)
        self.menuFriends.addAction(self.actionCreate_Followers_File)
        self.menuFriends.addAction(self.actionCreate_Following_Files)
        self.menuFriends.addAction(self.actionRead_Followers_File)
        self.menuFriends.addAction(self.actionRead_Following_File)
        self.menuFriends.addAction(self.actionStatistics)
        self.menuHelp.addAction(self.actionBot_File_Keys_2)
        self.menuHelp.addAction(self.actionAbout_2)
        self.menubar.addAction(self.menuTwitter_Dash.menuAction())
        self.menubar.addAction(self.menuFriends.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Mw_TwitteDash)
        
        
        QtCore.QMetaObject.connectSlotsByName(Mw_TwitteDash)

    def retranslateUi(self, Mw_TwitteDash):
        _translate = QtCore.QCoreApplication.translate
        Mw_TwitteDash.setWindowTitle(_translate("Mw_TwitteDash", "Twitter Dash"))
        self.Label_ConKey.setText(_translate("Mw_TwitteDash", "Consumer Key"))
        self.Label_ConSec.setText(_translate("Mw_TwitteDash", "Consumer Secret"))
        self.Label_AccKey.setText(_translate("Mw_TwitteDash", "Access Key"))
        self.Label_AccKey_2.setText(_translate("Mw_TwitteDash", "Access Secret"))
        self.pB_LdCred.setText(_translate("Mw_TwitteDash", "Load Credentials"))
        self.pB_AutCred.setText(_translate("Mw_TwitteDash", "Authenticate"))
        self.pB_SvCred.setText(_translate("Mw_TwitteDash", "Save Credentials"))
        self.pB_DeCred.setText(_translate("Mw_TwitteDash", "Delete Credentials"))
        self.Label_UserName.setText(_translate("Mw_TwitteDash", "User Name"))
        self.menuTwitter_Dash.setTitle(_translate("Mw_TwitteDash", "Twitter Dash"))
        self.menuFriends.setTitle(_translate("Mw_TwitteDash", "Friends"))
        self.menuHelp.setTitle(_translate("Mw_TwitteDash", "Help"))
        self.actionRead_Authentication_File.setText(_translate("Mw_TwitteDash", "Authenticate Credentials"))
        
        self.actionTwitter_Bot_Settings.setText(_translate("Mw_TwitteDash", "Bot Settings"))
        #self.actionTwitter_Bot_Settings.setEnabled(False)
        
        self.actionTwitter_Auto_Follow_Request.setText(_translate("Mw_TwitteDash", "Auto Follow Settings"))
        self.actionTwitter_Auto_Follow_Request.setEnabled(False)
        
        self.actionTrending_Topics_Settings.setText(_translate("Mw_TwitteDash", "Trending Topics Settings"))
        self.actionTrending_Topics_Settings.setEnabled(False)
        
        self.actionSecurity.setText(_translate("Mw_TwitteDash", "Security"))
        self.actionSecurity.setEnabled(False)
        
        self.actionExit.setText(_translate("Mw_TwitteDash", "Exit"))
        
        self.actionBot_File_Keys.setText(_translate("Mw_TwitteDash", "Bot File Keys"))
        
        self.actionAbout.setText(_translate("Mw_TwitteDash", "About"))
        
        self.actionCreate_Followers_File.setText(_translate("Mw_TwitteDash", "Create Followers File"))
        self.actionCreate_Followers_File.setEnabled(False)
        
        
        self.actionCreate_Following_Files.setText(_translate("Mw_TwitteDash", "Create Following Files"))
        self.actionCreate_Following_Files.setEnabled(False)
        
        self.actionRead_Followers_File.setText(_translate("Mw_TwitteDash", "Read Followers File"))
        self.actionRead_Followers_File.setEnabled(False)
        
        self.actionRead_Following_File.setText(_translate("Mw_TwitteDash", "Read Following File"))
        self.actionRead_Following_File.setEnabled(False)
        
        self.actionStatistics.setText(_translate("Mw_TwitteDash", "Statistics"))
        self.actionStatistics.setEnabled(False)
        
        self.actionBot_File_Keys_2.setText(_translate("Mw_TwitteDash", "Bot File Keys"))
        
        self.actionAbout_2.setText(_translate("Mw_TwitteDash", "About"))


if __name__ == "__main__":
    import sys
    TwErrorLog.CreateErrLog("","twitterDash.log")
    twactions = TwitterActions()
    app = QtWidgets.QApplication(sys.argv)
    Mw_TwitteDash = QtWidgets.QMainWindow()
    ui = Ui_Mw_TwitteDash()
    ui.setupUi(Mw_TwitteDash)
    Mw_TwitteDash.show()
    sys.exit(app.exec_())
