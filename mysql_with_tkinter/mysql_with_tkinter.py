import customtkinter
from tkintermapview import TkinterMapView
from tkinter import StringVar
from tkinter import ttk
import pymysql

customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):

    APP_NAME = "TkinterMapView with CustomTkinter"
    WIDTH = 1500
    HEIGHT = 800

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []
        self.data = []
        self.columns = ["Marker ID", "Latitude", "Longitude", "Number Plate", "Time", "Situation"] #표 첫번째 행 "car num", "time", "situation"

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set Marker",
                                                command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # Data column
        self.data_table = ttk.Treeview(self.frame_left, columns=self.columns, show="headings")
        for col in self.columns:
            self.data_table.heading(col, text=col)
            self.data_table.column(col, width=100)  # Adjust the width of each column as needed
        self.data_table.grid(row=2, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")



        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.button_fetch_data = customtkinter.CTkButton(master=self.frame_left, text="Fetch Data", command=self.fetch_data_from_database)
        self.button_fetch_data.grid(row=3, column=0, padx=(20, 20), pady=(10, 0))
        
        # Set default values
        
        self.map_widget.set_address("Kookmin university")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")
        
        current_position = self.map_widget.get_position()
        self.map_widget.set_marker(current_position[0], current_position[1])

    def fetch_data_from_database(self):
        # Connect to the database
        connection = pymysql.connect(host='localhost', user='root', passwd='1234', db='mydb')

        # Create a cursor object
        cursor = connection.cursor()

        # Execute SQL query to fetch data
        cursor.execute("SELECT * FROM person")

        # Fetch the results
        results = cursor.fetchall()

        # Clear existing data in the table
        self.data_table.delete(*self.data_table.get_children())

        self.clear_marker_event()
        
        # Insert new data into the table
        for row in results:
            marker_id, latitude, longitude, number_plate, time, situation = row
            latitude, longitude = float(latitude), float(longitude)
            marker_id = len(self.marker_list) + 1
            marker = self.map_widget.set_marker(latitude, longitude)
            self.marker_list.append(marker)
            self.data.append((marker_id, latitude, longitude))
            self.data_table.insert("", "end", values=(marker_id, latitude, longitude, number_plate, time, situation))
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
    
    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.map_widget.set_marker(current_position[0], current_position[1])

    def clear_marker_event(self):
        while self.marker_list:
            marker = self.marker_list.pop()
            marker.delete()
        self.data.clear()
        self.update_data_table()


    def update_data_table(self):
        self.data_table.delete(*self.data_table.get_children())
        for item in self.data:
            marker_id, latitude, longitude, number_plate, time, situation = item
            self.data_table.insert("", "end", values=(marker_id, latitude, longitude, number_plate, time, situation))


    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
