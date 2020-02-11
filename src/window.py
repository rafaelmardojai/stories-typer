# window.py
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

import codecs
import locale
import logging
import os
import urllib
from gettext import gettext as _

from gi.repository import Gtk
from .editor import Editor

LOGGER = logging.getLogger('storiestyper')

@Gtk.Template(resource_path='/com/rafaelmardojai/StoriesTyper/ui/window.ui')
class AppWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'AppWindow'

    headerbar = Gtk.Template.Child()
    mainbox = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.editor = Editor(window=self)
        self.mainbox.pack_start(self.editor, True, True, 0)

    def open_document(self, _widget=None):
        fountain_filter = Gtk.FileFilter.new()
        fountain_filter.add_mime_type('text/plain')
        fountain_filter.add_pattern('*.fou;*.fountain')
        fountain_filter.set_name(_('Fountain Files'))

        plaintext_filter = Gtk.FileFilter.new()
        plaintext_filter.add_mime_type('text/plain')
        plaintext_filter.set_name(_('Plain Text Files'))

        filechooser = Gtk.FileChooserNative()
        filechooser.set_transient_for(self)
        filechooser.set_modal(True)
        filechooser.add_filter(fountain_filter)
        filechooser.add_filter(plaintext_filter)
        response = filechooser.run()

        if response == Gtk.ResponseType.ACCEPT:
            filename = filechooser.get_filename()
            self.load_file(filename)
            filechooser.destroy()

        elif response == Gtk.ResponseType.REJECT:
            filechooser.destroy()

    def load_file(self, filename=None):
        if filename:
            try:
                if os.path.exists(filename):
                    current_file = codecs.open(filename, encoding="utf-8", mode='r')
                    self.editor.load_file(current_file)
                    current_file.close()

            except Exception:
                LOGGER.warning("Error Reading File: %r" % Exception)
            #self.did_change = False
        else:
            LOGGER.warning("No File arg")
        
