# sourceview.py
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

from gi.repository import Gtk, GtkSource

class SourceView(GtkSource.View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_show_line_numbers(True)
        self.set_monospace(True)

        self.buffer = self.get_buffer()
        self.buffer.set_highlight_syntax(True)

        # Set language
        self.lm = GtkSource.LanguageManager()
        language = self.lm.get_language('fountain')
        self.buffer.set_language(language)

        # Set style
        self.ssm = GtkSource.StyleSchemeManager()
        style = self.ssm.get_scheme('storiestyper-light')
        self.buffer.set_style_scheme(style)

        self.show_all()

