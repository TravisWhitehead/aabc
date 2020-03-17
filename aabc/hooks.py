'''
Copyleft (C) 2015 Matlink

Hardly based on GooglePlayDownloader https://framagit.org/tuxicoman/googleplaydownloader
Copyright (C) 2013 Tuxicoman

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
def connected(function):
    """
    Decorator that checks the gpapi status before doing any request
    """
    def check_connection(self, *args, **kwargs):
        if self.gpapi is None or self.gpapi.authSubToken is None:
            ok, err = self.connect()
            if not ok:
                exit(err)
        return function(self, *args, **kwargs)
    return check_connection
