# -*- coding: utf-8 -*-
"""
Display the current keyboard layout.

This module displays the current active keyboard layout.
Requires:
    - xkblayout-state
    or
    - setxkbmap and xset (Works for the first two predefined layouts.)

Configuration parameters:
    - cache_timeout: check for keyboard layout change every seconds
    - colors: "comma separated list of color values for each layout"

@author shadowprince, tuxitop
@license Eclipse Public License
"""

from subprocess import check_output
from time import time
import re


class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 1
    colors = '#268BD2, #FCE94F'

    def __init__(self):
        """
        find the best implementation to get the keyboard's layout
        """
        try:
            self._xkblayout()
        except:
            self.command = self._xset
        else:
            self.command = self._xkblayout
        self.colors_lst = self.colors.split(",")
        self.layouts = self._get_layouts()

    def keyboard_layout(self, i3s_output_list, i3s_config):
        response = {
            'cached_until': time() + self.cache_timeout,
            'full_text': ''
        }

        lang = self.command().strip()
        lang_idx = self.layouts.index(lang)
        try:
            lang_color = self.colors_lst[lang_idx].strip()
        except:
            lang_color = None

        response['full_text'] = lang or '??'
        if lang_color:
            response['color'] = lang_color

        return response

    def _get_layouts(self):
        """
        Returns a list of predefined keyboard layouts
        """
        layouts_re = re.compile(r".*layout:\s*((\w+,?)+).*", flags=re.DOTALL)
        out = check_output(["setxkbmap", "-query"]).decode("utf-8")
        layouts = re.match(layouts_re, out).group(1).split(",")
        return layouts

    def _xkblayout(self):
        """
        check using xkblayout-state (preferred method)
        """
        return check_output(
            ["xkblayout-state", "print", "%s"]
        ).decode('utf-8')

    def _xset(self):
        """
        Check using setxkbmap >= 1.3.0 and xset
        This method works only for the first two predefined layouts.
        """
        ledmask_re = re.compile(r".*LED\smask:\s*(\d+).*", flags=re.DOTALL)

        if len(self.layouts) == 1:
            return layouts[0]

        xset_output = check_output(["xset", "-q"]).decode("utf-8")
        led_mask = re.match(ledmask_re, xset_output).group(1)
        if led_mask == "00000000":
            return self.layouts[0]
        elif led_mask == "00001000":
            return self.layouts[1]
        return "Err"


if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_good': '#00FF00',
        'color_degraded': '#FFFF00',
        'color_bad': '#FF0000',
    }
    while True:
        print(x.keyboard_layout([], config))
        sleep(1)
