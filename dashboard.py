import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Dashboard')
        
        # Create a label to display the video frame
        self.label = QLabel()
        
        # Create a layout to organize the label
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        
        # Set the layout for the widget
        self.setLayout(layout)
        
        # Initialize the video capture object
        self.cap = cv2.VideoCapture(0)
        
        # Define the font and text to be displayed
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.text = 'Hello, World!'
        
    def update_frame(self):
        # Read a frame from the video capture object
        ret, frame = self.cap.read()
        
        if ret:
            # Add text to the frame
            cv2.putText(frame, self.text, (50, 50), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
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
