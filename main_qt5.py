#!/usr/bin/python3
"""
Jacopo Moioli
8/12/19
Programma che calcola la media delle diverse materie
Per open-day badoni 14/12
"""

import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QCalendarWidget,
    QComboBox,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QDate

import datetime

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.pyplot import plot, ion, show
from matplotlib import style
from matplotlib.ticker import FuncFormatter

matplotlib.use("Qt5Agg")  # mpl gui framework QT5
listamaterie = {}  # Dizionario
listavoti = []


class Voto:
    def __init__(self, materia, voto, data):
        self.materia = materia
        self.voto = voto
        self.data = datetime.date(int(data[0:4]), int(data[5:7]), int(data[8:10]))


def saveVoto():
    """
    saveVoto()
    Acquisisce i dati in input dalle entry, li verifica e crea nuova materia e aggiunge voto o aggiunge solo voto
    """

    try:
        materia = materiaEntry.text().lower()
        voto = float(votoEntry.text().replace(",", "."))
        data = calendar.selectedDate().toString("yyyy/MM/dd")
        if (
            materia != "" and voto != "" and float(voto) >= 0 and float(voto) < 10.5
        ):  # Verificare che non sia input vuoto o voto fuori dai limiti
            if materia not in listamaterie:
                print(f"[!]Creating {materia}")
                listamaterie[materia] = []  # crea chiave materia e lista come valore
                voti = []  # inizializza lista voti
                listamaterie[materia].append(voti)  # Aggiunge lista voti

            print(f"   Adding {voto} ({data}) to {materia}")
            listamaterie[materia][0].append(voto)  # Aggiunge voto
            voto = Voto(materia, voto, data)
            listavoti.append(voto)
        else:
            raise ValueError

    except ValueError:
        print("[!]Error: ValueError")
        errorBox = QMessageBox()
        errorBox.setIcon(QMessageBox.Critical)
        errorBox.setWindowTitle("Unvalid Input")
        errorBox.setText(
            "Attenzione, Si è inserito un dato non valido"
        )  # Se dato non valido
        errorBox.setStandardButtons(QMessageBox.Ok)
        errorBox.exec()
        materia = ""
        voto = ""

    votoEntry.setText("")  # Svuota l'entry del voto


def resetWithConf():
    """
    resetWithConf()
    resetta il dizionario e tutte le entry con un messaggio di conferma
    """
    confBox = QMessageBox()
    confBox.setIcon(QMessageBox.Warning)
    confBox.setWindowTitle("Conferma Reset")
    confBox.setText("Eseguire il reset?")
    confBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    print("[!]Reset with confirmation")
    confirm = confBox.exec()
    if confirm == QMessageBox.Yes:
        print("   Yes")
        print("[!]Resetting all")
        listamaterie.clear()
        materiaEntry.setText("")
        votoEntry.setText("")
    else:
        print("   No")


def reset():
    """
    reset()
    resetta il dizionario e tutte le entry
    """
    print("[!]Resetting all")
    listamaterie.clear()
    materiaEntry.setText("")
    votoEntry.setText("")


def makeSituationGraph():
    """
    makeGraph()
    Utilizzando matplotlib, crea un array 'names' e un array 'datas', i quali contengono rispettivamente i nomi delle materie e la media della materia.
    Crea un grafico a barre con x=nomemateria e y=mediamateria. Stampa il grafico (con la possibilità di salvarlo su file)
    """
    print("[!]Creating the graph...")
    style.use("ggplot")
    ion()  # Impostare modalità interattiva MPL per eseguire il codice dopo la creazione del grafico
    names = []
    datas = []

    for materia in listamaterie:  # Creazione assi
        names.append(materia)
        datas.append(listamaterie.get(materia)[1])
    plt.bar(names, datas, align="center")
    plt.title("Situazione Generale")
    plt.ylabel("Voti")
    plt.xlabel("Materie")
    plt.tight_layout()
    print("[!]Showing the graph")
    plt.show()
    # plt.savefig('medie.png')   #Forzare il salvataggio del grafico


def makeSubjectGraph(materiaGrafico):
    """
    makeSubjectGraph(materiaGrafico)
    crea il grafico individuale per la materia passata come argomento
    sull'asse x la data del test, asse y valore del voto

    Args:
    materiaGrafico: materia della quale si vuole fare il grafico

    """
    print("[!]Creating the graph...")
    print(listamaterie)
    print(listavoti)
    ion()  # Impostare modalità interattiva MPL per eseguire il codice dopo la creazione del grafico
    dates = []
    voti = []

    for materia in listamaterie:
        if materia == materiaGrafico:
            for voto in listavoti:
                if voto.materia == materia:
                    dates.append(voto.data)
                    voti.append(voto.voto)

    plt.plot_date(dates, voti, "-o")  # , 'o-')
    plt.title(f"Situazione {materiaGrafico}")
    plt.ylabel("Voti")
    plt.xlabel("Date")
    print("[!]Showing the graph")
    plt.show()


def printResult():
    """
    printResult()
    Stampa le medie delle diverse materie in un message box info e resetta
    """

    def closeResult():
        """
        closeResult()
        Chiude la finestra del risultato e chiama la funzione reset
        """
        resultWindow.close()
        widget.close()
        sys.exit()

    def getGraphSubject():
        """
        getGraphSubject()
        Chiama la funzione makeSubjectGraph con attributo selezione dal QComboBox
        """
        subject = selectionSubjectGraph.currentText()
        makeSubjectGraph(subject)

    resultWindow = QWidget()
    grid = QGridLayout()

    selectionSubjectGraph = QComboBox(resultWindow)

    msg = ""
    for materia in listamaterie:
        msg = msg + "".join(
            "La media di " + materia + " vale " + str(listamaterie[materia][1]) + "\n"
        )
        selectionSubjectGraph.addItem(materia)
    print("[!]Printing the results")

    resultLabel = QLabel(resultWindow)
    resultLabel.setText(msg)
    grid.addWidget(resultLabel, 0, 1)

    okButton = QPushButton(resultWindow)
    okButton.setText("OK")
    okButton.clicked.connect(closeResult)
    grid.addWidget(okButton, 1, 1)

    grid.addWidget(selectionSubjectGraph, 2, 1)

    subjectGraphButton = QPushButton(resultWindow)
    subjectGraphButton.setText("Grafico materia")
    subjectGraphButton.clicked.connect(getGraphSubject)
    grid.addWidget(subjectGraphButton, 3, 1)

    situationGraphButton = QPushButton(resultWindow)
    situationGraphButton.setText("Grafico Situazione")
    situationGraphButton.clicked.connect(makeSituationGraph)
    grid.addWidget(situationGraphButton, 4, 1)

    resultWindow.setGeometry(20, 20, 170, 100)
    resultWindow.setWindowTitle("Risultati")
    resultWindow.setLayout(grid)
    resultWindow.show()
    if resultWindow.closeEvent(resultWindow):
        pass


def getMedie():
    """
    getMedie()
    calcola la media dei voti per ogni materia e la salva sulla lista valore della chiave materia
    """
    # reset()
    if len(listamaterie) == 0:
        errorBox = QMessageBox()
        errorBox.setIcon(QMessageBox.Critical)
        errorBox.setWindowTitle("Unvalid Input")
        errorBox.setText(
            "Attenzione, non si è inserito alcun dato"
        )  # Se non esiste nessuna materia
        errorBox.setStandardButtons(QMessageBox.Ok)
        errorBox.exec()

        print("[!]Error: no data")
    else:
        for materia in listamaterie:
            voti = listamaterie.get(materia)[0]
            somma = 0
            print(f"[!]Calculating the average of {materia}")
            for voto in voti:
                somma += float(voto)
            media = somma / len(voti)
            print(f"[!]Saving the average of {materia}")
            listamaterie[materia].append(round(media, 1))
        printResult()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QWidget()
    grid = QGridLayout()

    # MATERIA
    materiaLabel = QLabel(widget)  # Creazione Label
    materiaLabel.setText("Materia: ")  # Testo Label
    materiaEntry = QLineEdit()  # Creazione entry

    grid.addWidget(materiaLabel, 0, 0)  # Pos. label
    grid.addWidget(materiaEntry, 0, 1)  # Pos. Entry

    # VOTO
    votoLabel = QLabel(widget)
    votoLabel.setText("Voto:")
    votoEntry = QLineEdit()  # input
    grid.addWidget(votoLabel, 1, 0)
    grid.addWidget(votoEntry, 1, 1)

    # DATA
    dataLabel = QLabel(widget)
    dataLabel.setText("Data:")
    calendar = QCalendarWidget(widget)
    calendar.setGridVisible = False
    calendar.setGeometry(10, 10, 10, 10)
    grid.addWidget(dataLabel, 2, 0)
    grid.addWidget(calendar, 2, 1)

    # BOTTONE AGGIUNTA VOTO
    votoButton = QPushButton(widget)
    votoButton.setText("Add")
    votoButton.clicked.connect(saveVoto)
    grid.addWidget(votoButton, 3, 0)

    # BOTTONE MEDIA
    mediaButton = QPushButton(widget)
    mediaButton.setText("Media")
    mediaButton.clicked.connect(getMedie)
    grid.addWidget(mediaButton, 3, 1)

    # BOTTONE RESET
    resetButton = QPushButton(widget)
    resetButton.setText("Reset")
    resetButton.clicked.connect(resetWithConf)
    grid.addWidget(resetButton, 3, 2)

    # IMPOSTAZIONI FINESTRA
    widget.setGeometry(50, 50, 320, 200)
    widget.setWindowTitle("Media Scolastica")
    widget.setLayout(grid)
    widget.show()
    sys.exit(app.exec_())


"""
Known Issues:
- Dati rimanenti anche dopo il reset su plot MPL makeSubjectGraph
    ""Risolto"" temporaneamente a linea 179/180 con la chiusura del programma dopo il plot 
- Problema con la linea che collega i voti (157) se non inseriti in ordine cronologico
    Fix se sorting manuale delle date (?)

TODO: 
- Incorporare il dizionario materia:[voti]media in oggetto voto (e modificare i cicli)
"""
