class ExpiryDialog(QDialog):
    """Simple dialog to show expiring items"""
    
    def __init__(self, parent, logger, expiring_items):
        super().__init__(parent)
        self.logger = logger
        self.expiring_items = expiring_items
        self.setWindowTitle("Expiring Food Alert")
        self.setMinimumWidth(300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        title_label = QLabel("Food Items Expiring Soon!")
        title_label.setStyleSheet("font-weight: bold; color: red;")
        layout.addWidget(title_label)
        
        items_text = ""
        for name, days_left in self.expiring_items:
            if days_left == 0:
                items_text += f"• {name} - EXPIRES TODAY!\n"
            else:
                items_text += f"• {name} - Expires in {days_left} day(s)\n"
                
        items_label = QLabel(items_text)
        layout.addWidget(items_label)

        btn_layout = QHBoxLayout()
        
        suggest_btn = QPushButton("Suggest Recipes")
        suggest_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        suggest_btn.clicked.connect(self.suggest_recipes)
        btn_layout.addWidget(suggest_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def suggest_recipes(self):
        self.logger.suggest_recipes([name for name, _ in self.expiring_items])
        self.accept()

class StartupExpiryDialog(QDialog):
    """Dialog to show expiring items on startup with warning styling"""
    
    def __init__(self, parent, logger, expiring_items):
        super().__init__(parent)
        self.logger = logger
        self.expiring_items = expiring_items
        self.setWindowTitle("⚠️ Food Expiry Alert ⚠️")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout()
        
        # Create a frame with red background for the alert
        alert_frame = QFrame()
        alert_frame.setStyleSheet("background-color: #FFCCCC; border-radius: 5px; padding: 10px;")
        alert_layout = QVBoxLayout(alert_frame)
        
        # Add warning icon and title
        title_layout = QHBoxLayout()
        warning_label = QLabel("⚠️")
        warning_label.setStyleSheet("font-size: 24px;")
        title_layout.addWidget(warning_label)
        
        title_label = QLabel("Food Items Expiring Soon!")
        title_label.setStyleSheet("font-weight: bold; color: #CC0000; font-size: 16px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        warning_label2 = QLabel("⚠️")
        warning_label2.setStyleSheet("font-size: 24px;")
        title_layout.addWidget(warning_label2)
        
        alert_layout.addLayout(title_layout)
        
        # Add horizontal separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #CC0000;")
        alert_layout.addWidget(separator)
        
        # Add expiring items list
        items_text = ""
        for name, days_left in self.expiring_items:
            if days_left == 0:
                items_text += f"• <b>{name}</b> - <span style='color: #CC0000;'>EXPIRES TODAY!</span><br>"
            elif days_left == 1:
                items_text += f"• <b>{name}</b> - <span style='color: #FF6600;'>Expires TOMORROW!</span><br>"
            else:
                items_text += f"• <b>{name}</b> - Expires in {days_left} days<br>"
                
        items_label = QLabel()
        items_label.setText(items_text)
        items_label.setStyleSheet("font-size: 14px;")
        items_label.setTextFormat(Qt.RichText)
        alert_layout.addWidget(items_label)
        
        # Add the alert frame to main layout
        layout.addWidget(alert_frame)
        
        # Add progress bar to show urgency
        urgency_label = QLabel("Food waste risk level:")
        urgency_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(urgency_label)
        
        urgency_bar = QProgressBar()
        urgency_bar.setRange(0, 100)
        
        # Calculate urgency based on expiry dates
        total_items = len(self.expiring_items)
        expiring_today = sum(1 for _, days in self.expiring_items if days == 0)
        expiring_tomorrow = sum(1 for _, days in self.expiring_items if days == 1)
        
        urgency_value = min(100, int((expiring_today * 50 + expiring_tomorrow * 30 + (total_items - expiring_today - expiring_tomorrow) * 10) / total_items))
        urgency_bar.setValue(urgency_value)
        
        # Set color based on urgency
        if urgency_value > 70:
            urgency_bar.setStyleSheet("QProgressBar::chunk { background-color: #CC0000; }")
        elif urgency_value > 40:
            urgency_bar.setStyleSheet("QProgressBar::chunk { background-color: #FF6600; }")
        else:
            urgency_bar.setStyleSheet("QProgressBar::chunk { background-color: #FFCC00; }")
            
        layout.addWidget(urgency_bar)

        # Add buttons
        btn_layout = QHBoxLayout()
        
        suggest_btn = QPushButton("Suggest Recipes")
        suggest_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        suggest_btn.clicked.connect(self.suggest_recipes)
        btn_layout.addWidget(suggest_btn)
        
        close_btn = QPushButton("Dismiss")
        close_btn.clicked.connect(self.reject)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        # Tips for preventing food waste
        tips_frame = QFrame()
        tips_frame.setStyleSheet("background-color: #E8F5E9; border-radius: 5px; padding: 8px;")
        tips_layout = QVBoxLayout(tips_frame)
        
        tips_label = QLabel("💡 <b>Tip:</b> Check your expiring items daily and plan meals accordingly to reduce food waste.")
        tips_label.setWordWrap(True)
        tips_layout.addWidget(tips_label)
        
        layout.addWidget(tips_frame)
        
        self.setLayout(layout)
    
    def suggest_recipes(self):
        self.logger.suggest_recipes([name for name, _ in self.expiring_items])
        self.accept()

class RecipeDialog(QDialog):
    """Dialog to display recipe suggestions"""
    
    def __init__(self, parent, recipe):
        super().__init__(parent)
        self.recipe = recipe
        self.setWindowTitle("Recipe Suggestion")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        name_label = QLabel(self.recipe["name"])
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(name_label)
        
        ingredients_label = QLabel("Ingredients:")
        ingredients_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(ingredients_label)
        
        ingredients_text = "• " + "\n• ".join(self.recipe["ingredients"])
        ingredients_list = QLabel(ingredients_text)
        layout.addWidget(ingredients_list)
        
        instructions_label = QLabel("Instructions:")
        instructions_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(instructions_label)
        
        instructions_text = QLabel(self.recipe["instructions"])
        instructions_text.setWordWrap(True)
        layout.addWidget(instructions_text)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

class RecipeSelectionDialog(QDialog):
    """Dialog to display multiple recipe options"""
    
    def __init__(self, parent, matching_recipes):
        super().__init__(parent)
        self.matching_recipes = matching_recipes
        self.selected_recipe = None
        self.setWindowTitle("Recipe Suggestions")
        self.setMinimumWidth(500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        title_label = QLabel("Suggested Recipes")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title_label)
        
        self.recipe_table = QTableWidget()
        self.recipe_table.setColumnCount(3)
        self.recipe_table.setHorizontalHeaderLabels(["Recipe Name", "Match %", "Matching Ingredients"])
        self.recipe_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.recipe_table.setSelectionMode(QTableWidget.SingleSelection)
        self.recipe_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.recipe_table.setAlternatingRowColors(True)
        
        self.recipe_table.setRowCount(len(self.matching_recipes))
        for row, match_data in enumerate(self.matching_recipes):
            recipe = match_data['recipe']
            self.recipe_table.setItem(row, 0, QTableWidgetItem(recipe['name']))
            self.recipe_table.setItem(row, 1, QTableWidgetItem(f"{int(match_data['match_percentage'])}%"))
            self.recipe_table.setItem(row, 2, QTableWidgetItem(", ".join(match_data['matched_ingredients'])))
        
        self.recipe_table.resizeColumnsToContents()
        layout.addWidget(self.recipe_table)
        
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        view_btn = QPushButton("View Recipe")
        view_btn.setDefault(True)
        view_btn.clicked.connect(self.view_selected_recipe)
        btn_layout.addWidget(view_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def view_selected_recipe(self):
        selected_rows = self.recipe_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            self.selected_recipe = self.matching_recipes[row]['recipe']
            self.accept()
        else:
            QMessageBox.information(self, "Selection Required", "Please select a recipe to view.")

class ScanDialog(QDialog):
    """Dialog to simulate product scanning"""
    
    def __init__(self, parent, logger):
        super().__init__(parent)
        self.logger = logger
        self.setWindowTitle("Scanning Product")
        self.setMinimumWidth(300)
        self.scanning_complete = False
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        scan_label = QLabel("Scanning Product...")
        scan_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(scan_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Initializing scanner...")
        layout.addWidget(self.status_label)
        
        btn_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        self.add_btn = QPushButton("Add to Inventory")
        self.add_btn.setEnabled(False)
        self.add_btn.clicked.connect(self.add_scanned_item)
        btn_layout.addWidget(self.add_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_scan_progress)
        self.timer.start(100)
        
        self.product_data = None
        
    def update_scan_progress(self):
        current_value = self.progress_bar.value()
        
        if current_value < 100:
            new_value = current_value + random.randint(1, 5)
            self.progress_bar.setValue(min(new_value, 100))
            
            if new_value < 30:
                self.status_label.setText("Scanning barcode...")
            elif new_value < 60:
                self.status_label.setText("Retrieving product information...")
            elif new_value < 90:
                self.status_label.setText("Reading nutritional data...")
            else:
                self.status_label.setText("Finalizing product details...")
                
            if new_value >= 100 and not self.scanning_complete:
                self.scanning_complete = True
                self.timer.stop()
                self.generate_product_data()
                self.status_label.setText(f"Scan complete! Found: {self.product_data['name']}")
                self.add_btn.setEnabled(True)
    
    def generate_product_data(self):
        """Generate random product data for the demo"""
        sample_products = [
            {"name": "Organic Milk", "category": "Dairy", "quantity": 1.0},
            {"name": "Chicken Breast", "category": "Meat", "quantity": 0.5},
            {"name": "Spinach", "category": "Vegetables", "quantity": 1.0},
            {"name": "Banana", "category": "Fruits", "quantity": 1.0},
            {"name": "Whole Wheat Bread", "category": "Bakery", "quantity": 1.0},
            {"name": "Canned Beans", "category": "Pantry", "quantity": 1.0}
        ]
        
        self.product_data = random.choice(sample_products)
        
    def add_scanned_item(self):
        """Add the scanned item to the inventory"""
        if self.product_data:
            self.logger.add_food_item(
                self.product_data["name"],
                self.product_data["category"],
                self.product_data["quantity"]
            )
        self.accept()

class ReportDialog(QDialog):
    """Dialog to display food waste reports"""
    
    def __init__(self, parent, report_data, report_type="weekly"):
        super().__init__(parent)
        self.report_data = report_data
        self.report_type = report_type
        self.setWindowTitle(f"{report_type.capitalize()} Food Waste Report")
        self.setMinimumWidth(600)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel(f"{self.report_type.capitalize()} Food Waste Report")
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(title_label)
        
        # Date range
        date_range = QLabel(f"Period: {self.report_data['start_date']} to {self.report_data['end_date']}")
        layout.addWidget(date_range)
        
        # Summary statistics
        stats_frame = QFrame()
        stats_frame.setStyleSheet("background-color: #E8F5E9; border-radius: 5px; padding: 10px;")
        stats_layout = QGridLayout(stats_frame)
        
        stats_layout.addWidget(QLabel("Total Items:"), 0, 0)
        stats_layout.addWidget(QLabel(str(self.report_data['total_items'])), 0, 1)
        
        stats_layout.addWidget(QLabel("Expired Items:"), 1, 0)
        stats_layout.addWidget(QLabel(str(self.report_data['expired_items'])), 1, 1)
        
        stats_layout.addWidget(QLabel("Consumed Items:"), 2, 0)
        stats_layout.addWidget(QLabel(str(self.report_data['consumed_items'])), 2, 1)
        
        waste_percentage = self.report_data['waste_percentage']
        stats_layout.addWidget(QLabel("Waste Percentage:"), 3, 0)
        waste_label = QLabel(f"{waste_percentage:.1f}%")
        
        # Color the waste percentage based on value
        if waste_percentage > 25:
            waste_label.setStyleSheet("color: #CC0000; font-weight: bold;")  # Red
        elif waste_percentage > 10:
            waste_label.setStyleSheet("color: #FF6600; font-weight: bold;")  # Orange
        else:
            waste_label.setStyleSheet("color: #009900; font-weight: bold;")  # Green
            
        stats_layout.addWidget(waste_label, 3, 1)
        
        layout.addWidget(stats_frame)
        
        # Items table
        if self.report_data['items']:
            items_label = QLabel("Food Items in this Period:")
            items_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            layout.addWidget(items_label)
            
            self.items_table = QTableWidget()
            self.items_table.setColumnCount(5)
            self.items_table.setHorizontalHeaderLabels(["Name", "Category", "Status", "Purchase Date", "Expiry Date"])
            self.items_table.setSelectionBehavior(QTableWidget.SelectRows)
            self.items_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.items_table.setAlternatingRowColors(True)
            
            self.items_table.setRowCount(len(self.report_data['items']))
            for row, item in enumerate(self.report_data['items']):
                self.items_table.setItem(row, 0, QTableWidgetItem(item['name']))
                self.items_table.setItem(row, 1, QTableWidgetItem(item['category']))
                
                status_item = QTableWidgetItem(item['status'])
                if item['status'] == "Expired":
                    status_item.setBackground(QColor(255, 200, 200))  # Light red
                elif item['status'] == "Consumed":
                    status_item.setBackground(QColor(200, 255, 200))  # Light green
                elif item['status'] == "Active":
                    status_item.setBackground(QColor(200, 200, 255))  # Light blue
                    
                self.items_table.setItem(row, 2, status_item)
                self.items_table.setItem(row, 3, QTableWidgetItem(item['purchase_date']))
                self.items_table.setItem(row, 4, QTableWidgetItem(item['expiry_date']))
            
            self.items_table.resizeColumnsToContents()
            layout.addWidget(self.items_table)
        
        # Tips section
        tips_frame = QFrame()
        tips_frame.setStyleSheet("background-color: #E1F5FE; border-radius: 5px; padding: 10px;")
        tips_layout = QVBoxLayout(tips_frame)
        
        tips_label = QLabel("💡 Tips to Reduce Food Waste:")
        tips_label.setStyleSheet("font-weight: bold;")
        tips_layout.addWidget(tips_label)
        
        tips_text = QLabel(
            "• Plan meals before shopping and buy only what you need\n"
            "• Store food properly to extend shelf life\n"
            "• Use the 'First In, First Out' method in your fridge\n"
            "• Check your inventory regularly and use expiring items first\n"
            "• Freeze foods before they expire if you can't use them right away"
        )
        tips_text.setWordWrap(True)
        tips_layout.addWidget(tips_text)
        
        layout.addWidget(tips_frame)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


if __name__ == "__main__":
    try:
        app = FoodWasteLogger()
        sys.exit(app.run())
    except Exception as e:
        app = QApplication([])
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Startup Error")
        error_dialog.setText("There was an error starting the application.")
        error_dialog.setDetailedText(f"Error details: {str(e)}")
        error_dialog.setStandardButtons(QMessageBox.Ok)
        error_dialog.exec_()
        sys.exit(1) 