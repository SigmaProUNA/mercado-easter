from PyQt6.QtWidgets import QMessageBox, QVBoxLayout, QInputDialog, QTableView, QDialog, QLabel, QPushButton, QTextEdit
from PyQt6.QtGui import QStandardItemModel
import fastmath

LANG_DICT: dict


# Messagem na tela
def message(mtype, text):
    types = [LANG_DICT["info"], LANG_DICT["warning"], LANG_DICT["error"]]

    msg = QMessageBox()
    msg.setWindowTitle(types[mtype])
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def ask_input(text: str, title: str, default: str = "", input_type: type = str) -> str:
    input_dialog = QInputDialog()
    input_dialog.setWindowTitle(title)
    input_dialog.setLabelText(text)
    input_dialog.setTextValue(default)

    if input_dialog.exec() == QInputDialog.DialogCode.Accepted:
        inp = input_dialog.textValue()
        
        if inp == "":
            return ""
        
        # Verifica se o input é igual ao tipo esperado
        if input_type == int:
            while not fastmath.is_integer(inp):
                message(1, LANG_DICT["invalid_type_int"])
                inp = ask_input(text, title, default, input_type)
        
        return inp
    else:
        return ""
    
    
def ask_yes_no(text: str, title: str) -> bool:
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg.setDefaultButton(QMessageBox.StandardButton.No)
    
    if msg.exec() == QMessageBox.StandardButton.Yes:
        return True
    else:
        return False
    
    
# Exibir um dialogo com tabela e botão de fechar
def table_dialog(title: str, label: str, headers: list, content: list[list]):    
    dialog = QDialog()
    dialog.setWindowTitle(title)
    dialog.setMinimumSize(600, 400)
    dialog_layout = QVBoxLayout()
    
    text_label = QLabel(label)
    close_button = QPushButton(LANG_DICT["close"])
    close_button.clicked.connect(dialog.close)
    
    row_count = len(content)
    column_count = len(headers)
    table = QTableView()
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(headers)
    
    model.setRowCount(row_count)
    model.setColumnCount(column_count)
    
    for row in range(row_count):
        for column in range(column_count):
            indx = model.index(row, column)
            model.setData(indx, str(content[row][column]))
    
    table.setModel(model)
    
    dialog_layout.addWidget(text_label)
    dialog_layout.addWidget(table)
    dialog_layout.addWidget(close_button)
    
    dialog.setLayout(dialog_layout)
    dialog.exec()
    

# Exibe texto markdown
def show_markdown(text: str, title: str):
    dialog = QDialog()
    dialog.setWindowTitle(title)
    
    layout = QVBoxLayout()
    text_edit = QTextEdit()
    close_button = QPushButton(LANG_DICT["close"])
    close_button.clicked.connect(dialog.close)
    
    text_edit.setMarkdown(text)
    layout.addWidget(text_edit)
    layout.addWidget(close_button)
    
    dialog.setLayout(layout)
    dialog.exec()

