#!/usr/bin/env python


#
# Import Gtk and make sure we have the right version
#
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


#
# Define the main window class
#
class main_window:

    #
    # Initialize the window class
    #
    def __init__(self):
        # Load the Glade file
        self.gladefile = "example1.glade" 
        self.builder = Gtk.Builder() 
        self.builder.add_from_file(self.gladefile) 

        # Connect the signals
        self.builder.connect_signals(self)

        # Load the main window and display it on the screen
        self.main_window = self.builder.get_object("main_window")
        self.main_window.show() 

    #
    # They clicked on the window's destroy button
    #
    def on_main_window_destroy(self, object, data=None):
        print("quit with cancel")
        Gtk.main_quit()

    #
    # They clicked on file/quit from the menu
    #
    def on_menu_quit_activate(self, menuitem, data=None):
        print("quit from menu")
        Gtk.main_quit()

#
# If this is run as a stand alone program, create the 
# main window and and it off to GTK for processing. 
# Otherwise, just define the class.
#
if __name__ == "__main__":
    main = main_window() 
    Gtk.main() 
