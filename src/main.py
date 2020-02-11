# main.py
#
# Copyright 2019 Rafael Mardojai CM
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, Gio

from .window import AppWindow
from .about import AboutDialog

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.rafaelmardojai.StoriesTyper',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # TODO: move actions to a new class "AppActions"
        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.on_open)
        self.add_action(action)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        # Load CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_resource('/com/rafaelmardojai/StoriesTyper/css/style.css')
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = AppWindow(application=self)
        self.win.present()

    def on_open(self, action, param):
        self.win.open_document()

    def on_about(self, action, param):
        about_dialog = AboutDialog()
        about_dialog.set_transient_for(self.win)
        about_dialog.set_modal(True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


def main(version):
    app = Application()
    return app.run(sys.argv)
