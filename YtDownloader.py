from pytube import YouTube
from moviepy.editor import *
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QTextEdit, QMessageBox, QRadioButton, QMainWindow
from PyQt6.QtCore import QCoreApplication

def convert(nameToWrite, choose):
    CurrentFileName = '{}.mp4'.format(nameToWrite)
    FinalFileName = '{}.mp3'.format(nameToWrite)
    videoclip = VideoFileClip(CurrentFileName)
    audioclip = videoclip.audio
    QCoreApplication.processEvents()
    audioclip.write_audiofile(FinalFileName,bitrate=choose,verbose=False,logger=None)
    audioclip.close()
    videoclip.close()
    os.remove(CurrentFileName)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.setWindowTitle("YtDownloader")
        self.setFixedSize(800,360)
        self.widgets()
        self.choose = "320K"

    def widgets(self):
        #Info label
        self.templateStatusLabel = QLabel("Program status: ",self)
        self.templateStatusLabel.setGeometry(20,320,100,20)

        self.statusLabel = QLabel("Ready to download",self)
        self.statusLabel.setGeometry(120,320,200,20)

        #Our button to download
        btn1 = QPushButton("Download songs!",self)
        btn1.clicked.connect(self.downloadButton) # change here back to self.downloadButton
        btn1.setGeometry(580,240,200,100)
        #Text area
        self.messageA = QTextEdit(self)
        self.messageA.setPlaceholderText("Type links to yt here:")
        self.messageA.setGeometry(20,20,760,200)
        #Radio buttons to choose bitrate
        rb1 = QRadioButton("128Kb/s", self)
        rb1.setGeometry(100,240,100,100)
        rb1.toggled.connect(self.onClicked)

        rb2 = QRadioButton("256Kb/s", self)
        rb2.setGeometry(200,240,100,100)
        rb2.toggled.connect(self.onClicked)

        rb3 = QRadioButton("320Kb/s", self)
        rb3.setGeometry(300,240,100,100)
        rb3.setChecked(True)
        rb3.toggled.connect(self.onClicked)

        label = QLabel("Choose bitrate:",self)
        label.setGeometry(180,250,100,20)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            choice = radioButton.text()
            if (choice == "128Kb/s"):
                self.choose = "128K"
            elif (choice == "256Kb/s"):
                self.choose = "256K"
            elif (choice == "320Kb/s"):
                self.choose = "320K"

    def downloadButton(self):
        array = self.messageA.toPlainText().splitlines()
        downloadedSongs = []
        try:
            array.remove('')
        except:
            True
        songCount = len(array)
        self.downloadingLabel(0,songCount)
        
        for x in range (0,songCount):
            QCoreApplication.processEvents()
            ytObj = YouTube(array[x])
            nameToWrite = ytObj.title.replace('"', '').replace('/', '-').replace('|',' ').replace(':', '_')
            newFile = ytObj.streams.get_by_itag(18)
            newFile.download(filename="{}.mp4".format(nameToWrite))
            downloadedSongs.append(nameToWrite)
            convert(nameToWrite, self.choose)
            self.downloadingLabel(x+1,songCount)
        popupMessage = QMessageBox()
        popupMessage.setWindowTitle("Downloaded sucessful!")
        temp = "Downloaded: \n"
        for x in downloadedSongs:
            QCoreApplication.processEvents()
            temp += x
            temp += "\n"
        popupMessage.setText(temp)
        popupMessage.exec()
        self.afterDownloadingLabel()
    
    def downloadingLabel(self,position,all):
        self.statusLabel.setText("Downloaded %s of %s songs." %(position, all))
    def afterDownloadingLabel(self):
        self.statusLabel.setText("Sucessful download!")
   

app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())