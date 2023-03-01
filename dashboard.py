import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Dashboard')
        
        # Create a label to display the video frame
        self.label = QLabel()
        
        # Create a layout to organize the label
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        # Create a layout for the side panel
        side_panel_layout = QVBoxLayout()

        # Define the font and text to be displayed
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.doubted = 0
        self.total = 0
        self.leaky = 0
        self.verified = 0

        # Add labels for each variable and its value to the side panel
        self.doubted_label = QLabel('Doubted: {}'.format(self.doubted))
        self.total_label = QLabel('Total: {}'.format(self.total))
        self.leaky_label = QLabel('Leaky: {}'.format(self.leaky))
        self.verified_label = QLabel('Verified: {}'.format(self.verified))
        side_panel_layout.addWidget(self.doubted_label)
        side_panel_layout.addWidget(self.total_label)
        side_panel_layout.addWidget(self.leaky_label)
        side_panel_layout.addWidget(self.verified_label)

        # Create a horizontal layout to hold the video frame and the side panel
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.label)
        horizontal_layout.addLayout(side_panel_layout)

        # Set the layout for the widget
        layout.addLayout(horizontal_layout)
        self.setLayout(layout)
        
        # Initialize the video capture object
        self.cap = cv2.VideoCapture(0)

        self.update_side_panel()

    def update_side_panel(self):
        # Update the values displayed in the side panel
        self.doubted_label.setText('Doubted: {}'.format(self.doubted))
        self.total_label.setText('Total: {}'.format(self.total))
        self.leaky_label.setText('Leaky: {}'.format(self.leaky))
        self.verified_label.setText('Verified: {}'.format(self.verified))

    def update_frame(self):
        # Read a frame from the video capture object
        ret, frame = self.cap.read()
        
        if ret:
            # Add text to the frame
            cv2.putText(frame, 'Hello, World!', (50, 50), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Convert the frame to a QImage
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # Set the QImage as the pixmap for the label
            pixmap = QPixmap.fromImage(q_image)
            self.label.setPixmap(pixmap)
            
    def closeEvent(self, event):
        # Release the video capture object
        self.cap.release()
        
        # Call the base class closeEvent() function
        super().closeEvent(event)
        
if __name__ == '__main__':
    # Create the application object
    app = QApplication(sys.argv)
    
    # Create the dashboard widget
    dashboard = Dashboard()
    
    # Set the size of the dashboard
    dashboard.resize(640, 480)
    
    # Show the dashboard
    dashboard.show()
    
    # Start a timer to update the video frame
    timer = QTimer()
    timer.timeout.connect(dashboard.update_frame)
    timer.start(30)
    
    # Run the event loop
    sys.exit(app.exec_())
