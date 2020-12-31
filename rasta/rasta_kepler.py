#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 22:37:01 2020

This class is an extension of keplergl_cli's Visuazlize class. As the PR is
not merged in the original code, therefore, this will reflect the desired
changes from the forked version.

@author: ikespand
"""


import os
import tempfile
import webbrowser
from keplergl_cli.keplergl_cli import Visualize
from keplergl import KeplerGl
from pkg_resources import resource_filename
import json

# %%


class RastaKepler(Visualize):
    """Inheriting from the `Visualize` and adding option to pass the output
    map to save map at custom location alongisde the option to pass
    a custom config file.
    """

    def __init__(
        self,
        data=None,
        names=None,
        read_only=False,
        api_key=None,
        style=None,
        config_file=None,
        output_map=None,
    ):
        if api_key is not None:
            self.MAPBOX_API_KEY = api_key
        else:
            self.MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")
            msg = "Warning: api_key not provided and MAPBOX_API_KEY "
            msg += "environment variable not set.\nMap may not display."
            if self.MAPBOX_API_KEY is None:
                print(msg)
        if config_file is None:
            self.config_file = resource_filename(
                "rasta", "keplergl_config.json"
            )
        else:
            self.config_file = config_file
        print(self.config_file)

        if output_map is not None:
            self.path = output_map + "_vis.html"
        else:
            self.path = os.path.join(tempfile.mkdtemp(), "defaultmap_vis.html")
        config = self.config(style=style)
        self.map = KeplerGl(config=config)

        if data is not None:
            self.add_data(data=data, names=names)
            self.html_path = self.render(read_only=read_only)

    def config(self, style=None):
        """Load kepler.gl config and insert Mapbox API Key"""

        # config_file = resource_filename('keplergl_cli', 'keplergl_config.json')

        # First load config file as string, replace {MAPBOX_API_KEY} with the
        # actual api key, then parse as JSON
        with open(self.config_file) as f:
            text = f.read()

        text = text.replace("{MAPBOX_API_KEY}", self.MAPBOX_API_KEY)
        keplergl_config = json.loads(text)

        # If style_url is not None, replace existing value
        standard_styles = [
            "streets",
            "outdoors",
            "light",
            "dark",
            "satellite",
            "satellite-streets",
        ]
        if style is not None:
            style = style.lower()
            if style in standard_styles:
                # Just change the name of the mapStyle.StyleType key
                keplergl_config["config"]["config"]["mapStyle"][
                    "styleType"
                ] = style
            else:
                # Add a new style with that url
                d = {
                    "accessToken": self.MAPBOX_API_KEY,
                    "custom": True,
                    "id": "custom",
                    "label": "Custom map style",
                    "url": style,
                }
                keplergl_config["config"]["config"]["mapStyle"]["mapStyles"][
                    "custom"
                ] = d
                keplergl_config["config"]["config"]["mapStyle"][
                    "styleType"
                ] = "custom"

        # Remove map state in the hope that it'll auto-center based on data
        # keplergl_config['config']['config'].pop('mapState')
        return keplergl_config["config"]

    def render(self, open_browser=True, read_only=False):
        """Export kepler.gl map to HTML file and open in Chrome"""
        self.map.save_to_html(file_name=self.path, read_only=read_only)
        # Open saved HTML file in new tab in default browser
        if open_browser:
            webbrowser.open_new_tab("file://" + self.path)
        return self.path
