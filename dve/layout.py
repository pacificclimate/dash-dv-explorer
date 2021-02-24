import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import plotly.express as px
import numpy as np


def header(data):
    """
    Layout element for parts common to all tabs.
    Not actually a "header" so should probably be renamed or broken up into
    true header and other parts.
    """
    dd_options = [dict(label=name, value=name) for name in data.keys()]
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H1("Design Value Explorer"),
                    dcc.Dropdown(
                        id="design-value-name",
                        options=dd_options,
                        value=list(data.keys())[0],
                        placeholder="Select a design value to display...",
                        searchable=True,
                        clearable=False,
                    ),
                    html.Br(),
                    html.Div(id="item-display"),
                ],
                style={"margin-left": "20px", "margin-right": "20px"},
            )
        ]
    )


def overlay_options():
    """
    Layout for Overlay Options section.
    This function returns a list of rows.
    """
    
    return [
        # Section title
        dbc.Row(dbc.Col(html.H4("Overlay Options"))),

        # Control titles
        dbc.Row(
            [
                dbc.Col(html.Div(
                    id="ens-output-container",
                    style={
                        "align": "center",
                        "marginRight": "1em",
                    },
                )),
                dbc.Col(html.Div(
                    id="raster-output-container",
                    style={
                        "align": "center",
                        "marginRight": "1em",
                    },
                )),
                dbc.Col(html.Div(
                    id="mask-output-container",
                    style={
                        "align": "center",
                        "marginRight": "1em",
                    },
                )),
                dbc.Col(html.Div(id="station-output-container")),
            ]
        ),

        # Controls
        dbc.Row(
            [
                dbc.Col(
                    daq.ToggleSwitch(
                        id="ens-switch", value=False
                    ),
                ),
                dbc.Col(
                    daq.ToggleSwitch(
                        id="raster-switch", value=True
                    ),
                ),
                dbc.Col(
                    daq.ToggleSwitch(
                        id="toggle-mask",
                        size=50,
                        value=True,
                    ),
                ),
                dbc.Col(
                    daq.ToggleSwitch(
                        id="toggle-station-switch",
                        size=50,
                        value=False,
                    ),
                ),
            ]
        ),
    ]


def colourbar_options(data, colormaps):
    """
    Layout for Colourbar Options section.
    This function returns a list of rows.
    """
    
    (first_dv,) = data[list(data.keys())[0]]["reconstruction"].data_vars
    first_rfield = data[list(data.keys())[0]]["reconstruction"][first_dv]
    dmin = np.nanmin(first_rfield)
    dmax = np.nanmax(first_rfield)
    num_range_slider_steps = 10

    return [
        # Section title
        # TODO: Improve title -- something like Colour Scale Options
        dbc.Row(dbc.Col(html.H4("Colourbar Options"))),
        
        # Control titles
        dbc.Row(
            [
                dbc.Col(html.Div(html.P("Colour Map"))),
                dbc.Col(html.Div(id="log-output-container")),
                dbc.Col(html.Div(id="cbar-slider-output-container")),
                dbc.Col(html.Div(id="range-slider-output-container")),
            ]
        ),
        
        # Controls
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(
                    # TODO: Rename this to colour-map
                    id="colorscale",
                    options=[
                        {"value": x, "label": x} for x in colormaps
                    ],
                    value=None,
                )),
                dbc.Col(
                    daq.ToggleSwitch(
                        # TODO: Rename
                        id="toggle-log", value=True, size=50
                    )
                ),
                dbc.Col(
                    dcc.Slider(
                        # TODO: Rename to colourscale-range
                        id="cbar-slider",
                        min=2,
                        max=30,
                        step=1,
                        value=10,
                    ),
                ),
                dbc.Col(
                    dcc.RangeSlider(
                        # TODO: Rename
                        id="range-slider",
                        min=dmin,
                        max=dmax,
                        step=(dmax - dmin)
                             / num_range_slider_steps,
                        vertical=False,
                        value=[dmin, dmax],
                    ),
                ),

            ]
        ),
    ]


def map_tab(data, colormaps):
    return dbc.Tab(
        label="Map",
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Graph(id="my-graph")], align="center", width="auto"
                    ),
                    dbc.Col(
                        [
                            *overlay_options(),
                            *colourbar_options(data, colormaps)
                        ],
                        align="center",
                        width="auto",
                    ),
                ]
            )
        ],
    )


def table_C2_tab():
    return dbc.Tab(
        label="Table C-2",
        children=[
            html.H4("Reconstruction Values at Table C2 Locations"),
            html.Div(id="table"),
        ],
    )


def main(data, colormaps):

    # TODO: Replace this use of preloaded data with on-demand requests
    #   for the data to be loaded.

    # TODO: Remove? What were these for?
    # default_markers = np.linspace(dmin, dmax, N)

    return dbc.Container(
        id="big-app-container",
        fluid=True,
        children=[
            header(data),
            dbc.Row(
                dbc.Col(
                    dbc.Tabs([map_tab(data, colormaps), table_C2_tab()]),
                )
            ),
        ],
    )
