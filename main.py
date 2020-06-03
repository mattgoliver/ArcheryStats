from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
import sqlite3
import sys


# Score Processing Functions


# Sort raw data into separate flights | Returns: list of all flights/scores
def listCleanUp(lst):

    # Turn string into list, separated by flights (every 5 arrows)
    scores_clean = lst.split(',')
    master_score_list = []
    for flight in scores_clean:
        individual_score = flight.split()
        master_score_list.append(individual_score)
    return master_score_list


# Get total (out of 50) score for each flight, adds to and returns list of all totals
def getFlightScore(lst):
    average_score = []
    for flight in lst:
        total = 0
        if len(flight) != 5:
            print("Missing score, please check: "+str(flight))
        for num in flight:
            total += int(num)
        if total > 50:
            print("Error in data, please check: "+str(flight))
        average_score.append(total)
    return average_score


# Average all flight scores together | Returns: average flight score of list
def getAverageFlightScore(lst):
    total = 0
    for num in lst:
        total += num
    average = total / len(lst)
    return round(average, 2)


# Collect data on individual shots | Returns: list with total arrows and individual arrow scores
def arrowStats(str):
    cleaned = str.replace(",", " ")
    nums = cleaned.split()
    stats = []
    total_arrows = len(nums)
    ten = 0
    nine = 0
    eight = 0
    seven = 0
    six = 0
    five = 0
    four = 0
    three = 0
    two = 0
    one = 0
    zero = 0

    # There's definitely a way to condense this, but I don't know how to
    for num in nums:
        num = int(num)
        if num == 10:
            ten += 1
            continue
        elif num == 9:
            nine += 1
            continue
        elif num == 8:
            eight += 1
            continue
        elif num == 7:
            seven += 1
            continue
        elif num == 6:
            six += 1
            continue
        elif num == 5:
            five += 1
            continue
        elif num == 4:
            four += 1
            continue
        elif num == 3:
            three += 1
            continue
        elif num == 2:
            two += 1
            continue
        elif num == 1:
            one += 1
            continue
        else:
            zero += 1
            continue
    stats.append(total_arrows)
    stats.append(ten)
    stats.append(nine)
    stats.append(eight)
    stats.append(seven)
    stats.append(six)
    stats.append(five)
    stats.append(four)
    stats.append(three)
    stats.append(two)
    stats.append(one)
    stats.append(zero)
    return stats


# Send raw scores through the above functions to get what I need to save data | Returns: cleanList, flightScore, averageFlightScore, arrowStatsStr
def cleanUpTime(rawlist):
    cleanList = listCleanUp(rawlist)
    flightScore = getFlightScore(cleanList)
    averageFlightScore = getAverageFlightScore(flightScore)
    arrowStatsStr = arrowStats(rawlist)
    #print("arrowStatsStr: " + str(arrowStatsStr)+", averageFlightScore: "+str(averageFlightScore)+", flightScore: "+str(flightScore)+", cleanList: "+str(cleanList))
    return cleanList, flightScore, averageFlightScore, arrowStatsStr


# Combine all results into one data set | Returns: arrowsShot, averageFlightScore, individualScores
def allTimeResults(results):
    arrowsShot = 0
    averageFlightScore = 0
    tens = 0
    nines = 0
    eights = 0
    sevens = 0
    sixes = 0
    fives = 0
    fours = 0
    threes = 0
    twos = 0
    ones = 0
    zeros = 0
    individualScores = []
    for day in results:
        arrowsShot += int(day[1])
        averageFlightScore += int(day[2])
        tens += int(day[3])
        nines += int(day[4])
        eights += int(day[5])
        sevens += int(day[6])
        sixes += int(day[7])
        fives += int(day[8])
        fours += int(day[9])
        threes += int(day[10])
        twos += int(day[11])
        ones += int(day[12])
        zeros += int(day[13])
    individualScores.append(tens)
    individualScores.append(nines)
    individualScores.append(eights)
    individualScores.append(sevens)
    individualScores.append(sixes)
    individualScores.append(fives)
    individualScores.append(fours)
    individualScores.append(threes)
    individualScores.append(twos)
    individualScores.append(ones)
    individualScores.append(zeros)
    averageFlightScore = averageFlightScore/len(results)
    return arrowsShot, averageFlightScore, individualScores


# Make pie graph based on inputted data | Returns: nothing
def pieGraphScores(scores, title="", show=True, save=False):

    # Define the label stuffs
    labelStr = '10', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0'
    labelNum = np.array(scores)
    labelNumPercent = 100.*labelNum/labelNum.sum()

    # Combine labelStr with labelNum to go into legend
    label = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(labelStr, labelNumPercent)]

    # Setup the pie graph
    fig1, axl = plt.subplots()
    axl.pie(labelNum, shadow=False, startangle=90, counterclock=True)
    axl.axis('equal')

    # Setup legend and title
    plt.legend(label, title='Scores', bbox_to_anchor=(0.15, 1.), fontsize=8)
    plt.title(title, loc='center')

    if save == True:
        plt.savefig('piechart'+datetime.today().strftime('%m-%d-%H-%M')+".png")
    if show == True:
        plt.show()


# Score Processing Functions Over


# Database Functions Below


# Save data (date, arrows shot, average flight score, and individual arrow scores) to database | Returns: nothing
def saveData(data):

    # Run code to clean up/format data
    cleanList, flightScore, averageFlightScore, arrowStatsStr = cleanUpTime(data)

    # Connect to data base
    connection = sqlite3.connect('saveData.db')
    cursor = connection.cursor()

    # Creates table if there already isn't one, should only run if creating new data base
    command1 = """CREATE TABLE IF NOT EXISTS data(date STRING PRIMARY KEY, arrowsShot INTEGER, averageFlightScore INTEGER, tens INTEGER, nines INTEGER, eights INTEGER, sevens INTEGER, sixes INTEGER, fives INTEGER, fours INTEGER, threes INTEGER, twos INTEGER, ones INTEGER, zeros INTEGER)"""
    cursor.execute(command1)

    # Get data ready to be inserted
    dataToSave = (datetime.today().strftime('%Y-%m-%d'), arrowStatsStr[0], averageFlightScore, arrowStatsStr[1], arrowStatsStr[2], arrowStatsStr[3], arrowStatsStr[4], arrowStatsStr[5], arrowStatsStr[6], arrowStatsStr[7], arrowStatsStr[8], arrowStatsStr[9], arrowStatsStr[10], arrowStatsStr[11])

    # Insert data
    cursor.execute("INSERT INTO data(date, arrowsShot, averageFlightScore, tens, nines, eights, sevens, sixes, fives, fours, threes, twos, ones, zeros) VALUES "+str(dataToSave))

    # Close database connection
    connection.commit()
    cursor.close()
    connection.close()


# Pulls all data from database | Returns lists of: date, arrowsShot, averageFlightScore, and individual arrow scores
def retrieveData(gui=False):

    # Connect to database
    connection = sqlite3.connect('saveData.db')
    cursor = connection.cursor()

    # Select all data and pull into program
    cursor.execute("SELECT * FROM data")
    results = cursor.fetchall()

    # Close connection
    cursor.close()
    connection.close()

    # Add results to GUI list
    if gui == True:
        databaseInfoView.clear()
        for i in results:
            databaseInfoView.addItem(str(i))

    return results


# Deletes selected data from database
def deleteData(date):

    # Connect to database
    connection = sqlite3.connect('saveData.db')
    cursor = connection.cursor()

    # Delete data
    print("DELETE FROM data WHERE date = "+date)
    cursor.execute("DELETE FROM data WHERE date = '"+date+"'")

    # Close connection
    connection.commit()
    cursor.close()
    connection.close()


# Database Functions Over


# GUI Functions Below


# Keep track of item currently selected on GUI list
def itemClicked(item):
    modded = item.text().replace("(", "")
    modded = modded.replace(")", "")
    modded = modded.replace("'", "")
    modded = modded.split(", ")
    global currentlySelectedItem
    currentlySelectedItem = modded

    # Update text under list
    data = ("Arrows shot: " + str(currentlySelectedItem[1]) + ", Average flight score: " + str(currentlySelectedItem[2]))
    outputText.setText(data)


# Calls pieGraphScores() for GUI
def guiPieGraphScores():
    global currentlySelectedItem
    scores = []
    for num in currentlySelectedItem[3:14]:
        scores.append(int(num))
    if savePieGraph.isChecked() == True:
        pieGraphScores(scores, title=str(currentlySelectedItem[0]), save=True)
    else:
        pieGraphScores(scores, title=str(currentlySelectedItem[0]), save=False)


# Calls saveData() for GUI
def guiSaveData():
    if rawScoreData.text() == "":
        print("No text provided")
        return
    saveData(rawScoreData.text())
    retrieveData(gui=True)


# Calls deleteData() for GUI
def guiDeleteSelectedData():
    global currentlySelectedItem
    date = str(currentlySelectedItem[0])
    print("Deleting date: "+date)
    deleteData(date)
    retrieveData(gui=True)


# Actual GUI Stuff Below


app = QApplication(sys.argv)
MainWindow = QMainWindow()
MainWindow.setObjectName("MainWindow")
MainWindow.resize(793, 401)
centralwidget = QtWidgets.QWidget(MainWindow)
centralwidget.setObjectName("centralwidget")

rawScoreData = QtWidgets.QLineEdit(centralwidget)
rawScoreData.setGeometry(QtCore.QRect(20, 20, 631, 41))
rawScoreData.setObjectName("rawScoreData")

saveDataButton = QtWidgets.QPushButton(centralwidget)
saveDataButton.setGeometry(QtCore.QRect(660, 20, 131, 41))
saveDataButton.setObjectName("saveDataButton")
saveDataButton.clicked.connect(lambda: guiSaveData())

retrieveDataButton = QtWidgets.QPushButton(centralwidget)
retrieveDataButton.setGeometry(QtCore.QRect(310, 80, 141, 41))
retrieveDataButton.setObjectName("retrieveDataButton")
retrieveDataButton.clicked.connect(lambda: retrieveData(gui=True))

generatePieGraph = QtWidgets.QPushButton(centralwidget)
generatePieGraph.setGeometry(QtCore.QRect(310, 140, 141, 41))
generatePieGraph.setObjectName("generatePieGraph")
generatePieGraph.clicked.connect(lambda: guiPieGraphScores())

savePieGraph = QtWidgets.QCheckBox(centralwidget)
savePieGraph.setGeometry(QtCore.QRect(480, 140, 141, 41))
savePieGraph.setObjectName("savePieGraph")

deleteDataButton = QtWidgets.QPushButton(centralwidget)
deleteDataButton.setGeometry(QtCore.QRect(310, 200, 141, 41))
deleteDataButton.setObjectName("deleteDataButton")
deleteDataButton.clicked.connect(lambda: guiDeleteSelectedData())

currentlySelectedItem = []
databaseInfoView = QtWidgets.QListWidget(centralwidget)
databaseInfoView.setGeometry(QtCore.QRect(20, 70, 285, 180))
databaseInfoView.setObjectName("databaseInfoView")
databaseInfoView.setAlternatingRowColors(True)
databaseInfoView.itemClicked.connect(itemClicked)

outputText = QtWidgets.QLabel(centralwidget)
outputText.setGeometry(30, 250, 300, 100)
outputText.setObjectName("outputText")

MainWindow.setCentralWidget(centralwidget)
menubar = QtWidgets.QMenuBar(MainWindow)
menubar.setGeometry(QtCore.QRect(0, 0, 793, 21))
menubar.setObjectName("menubar")
MainWindow.setMenuBar(menubar)
statusbar = QtWidgets.QStatusBar(MainWindow)
statusbar.setObjectName("statusbar")
MainWindow.setStatusBar(statusbar)

_translate = QtCore.QCoreApplication.translate
MainWindow.setWindowTitle(_translate("MainWindow", "ArcheryStats"))
saveDataButton.setText(_translate("MainWindow", "Save Data to Database"))
retrieveDataButton.setText(_translate("MainWindow", "Refresh Database View"))
generatePieGraph.setText(_translate("MainWindow", "Generate Pie Graph"))
deleteDataButton.setText(_translate("MainWindow", "Delete Selected Data"))
savePieGraph.setText(_translate("MainWindow", "Save Pie Graph"))

MainWindow.show()
sys.exit(app.exec_())
