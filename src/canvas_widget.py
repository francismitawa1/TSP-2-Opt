"""
Canvas Widget for 2-Opt TSP Visualization
Shows edge swaps and tour improvements
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
import math


class TwoOptCanvas(QWidget):
    """Custom canvas for visualizing 2-Opt algorithm"""
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 500)
        self.setStyleSheet("background-color: white; border: 2px solid #e0e0e0; border-radius: 8px;")
        
        # Data
        self.cities = []
        self.current_tour = None
        self.scaled_cities = []
        
        # Visualization state
        self.considering_swap = None  # (i, k) indices being considered
        self.swap_performed = None  # Recently performed swap
        self.swap_highlight_counter = 0
    
    def set_cities(self, cities):
        """Set cities to display"""
        self.cities = cities
        self.current_tour = None
        self.considering_swap = None
        self.swap_performed = None
        self.update()
    
    def set_tour(self, tour):
        """Set current tour"""
        self.current_tour = tour
        self.update()
    
    def set_considering_swap(self, swap_indices):
        """Highlight edges being considered for swap"""
        self.considering_swap = swap_indices
        self.update()
    
    def set_swap_performed(self, swap_indices):
        """Show swap that was just performed"""
        self.swap_performed = swap_indices
        self.swap_highlight_counter = 10  # Frames to highlight
        self.update()
    
    def clear_visualization(self):
        """Clear all visualization"""
        self.current_tour = None
        self.considering_swap = None
        self.swap_performed = None
        self.update()
    
    def scale_coordinates(self):
        """Scale city coordinates to canvas"""
        if not self.cities:
            return
        
        width = self.width()
        height = self.height()
        padding = 60
        
        x_coords = [city[1] for city in self.cities]
        y_coords = [city[2] for city in self.cities]
        
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        x_range = x_max - x_min if x_max != x_min else 1
        y_range = y_max - y_min if y_max != y_min else 1
        
        self.scaled_cities = []
        for name, x, y in self.cities:
            canvas_x = padding + ((x - x_min) / x_range) * (width - 2 * padding)
            canvas_y = padding + ((y - y_min) / y_range) * (height - 2 * padding)
            self.scaled_cities.append((name, canvas_x, canvas_y))
    
    def paintEvent(self, event):
        """Paint the canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.cities:
            self.draw_empty_state(painter)
            return
        
        self.scale_coordinates()
        
        # Draw current tour
        if self.current_tour and len(self.current_tour) > 1:
            self.draw_tour(painter)
        
        # Draw swap highlights
        if self.considering_swap:
            self.draw_considering_swap(painter)
        
        if self.swap_performed and self.swap_highlight_counter > 0:
            self.draw_swap_performed(painter)
            self.swap_highlight_counter -= 1
        
        # Draw cities
        self.draw_cities(painter)
    
    def draw_empty_state(self, painter):
        """Draw empty state message"""
        painter.setPen(QPen(QColor("#999999")))
        painter.setFont(QFont("Arial", 12))
        text = "Add cities to visualize 2-Opt algorithm"
        painter.drawText(self.rect(), Qt.AlignCenter, text)
    
    def draw_cities(self, painter):
        """Draw city markers"""
        for i, (name, x, y) in enumerate(self.scaled_cities):
            # Start city in green
            if i == 0:
                color = QColor("#4CAF50")
            else:
                color = QColor("#2196F3")
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color.darker(120), 2))
            painter.drawEllipse(QPointF(x, y), 10, 10)
            
            # City label
            painter.setPen(QPen(Qt.black))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            label_rect = QRectF(x - 40, y - 28, 80, 20)
            painter.drawText(label_rect, Qt.AlignCenter, name)
            
            # City index
            painter.setFont(QFont("Arial", 8))
            painter.setPen(QPen(Qt.white))
            index_rect = QRectF(x - 5, y - 3, 10, 10)
            painter.drawText(index_rect, Qt.AlignCenter, str(i))
    
    def draw_tour(self, painter):
        """Draw the current tour"""
        if not self.current_tour or len(self.current_tour) < 2:
            return
        
        # Draw all edges in blue
        painter.setPen(QPen(QColor("#2196F3"), 2, Qt.SolidLine))
        
        for i in range(len(self.current_tour)):
            idx1 = self.current_tour[i]
            idx2 = self.current_tour[(i + 1) % len(self.current_tour)]
            
            if idx1 < len(self.scaled_cities) and idx2 < len(self.scaled_cities):
                city1 = self.scaled_cities[idx1]
                city2 = self.scaled_cities[idx2]
                
                painter.drawLine(QPointF(city1[1], city1[2]), 
                               QPointF(city2[1], city2[2]))
    
    def draw_considering_swap(self, painter):
        """Highlight edges being considered for swap"""
        if not self.considering_swap or not self.current_tour:
            return
        
        i, k = self.considering_swap
        n = len(self.current_tour)
        
        # Edges that would be removed (red dashed)
        edge1_start = self.current_tour[i-1]
        edge1_end = self.current_tour[i]
        edge2_start = self.current_tour[k]
        edge2_end = self.current_tour[(k+1) % n]
        
        painter.setPen(QPen(QColor("#F44336"), 3, Qt.DashLine))
        
        # Draw first edge to remove
        if edge1_start < len(self.scaled_cities) and edge1_end < len(self.scaled_cities):
            c1 = self.scaled_cities[edge1_start]
            c2 = self.scaled_cities[edge1_end]
            painter.drawLine(QPointF(c1[1], c1[2]), QPointF(c2[1], c2[2]))
        
        # Draw second edge to remove
        if edge2_start < len(self.scaled_cities) and edge2_end < len(self.scaled_cities):
            c1 = self.scaled_cities[edge2_start]
            c2 = self.scaled_cities[edge2_end]
            painter.drawLine(QPointF(c1[1], c1[2]), QPointF(c2[1], c2[2]))
        
        # Edges that would be added (green dashed)
        painter.setPen(QPen(QColor("#4CAF50"), 3, Qt.DashLine))
        
        # New edge 1
        if edge1_start < len(self.scaled_cities) and edge2_start < len(self.scaled_cities):
            c1 = self.scaled_cities[edge1_start]
            c2 = self.scaled_cities[edge2_start]
            painter.drawLine(QPointF(c1[1], c1[2]), QPointF(c2[1], c2[2]))
        
        # New edge 2
        if edge1_end < len(self.scaled_cities) and edge2_end < len(self.scaled_cities):
            c1 = self.scaled_cities[edge1_end]
            c2 = self.scaled_cities[edge2_end]
            painter.drawLine(QPointF(c1[1], c1[2]), QPointF(c2[1], c2[2]))
    
    def draw_swap_performed(self, painter):
        """Highlight swap that was just performed"""
        if not self.swap_performed or not self.current_tour:
            return
        
        i, k = self.swap_performed
        n = len(self.current_tour)
        
        # Highlight the new edges in bright green
        edge1_start = self.current_tour[i-1]
        edge2_start = self.current_tour[k]
        edge1_end = self.current_tour[i]
        edge2_end = self.current_tour[(k+1) % n]
        
        # Pulsing effect
        alpha = int(255 * (self.swap_highlight_counter / 10))
        painter.setPen(QPen(QColor(76, 175, 80, alpha), 5, Qt.SolidLine))
        
        # Draw new edges
        if edge1_start < len(self.scaled_cities) and edge2_start < len(self.scaled_cities):
            c1 = self.scaled_cities[edge1_start]
            c2 = self.scaled_cities[edge2_start]
            painter.drawLine(QPointF(c1[1], c1[2]), QPointF(c2[1], c2[2]))
        
        if edge1_end < len(self.scaled_cities) and edge2_end < len(self.scaled_cities):
            c1 = self.scaled_cities[edge1_end]
            c2 = self.scaled_cities[edge2_end]
            painter.drawLine(QPointF(c1[1], c1[2]), QPointF(c2[1], c2[2]))