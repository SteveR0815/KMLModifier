import shutil
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout, QLineEdit, QWidget

from pykml import parser
from geopy.geocoders import Nominatim
from googletrans import Translator

# print("hello world!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KML Modifier")

        # Create a button to select a KML file
        self.button = QPushButton('Choose a KML-File')
        self.button.clicked.connect(self.choose_file)

        # Create an input field to display the path of the selected file
        self.input_field = QLineEdit()
        self.input_field.setReadOnly(True)

        # Create a list to display all countries contained in the placemarks of the KML file
        self.list_widget = QListWidget()

        # Create a button to analyze the KML file
        self.process_button = QPushButton('Analyze (Countries)')
        self.process_button.clicked.connect(self.process_items)
        self.process_button.setEnabled(False)

        # Create a Layout -> add Buttons, Input field and List
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.input_field)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.process_button)

        # Set the Layout as Main Layout of the Window
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Initialize input_file_path
        self.input_file_path = None

    def get_country(self, lat, lon):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(f"{lat}, {lon}")
        if location is not None:
            address = location.raw['address']
            country_name = address.get('country', '')
            # translator = Translator()
            # translated = translator.translate(country_name, src='auto', dest='en')
            return country_name
        else:
            return "Unknown"


    def choose_file(self):
        # Open Dialog for KML selection
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a KML-File", "", "KML-Files (*.kml)",
                                                   options=options)


        # If a file has been selected -> add elements to list and activate Button "Analyze (Countries)"
        if file_name:
            try:
                # Define the output file path
                output_file_path = file_name + ".copy"

                with open(file_name, 'rb') as fsrc, open(output_file_path, 'wb') as fdst:
                    shutil.copyfileobj(fsrc, fdst)

                    # Read the output file copied before in binary mode
                    root = parser.fromstring(open(output_file_path, 'rb').read())

                    # Create a list to store all countries found
                    all_countries = []

                    # Loop through all Placemarks in the file
                    for placemark in root.Document.Placemark:
                        # Get the coordinates for the current Placemark
                        coordinates = placemark.Point.coordinates.text.strip()

                        # Split the coordinates into a list of points
                        points = coordinates.split()

                        # Loop through all points and print their coordinates
                        for point in points:
                            lon, lat = point.split(',')
                            #        print(f"Latitude: {lat}, Longitude: {lon}")
                            country = self.get_country(lat, lon)
                            #       Store each country within loop
                            all_countries.append(country)

                            #                    if country != country_filter:
                            #                        placemark.getparent().remove(placemark)

                    # Before updating the output file print all unique countries
                    unique_countries = set(all_countries)
                    #            print(unique_countries)
                    # Add unique country names to list widget
                    for country in unique_countries:
                        self.list_widget.addItem(country)
                    self.input_file_path = file_name
                    self.input_field.setText(self.input_file_path)
                    self.process_button.setEnabled(True)

            except Exception as e:
                # Display an error message if the KML file cannot be parsed
                self.list_widget.clear()
                self.list_widget.addItem("Error: Failed to read KML file.")
                self.input_field.clear()
                self.process_button.setEnabled(False)
                print(f"Error: {e}")

    def process_items(self):
        # Process Elements
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
            print(item.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

#
# # Set input and output path and check country
# # -> only placemarks of this country should be copied
# country_filter   = 'Deutschland'
# input_file_path  = 'L:\My Drive\_PRV_\_Cloud\_DEV_\Travel locations - General.kml'
# output_file_path = 'L:\My Drive\_PRV_\_Cloud\_DEV_\Travel locations - Deutschland.kml'
#
# with open(input_file_path, 'rb') as fsrc, open(output_file_path, 'wb') as fdst:
#     shutil.copyfileobj(fsrc, fdst)
#
# # Read the output file copied before in binary mode
# root = parser.fromstring(open(output_file_path, 'rb').read())
#
# # Create a list to store all countries found
# all_countries = []
#
# # Loop through all Placemarks in the file
# for placemark in root.Document.Placemark:
#     # Get the coordinates for the current Placemark
#     coordinates = placemark.Point.coordinates.text.strip()
#
#     # Split the coordinates into a list of points
#     points = coordinates.split()
#
#     # Loop through all points and print their coordinates
#     for point in points:
#         lon, lat = point.split(',')
# #        print(f"Latitude: {lat}, Longitude: {lon}")
#         country = get_country(lat, lon)
# #       Store each country within loop
#         all_countries.append(country)
#
#         if country != country_filter:
#             placemark.getparent().remove(placemark)

# # Before updating the output file print all unique countries
# unique_countries = set(all_countries)
# print(unique_countries)

# Update modified output file
# parser.etree.ElementTree(root).write(output_file_path, pretty_print=True)
