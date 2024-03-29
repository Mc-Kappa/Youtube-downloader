from pytube import YouTube
from moviepy.editor import *
from PyQt6.QtWidgets import QApplication, QPushButton, QLabel, QTextEdit, QMessageBox, QRadioButton, QMainWindow
from PyQt6.QtCore import QCoreApplication

def convert(downloadedVideoName, nameToWrite, choose):
    FinalFileName = f'{nameToWrite}.mp3'
    videoclip = VideoFileClip(downloadedVideoName)
    audioclip = videoclip.audio
    QCoreApplication.processEvents()
    audioclip.write_audiofile(FinalFileName,bitrate=choose,verbose=False,logger=None)
    audioclip.close()
    videoclip.close()
    os.remove(downloadedVideoName)

def deleteSpecialSigns(str):
    return str.replace("\\","").replace("/","").replace(":","").replace("*","").replace("?","").replace("<","").replace(">","").replace("\"","").replace("|","")


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
        counter = 0 
        while array:
            fileName = ""
            song_to_download = array.pop()
            QCoreApplication.processEvents()
            ytObj = YouTube(song_to_download)
            '''
            Once time, there was kind of problem with pytube, and there was errors during donwloading songs, so decided to change loop for try until you wouldn't download it. 
            '''
            try:
                nameToWrite = deleteSpecialSigns(ytObj.title)
            except:
                array.append(song_to_download)
                continue
            author = deleteSpecialSigns(ytObj.author)
            if ("Topic" in author):
                author = author.replace(" Topic", "")

            fileName = author + " - " + nameToWrite
            newFile = ytObj.streams.get_by_itag(18)
            downloadedVideoName = newFile.download(filename=f"{str(fileName)}.mp4")
            downloadedSongs.append(fileName)
            convert(downloadedVideoName, fileName, self.choose)
            counter+=1 
            self.downloadingLabel(counter,songCount)

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