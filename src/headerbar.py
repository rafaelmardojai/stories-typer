# headerbar.py
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

from gi.repository import Gio, Gtk

@Gtk.Template(resource_path='/com/rafaelmardojai/StoriesTyper/ui/headerbar.ui')
class HeaderBar(Gtk.HeaderBar):
    __gtype_name__ = 'HeaderBar'

    btn_menu = Gtk.Template.Child()
    menu = Gtk.Template.Child()
    dark_switch = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)

        self.window = window
        self.settings = Gio.Settings.new("com.rafaelmardojai.StoriesTyper")

        self.dark_switch.set_state(self.settings.get_value('dark-theme'))


class FullScreenHeaderBar(Gtk.EventBox):

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)

        self.props.height_request = 1
        self.props.valign = Gtk.Align.START

        self.revealer = Gtk.Revealer()
        self.revealer.props.valign = Gtk.Align.START
        self.revealer.set_reveal_child(False)
        self.add(self.revealer)
        self.revealer.show()

        self.headerbar = HeaderBar(window=window)
        self.headerbar.props.valign = Gtk.Align.START
        self.revealer.add(self.headerbar)
        self.headerbar.show_all()

        self.connect('enter_notify_event', self.show_hb)
        self.connect('leave_notify_event', self.hide_hb)
        self.headerbar.menu.connect('closed', self.hide_hb)

        self.hide()

    def show_hb(self, widget, data=None):
        self.revealer.set_reveal_child(True)

    def hide_hb(self, widget, data=None):
        if self.headerbar.btn_menu.get_active():
            pass
        else:
            self.revealer.set_reveal_child(False)

