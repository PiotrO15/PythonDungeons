import sys

import generator
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox, QLabel
from PySide6.QtGui import QPainter, QColor, QPen, QPixmap
from PySide6.QtCore import Qt, QRect

from generator import Direction


class DungeonGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dungeon Generator")
        self.setGeometry(100, 100, 600, 600)

        self.dungeon_size = 5
        self.room_count = 10
        # self.dungeon, self.doors = self.generate_dungeon(self.room_count)
        self.dungeon = generator.generate_dungeon(self.dungeon_size, self.room_count)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.room_count_spinbox = QSpinBox()
        self.room_count_spinbox.setRange(1, 81)  # Since the grid is 9x9, max 81 rooms
        self.room_count_spinbox.setValue(self.room_count)
        self.room_count_spinbox.valueChanged.connect(self.update_room_count)

        generate_button = QPushButton("Generate Dungeon")
        generate_button.clicked.connect(self.generate_new_dungeon)

        self.dungeon_label = QLabel()
        self.dungeon_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.room_count_spinbox)
        layout.addWidget(generate_button)
        layout.addWidget(self.dungeon_label)

        self.setLayout(layout)

        self.update_dungeon_display()

    def update_room_count(self, value):
        self.room_count = value

    def generate_new_dungeon(self):
        self.dungeon = generator.generate_dungeon(self.dungeon_size, self.room_count)
        self.update_dungeon_display()

    def update_dungeon_display(self):
        pixmap = self.draw_dungeon()
        self.dungeon_label.setPixmap(pixmap)

    def draw_dungeon(self):
        cell_size = 50
        door_size = 10
        margin = 20
        size = self.dungeon_size * cell_size + 2 * margin

        pixmap = QPixmap(size, size)
        pixmap.fill(QColor(50, 50, 50))

        painter = QPainter(pixmap)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(0, 0, 0, 0))
        painter.setPen(pen)

        for y in range(self.dungeon_size):
            for x in range(self.dungeon_size):
                room = self.dungeon[x, y]
                if self.dungeon[x, y]:
                    rect = QRect(margin + x * cell_size + cell_size * 0.1,
                                 margin + y * cell_size + cell_size * 0.1,
                                 int(cell_size * room.size[0] - cell_size * 0.2),
                                 int(cell_size * room.size[1] - cell_size * 0.2))
                    if room.master is None:
                        if self.dungeon[x, y].end:
                            painter.fillRect(rect, Qt.red)
                        else:
                            painter.fillRect(rect, Qt.gray)
                    # Draw doors
                    for neighbor in room.neighbors:
                        if neighbor.direction == Direction.UP:
                            door_rect = QRect(margin + neighbor.position[0] * cell_size + (cell_size - door_size) // 2,
                                              margin + neighbor.position[1] * cell_size - cell_size * 0.1 + 5,
                                              door_size, 5)
                            painter.fillRect(door_rect, Qt.red)
                        if neighbor.direction == Direction.RIGHT:
                            door_rect = QRect(margin + (neighbor.position[0] + 1) * cell_size - cell_size * 0.1,
                                              margin + neighbor.position[1] * cell_size + (cell_size - door_size) // 2,
                                              5, door_size)
                            painter.fillRect(door_rect, Qt.blue)
                        if neighbor.direction == Direction.DOWN:
                            door_rect = QRect(margin + neighbor.position[0] * cell_size + (cell_size - door_size) // 2,
                                              margin + (neighbor.position[1] + 1) * cell_size - cell_size * 0.1,
                                              door_size, 5)
                            painter.fillRect(door_rect, Qt.green)
                        if neighbor.direction == Direction.LEFT:
                            door_rect = QRect(margin + neighbor.position[0] * cell_size - cell_size * 0.1 + 5,
                                              margin + neighbor.position[1] * cell_size + (cell_size - door_size) // 2,
                                              5, door_size)
                            painter.fillRect(door_rect, Qt.yellow)

        painter.end()
        return pixmap


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DungeonGenerator()
    window.show()
    sys.exit(app.exec())