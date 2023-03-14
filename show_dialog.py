from PyQt6 import QtWidgets, QtGui


def showDialog(msg, dialogFlag, iconFlag):
    msgBox = QtWidgets.QMessageBox()
    msgBox.setWindowTitle("Image Processor")
    msgBox.setWindowIcon(QtGui.QIcon("./Logo/logo.ico"))
    msgBox.setText(msg)

    if iconFlag == "info":
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Information)
    elif iconFlag == "question":
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Question)
    elif iconFlag == "warning":
        msgBox.setIcon(QtWidgets.QMessageBox.Icon.Warning)

    if dialogFlag == "ok":
        msgBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

    elif dialogFlag == "okcancel":
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Ok
            | QtWidgets.QMessageBox.StandardButton.Cancel
        )

    response = msgBox.exec()
    return response
