from ui.views.visor import VisorImagenes
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    # app.setStyleSheet("* { font-family: 'Arial'; }")
    ventana = VisorImagenes()
    ventana.show()
    sys.exit(app.exec())
        
        
if __name__ == "__main__":
    main()