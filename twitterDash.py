# -*- coding: utf-8 -*-
# Created by : Jairo J. Rodriguez
# email Address : rodriguezjfz@gmail.com
# Description : Twitter Dash Board Implementation 
# Last MOdificatio : Nov 19, 2017

import xml.dom.minidom
import urllib
import datetime, codecs, tweepy, xml.etree.cElementTree as et
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QFileDialog


class TwErrorLog(object):
    def CreateErrLog(self,fileName):
        LogFileName=fileName
        logfile=codecs.open(LogFileName,'w',encoding='utf8')
        logfile.write("Twitter Dash Board Started")
        logfile.close()
        
    def WriteInLog(self,fileName,message):
        logfile=codecs.open(fileName,'a', encoding='utf8')
        logfile.write("\n\r" + str(datetime.datetime.now())+"   "+ message + "\n\r")
        logfile.close()
    
class TwitterActions(object):
    def AuthTwCredentials(self,twd_consumer_key,twd_consumer_secret,
                          twd_access_key,twd_access_secret,twd_lcdNumber,
                          twd_ProfilePic,twd_userInfo):
        
       
        twd_userInfo.show()
    
        
        twd_ck=twd_consumer_key.toPlainText()
        twd_cs=twd_consumer_secret.toPlainText()
        twd_ak=twd_access_key.toPlainText()
        twd_as=twd_access_secret.toPlainText()
        print(twd_ck)
        print(twd_cs)
        print(twd_ak)
        print(twd_as)
        
        auth = tweepy.OAuthHandler(twd_ck,
                                   twd_cs)
        
        auth.set_access_token(twd_ak,twd_as)
        
        try:
            TwErrorLog.WriteInLog(self,'twitterDash.log', 
                                 "Authenticating user with consumer key : "
                                 +twd_ck)
            twapi = tweepy.API(auth)
            myUser=twapi.me()
            
            
            twd_lcdNumber.setPlainText(str(myUser.followers_count))
            #twd_lcdNumber.display(myUser.followers_count)
            
            url=myUser.profile_image_url
            print(url)
            data = urllib.request.urlopen(url).read()
            twd_ProfilePic.pixmap=QPixmap()            
            image = QtGui.QImage()         
            image.loadFromData(data)
            scaled_image = image.scaled( twd_ProfilePic.size(), QtCore.Qt.KeepAspectRatio)
            twd_ProfilePic.setPixmap(QtGui.QPixmap(scaled_image))
                     
            print(myUser.followers_count)

        except Exception as err:
            errMsg = str(err)
            TwErrorLog.WriteInLog(self,'twitterDash.log', errMsg) 
            print (errMsg)
                                  
            pass
       
    def SaveTwCredentials(self,twd_username,twd_consumer_key,twd_consumer_secret,
                          twd_access_key,twd_access_secret):
        twd_ck=twd_consumer_key.toPlainText()
        twd_cs=twd_consumer_secret.toPlainText()
        twd_ak=twd_access_key.toPlainText()
        twd_as=twd_access_secret.toPlainText()
        twd_un=twd_username.toPlainText()

   
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
        fileName, _ = QFileDialog.getSaveFileName(caption="Save Credentials file",
                                                  options=options, filter="*.xml")
        tree.write(fileName)
        
    def LoadTwCredentials(self,xmlFile,twd_username,twd_consumer_key,
                          twd_consumer_secret,
                          twd_access_key,twd_access_secret):
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(caption="Open Credential file",
                                                  options=options, filter="*.xml")
        xmlFile=fileName
                
        try: 
            doc=xml.dom.minidom.parse(xmlFile)           
            for node in doc.getElementsByTagName("user"):
                user=node.getAttribute("name")
                twd_username.setPlainText(str(user))
                for i in node.childNodes:
                    credential=i.getAttribute("name")
                
                    key = i.getAttribute("value")
                    if "consumer key" in credential :
                        twd_consumer_key.setPlainText(key)
                    if "consumer secret" in credential :
                        twd_consumer_secret.setPlainText(key)
                    if "access key" in credential :
                        twd_access_key.setPlainText(key)
                    if "access secret" in credential :
                        twd_access_secret.setPlainText(key)
        except Exception as err:
            errMsg = str(err)
            TwErrorLog.WriteInLog(self,'twitterDash.log', errMsg) 
            print (errMsg)  
            pass               
                                                    
class XmlFileMngr():
    
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;XML Files (*.xml)", options=options)
        if fileName:
            print(fileName)
 
    def openFileNamesDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;XML Files (*.xml)", options=options)
        if files:
            print(files)
 
    def saveFileDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;XML Files (*.xml)", options=options)
        if fileName:
            print(fileName)

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
             "AuthCred.xml",self.pTE_UserName,self.pTE_ConKey, self.pTE_ConSec,
             self.pTE_AccKey, self.pTE_AccSec))
        ###################################################################
        self.pB_AutCred = QtWidgets.QPushButton(self.widget_ReadCredentials)
        self.pB_AutCred.setGeometry(QtCore.QRect(640, 260, 111, 28))
        self.pB_AutCred.setObjectName("pB_AutCred")
        
        ########## Button Event <JJRU>#####################################
        self.pB_AutCred.clicked.connect(lambda: twactions.AuthTwCredentials(
            self.pTE_ConKey, self.pTE_ConSec,
            self.pTE_AccKey, self.pTE_AccSec,
            self.pTE_UsrInf_FollowersCount,self.label,self.widget_UserInfo))     
        ###################################################################
        
        self.pB_SvCred = QtWidgets.QPushButton(self.widget_ReadCredentials)
        self.pB_SvCred.setGeometry(QtCore.QRect(310, 260, 111, 28))
        self.pB_SvCred.setObjectName("pB_SvCred")
        self.pB_DeCred = QtWidgets.QPushButton(self.widget_ReadCredentials)
        self.pB_DeCred.setGeometry(QtCore.QRect(430, 260, 121, 28))
        self.pB_DeCred.setObjectName("pB_DeCred")
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
        self.actionTwitter_Auto_Follow_Request = QtWidgets.QAction(Mw_TwitteDash)
        self.actionTwitter_Auto_Follow_Request.setObjectName("actionTwitter_Auto_Follow_Request")
        self.actionTrending_Topics_Settings = QtWidgets.QAction(Mw_TwitteDash)
        self.actionTrending_Topics_Settings.setObjectName("actionTrending_Topics_Settings")
        self.actionSecurity = QtWidgets.QAction(Mw_TwitteDash)
        self.actionSecurity.setObjectName("actionSecurity")
        self.actionExit = QtWidgets.QAction(Mw_TwitteDash)
        self.actionExit.setObjectName("actionExit")
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
        self.actionTwitter_Auto_Follow_Request.setText(_translate("Mw_TwitteDash", "Auto Follow Settings"))
        self.actionTrending_Topics_Settings.setText(_translate("Mw_TwitteDash", "Trending Topics Settings"))
        self.actionSecurity.setText(_translate("Mw_TwitteDash", "Security"))
        self.actionExit.setText(_translate("Mw_TwitteDash", "Exit"))
        self.actionBot_File_Keys.setText(_translate("Mw_TwitteDash", "Bot File Keys"))
        self.actionAbout.setText(_translate("Mw_TwitteDash", "About"))
        self.actionCreate_Followers_File.setText(_translate("Mw_TwitteDash", "Create Followers File"))
        self.actionCreate_Following_Files.setText(_translate("Mw_TwitteDash", "Create Following Files"))
        self.actionRead_Followers_File.setText(_translate("Mw_TwitteDash", "Read Followers File"))
        self.actionRead_Following_File.setText(_translate("Mw_TwitteDash", "Read Following File"))
        self.actionStatistics.setText(_translate("Mw_TwitteDash", "Statistics"))
        self.actionBot_File_Keys_2.setText(_translate("Mw_TwitteDash", "Bot File Keys"))
        self.actionAbout_2.setText(_translate("Mw_TwitteDash", "About"))


if __name__ == "__main__":
    import sys
    
    twactions = TwitterActions() 
    app = QtWidgets.QApplication(sys.argv)
    Mw_TwitteDash = QtWidgets.QMainWindow()
    ui = Ui_Mw_TwitteDash()
    ui.setupUi(Mw_TwitteDash)
    Mw_TwitteDash.show()
    sys.exit(app.exec_())

