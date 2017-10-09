#!/usr/bin/env python


#
# Import Gtk and make sure we have the right version
#
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#
# We need the os & json libraries for the preferences file IO
#
import os, json

#
# Define the main window class
#
class main_window:

    #
    # Initialize the window class
    #
    def __init__(self):
        # Load the Glade file
        self.gladefile = "example4.glade" 
        self.builder = Gtk.Builder() 
        self.builder.add_from_file(self.gladefile) 

        # Initialize the default preferences and load the saved values
        self.pref_file = "example4.json"
        self.prefs = dict(
                message="Hello World!",
                save_size=False,
                save_pos=False,
                show_status=True,
            )
        self.prefs = self.load_preferences(self.pref_file, self.prefs)

        # Connect the signals
        self.builder.connect_signals(self)

        # Load the main window and the children
        self.main_window = self.builder.get_object("main_window")
        self.about_dialog = self.builder.get_object("about_dialog")
        self.menu_status = self.builder.get_object("menu_status")
        self.menu_status.set_active(True)
        self.statusbar = self.builder.get_object("statusbar")
        self.statusbar_context_id = self.statusbar.get_context_id("status")
        self.msg_label = self.builder.get_object("msg_label")

        # Load the preferences dialog and its widgets
        self.pref_dialog = self.builder.get_object("pref_dialog")
        self.pref_msg = self.builder.get_object("pref_msg")
        self.pref_save_size = self.builder.get_object("pref_save_size")

        # Show the status bar?
        if self.prefs["show_status"]: 
            self.statusbar.show()
        else:
            self.statusbar.hide()

        # Remember the size and position?
        if self.prefs["save_size"]:
            w, h = self.prefs["size"]
            self.main_window.set_default_size(w, h)
            x, y = self.prefs["pos"]
            self.main_window.move(x, y)

        # Set the label text
        self.msg_label.set_label(self.prefs["message"])

        # Let the user know we're ready
        self.statusbar.push(self.statusbar_context_id, "Ready")

        # Display the window on the screen
        self.main_window.show() 

    #
    # Load previously saved preferences from a JSON file
    #
    # NOTE: 
    #   The default preferences are passed in as "prefs" 
    #   while the preferences loaded from the file are stored
    #   in "data". The prefs.update(data) statement merges the
    #   values loaded from the file into "prefs". Duplicate values
    #   in "prefs" are overwritten with values from "data" and 
    #   unique values to both are retained.
    #
    def load_preferences(self, pref_file, prefs):
        print("Loading preferences")
        if os.path.exists(pref_file):
            f = open(pref_file, "r")
            data = json.loads(f.read())
            f.close()
            prefs.update(data)
        return prefs

    #
    # Save the prefrences file as JSON data
    #
    def save_preferences(self, pref_file, prefs):
        print("Saving preferences")

        # Remember the size?
        if prefs["save_size"]:
            self.prefs["size"] = self.main_window.get_size()
            prefs["pos"] = self.main_window.get_position()

        data = json.dumps(prefs, indent=4, sort_keys=True)
        f = open(pref_file, "w")
        f.write(data)
        f.close()

    #
    # They clicked on the window's destroy button
    #
    def on_main_window_destroy(self, object, data=None):
        print("quit with cancel")
        Gtk.main_quit()

    #
    # The window is being deleted, save the preferences
    #
    def on_main_window_delete_event(self, object, data=None):
        print("The window is being closed, saving our preferences")
        self.save_preferences(self.pref_file, self.prefs)
        return False

    #
    # They clicked on file/quit from the menu
    #
    # NOTE:
    #   By calling Gtk.main.quit() directly, we bypass
    #   the destroy event, so if we want to save the 
    #   preferences from one place (or ask "Are you sure?")
    #   we need to call on_main_window_delete_event() directly
    #   (or trigger the event ourselves).
    #
    def on_menu_quit_activate(self, menuitem, data=None):
        print("quit from menu")
        if not self.on_main_window_delete_event(menuitem, None):
            Gtk.main_quit()

    #
    # They clicked on help/about from the menu
    #
    def on_menu_about_activate(self, menuitem, data=None):
        print("help about selected")
        self.response = self.about_dialog.run()
        self.about_dialog.hide()

    #
    # They clicked on view/status from the menu
    #
    def on_menu_status_toggled(self, menuitem, data=None):
        if self.menu_status.get_active():
            print("view/status menu now checked, enabling status bar")
            self.statusbar.show()
        else:
            print("view/status menu now unchecked, disabling status bar")
            self.statusbar.hide()

    #
    # They clicked on edit/preferences from the menu
    #
    #   NOTE: The responses returned by Gtk.Dialog.run() are an 
    #   enumeration defined in the Gtk.ResponseType class. You 
    #   can find the list here:
    #
    #   https://lazka.github.io/pgi-docs/Gtk-3.0/enums.html#Gtk.ResponseType
    #
    def on_menu_pref_activate(self, menuitem, data=None):
        print("edit/preferences selected")

        self.pref_msg.set_text(self.prefs['message'])
        self.pref_save_size.set_active(self.prefs['save_size'])

        response = self.pref_dialog.run()
        if response == Gtk.ResponseType.OK:
            self.prefs['message'] = self.pref_msg.get_text()
            self.prefs['save_size'] = self.pref_save_size.get_active()

            print("new message: %s" % self.prefs['message'])
            self.msg_label.set_label(self.prefs['message'])
        self.pref_dialog.hide()

#
# If this is run as a stand alone program, create the 
# main window and and it off to GTK for processing. 
# Otherwise, just define the class.
#
if __name__ == "__main__":
    main = main_window() 
    Gtk.main() 
