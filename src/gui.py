"""
PyQt5 GUI for 2-Opt TSP Solver
Professional interface with swap visualization
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QListWidget, 
                             QGroupBox, QGridLayout, QMessageBox, QProgressBar,
                             QSplitter, QFrame, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import sys

from src.algorithm import TwoOptTSP
from src.canvas_widget import TwoOptCanvas


class SolverThread(QThread):
    """Background thread for running 2-Opt solver"""
    
    progress_update = pyqtSignal(dict)
    solution_found = pyqtSignal(list, float)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, cities, initial_method='nearest_neighbor'):
        super().__init__()
        self.cities = cities
        self.initial_method = initial_method
        self.solver = None
        self.should_stop = False
        
    def run(self):
        """Execute solving in background"""
        try:
            self.solver = TwoOptTSP(self.cities)
            self.solver.set_progress_callback(self.on_progress)
            
            tour, distance = self.solver.solve(self.initial_method)
            
            if not self.should_stop:
                self.solution_found.emit(tour, distance)
                
        except Exception as e:
            self.error_occurred.emit(str(e))
    
    def on_progress(self, stats):
        """Handle progress updates"""
        if not self.should_stop:
            self.progress_update.emit(stats)
    
    def stop(self):
        """Stop solver"""
        self.should_stop = True


class TwoOptMainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TSP 2-Opt Solver - Local Search Optimization")
        self.setGeometry(100, 100, 1400, 800)
        
        # Data
        self.cities = []
        self.solution = None
        self.total_distance = 0
        self.solver_thread = None
        
        # Setup UI
        self.init_ui()
        self.apply_styles()
        
    def init_ui(self):
        """Initialize user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Right panel
        right_panel = self.create_visualization_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([400, 1000])
        
    def create_control_panel(self):
        """Create control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("🔄 2-Opt TSP Solver")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # City input
        input_group = QGroupBox("Add New City")
        input_layout = QGridLayout()
        
        input_layout.addWidget(QLabel("City Name:"), 0, 0)
        self.city_name_input = QLineEdit()
        self.city_name_input.setPlaceholderText("e.g., Paris")
        input_layout.addWidget(self.city_name_input, 0, 1)
        
        input_layout.addWidget(QLabel("X Coordinate:"), 1, 0)
        self.x_coord_input = QLineEdit()
        self.x_coord_input.setPlaceholderText("e.g., 150.0")
        input_layout.addWidget(self.x_coord_input, 1, 1)
        
        input_layout.addWidget(QLabel("Y Coordinate:"), 2, 0)
        self.y_coord_input = QLineEdit()
        self.y_coord_input.setPlaceholderText("e.g., 200.0")
        input_layout.addWidget(self.y_coord_input, 2, 1)
        
        self.add_city_btn = QPushButton("➕ Add City")
        self.add_city_btn.clicked.connect(self.add_city)
        input_layout.addWidget(self.add_city_btn, 3, 0, 1, 2)
        
        self.load_sample_btn = QPushButton("📋 Load Sample Cities")
        self.load_sample_btn.clicked.connect(self.load_sample_cities)
        input_layout.addWidget(self.load_sample_btn, 4, 0, 1, 2)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Cities list
        list_group = QGroupBox("Cities Added")
        list_layout = QVBoxLayout()
        
        self.cities_list = QListWidget()
        self.cities_list.setMaximumHeight(120)
        list_layout.addWidget(self.cities_list)
        
        self.remove_city_btn = QPushButton("🗑️ Remove Selected")
        self.remove_city_btn.clicked.connect(self.remove_city)
        list_layout.addWidget(self.remove_city_btn)
        
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # Algorithm settings
        settings_group = QGroupBox("Algorithm Settings")
        settings_layout = QVBoxLayout()
        
        settings_layout.addWidget(QLabel("Initial Tour Method:"))
        self.initial_method_combo = QComboBox()
        self.initial_method_combo.addItems(["Nearest Neighbor", "Random"])
        settings_layout.addWidget(self.initial_method_combo)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Control buttons
        control_group = QGroupBox("Solver Controls")
        control_layout = QVBoxLayout()
        
        self.start_btn = QPushButton("▶️ Start 2-Opt")
        self.start_btn.clicked.connect(self.start_solving)
        self.start_btn.setMinimumHeight(45)
        control_layout.addWidget(self.start_btn)
        
        self.reset_btn = QPushButton("🔄 Reset")
        self.reset_btn.clicked.connect(self.reset_all)
        self.reset_btn.setMinimumHeight(45)
        control_layout.addWidget(self.reset_btn)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Statistics
        stats_group = QGroupBox("Algorithm Statistics")
        stats_layout = QVBoxLayout()
        
        self.iterations_label = QLabel("Iterations: 0")
        self.swaps_label = QLabel("Swaps Made: 0")
        self.improvements_label = QLabel("Improvements: 0")
        self.time_label = QLabel("Computation Time: 0.000s")
        self.improvement_pct_label = QLabel("Tour Improvement: 0%")
        self.current_action_label = QLabel("Action: Ready")
        self.current_action_label.setWordWrap(True)
        
        for label in [self.iterations_label, self.swaps_label,
                     self.improvements_label, self.time_label,
                     self.improvement_pct_label, self.current_action_label]:
            label.setFont(QFont("Consolas", 9))
            stats_layout.addWidget(label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        stats_layout.addWidget(self.progress_bar)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        
        self.distance_label = QLabel("Total Distance: N/A")
        self.distance_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.distance_label.setStyleSheet("color: #2E7D32;")
        results_layout.addWidget(self.distance_label)
        
        self.initial_distance_label = QLabel("Initial Distance: N/A")
        self.initial_distance_label.setFont(QFont("Arial", 10))
        results_layout.addWidget(self.initial_distance_label)
        
        self.status_label = QLabel("Status: Ready")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setWordWrap(True)
        results_layout.addWidget(self.status_label)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
        
        return panel
    
    def create_visualization_panel(self):
        """Create visualization panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        title = QLabel("2-Opt Edge Swap Visualization")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.canvas = TwoOptCanvas()
        layout.addWidget(self.canvas)
        
        # Legend
        legend_frame = QFrame()
        legend_frame.setFrameStyle(QFrame.Box)
        legend_layout = QHBoxLayout(legend_frame)
        
        legend_layout.addWidget(QLabel("🔵 Current Tour"))
        legend_layout.addWidget(QLabel("🔴 Edges to Remove"))
        legend_layout.addWidget(QLabel("🟢 New Edges"))
        legend_layout.addWidget(QLabel("✨ Swap Performed"))
        legend_layout.addStretch()
        
        layout.addWidget(legend_frame)
        
        instructions = QLabel("💡 Add at least 4 cities and click 'Start 2-Opt' to watch edge swaps!")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(instructions)
        
        return panel
    
    def apply_styles(self):
        """Apply styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
            QPushButton:pressed {
                background-color: #E65100;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #FF9800;
            }
            QListWidget {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
            }
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #FF9800;
            }
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
            }
        """)
    
    def add_city(self):
        """Add city to list"""
        try:
            name = self.city_name_input.text().strip()
            x = float(self.x_coord_input.text())
            y = float(self.y_coord_input.text())
            
            if not name:
                QMessageBox.warning(self, "Invalid Input", "Please enter a city name")
                return
            
            if any(city[0] == name for city in self.cities):
                QMessageBox.warning(self, "Duplicate", f"City '{name}' already exists")
                return
            
            self.cities.append((name, x, y))
            self.cities_list.addItem(f"{name} ({x:.1f}, {y:.1f})")
            
            self.city_name_input.clear()
            self.x_coord_input.clear()
            self.y_coord_input.clear()
            self.city_name_input.setFocus()
            
            self.canvas.set_cities(self.cities)
            self.status_label.setText(f"Status: {len(self.cities)} cities added")
            
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", 
                               "Please enter valid numeric coordinates")
    
    def remove_city(self):
        """Remove selected city"""
        current_row = self.cities_list.currentRow()
        if current_row >= 0:
            self.cities.pop(current_row)
            self.cities_list.takeItem(current_row)
            self.canvas.set_cities(self.cities)
            self.status_label.setText(f"Status: {len(self.cities)} cities added")
    
    def load_sample_cities(self):
        """Load sample cities"""
        sample_cities = [
            ("A", 50, 200),
            ("B", 300, 350),
            ("C", 150, 100),
            ("D", 250, 400),
            ("E", 400, 300),
            ("F", 100, 150),
            ("G", 350, 150),
            ("H", 200, 250)
        ]
        
        self.cities = sample_cities
        self.cities_list.clear()
        for name, x, y in sample_cities:
            self.cities_list.addItem(f"{name} ({x:.1f}, {y:.1f})")
        
        self.canvas.set_cities(self.cities)
        self.status_label.setText(f"Status: {len(self.cities)} sample cities loaded")
    
    def start_solving(self):
        """Start solving"""
        if len(self.cities) < 4:
            QMessageBox.warning(self, "Insufficient Cities",
                              "Please add at least 4 cities")
            return
        
        self.start_btn.setEnabled(False)
        self.add_city_btn.setEnabled(False)
        self.load_sample_btn.setEnabled(False)
        self.initial_method_combo.setEnabled(False)
        
        self.progress_bar.setVisible(True)
        self.status_label.setText("Status: Starting 2-Opt algorithm...")
        self.current_action_label.setText("Action: Initializing...")
        
        # Get initial method
        method = 'nearest_neighbor' if self.initial_method_combo.currentIndex() == 0 else 'random'
        
        self.solver_thread = SolverThread(self.cities, method)
        self.solver_thread.progress_update.connect(self.on_progress_update)
        self.solver_thread.solution_found.connect(self.on_solution_found)
        self.solver_thread.error_occurred.connect(self.on_error)
        self.solver_thread.start()
    
    def on_progress_update(self, stats):
        """Handle progress updates"""
        iteration = stats.get('iteration', 0)
        swaps = stats.get('swaps_made', 0)
        improvements = stats.get('improvements', 0)
        distance = stats.get('distance', 0)
        phase = stats.get('phase', 'unknown')
        
        self.iterations_label.setText(f"Iterations: {iteration}")
        self.swaps_label.setText(f"Swaps Made: {swaps}")
        self.improvements_label.setText(f"Improvements: {improvements}")
        self.distance_label.setText(f"Current Distance: {distance:.2f}")
        
        # Update canvas
        if stats.get('tour'):
            self.canvas.set_tour(stats['tour'])
        
        if phase == 'initial':
            self.current_action_label.setText("Action: Created initial tour")
            self.initial_distance_label.setText(f"Initial Distance: {distance:.2f}")
        
        elif phase == 'searching':
            if stats.get('considering_swap'):
                self.canvas.set_considering_swap(stats['considering_swap'])
                i, k = stats['considering_swap']
                self.current_action_label.setText(f"Action: Considering swap at positions {i} and {k}")
        
        elif phase == 'swap':
            if stats.get('swap_performed'):
                self.canvas.set_swap_performed(stats['swap_performed'])
                improvement = stats.get('improvement', 0)
                self.current_action_label.setText(
                    f"Action: ✓ Swap performed! Improved by {improvement:.2f}"
                )
        
        self.status_label.setText(f"Status: Running... (Iteration {iteration})")
    
    def on_solution_found(self, tour, distance):
        """Handle solution found"""
        self.solution = tour
        self.total_distance = distance
        
        self.distance_label.setText(f"Final Distance: {distance:.2f}")
        self.status_label.setText("Status: ✅ 2-Opt Complete!")
        self.current_action_label.setText("Action: No more improvements possible")
        self.progress_bar.setVisible(False)
        
        if self.solver_thread and self.solver_thread.solver:
            stats = self.solver_thread.solver.get_statistics()
            self.iterations_label.setText(f"Iterations: {stats['iterations']}")
            self.swaps_label.setText(f"Swaps Made: {stats['swaps_made']}")
            self.improvements_label.setText(f"Improvements: {stats['improvements']}")
            self.time_label.setText(f"Computation Time: {stats['computation_time']:.3f}s")
            self.improvement_pct_label.setText(f"Tour Improvement: {stats['improvement_percent']:.1f}%")
        
        self.canvas.set_tour(self.solution)
        
        self.start_btn.setEnabled(True)
        self.add_city_btn.setEnabled(True)
        self.load_sample_btn.setEnabled(True)
        self.initial_method_combo.setEnabled(True)
    
    def on_error(self, error_msg):
        """Handle error"""
        QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")
        self.reset_all()
    
    def reset_all(self):
        """Reset everything"""
        if self.solver_thread and self.solver_thread.isRunning():
            self.solver_thread.stop()
            self.solver_thread.wait()
        
        self.solution = None
        self.total_distance = 0
        
        self.start_btn.setEnabled(True)
        self.add_city_btn.setEnabled(True)
        self.load_sample_btn.setEnabled(True)
        self.initial_method_combo.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        self.distance_label.setText("Total Distance: N/A")
        self.initial_distance_label.setText("Initial Distance: N/A")
        self.status_label.setText("Status: Reset - Ready")
        self.current_action_label.setText("Action: Ready")
        
        self.iterations_label.setText("Iterations: 0")
        self.swaps_label.setText("Swaps Made: 0")
        self.improvements_label.setText("Improvements: 0")
        self.time_label.setText("Computation Time: 0.000s")
        self.improvement_pct_label.setText("Tour Improvement: 0%")
        
        self.canvas.clear_visualization()