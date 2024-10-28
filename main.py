import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt


class CandyDispenser(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Candy Dispenser with Animation")
        self.setGeometry(100, 100, 400, 400)

        # Initialize stack (as the candy dispenser)
        self.stack = []

        # Create layout
        self.layout = QVBoxLayout()

        # Add a spacer at the top so that candies will be pushed upwards
        self.layout.addSpacerItem(QSpacerItem(20, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Create label to show stack status
        self.stack_label = QLabel("Candy Dispenser is Empty")
        self.layout.addWidget(self.stack_label)

        # Create buttons for push, pop, peek
        self.push_button = QPushButton("Push Candy")
        self.push_button.clicked.connect(self.push_candy)
        self.layout.addWidget(self.push_button)

        self.pop_button = QPushButton("Pop Candy")
        self.pop_button.clicked.connect(self.pop_candy)
        self.layout.addWidget(self.pop_button)

        self.peek_button = QPushButton("Peek Candy")
        self.peek_button.clicked.connect(self.peek_candy)
        self.layout.addWidget(self.peek_button)

        # Set the layout
        self.setLayout(self.layout)

    def create_candy_label(self):
        """Create a new candy label."""
        candy_label = QLabel("🍬 Candy")
        candy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return candy_label

    def animate_push(self, candy_label):
        """Animate the candy being pushed into the dispenser."""
        # Set initial position of the candy (offscreen, at the top)
        candy_label.setGeometry(QRect(150, 0, 100, 50))
        self.layout.addWidget(candy_label)

        # Create a property animation for the y-position
        animation = QPropertyAnimation(candy_label, b"geometry")
        animation.setDuration(800)
        animation.setStartValue(QRect(150, -50, 100, 50))  # Start above the window
        animation.setEndValue(QRect(150, 200 - 30 * len(self.stack), 100, 50))  # End in the stack
        animation.setEasingCurve(QEasingCurve.Type.OutBounce)  # Simulate spring effect
        animation.start()

        return animation

    def animate_pop(self, candy_label):
        """Animate the candy being popped from the dispenser."""
        # Create a property animation for the y-position
        animation = QPropertyAnimation(candy_label, b"geometry")
        animation.setDuration(800)
        animation.setStartValue(QRect(150, candy_label.y(), 100, 50))
        animation.setEndValue(QRect(150, -50, 100, 50))  # Move upwards off the screen
        animation.setEasingCurve(QEasingCurve.Type.InBack)
        animation.finished.connect(lambda: candy_label.deleteLater())  # Remove widget after animation
        animation.start()

        return animation

    def update_stack_label(self):
        """Update the label to reflect the current stack contents."""
        if self.stack:
            self.stack_label.setText(f"Stack: {len(self.stack)} candies")
        else:
            self.stack_label.setText("Candy Dispenser is Empty")

    def push_candy(self):
        """Add a candy to the dispenser with animation."""
        candy_label = self.create_candy_label()
        self.stack.append(candy_label)
        self.update_stack_label()

        # Animate the push operation
        self.animate_push(candy_label)

    def pop_candy(self):
        """Remove the last candy from the dispenser with animation."""
        if self.stack:
            candy_label = self.stack.pop()
            self.update_stack_label()

            # Animate the pop operation
            self.animate_pop(candy_label)

    def peek_candy(self):
        """Show the top candy without removing it."""
        if self.stack:
            self.stack_label.setText(f"Top candy: 🍬")
        else:
            self.stack_label.setText("Candy Dispenser is Empty")


# Main block to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dispenser = CandyDispenser()
    dispenser.show()
    sys.exit(app.exec())
