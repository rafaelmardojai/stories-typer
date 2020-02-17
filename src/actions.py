# actions.py
#
# Copyright 2020 Rafael Mardojai CM
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

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import GLib, Gio, Gtk

from .about import AboutDialog

class Actions(object):

    def __init__(self):
        actions = [
            {
                'name'  : 'open',
                'func'  : self.on_open,
                'accels': ['<Ctl>o']
            },
            {
                'name'  : 'fullscreen',
                'func'  : self.on_fullscreen,
                'accels': ['F11'],
                'state' : True
            },
            {
                'name'  : 'dark',
                'func'  : self.on_dark,
                'state' : True
            },
            {
                'name'  : 'about',
                'func'  : self.on_about

            },
            {
                'name'  : 'quit',
                'func'  : self.on_quit
            }
        ]

        for a in actions:
            if 'state' in a:
                action = Gio.SimpleAction.new_stateful(
                    a['name'], None, GLib.Variant.new_boolean(False))
                action.connect('change-state', a['func'])
            else:
                action = Gio.SimpleAction.new(a['name'], None)
                action.connect('activate', a['func'])

            self.add_action(action)

            if 'accels' in a:
                self.set_accels_for_action('app.' + a['name'], a['accels'])

    def on_open(self, action, param):
        self.window.open_document()

    def on_fullscreen(self, action, param):
        action.set_state(param)
        self.window.set_fullscreen(param)

    def on_dark(self, action, param):
        action.set_state(param)
        self.window.set_dark(param)

    def on_about(self, action, param):
        about_dialog = AboutDialog()
        about_dialog.set_transient_for(self.window)
        about_dialog.set_modal(True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()
 
