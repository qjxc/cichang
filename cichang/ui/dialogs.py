from PyQt5 import QtWidgets

class AddCoilDialog(QtWidgets.QDialog):
    """
    对话框：用于输入新线圈的参数（半径、圈数、高度、电流）
    """
    def __init__(self, parent=None):
        super(AddCoilDialog, self).__init__(parent)
        self.setWindowTitle("添加新线圈")
        self.init_ui()
    
    def init_ui(self):
        layout = QtWidgets.QFormLayout(self)
        
        self.radius_edit = QtWidgets.QLineEdit(self)
        self.turns_edit = QtWidgets.QLineEdit(self)
        self.height_edit = QtWidgets.QLineEdit(self)
        self.current_edit = QtWidgets.QLineEdit(self)
        
        layout.addRow("半径:", self.radius_edit)
        layout.addRow("圈数:", self.turns_edit)
        layout.addRow("高度:", self.height_edit)
        layout.addRow("电流:", self.current_edit)
        
        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)
    
    def get_values(self):
        try:
            radius = float(self.radius_edit.text())
            turns = int(self.turns_edit.text())
            height = float(self.height_edit.text())
            current = float(self.current_edit.text())
            return radius, turns, height, current
        except ValueError:
            return None
