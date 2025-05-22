from PyQt6.QtWidgets import QMessageBox, QHBoxLayout, QVBoxLayout

LANG_DICT: dict


# Messagem na tela
def message(mtype, text):
    types = [LANG_DICT["info"], LANG_DICT["warning"], LANG_DICT["error"]]

    msg = QMessageBox()
    msg.setWindowTitle(types[mtype])
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


# Pergunta sim ou não
def ask_yes_no(text):
    msg = QMessageBox()
    msg.setWindowTitle(LANG_DICT["confirmation"])
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

    if msg.exec() != QMessageBox.StandardButton.Yes:
        return False

    return True


# Cria layouts espaçados
def spaced_layout(layout: QHBoxLayout | QVBoxLayout, stretch: int, widgets: list):
    layout.addStretch(stretch)

    for widget in widgets:
        layout.addWidget(widget)

    layout.addStretch(stretch)

    return layout
