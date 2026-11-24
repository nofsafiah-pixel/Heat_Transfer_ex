from pathlib import Path

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("graphWindow")
        self.setWindowTitle("Temperature Graphs")
        self.setMinimumSize(820, 600)

        stylesheet_path = Path(__file__).with_name("graph_window.qss")
        self.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))

        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(28, 24, 28, 24)
        window_layout.setSpacing(16)

        page_title = QLabel("Temperature Graphs")
        page_title.setObjectName("graphTitle")
        window_layout.addWidget(page_title)

        series_row = QHBoxLayout()
        series_label = QLabel("Display series")
        series_label.setObjectName("seriesLabel")
        series_row.addWidget(series_label)

        self.series_selector = QComboBox()
        self.series_selector.setObjectName("seriesSelector")
        self.series_selector.addItems(["Left Body", "Right Body", "Both"])
        self.series_selector.setMinimumWidth(190)
        series_row.addWidget(self.series_selector)
        series_row.addStretch()
        window_layout.addLayout(series_row)

        graph_frame = QFrame()
        graph_frame.setObjectName("graphFrame")
        graph_layout = QVBoxLayout(graph_frame)
        graph_layout.setContentsMargins(12, 12, 12, 12)

        self.figure = Figure(figsize=(8, 5))
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setObjectName("graphCanvas")
        graph_layout.addWidget(self.canvas)
        window_layout.addWidget(graph_frame, 1)

        button_row = QHBoxLayout()
        button_row.addStretch()

        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("resetButton")
        self.reset_button.clicked.connect(self.plot_data)
        button_row.addWidget(self.reset_button)

        self.save_csv_button = QPushButton("Save CSV")
        self.save_csv_button.setObjectName("secondaryButton")
        self.save_csv_button.clicked.connect(self._show_csv_placeholder)
        button_row.addWidget(self.save_csv_button)

        self.save_graph_button = QPushButton("Save Graph")
        self.save_graph_button.setObjectName("secondaryButton")
        self.save_graph_button.clicked.connect(self._show_save_graph_placeholder)
        button_row.addWidget(self.save_graph_button)
        window_layout.addLayout(button_row)

        self.plot_data()

    def plot_data(self) -> None:
        """Set up placeholder axes for future simulation data."""
        self.axes.clear()
        self.axes.set_title("Temperature over time")
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Temperature (°C)")
        self.axes.grid(True)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def _show_csv_placeholder(self) -> None:
        QMessageBox.information(
            self,
            "Save CSV",
            "CSV export will be added with the simulation data.",
        )

    def _show_save_graph_placeholder(self) -> None:
        QMessageBox.information(
            self,
            "Save Graph",
            "Graph saving will be available when plotting is implemented.",
        )
