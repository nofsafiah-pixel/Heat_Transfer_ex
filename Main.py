from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from about import AboutWindow
from graph_window import GraphWindow


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("heatTransferWindow")
        self.setWindowTitle("Heat Transfer | Thermal Lab")
        self.setMinimumSize(1060, 760)

        stylesheet_path = Path(__file__).with_name("style.qss")
        self.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(34, 28, 34, 28)
        page_layout.setSpacing(22)

        heading_layout = QVBoxLayout()
        heading_layout.setSpacing(5)

        page_eyebrow = QLabel("THERMAL LAB  /  STEP 02A")
        page_eyebrow.setObjectName("pageEyebrow")
        heading_layout.addWidget(page_eyebrow)

        page_title = QLabel("Heat Transfer")
        page_title.setObjectName("pageTitle")
        heading_layout.addWidget(page_title)

        page_subtitle = QLabel(
            "Set up two bodies and the conductive path between them."
        )
        page_subtitle.setObjectName("pageSubtitle")
        heading_layout.addWidget(page_subtitle)
        page_layout.addLayout(heading_layout)

        bodies_layout = QHBoxLayout()
        bodies_layout.setSpacing(18)

        (
            self.left_body_card,
            self.left_temperature_slider,
            self.left_temperature_display,
        ) = self._create_body_panel(
            "left",
            "Left body",
            "HOT RESERVOIR",
            200,
        )
        bodies_layout.addWidget(self.left_body_card, 5)

        bridge_panel = self._create_bridge_panel()
        bodies_layout.addWidget(bridge_panel, 3)

        (
            self.right_body_card,
            self.right_temperature_slider,
            self.right_temperature_display,
        ) = self._create_body_panel(
            "right",
            "Right body",
            "COOL RESERVOIR",
            0,
        )
        bodies_layout.addWidget(self.right_body_card, 5)

        self.left_temperature_slider.valueChanged.connect(
            self.left_temperature_display.setValue
        )
        self.right_temperature_slider.valueChanged.connect(
            self.right_temperature_display.setValue
        )
        page_layout.addLayout(bodies_layout, 1)

        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)
        action_layout.addStretch()

        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setCheckable(True)
        self.start_button.setMinimumWidth(150)
        action_layout.addWidget(self.start_button)

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setObjectName("secondaryButton")
        self.graphs_button.setMinimumWidth(120)
        self.graph_window = GraphWindow()
        self.graphs_button.clicked.connect(self._open_graph_window)
        action_layout.addWidget(self.graphs_button)

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("secondaryButton")
        self.about_button.setMinimumWidth(120)
        self.about_button.clicked.connect(self._open_about_window)
        action_layout.addWidget(self.about_button)

        page_layout.addLayout(action_layout)
        self.about_window = None

    def _create_body_panel(
        self,
        side_name: str,
        title: str,
        reservoir_caption: str,
        initial_temperature: int,
    ) -> tuple[QFrame, QSlider, QDoubleSpinBox]:
        body_card = QFrame()
        body_card.setObjectName(f"{side_name}BodyCard")
        body_layout = QVBoxLayout(body_card)
        body_layout.setContentsMargins(22, 20, 22, 22)
        body_layout.setSpacing(14)

        body_heading = QLabel(title)
        body_heading.setObjectName("bodyTitle")
        body_layout.addWidget(body_heading)

        body_caption = QLabel(reservoir_caption)
        body_caption.setObjectName(f"{side_name}ReservoirCaption")
        body_layout.addWidget(body_caption)

        material_label = QLabel("Material")
        material_label.setObjectName(f"{side_name}MaterialLabel")
        body_layout.addWidget(material_label)

        material_selector = QComboBox()
        material_selector.setObjectName(f"{side_name}MaterialSelector")
        material_selector.addItems(
            ["Custom", "Water", "Copper", "Iron", "Aluminum"]
        )
        body_layout.addWidget(material_selector)

        temperature_row = QHBoxLayout()
        temperature_label = QLabel("Temperature")
        temperature_label.setObjectName(f"{side_name}TemperatureLabel")
        temperature_row.addWidget(temperature_label)
        temperature_row.addStretch()

        temperature_display = QDoubleSpinBox()
        temperature_display.setObjectName(f"{side_name}TemperatureDisplay")
        temperature_display.setRange(0.0, 200.0)
        temperature_display.setDecimals(1)
        temperature_display.setSuffix(" °C")
        temperature_display.setReadOnly(True)
        temperature_display.setButtonSymbols(QDoubleSpinBox.NoButtons)
        temperature_display.setValue(float(initial_temperature))
        temperature_row.addWidget(temperature_display)
        body_layout.addLayout(temperature_row)

        temperature_slider = QSlider(Qt.Horizontal)
        temperature_slider.setObjectName(f"{side_name}TemperatureSlider")
        temperature_slider.setRange(0, 200)
        temperature_slider.setValue(initial_temperature)
        temperature_slider.setAccessibleName(f"{title} temperature")
        body_layout.addWidget(temperature_slider)

        properties_layout = QGridLayout()
        properties_layout.setHorizontalSpacing(12)
        properties_layout.setVerticalSpacing(12)

        mass_label = QLabel("Mass")
        mass_label.setObjectName(f"{side_name}MassLabel")
        properties_layout.addWidget(mass_label, 0, 0)

        mass_input = self._create_parameter_input(
            f"{side_name}MassInput",
            " kg",
            10.0,
        )
        properties_layout.addWidget(mass_input, 0, 1)

        heat_capacity_label = QLabel("Heat capacity")
        heat_capacity_label.setObjectName(f"{side_name}HeatCapacityLabel")
        heat_capacity_label.setWordWrap(True)
        properties_layout.addWidget(heat_capacity_label, 1, 0)

        heat_capacity_input = self._create_parameter_input(
            f"{side_name}HeatCapacityInput",
            " J/kg°C",
            0.4,
        )
        properties_layout.addWidget(heat_capacity_input, 1, 1)
        body_layout.addLayout(properties_layout)
        body_layout.addStretch()

        return body_card, temperature_slider, temperature_display

    def _create_bridge_panel(self) -> QFrame:
        bridge_panel = QFrame()
        bridge_panel.setObjectName("bridgePanel")
        bridge_layout = QVBoxLayout(bridge_panel)
        bridge_layout.setContentsMargins(18, 22, 18, 22)
        bridge_layout.setSpacing(15)

        bridge_heading = QLabel("CONDUCTIVE PATH")
        bridge_heading.setObjectName("bridgeHeading")
        bridge_heading.setAlignment(Qt.AlignCenter)
        bridge_layout.addWidget(bridge_heading)

        bridge_bar = QFrame()
        bridge_bar.setObjectName("bridgeBar")
        bridge_bar.setFixedHeight(18)
        bridge_layout.addWidget(bridge_bar)

        bridge_caption = QLabel("Thermal bridge")
        bridge_caption.setObjectName("bridgeCaption")
        bridge_caption.setAlignment(Qt.AlignCenter)
        bridge_layout.addWidget(bridge_caption)

        bridge_description = QLabel("Heat transfers between the two bodies")
        bridge_description.setObjectName("bridgeDescription")
        bridge_description.setWordWrap(True)
        bridge_description.setAlignment(Qt.AlignCenter)
        bridge_layout.addWidget(bridge_description)

        conductivity_label = QLabel("Conductivity")
        conductivity_label.setObjectName("conductivityLabel")
        bridge_layout.addWidget(conductivity_label)

        self.conductivity_input = self._create_parameter_input(
            "conductivityInput",
            " J/s°C",
            1.0,
        )
        bridge_layout.addWidget(self.conductivity_input)
        bridge_layout.addStretch()
        return bridge_panel

    @staticmethod
    def _create_parameter_input(
        object_name: str,
        suffix: str,
        initial_value: float,
    ) -> QDoubleSpinBox:
        parameter_input = QDoubleSpinBox()
        parameter_input.setObjectName(object_name)
        parameter_input.setRange(0.01, 10000.0)
        parameter_input.setDecimals(2)
        parameter_input.setSingleStep(0.01)
        parameter_input.setValue(initial_value)
        parameter_input.setSuffix(suffix)
        return parameter_input

    def _open_about_window(self) -> None:
        self.about_window = AboutWindow()
        self.about_window.show()

    def _open_graph_window(self) -> None:
        self.graph_window.show()
        self.graph_window.raise_()
        self.graph_window.activateWindow()


if __name__ == "__main__":
    app = QApplication()
    window = HeatTransfer()
    window.show()
    app.exec()
