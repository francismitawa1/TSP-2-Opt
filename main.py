"""
TSP 2-Opt Solver - PyQt5 Version
Main entry point for the application
Author: [Francis Mitawa]
Date: November 2025
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.gui import TwoOptMainWindow


def main():
    """Initialize and run the 2-Opt TSP application"""
    app = QApplication(sys.argv)
    
    app.setApplicationName("TSP 2-Opt Solver")
    app.setOrganizationName("University TSP Project")
    
    window = TwoOptMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()