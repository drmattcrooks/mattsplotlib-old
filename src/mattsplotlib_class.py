import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator
import numpy as np
import warnings
import matplotlib
import style
import matplotlib.colors as mcolors
import plotly
from pdf2image import convert_from_path, convert_from_bytes
import tempfile
from plotly.subplots import make_subplots



class mattsplotlib():

    def __init__(self, **kwargs):

        self.marker_dict = {'.': 'circle',
                            ',': 'circle',
                            'o': 'circle',
                            'v': 'triangle-down',
                            '^': 'triangle-up',
                            '<': 'triangle-left',
                            '>': 'triangle-right',
                            '1': 'y-down',
                            '2': 'y-up',
                            '3': 'y-left',
                            '4': 'y-right',
                            '8': 'octagon',
                            's': 'square',
                            'p': 'pentagon',
                            'P': 'cross',
                            '*': 'star',
                            'h': 'hexagon',
                            'H': 'hexagon2',
                            '+': 'cross-thin',
                            'x': 'x-thin',
                            'X': 'x',
                            'D': 'diamond',
                            'd': 'diamond-tall',
                            '|': 'line-ns',
                            '_': 'line-ew'}

        self.line_style_dict = {'--': 'dash',
                                '-': None}

        self.base_color_dict = {'b': 'blue',
                                'g': 'green',
                                'r': 'red',
                                'm': 'magenta',
                                'c': 'cyan',
                                'y': 'yellow',
                                'k': 'black',
                                'w': 'white'}

        self.color_iterable = ['steelblue', 'sandybrown', 'forestgreen', 'firebrick']#'[self._rgb_tuple_to_str(self.matplotlibify_the_color(c)) for c in list(mcolors.TABLEAU_COLORS.keys())]

        self.default_color = 'steelblue'

        self.plot_types = []

        self.next_plot_color = 0

        self.annotations = None

        self.default_style_sheet = kwargs.get('style_sheet', '/Users/crookm12/Documents/GitHubPersonal/mattsplotlib/src/mattsplotlib.mplstyle')

        self.spines = {}
        for spine in ['top', 'left', 'bottom', 'right']:
            self.spines[spine] = spine_class(spine)

        if 'figure' in kwargs:
            self.fig = kwargs['figure']

        if 'row' in kwargs:
            row = kwargs.get('row', 1)
            col = kwargs.get('col', 1)

            self.subplot_row_col = {'row': row, 'col': col}
            self.style_use(self.default_style_sheet)

            figsize = kwargs.get('figsize', self.figsize)
            if figsize is None:
                layout = {'autosize': True}
            else:
                layout = {'width': figsize[0] * 500 / 7,
                          'height': figsize[1] * 500 / 7}
            self.fig.update_layout(layout)
            self.subplot_layout = kwargs['subplot_layout']

            self.fig.update_layout({'plot_bgcolor': self.rcParams_layout['plot_bgcolor'],
                                    'paper_bgcolor': self.rcParams_layout['paper_bgcolor']})
            self.fig.update_xaxes(self.rcParams_layout['xaxis'], **self.subplot_row_col)
            self.fig.update_yaxes(self.rcParams_layout['yaxis'], **self.subplot_row_col)
            self.fig.update_xaxes(title=None, **self.subplot_row_col)
            self.fig.update_xaxes(title=None, **self.subplot_row_col)
            self.fig.update_layout(legend={'itemsizing': 'constant'})
            self.fig._set_rcParams(self.rcParams_savefig)

        else:
            self.subplot_row_col = None

        for spine in self.spines:
            self.spines[spine]._attach_spines_to_ax(self.fig, **self.subplot_row_col)


    def _get_default_plot_color(self):
        dc = self.color_iterable[self.next_plot_color]
        self.next_plot_color += 1
        return dc


    def figure(self, *args, **kwargs):

        self.style_use('/Users/crookm12/Documents/GitHubPersonal/mattsplotlib/src/mattsplotlib.mplstyle')

        figsize = kwargs.get('figsize', self.figsize)

        self.fig = figure_handle(data=(),
                                 layout={'width': figsize[0] * 500 / 7,
                                         'height': figsize[1] * 500 / 7})

        self.fig.update_layout({'plot_bgcolor': self.rcParams_layout['plot_bgcolor'],
                                'paper_bgcolor': self.rcParams_layout['paper_bgcolor']})
        self.fig.update_xaxes(self.rcParams_layout['xaxis'], **self.subplot_row_col)
        self.fig.update_yaxes(self.rcParams_layout['yaxis'], **self.subplot_row_col)
        self.fig.update_xaxes(title=None, **self.subplot_row_col)
        self.fig.update_xaxes(title=None, **self.subplot_row_col)
        self.fig.update_layout(legend={'itemsizing': 'constant'})
        self.fig._set_rcParams(self.rcParams_savefig)

    def nxdraw(self, *args, **kwargs):
        self._nxdraw(*args, **kwargs)

    def _nxdraw(self, *args, **kwargs):

        self.plot_types.append('network')

        if len(args) < 2:
            raise ValueError(f"2 required positional arguments: G and pos required. Only {len(args)} provided")

        G = args[0]
        pos = args[1]

        xcoords = []
        ycoords = []
        xmin = 0
        xmax = 0
        ymin = 0
        ymax = 0

        if type(pos[list(pos.keys())[0]]) != np.ndarray:
            raise ValueError(f"coordinate values in pos should be arrays, {type(pos[list(pos.keys())[0]])}s provided ")

        is_3d = (pos[list(pos.keys())[0]].shape[0] == 3)
        if is_3d:
            zcoords = []
            zmin = 0
            zmax = 0

        for edge in G.edges:
            xcoords.append(pos[edge[0]][0])
            ycoords.append(pos[edge[0]][1])
            xcoords.append(pos[edge[1]][0])
            ycoords.append(pos[edge[1]][1])
            xcoords.append(None)
            ycoords.append(None)

            if pos[edge[0]][0] < xmin:
                xmin = pos[edge[0]][0]
            if pos[edge[1]][0] > xmax:
                xmax = pos[edge[1]][0]
            if pos[edge[0]][1] < ymin:
                ymin = pos[edge[0]][1]
            if pos[edge[1]][1] > ymax:
                ymax = pos[edge[1]][1]

            if is_3d:
                zcoords.append(pos[edge[0]][2])
                zcoords.append(pos[edge[1]][2])
                zcoords.append(None)
                if pos[edge[0]][2] < ymin:
                    zmin = pos[edge[0]][2]
                if pos[edge[1]][2] > ymax:
                    zmax = pos[edge[1]][2]


        node_id_dict = {node_name: i for i, node_name in enumerate(G.nodes())}

        xnodes = []
        ynodes = []

        if is_3d:
            znodes = []

        for node in G.nodes():
            xnodes.append(pos[node][0])
            ynodes.append(pos[node][1])
            if is_3d:
                znodes.append(pos[node][2])

        line_color = kwargs.get('edge_color', 'silver')
        linewidth = kwargs.get('edge_width', 1.5)
        node_colours = kwargs.get('node_color', ['steelblue'] * len(G.nodes))
        node_size = kwargs.get('node_size', 10 * is_3d + (15 * (1 - is_3d)))
        edge_alpha = kwargs.get('edge_alpha', 0.5 * is_3d + 1 * (1 - is_3d))

        if is_3d:
            line_color_rgba = self._convert_color_to_rgba_str(line_color, edge_alpha)
        else:
            line_color_rgba = self._convert_color_to_rgba_str(line_color, edge_alpha)

        if is_3d:
            go_scatter = go.Scatter3d
        else:
            go_scatter = go.Scatter

        edge_trace = go_scatter(mode='lines',
                                hoverinfo='text',
                                hovertext=None,
                                showlegend=False)

        edge_trace.update(line={'color': line_color_rgba,
                                'width': linewidth})


        edge_trace.update(x=xcoords, y=ycoords)
        if is_3d:
            edge_trace['z'] = zcoords


        cmap = 'Blues'
        if 'cmap' in kwargs:
            cmap = kwargs['cmap']

            if type(cmap) == matplotlib.colors.ListedColormap:
                color_map = list(cmap.colors)
            else:
                if type(cmap) not in [list, tuple]:
                    raise ValueError(f"cmap should either be a matplotlib.colors.ListedColormap item, a list, or a tuple of colors")
                else:
                    color_map = list(cmap)

            color_map_rgb = []
            for color in color_map:
                if type(color) in [tuple, list]:
                    color = f"rgb{tuple(color)}"
                elif color[:3] != 'rgb':
                    color = f"rgb{self._named_color_to_rgb_tuple(color)}"
                color_map_rgb.append(color)

            node_colours_distinct = list(color_map_rgb)

            if max(node_colours) > len(color_map_rgb):
                color_map_rgb *= int(np.ceil(max(node_colours) / len(cmap)))


            if type(node_colours[0]) == int:
                node_colours = [color_map_rgb[nc] for nc in node_colours]

        self.fig.add_trace(edge_trace)

        if not is_3d:
            node_trace = go_scatter(
                x=xnodes,
                y=ynodes,
                mode='markers',
                hovertext=list(G.nodes()),
                hoverinfo='text',
                marker=dict(
                    color=node_colours,
                    size=node_size,
                    opacity=1),
                showlegend=False)
            self.fig.add_trace(node_trace)

        else:
            for color in node_colours_distinct:
                print(color)
                node_names = []
                xnodes_coloured = []
                ynodes_coloured = []
                znodes_coloured = []
                for i, node in enumerate(G.nodes):
                    if node_colours[i] == color:
                        node_names.append(node)
                        xnodes_coloured.append(xnodes[i])
                        ynodes_coloured.append(ynodes[i])
                        znodes_coloured.append(znodes[i])

                node_trace = go_scatter(
                    x=xnodes_coloured,
                    y=ynodes_coloured,
                    z=znodes_coloured,
                    mode='markers',
                    hovertext=node_names,
                    hoverinfo='text',
                    marker=dict(
                        color=color,
                        size=node_size,
                        opacity=1),
                    showlegend=False)

                self.fig.add_trace(node_trace)

        self.fig.update_layout(plot_bgcolor = 'rgba(0,0,0,0)',
                               paper_bgcolor = 'rgba(0,0,0,0)',
                               clickmode = 'event+select',
                               margin = {'l': 20,
                                         'r': 20,
                                         'b': 20,
                                         't': 50})

        xrange = [xmin - 0.2, xmax + 0.2]
        yrange = [ymin - 0.2, ymax + 0.2]

        self.fig.update_xaxes(showgrid=False,
                              showline=False,
                              zeroline=False,
                              showticklabels=False,
                              range=xrange)
        self.fig.update_yaxes(showgrid=False,
                              showline=False,
                              zeroline=False,
                              showticklabels=False,
                              range=yrange)


        if is_3d:
            zrange = [zmin - 0.2, zmax + 0.2]
            self.fig.update_layout(scene=dict(
                xaxis=dict(
                    showbackground=False,
                    showgrid=False,
                    showline=False,
                    showspikes=False,
                    showticklabels=False,
                    showaxeslabels=False,
                    visible=False),
                yaxis=dict(
                    showbackground=False,
                    showgrid=False,
                    showline=False,
                    showspikes=False,
                    showticklabels=False,
                    showaxeslabels=False,
                    visible=False),
                zaxis=dict(
                    showbackground=False,
                    showgrid=False,
                    showline=False,
                    showspikes=False,
                    showticklabels=False,
                    showaxeslabels=False,
                    visible=False,
                    range=zrange)))

    def barh(self, *args, **kwargs):
        """
        horizontal bar plot.
        Addeds orientation = 'h' to function call of bar. Can also be achieved by directly passing orientation='h' into bar()
        :param args: positional arguments to pass to bar()
        :param kwargs: keyword arguments to pass to bar()
        :return: horizontal bar plot
        """
        kwargs['orientation'] = 'h'
        self.bar(*args, **kwargs)

    def bar(self,
            *args,
            **kwargs):

        kwargs.setdefault('orientation', 'v')

        if len(args) == 0:
            raise TypeError("bar() missing 2 required positional arguments: 'x' and 'height'")
        elif len(args) == 1:
            raise TypeError("bar() missing 1 required positional argument: 'height'")
        elif len(args) == 2:
            if type(args[0]) in [int, float]:
                x = [args[0]]
            else:
                x = list(args[0])
            if type(args[1]) in [int, float]:
                height = [args[1]]
            else:
                height = list(args[1])
            kwargs.setdefault('width', 0.8)

        elif len(args) == 3:
            if type(args[0]) in [int, float]:
                x = [args[0]]
            else:
                x = list(args[0])
            if type(args[1]) in [int, float]:
                height = [args[1]]
            else:
                height = list(args[1])
            if type(args[2]) in [int, float]:
                width = [args[2]]
            else:
                width = list(args[2])
            if type(width) in (list, np.ndarray):
                if len(width) == 1:
                    width = width[0]
                elif len(width) != len(x):
                    raise ValueError("shape mismatch: objects cannot be broadcast to a single shape")
            if 'width' in kwargs:
                raise TypeError("bar() got multiple values for argument 'width'")
            else:
                kwargs['width'] = width

        kwargs.setdefault('color', self._get_default_plot_color())
        kwargs.setdefault('alpha', 1)
        kwargs.setdefault('edgecolor', None)
        kwargs.setdefault('linewidth', 0)
        kwargs.setdefault('tick_label', None)
        kwargs.setdefault('log', False)
        kwargs.setdefault('hovertext', None)
        kwargs.setdefault('hoverinfo', 'text')
        if kwargs.get('align', 'center') == 'center':
            kwargs['width'] = abs(kwargs['width'])
            kwargs.setdefault('offset', - 0.5 * kwargs['width'])
        elif kwargs.get('align', 'center') == 'edge':
            if kwargs['width'] < 0:
                kwargs.setdefault('offset', kwargs['width'])
                kwargs['width'] = abs(kwargs['width'])
            else:
                kwargs.setdefault('offset', 0)
        else:
            if kwargs.get('align', 'center') == 'plotly':
                kwargs['offset'] = None
                kwargs['width'] = None

        self._bar(x=x, y=height, **kwargs)

    def _bar(self, x, y, **kwargs):
        """
        Create a bar chart using matplotlib syntax

        Other Parameters
----------------
color : scalar or array-like, optional
    The colors of the bar faces.

edgecolor : scalar or array-like, optional
    The colors of the bar edges.

linewidth : scalar or array-like, optional
    Width of the bar edge(s). If 0, don't draw edges.

tick_label : string or array-like, optional
    The tick labels of the bars.
    Default: None (Use default numeric labels.)

xerr, yerr : THIS FEATURE IS NOT AVAILABLE YET
    scalar or array-like of shape(N,) or shape(2,N), optional
    If not *None*, add horizontal / vertical errorbars to the bar tips.
    The values are +/- sizes relative to the data:

    - scalar: symmetric +/- values for all bars
    - shape(N,): symmetric +/- values for each bar
    - shape(2,N): Separate - and + values for each bar. First row
        contains the lower errors, the second row contains the
        upper errors.
    - *None*: No errorbar. (Default)

    See :doc:`/gallery/statistics/errorbar_features`
    for an example on the usage of ``xerr`` and ``yerr``.

ecolor : THIS FEATURE IS NOT AVAILABLE YET
    scalar or array-like, optional, default: 'black'
    The line color of the errorbars.

capsize : THIS FEATURE IS NOT AVAILABLE YET
    scalar, optional
   The length of the error bar caps in points.
   Default: None, which will take the value from
   :rc:`errorbar.capsize`.

error_kw : THIS FEATURE IS NOT AVAILABLE YET
    dict, optional
    Dictionary of kwargs to be passed to the `~.Axes.errorbar`
    method. Values of *ecolor* or *capsize* defined here take
    precedence over the independent kwargs.

log : bool, optional, default: False
    If *True*, set the y-axis to be log scale.

width : float, optional
    The width of the bars.

bar_mode : stacked
        """

        self.plot_types.append('bar')

        if kwargs['log']:
            yaxis_type = 'log'
        else:
            yaxis_type = 'linear'

        if 'xerr' in kwargs:
            warnings.warn('xerr specified - this feature is not support yet and the argument will be ignored')
        if 'yerr' in kwargs:
            warnings.warn('yerr specified - this feature is not support yet and the argument will be ignored')

        # perturb x so that multiple bars at the same x location don't get offset
        eps = 1e-3
        eps_rand = np.random.uniform(1 - 2 * eps, 1 - eps)

        bar_trace = self._get_bar_defaults()
        bar_trace.update(x=x,
                         y=y,
                         type='bar',
                         hoverinfo=kwargs['hoverinfo'],
                         hovertext=kwargs['hovertext'],
                         marker={'color': kwargs['color'],
                                 'opacity': kwargs['alpha'],
                                 'line': {'color': kwargs['edgecolor'],
                                          'width': kwargs['linewidth']}},
                         width=kwargs['width'],
                         offset=kwargs['offset'],
                         orientation=kwargs['orientation'])

        if 'fig' not in dir(self):
            self.figure()

        if 'name' in kwargs:
            bar_trace['name'] = kwargs['name']
            self.fig.update_layout(showlegend=True)
        else:
            if not self.fig.layout.showlegend:
                self.fig.update_layout(showlegend=False)

        if kwargs['tick_label'] is not None:
            self.fig.layout.xaxis['tickvals'] = x
            self.fig.layout.xaxis['ticktext'] = kwargs['tick_label']

        self.fig.add_trace(bar_trace, **self.subplot_row_col)

    def scatter(self,
                *args,
                bubble=None,
                **kwargs):

        if len(args) == 0:
            if ('x' not in kwargs) & ('y' not in kwargs):
                raise TypeError("scatter() missing 2 required positional arguments: 'x' and 'y'")
            else:
                x = kwargs.get('x')
                y = kwargs.get('y')
                s = kwargs.get('s')
                c = kwargs.get('c', 'steelblue')
        elif len(args) == 1:
            if 'y' not in kwargs:
                raise TypeError("scatter() missing 1 required positional argument: 'y'")
            else:
                x = args[0]
                y = kwargs.get('y')
                s = kwargs.get('s')
                c = kwargs.get('c', 'steelblue')
        elif len(args) == 2:
            x = args[0]
            y = args[1]
            s = kwargs.get('s', )
            c = kwargs.get('c', 'steelblue')
        elif len(args) == 3:
            x = args[0]
            y = args[1]
            s = args[2]
            c = kwargs.get('c', 'steelblue')
        elif len(args) == 4:
            x = args[0]
            y = args[1]
            s = args[2]
            c = args[3]

        kwargs.pop('x', None)
        kwargs.pop('y', None)
        kwargs.pop('s', None)
        kwargs.pop('c', None)

        if bubble:
            linewidths=1
            edgecolor='white'
            alpha = 0.5
        else:
            linewidths = 0
            edgecolor = None
            alpha = 1

        if 'hovertext' in kwargs:
            kwargs['hovertext'] = self._parse_hovertext(kwargs['hovertext'])

        self._scatter(x, y, s, c,
                      linewidths=linewidths,
                      edgecolor=edgecolor,
                      alpha=alpha,
                      **kwargs)

    def bubble(self,
               *args,
               **kwargs):

        self.scatter(*args, bubble=True, **kwargs)

    def _scatter(self,
                x,
                y,
                s,
                c,
                marker=None,
                cmap=None,
                norm=None,
                vmin=None,
                vmax=None,
                alpha=None,
                linewidths=0,
                edgecolors='white',
                hoverinfo='text',
                hovertext=None,
                line=None,
                **kwargs):
        """
A scatter plot of *y* vs *x* with varying marker size and/or color.

Parameters
----------
x, y : array_like, shape (n, )
    The data positions.

s : scalar or array_like, shape (n, ), optional
    The marker size in points**2.
    Default is ``rcParams['lines.markersize'] ** 2``.

c : color, sequence, or sequence of color, optional
    The marker color. Possible values:

    - A single color format string.
    - A sequence of color specifications of length n.
    - A sequence of n numbers to be mapped to colors using *cmap* and
      *norm*.
    - A 2-D array in which the rows are RGB or RGBA.

    Note that *c* should not be a single numeric RGB or RGBA sequence
    because that is indistinguishable from an array of values to be
    colormapped. If you want to specify the same RGB or RGBA value for
    all points, use a 2-D array with a single row.  Otherwise, value-
    matching will have precedence in case of a size matching with *x*
    and *y*.

    Defaults to ``None``. In that case the marker color is determined
    by the value of ``color``, ``facecolor`` or ``facecolors``. In case
    those are not specified or ``None``, the marker color is determined
    by the next color of the ``Axes``' current "shape and fill" color
    cycle. This cycle defaults to :rc:`axes.prop_cycle`.

marker : `~matplotlib.markers.MarkerStyle`, optional
    The marker style. *marker* can be either an instance of the class
    or the text shorthand for a particular marker.
    Defaults to ``None``, in which case it takes the value of
    :rc:`scatter.marker` = 'o'.
    See `~matplotlib.markers` for more information about marker styles.

cmap : `~matplotlib.colors.Colormap`, optional, default: None
    A `.Colormap` instance or registered colormap name. *cmap* is only
    used if *c* is an array of floats. If ``None``, defaults to rc
    ``image.cmap``.

norm : `~matplotlib.colors.Normalize`, optional, default: None
    A `.Normalize` instance is used to scale luminance data to 0, 1.
    *norm* is only used if *c* is an array of floats. If *None*, use
    the default `.colors.Normalize`.

vmin, vmax : scalar, optional, default: None
    *vmin* and *vmax* are used in conjunction with *norm* to normalize
    luminance data. If None, the respective min and max of the color
    array is used. *vmin* and *vmax* are ignored if you pass a *norm*
    instance.

alpha : scalar, optional, default: None
    The alpha blending value, between 0 (transparent) and 1 (opaque).

linewidths : scalar or array_like, optional, default: None
    The linewidth of the marker edges. Note: The default *edgecolors*
    is 'face'. You may want to change this as well.
    If *None*, defaults to rcParams ``lines.linewidth``.

edgecolors : color or sequence of color, optional, default: 'face'
    The edge color of the marker. Possible values:

    - 'face': The edge color will always be the same as the face color.
    - 'none': No patch boundary will be drawn.
    - A matplotib color.

    For non-filled markers, the *edgecolors* kwarg is ignored and
    forced to 'face' internally."""

        self.plot_types.append('scatter')

        if marker is not None:
            if marker not in self.marker_dict:
                if marker not in SymbolValidator().values:
                    warnings.warn(f"marker style {marker} not available, defaulting to 'o'")
                    marker = self.marker_dict['o']
            else:
                marker = self.marker_dict[marker]
        else:
            marker = self.marker_dict['o']

        if marker == 'markers':
            if s is None:
                s = 10
            if c is None:
                c = 'steelblue',
            if cmap is None:
                cmap = 'Blues'
            if alpha is None:
                if s is not None:
                    if max(s) <= 10:
                        alpha = 1
                    else:
                        alpha = 0.5
                else:
                    alpha = 1

        if linewidths is None:
            if max(s) <= 10:
                linewidths = 0
            else:
                linewidths = 1

        if norm is not None:
            warnings.warn('no functionality for norm: apply manually to the data first')
        if vmin is not None:
            warnings.warn('no functionality for vmin: apply manually to the data first')
        if vmax is not None:
            warnings.warn('no functionality for vmax: apply manually to the data first')


        if 'figsize' not in dir(self):
            self.figsize = (10, 7)

        x = list(x)
        y = list(y)

        if (type(s) == int) or (type(s) == float):
            s = [s] * len(x)

        scatter_data = {'x': x,
                    'y': y,
                    'mode': 'markers',
                    'marker': {'color': c,
                               'size': s,
                               'opacity': alpha,
                               'line': {'color': edgecolors,
                                        'width': linewidths},
                               'colorscale': cmap},
                    'hoverinfo': hoverinfo,
                    'hovertext': hovertext,
                    'marker_symbol': marker}

        if 'line' in kwargs:
            scatter_data['line'] = kwargs['line']

        if 'fig' not in dir(self):
            self.figure()

        if 'name' in kwargs:
            scatter_data['name'] = kwargs['name']
            self.fig.update_layout(showlegend=True)
        else:
            if not self.fig.layout.showlegend:
                self.fig.update_layout(showlegend=False)

        data = go.Scatter(scatter_data)

        self.fig.add_trace(data, **self.subplot_row_col)

    def _interpret_fmt(self, fmt):

        fmt_colour = []
        fmt_line = []
        fmt_marker = []

        for colour in self.base_color_dict:
            if colour in fmt:
                fmt_colour.append(colour)

        for line in ['--', '-.', ':', '-']:
            if line in fmt:
                fmt_line.append(line)
                fmt = fmt.replace(line, '')

        for marker in self.marker_dict:
            if marker in fmt:
                fmt_marker.append(marker)

        if len(colour) > 1:
            raise ValueError(f"Illegal format string {fmt}; two color symbols")
        if len(line) > 1:
            raise ValueError(f"Illegal format string {fmt}; two line style symbols")
        if len(marker) > 1:
            raise ValueError(f"Illegal format string {fmt}; two marker symbols")

        plot_style_dict = {'line': dict(),
                           'marker': {'line': dict()},
                           'marker_symbol': None,
                           'mode': 'lines'}

        if len(fmt_colour) == 1:
            plot_style_dict['line']['color'] = self.base_color_dict[fmt_colour[0]]
            plot_style_dict['marker']['color'] = self.base_color_dict[fmt_colour[0]]
            plot_style_dict['marker']['line']['color'] = self.base_color_dict[fmt_colour[0]]
        if len(fmt_marker) == 1:
            plot_style_dict['marker_symbol'] = self.marker_dict[fmt_marker[0]]
            plot_style_dict['marker']['size'] = self.markers['size']
            if fmt_line == []:
                plot_style_dict['mode'] = 'markers'
            else:
                plot_style_dict['mode'] = 'lines+markers'
        if len(fmt_line) == 1:
            plot_style_dict['line']['dash'] = self.line_style_dict[fmt_line[0]]

        return plot_style_dict



    def _plot(self,
              *args,
              plot_style_dict={},
              **kwargs):
            """
    A scatter plot of *y* vs *x* with varying marker size and/or color.

    Parameters
    ----------
    x, y : array_like, shape (n, )
        The data positions.

    marker : `~matplotlib.markers.MarkerStyle`, optional
        The marker style. *marker* can be either an instance of the class
        or the text shorthand for a particular marker.
        Defaults to ``None``, in which case it takes the value of
        :rc:`scatter.marker` = 'o'.
        See `~matplotlib.markers` for more information about marker styles.

    cmap : `~matplotlib.colors.Colormap`, optional, default: None
        A `.Colormap` instance or registered colormap name. *cmap* is only
        used if *c* is an array of floats. If ``None``, defaults to rc
        ``image.cmap``.

    norm : `~matplotlib.colors.Normalize`, optional, default: None
        A `.Normalize` instance is used to scale luminance data to 0, 1.
        *norm* is only used if *c* is an array of floats. If *None*, use
        the default `.colors.Normalize`.

    vmin, vmax : scalar, optional, default: None
        *vmin* and *vmax* are used in conjunction with *norm* to normalize
        luminance data. If None, the respective min and max of the color
        array is used. *vmin* and *vmax* are ignored if you pass a *norm*
        instance.

    alpha : scalar, optional, default: None
        The alpha blending value, between 0 (transparent) and 1 (opaque).

    linewidths : scalar or array_like, optional, default: None
        The linewidth of the marker edges. Note: The default *edgecolors*
        is 'face'. You may want to change this as well.
        If *None*, defaults to rcParams ``lines.linewidth``.

    edgecolors : color or sequence of color, optional, default: 'face'
        The edge color of the marker. Possible values:

        - 'face': The edge color will always be the same as the face color.
        - 'none': No patch boundary will be drawn.
        - A matplotib color.

        For non-filled markers, the *edgecolors* kwarg is ignored and
        forced to 'face' internally."""

            self.plot_types.append('plot')

            x = kwargs.get('x')
            y = kwargs.get('y')

            plot_trace = self._get_plot_defaults()
            plot_trace.update(x=x,
                              y=y,
                              hoverinfo=kwargs['hoverinfo'],
                              hovertext=kwargs['hovertext'],
                              **plot_style_dict)

            if 'fig' not in dir(self):
                self.figure()

            if 'name' in kwargs:
                plot_trace['name'] = kwargs['name']
                self.fig.update_layout(showlegend=True)
            else:
                if not self.fig.layout.showlegend:
                    self.fig.update_layout(showlegend=False)

            self.fig.add_trace(plot_trace, **self.subplot_row_col)

    def _get_plot_styles(self, fmt, **kwargs):

        if fmt is None:
            fmt = ''
        plot_style_dict = self._interpret_fmt(fmt)

        if 'color' in kwargs:
            color = self._convert_color_to_rgba_str(kwargs.get('color'), kwargs.get('alpha'))
            plot_style_dict['line']['color'] = color
            plot_style_dict['marker']['color'] = color
            plot_style_dict['marker']['line']['color'] = color
        else:
            if 'color' not in plot_style_dict['line']:

                default_color = self._get_default_plot_color()
                default_color = self._convert_color_to_rgba_str(default_color, kwargs.get('alpha', 1))

                plot_style_dict['line']['color'] = default_color
                plot_style_dict['marker']['color'] = default_color
                plot_style_dict['marker']['line']['color'] = default_color

        plot_style_dict['line']['width'] = kwargs.get('linewidth', self.lines['width'])
        plot_style_dict['marker']['line']['width'] = kwargs.get('linewidth', 1)

        if 'marker' in kwargs:
            plot_style_dict['marker_symbol'] = self.marker_dict[kwargs['marker']]
            if plot_style_dict['mode'] == 'lines':
                plot_style_dict['mode'] = 'lines+markers'
        if 'markersize' in kwargs:
            plot_style_dict['marker']['size'] = kwargs['markersize']
        if 'markeredgewidth' in kwargs:
            plot_style_dict['marker']['line']['width'] = kwargs['markeredgewidth']
        if 'markeredgecolor' in kwargs:
            plot_style_dict['marker']['line']['color'] = kwargs['markeredgecolor']
        if 'markerfacecolor' in kwargs:
            plot_style_dict['marker']['color'] = kwargs['markerfacecolor']

        return plot_style_dict

    def plot(self,
             *args,
             **kwargs):

        kwargs.setdefault('hovertext', None)
        kwargs['hovertext'] = self._parse_hovertext(kwargs['hovertext'])
        kwargs.setdefault('linestyle', self.lines['dash'])
        kwargs.setdefault('hoverinfo', 'text')
        # kwargs.setdefault('color', None)
        # if kwargs['color'] is None:
        #     kwargs['color'] = self._get_default_plot_color()
        #     kwargs['color'] = self._convert_color_to_rgba_str(kwargs.get('color'), kwargs.get('alpha'))
        #
        # else:
        #     kwargs['color'] = self._convert_color_to_rgba_str(kwargs.get('color'), kwargs.get('alpha'))

        # kwargs.setdefault('linewidth', self.lines['width'])
        #
        # mode = 'lines'
        # dash = kwargs.get('linestyle', self.lines['dash'])
        # if dash == '-':
        #     dash = None
        # elif dash == '.':
        #     dash = 'dot'
        #     mode = 'markers'
        # elif dash == '--':
        #     dash = 'dash'
        # elif dash == '-.':
        #     dash = 'dashdot'
        # elif dash == '.-':
        #     dash = None
        #     mode = 'markers+lines'
        # kwargs['dash'] = dash
        # kwargs['mode'] = mode

        if len(args) == 0:
            if ('x' not in kwargs) | (type(kwargs.get('x')) != str):
                raise ValueError(f"If specifying x as a keyword argument it should be a string column in a dataframe")
            if ('y' not in kwargs) | (type(kwargs.get('y')) != str):
                raise ValueError(f"If specifying y as a keyword argument it should be a string column in a dataframe")

            else:

                if 'df' not in kwargs:
                    raise ValueError("Keyword argument df not specified")

                df = kwargs['df']

                hovertext_col = kwargs.get('hovertext')

                if 'color' in kwargs:

                    if kwargs['color'] not in list(df):
                        raise ValueError(f"Column {kwargs['color']} specified for the colour is not in dataframe")
                    else:
                        color_col = kwargs['color']
                        list_of_colors = list(df[color_col].drop_duplicates())
                        for iter, cat in enumerate(list_of_colors):
                            df = kwargs['df']
                            x = df.loc[df[color_col] == cat, kwargs['x']].values
                            y = df.loc[df[color_col] == cat, kwargs['y']].values
                            _kwargs = dict(kwargs)
                            _kwargs['x'] = x
                            _kwargs['y'] = y
                            _kwargs['color'] = self._get_default_plot_color()
                            _kwargs['name'] = cat

                            if hovertext_col is not None:
                                _kwargs['hovertext'] = list(df.loc[df[color_col] == cat, hovertext_col])

                            self._plot(**_kwargs)
                else:
                    df = kwargs['df']
                    _kwargs = dict(kwargs)
                    _kwargs['x'] = df[kwargs['x']]
                    _kwargs['y'] = df[kwargs['y']]
                    if 'color' in kwargs:
                        try:
                            _kwargs['color'] = self.matplotlibify_the_color(kwargs.get('color'))
                        except:
                            raise ValueError(f"Unrecognised color {kwargs.get('color')}")

                    plot_style_dict = self._get_plot_styles(None, **_kwargs)
                    self._plot(plot_style_dict=plot_style_dict, **_kwargs)
        elif len(args) == 1:
            if type(args[0]) == str:
                raise ValueError(f"""Incorrect type for y coordinates. Must be one of the following:
                list, 
                range, 
                array, 
                tuple""")
            kwargs['y'] = list(args[0])
            kwargs['x'] = list(range(len(kwargs['y'])))

            plot_style_dict = self._get_plot_styles(None, **kwargs)
            self._plot(plot_style_dict=plot_style_dict, **kwargs)

        elif (len(args) == 2) & (type(args[1]) != str):
            kwargs['x'] = list(args[0])
            kwargs['y'] = list(args[1])
            plot_style_dict = self._get_plot_styles(None, **kwargs)
            self._plot(plot_style_dict=plot_style_dict, **kwargs)

        elif len(args) <= 3:
            if type(args[1]) == str:
                args = (range(len(args[0])), args[0], args[1])

            kwargs['x'] = list(args[0])
            kwargs['y'] = list(args[1])

            try:
                color = self.matplotlibify_the_color(args[2])
                kwargs['color'] = kwargs.get('color', color)
            except:
                try:
                    plot_style_dict = self._get_plot_styles(args[2], **kwargs)
                    # if len(args[2]) == 1:
                    #     if args[2] in self.marker_dict.keys():
                    #         kwargs['linestyle'] = kwargs.get('linestyle', args[2])
                    #         if args[2] == '.':
                    #             kwargs['mode'] = 'markers'
                    #     elif args[2] in self.base_color_dict.keys():
                    #         kwargs['color'] = self.matplotlibify_the_color(kwargs.get('color', args[2]))
                    #         kwargs['color'] = self._convert_color_to_rgba_str(kwargs.get('color'), kwargs.get('alpha'))
                    #
                    # for marker in ['-', '--'] + list(self.marker_dict.keys()):
                    #     for base_color in [''] + list(self.base_color_dict.keys()):
                    #         if args[2] == marker + base_color:
                    #             kwargs['linestyle'] = kwargs.get('linestyle', marker)
                    #             kwargs['color'] = self.matplotlibify_the_color(kwargs.get('color', base_color))
                    #             kwargs['color'] = self._convert_color_to_rgba_str(kwargs.get('color'), kwargs.get('alpha'))
                    #             if marker in list(self.marker_dict.keys()):
                    #                 kwargs['mode'] = 'markers'
                    #                 kwargs['marker'] = {'color': kwargs['color'],
                    #                                     'line': {'width': kwargs['linewidth'],
                    #                                              'color': kwargs['color']},
                    #                                     'size': kwargs.get('markersize', 5)}
                    #             break
                    #         elif args[2] == base_color + marker:
                    #             kwargs['linestyle'] = kwargs.get('linestyle', marker)
                    #             kwargs['color'] = self.matplotlibify_the_color(kwargs.get('color', base_color))
                    #             kwargs['color'] = self._convert_color_to_rgba_str(kwargs.get('color'), kwargs.get('alpha'))
                    #             if marker in list(self.marker_dict.keys()):
                    #                 kwargs['mode'] = 'markers'
                    #                 kwargs['marker'] = {'color': kwargs['color'],
                    #                                     'line': {'width': kwargs['linewidth'],
                    #                                              'color': kwargs['color']},
                    #                                     'size': kwargs.get('markersize', 5)}
                    #
                    #             break
                except:
                    string = args[2]
                    # for marker in self.marker_dict.keys():
                    #     print(marker)
                    #     string = string.replace(marker, '')
                    raise ValueError(f"Unrecognized character {string} in format string")

            self._plot(plot_style_dict=plot_style_dict, **kwargs)

        elif len(args) > 3:
            raise ValueError(f"Mattsplotlib does not support {len(args)} positional arguments. Try using keyword arguments instead")




    def text(self, *args, **kwargs):
        if len(args) == 0:
            if ('x' not in kwargs) & ('y' not in kwargs) & ('s' not in kwargs):
                raise TypeError("text() missing 3 required positional arguments: 'x', 'y', and 's'")
            elif ('x' in kwargs) & ('y' not in kwargs) & ('s' not in kwargs):
                raise TypeError("text() missing 2 required positional arguments: 'y' and 's'")
            elif ('x' not in kwargs) & ('y' in kwargs) & ('s' not in kwargs):
                raise TypeError("text() missing 2 required positional arguments: 'x' and 's'")
            elif ('x' not in kwargs) & ('y' not in kwargs) & ('s' in kwargs):
                raise TypeError("text() missing 2 required positional arguments: 'x' and 'y'")
            elif ('x' not in kwargs) & ('y' in kwargs) & ('s' in kwargs):
                raise TypeError("text() missing 1 required positional arguments: 'x'")
            elif ('x' in kwargs) & ('y' not in kwargs) & ('s' in kwargs):
                raise TypeError("text() missing 1 required positional arguments: 'y'")
            elif ('x' in kwargs) & ('y' in kwargs) & ('s' not in kwargs):
                raise TypeError("text() missing 1 required positional arguments: 's'")
            else:
                x = kwargs.get('x')
                y = kwargs.get('y')
                s = kwargs.get('s')
        elif len(args) == 1:
            x = args[0]
            if 'x' in kwargs:
                raise TypeError("text() got multiple values for argument 'x'")
            elif ('y' not in kwargs) & ('s' not in kwargs):
                raise TypeError("text() missing 2 required positional arguments: 'y' and 's'")
            elif ('y' in kwargs) & ('s' not in kwargs):
                raise TypeError("text() missing 1 required positional arguments: 's'")
            elif ('y' not in kwargs) & ('s' in kwargs):
                raise TypeError("text() missing 1 required positional arguments: 'y'")
            else:
                y = kwargs['y']
                s = kwargs['s']
        elif len(args) == 2:
            x = args[0]
            y = args[1]
            if 'x' in kwargs:
                raise TypeError("text() got multiple values for argument 'x'")
            if 'y' in kwargs:
                raise TypeError("text() got multiple values for argument 'y'")
            if ('s' not in kwargs):
                raise TypeError("text() missing 1 required positional arguments: 's'")
            else:
                s = kwargs['s']
        elif len(args) == 3:
            x = args[0]
            y = args[1]
            s = args[2]
            if 'x' in kwargs:
                raise TypeError("text() got multiple values for argument 'x'")
            if 'y' in kwargs:
                raise TypeError("text() got multiple values for argument 'y'")
            if 's' in kwargs:
                raise TypeError("text() got multiple values for argument 's'")
        else:
            raise TypeError("Too many positional arguments given")

        self._text(x, y, s, **kwargs)

    def fill(self, *args, **kwargs):
        if len(args) <= 3:
            if 'color' in kwargs:
               if 'c' in kwargs:
                   warnings.warn("Saw kwargs ['c', 'color'] which are all aliases for 'color'.  Kept value from 'color')")
               color = kwargs['color']
               kwargs.pop('color')
            elif 'c' in kwargs:
                color = kwargs['c']
            elif len(args) == 3:
                color = args[2]
            else:
                color = self._get_default_plot_color()

            if len(args) == 0:
                None
            if len(args) == 1:
                y = list(args[0])
                x = list(range(len(y)))
            elif len(args) == 2:
                x = args[0]
                y = args[1]
            elif len(args) == 3:
                x = args[0]
                y = args[1]

            self._fill(x, y, color, **kwargs)


        else:
            while len(args) > 0:
                fill_arg, args = self._split_fill_args(*args)
                self._fill(*fill_arg, **kwargs)


    def _get_arg_type(self, arg):

        if (type(arg) == list) | (type(arg) == np.ndarray):
            return 'list'
        elif (type(arg) == str):
            return 'str_'
        else:
            raise ValueError(f"unknown argument {arg}")

    def _get_fill_type(self, *args):

        fill_type = ''
        counter = 0
        for arg in args:
            fill_type += self._get_arg_type(arg)
            counter += 1
            if counter == 3:
                break
            if counter == len(args):
                break
            fill_type += '+'

        return fill_type

    def _split_fill_args(self, *args):

        # type 1: y coords filled to x axis - single list
        # type 2: x and y give, default color - list+list
        # type 3: x, y, and color given - list+list+str
        # type 4: y coords filled to x axis with color given - list+color

        # list+list+list => list+list: Type 2
        # list+list+string => list+list+string: Type 3
        # list+string/+* => list+string: Type 4

        fill_type = self._get_fill_type(*args)
        if fill_type == 'list+list+list':
            return (args[0], args[1]), args[2:]
        elif fill_type == 'list+list+str_':
            if len(args) == 3:
                return (args[0], args[1], args[2]), ()
            else:
                return (args[0], args[1], args[2]), args[3:]
        elif len(fill_type) == 4:
            if fill_type == 'list':
                return (args[0]), ()
            if fill_type == 'str_':
                raise ValueError(f"Cannot perform fill on args {args}")
        elif len(fill_type) == 9:
            if fill_type == 'list+str_':
                return (args[0], args[1]), ()
            elif fill_type == 'list+list':
                return (args[0], args[1]), ()
        elif len(fill_type) == 14:
            if fill_type[:9] == 'list+str_':
                return (args[0], args[1]), (args[2:])
        else:
            raise ValueError(f"Cannot perform fill on args {args}")

    def _fill(self, x, y, color, **kwargs):

        self.plot_types.append('fill')

        hovertext = kwargs.get('hovertext')

        if hovertext is not None:
            hoverinfo = 'text'
        else:
            hoverinfo = 'skip'
        #
        showlegend = kwargs.get('showlegend', False)
        #
        # fill_type = self._get_fill_type(*args)
        alpha = kwargs.get('alpha', 1)
        fill_data = {'x': x,
                     'y': y,
                     'mode': 'lines',
                     'fill': 'toself',
                     'fillcolor': color,
                     'hoverinfo': hoverinfo,
                     'hovertext': hovertext,
                     'hoveron': 'fills',
                     'line_width': 0,
                     'opacity': alpha,
                     'showlegend': showlegend}

        if showlegend & ('name' in kwargs):
            fill_data['name'] = kwargs.get('name')

        if (hovertext is not None) & ('name' not in kwargs):
            fill_data['name'] = kwargs.get('hovertext')

        if (hovertext is not None) & ('name' in kwargs):
            warnings.warn("Both 'name' and 'hovertext' given - defaulting to hovertext. \n"
                          "Plotly fill does not support hovertext. The workaround in Mattplotlib is "
                          "to assign the hovertext provided to the attribute name to provide a name "
                          "label at the side of the filled region. This name label is what will appear "
                          "in the legend so it is advised to not show the filled region in the legend. "
                          "This can be achieved by either not assigning a value to the keyword argument "
                          "showlegend or to explicitly set this to False on calling fill.\n"
                          "eg ax.fill(*args, showlegend=False)")
            fill_data['name'] = kwargs.get('hovertext')

        self.fig.add_trace(fill_data)
        # self.fig.update_layout(layout)

        #
        # if fill_type == 'list+list+str_':
        #     x = args[0]
        #     y = args[1]
        #     fillcolor = args[2]
        #     fill_data = {'x': x,
        #                  'y': y,
        #                  'mode': 'lines',
        #                  'fill' : 'toself',
        #                  'fillcolor': fillcolor,
        #                  'hoverinfo': hoverinfo,
        #                  'hovertext': hovertext,
        #                  'line_width': 0,
        #                  'opacity': alpha}
        #     layout = {'showlegend': showlegend}
        #     self.fig.add_trace(fill_data)
        #     self.fig.update_layout(layout)
        #
        # elif fill_type == 'list+list':
        #     x = args[0]
        #     y = args[1]
        #     fillcolor = self._get_default_plot_color()
        #
        #     self.fig.add_trace(
        #         go.Scatter(x=x,
        #                    y=y,
        #                    mode='lines',
        #                    fill='toself',
        #                    fillcolor=fillcolor,
        #                    line_color=None,
        #                    hoverinfo=hoverinfo,
        #                    hovertext=hovertext,
        #                    line_width=0,
        #                    opacity=alpha,
        #                    showlegend=showlegend))
        # elif fill_type == 'list+str_':
        #     y = args[0]
        #     x = list(range(len(y)))
        #     fillcolor = args[1]
        #
        #     self.fig.add_trace(
        #         go.Scatter(x=x,
        #                    y=y,
        #                    mode='lines',
        #                    fill='toself',
        #                    fillcolor=fillcolor,
        #                    line_color=None,
        #                    hoverinfo=hoverinfo,
        #                    hovertext=hovertext,
        #                    line_width=0,
        #                    opacity=alpha,
        #                    showlegend=showlegend))
        # elif fill_type == 'list':
        #     y = args[0]
        #     x = list(range(len(y)))
        #     fillcolor = self._get_default_plot_color()
        #
        #     self.fig.add_trace(
        #         go.Scatter(x=x,
        #                    y=y,
        #                    mode='lines',
        #                    fill='toself',
        #                    fillcolor=fillcolor,
        #                    line_color=None,
        #                    hoverinfo=hoverinfo,
        #                    hovertext=hovertext,
        #                    line_width=0,
        #                    opacity=alpha,
        #                    showlegend=showlegend))

    def _text(self, *args, **kwargs):

        if len(args) == 1:
            raise TypeError("text() missing 2 required positional arguments: 'y', and 's'")
        elif len(args) == 2:
            raise TypeError("text() missing 1 required positional arguments: 's'")

        x = args[0]
        y = args[1]
        s = args[2].replace("\n", "<br>")

        align = kwargs.get('horizontalalignment', 'center')
        horizontalalignment = kwargs.get('horizontalalignment', 'left')
        verticalalignment = kwargs.get('verticalalignment', 'bottom')
        if (verticalalignment == 'centre') | (verticalalignment == 'center'):
            verticalalignment = 'middle'

        if 'fontweight' in kwargs:
            if kwargs['fontweight'] == 'bold':
                s = f"<b>{s}</b>"

        font = self._extract_font_properties(**kwargs)
        if (self.subplot_row_col['row'], self.subplot_row_col['col']) != (1, 1):
            self.fig.add_annotation(
                x=x,
                y=y,
                xref='x',
                yref='y',
                text=s,
                showarrow=False,
                xanchor=horizontalalignment,
                yanchor=verticalalignment,
                align=align,
                font=font,
                **self.subplot_row_col
            )
        else:
            ann = list(self.fig.layout.annotations)
            for ann_ in ann:
                self.fig.add_annotation(ann_)
            self.fig.add_annotation(
                x=x,
                y=y,
                xref='x',
                yref='y',
                text=s,
                showarrow=False,
                xanchor=horizontalalignment,
                yanchor=verticalalignment,
                align=align,
                font=font,
                **self.subplot_row_col
            )

    def _parse_hovertext(self, hovertext):
        if hovertext is not None:

            if type(hovertext) == str:
                self._parse_hovertest_string(hovertext)
            elif type(hovertext) == list:
                hovertext = [self._parse_hovertest_string(hovertext_string) for hovertext_string in hovertext]
        return hovertext

    def _parse_hovertest_string(self, hovertext_string):

        if self.font['weight']:
            hovertext_string = f"<b>{hovertext_string}</b>"

        hovertext_string = hovertext_string.replace("\n", "<br>")

        return hovertext_string


    def _format_axes(self, **kwargs):
        font = self._extract_font_properties(**kwargs)
        self.fig.update_xaxes(tickfont=font, **self.subplot_row_col)
        self.fig.update_yaxes(tickfont=font, **self.subplot_row_col)
        self.fig.update_xaxes(titlefont=font, **self.subplot_row_col)
        self.fig.update_yaxes(titlefont=font, **self.subplot_row_col)

        self.fig.update_xaxes(gridcolor=self.rcParams_layout['xaxis']['gridcolor'],
                              **self.subplot_row_col)
        self.fig.update_xaxes(gridwidth=self.rcParams_layout['xaxis']['gridwidth'],
                              **self.subplot_row_col)
        self.fig.update_xaxes(zeroline=False,
                              **self.subplot_row_col)
        self.fig.update_yaxes(gridcolor=self.rcParams_layout['yaxis']['gridcolor'],
                              **self.subplot_row_col)
        self.fig.update_yaxes(zeroline=False,
                              **self.subplot_row_col)

        # self.fig.layout.yaxis['zeroline'] = False
        # self.fig.layout.xaxis['showgrid'] = False
        # self.fig.layout.xaxis['zeroline'] = False



    def set_xlabel(self,
               text,
               **kwargs):
        """Update x-axis title"""
        font = self._extract_font_properties(**kwargs)
        self.fig.update_xaxes(title={'text': text, 'font': font}, **self.subplot_row_col)

    def set_xticks(self,
                   xtick_locs,
                   rotation=0,
                   **kwargs):

        """Update x-axis ticks and labels"""
        font = self._extract_font_properties(**kwargs)
        self.fig.update_xaxes(tickvals=list(xtick_locs),
                              tickangle=-rotation,
                              tickfont=font,
                              **self.subplot_row_col)

    def set_xticklabels(self,
                        xticklabels,
                        rotation=0,
                        **kwargs):

        font = self._extract_font_properties(**kwargs)
        self.fig.update_xaxes(ticktext=list(xticklabels),
                              tickangle=-rotation,
                              tickfont=font,
                              **self.subplot_row_col)


    def set_ylabel(self,
               text,
               **kwargs):
        """Update y-axis title"""
        font = self._extract_font_properties(**kwargs)
        self.fig.update_yaxes(title={'text': text, 'font': font}, **self.subplot_row_col)

    def set_yticks(self,
               ytick_locs,
               rotation=0,
               **kwargs):

        "Update y-axis ticks and labels"
        font = self._extract_font_properties(**kwargs)
        self.fig.update_yaxes(tickvals=list(ytick_locs),
                              tickangle=-rotation,
                              tickfont=font,
                              **self.subplot_row_col)

    def set_yticklabels(self,
                        yticklabels,
                        rotation=0,
                        **kwargs):

        font = self._extract_font_properties(**kwargs)
        self.fig.update_yaxes(ticktext=list(yticklabels),
                              tickangle=-rotation,
                              tickfont=font,
                              **self.subplot_row_col)

    def set_xlim(self, xlim_lower, xlim_upper, **kwargs):
        "Set lower and upper limits on x axis"

        if self.subplot_layout.get('sharedx', None):
            self.fig.update_xaxes(range=[xlim_lower, xlim_upper], row=1, col=1)
        else:
            self.fig.update_xaxes(range=[xlim_lower, xlim_upper],
                                  **self.subplot_row_col)

    def set_ylim(self, ylim_lower, ylim_upper, *args, **kwargs):
        "Set lower and upper limits on y axis"
        # if ylim_lower == 0:
        #     ylim_lower = - 0.01 * ylim_upper

        if self.subplot_layout.get('sharedy', None):
            self.fig.update_yaxes(range=[ylim_lower, ylim_upper], row=1, col=1)
        else:
            self.fig.update_yaxes(range=[ylim_lower, ylim_upper],
                                  **self.subplot_row_col)

    def show(self):
        if self.fig is not None:
            self.fig.show()
            self.fig = None

    def set_title(self,
              title_text,
              y=1.0,
              **kwargs):

        "Set a title on the plot"
        font = self._extract_font_properties(**kwargs)
        if 'fontweight' in kwargs:
            title_text = f'<b>{title_text}</b>'.replace("\n", "<br>")

        if self.subplot_row_col is None:

            self.fig.update_layout(title={
                'text': title_text,
                'y': y,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': font})
            self.fig.layout.margin['t'] += 50

        else:
            self.annotations = list(self.fig.layout.annotations)
            for ann in self.annotations:
                self.fig.add_annotation(ann)

            plot_id = (self.subplot_row_col['row'] - 1) * self.subplot_layout['cols'] + self.subplot_row_col['col'] - 1
            self.fig.layout.annotations[plot_id].update(text=title_text, y=y, font=font)

    def _order_data(self, data):

        # extract plots and add them first
        return_data = []
        for plot_id, plot in enumerate(self.plot_types):
            if plot == 'plot':
                return_data.append(data[plot_id])

        for plot_id, plot in enumerate(self.plot_types):
            if plot != 'plot':
                return_data.append(data[plot_id])

        return tuple(return_data)


    def legend(self,
               *args,
               **kwargs):

        labels = None
        if len(args) > 0:
            labels = args[0]

        font = self._extract_font_properties(**kwargs)
        self.fig.layout.font = font
        self.fig.update_layout(showlegend=True)

        i = 0
        if labels is None:
            None
        else:
            for handle in self.fig.data:
                if i <= len(labels):
                    if 'showlegend' in handle:
                        if self.fig.data[i].showlegend == False:
                            None
                        elif labels[i] == '_nolabel_':
                            self.fig.data[i].showlegend = False
                        else:
                            self.fig.data[i]['name'] = labels[i]
                    else:
                        if labels[i] == '_nolabel_':
                            self.fig.data[i].showlegend = False
                        else:
                            self.fig.data[i]['name'] = labels[i]
                    i += 1


        if 'title' in kwargs:
            self.fig.update_layout(legend_title_text=kwargs['title'])

        loc = kwargs.get('loc', self.rcParams_legend['loc'])
        if (loc == 'best') | (loc == 0):
            None
        elif (loc == 'upper right') | (loc == 1):
            self.fig.layout.legend['xanchor'] = 'right'
            self.fig.layout.legend['yanchor'] = 'top'
            self.fig.layout.legend['x']=0.95
            self.fig.layout.legend['y']=0.95
        elif (loc == 'upper left') | (loc == 2):
            self.fig.layout.legend['xanchor'] = 'left'
            self.fig.layout.legend['yanchor'] = 'top'
            self.fig.layout.legend['x'] = 0.05
            self.fig.layout.legend['y'] = 0.95
        elif (loc == 'lower left') | (loc == 3):
            self.fig.layout.legend['xanchor'] = 'left'
            self.fig.layout.legend['yanchor'] = 'bottom'
            self.fig.layout.legend['x'] = 0.05
            self.fig.layout.legend['y'] = 0.05
        elif (loc == 'lower right') | (loc == 4):
            self.fig.layout.legend['xanchor'] = 'right'
            self.fig.layout.legend['yanchor'] = 'bottom'
            self.fig.layout.legend['x'] = 0.95
            self.fig.layout.legend['y'] = 0.05
        elif (loc == 'right') | (loc == 5):
            self.fig.layout.legend['xanchor'] = 'right'
            self.fig.layout.legend['yanchor'] = 'middle'
            self.fig.layout.legend['x'] = 0.95
            self.fig.layout.legend['y'] = 0.5
        elif (loc == 'center left') | (loc == 6):
            self.fig.layout.legend['xanchor'] = 'left'
            self.fig.layout.legend['yanchor'] = 'middle'
            self.fig.layout.legend['x'] = 0.05
            self.fig.layout.legend['y'] = 0.5
        elif (loc == 'center right') | (loc == 7):
            self.fig.layout.legend['xanchor'] = 'right'
            self.fig.layout.legend['yanchor'] = 'middle'
            self.fig.layout.legend['x'] = 0.95
            self.fig.layout.legend['y'] = 0.5
        elif (loc == 'lower center') | (loc == 8):
            self.fig.layout.legend['xanchor'] = 'center'
            self.fig.layout.legend['yanchor'] = 'bottom'
            self.fig.layout.legend['x'] = 0.5
            self.fig.layout.legend['y'] = 0.05
        elif (loc == 'upper center') | (loc == 9):
            self.fig.layout.legend['xanchor'] = 'center'
            self.fig.layout.legend['yanchor'] = 'top'
            self.fig.layout.legend['x'] = 0.5
            self.fig.layout.legend['y'] = 0.95
        elif (loc == 'center') | (loc == 10):
            self.fig.layout.legend['xanchor'] = 'center'
            self.fig.layout.legend['yanchor'] = 'middle'
            self.fig.layout.legend['x'] = 0.5
            self.fig.layout.legend['y'] = 0.5

        if 'fontsize' in kwargs:
            fontsize = kwargs['fontsize']
            if type(fontsize) == int:
                self.fig.layout.font['size'] = fontsize
            elif type(fontsize) == 'xx-small':
                self.fig.layout.font['size'] = max(default_font['size'] - 6, 2)
            elif type(fontsize) == 'x-small':
                self.fig.layout.font['size'] = max(default_font['size'] - 4, 2)
            elif type(fontsize) == 'small':
                self.fig.layout.font['size'] = max(default_font['size'] - 2, 2)
            elif type(fontsize) == 'large':
                self.fig.layout.font['size'] = default_font['size'] + 2
            elif type(fontsize) == 'x-large':
                self.fig.layout.font['size'] = default_font['size'] + 4
            elif type(fontsize) == 'xx-large':
                self.fig.layout.font['size'] = default_font['size'] + 6

        frameon = kwargs.get('frameon')
        edgecolor = kwargs.get('edgecolor')
        facecolor = kwargs.get('facecolor')
        if frameon is not None:
            if not frameon:
                self.fig.layout.legend['borderwidth'] = 0
            else:
                self.fig.layout.legend['borderwidth'] = 2
                self.fig.layout.legend['bordercolor'] = 'grey'
        if edgecolor is not None:
            self.fig.layout.legend['bordercolor'] = edgecolor
        if facecolor is not None:
            self.fig.layout.legend['bgcolor'] = facecolor

    def grid(self, b, which=None, axis='both'):
        if b:
            if axis == 'x':
                self.fig.update_xaxes(showgrid=True,
                                  **self.subplot_row_col)
                self.fig.update_yaxes(showgrid=False,
                                  **self.subplot_row_col)
            elif axis == 'y':
                self.fig.update_xaxes(showgrid=False,
                                  **self.subplot_row_col)
                self.fig.update_yaxes(showgrid=True,
                                  **self.subplot_row_col)
            elif axis == 'both':
                self.fig.update_xaxes(showgrid=True,
                                  **self.subplot_row_col)
                self.fig.update_yaxes(showgrid=True,
                                  **self.subplot_row_col)
        else:
            self.fig.update_xaxes(showgrid=False,
                                  **self.subplot_row_col)
            self.fig.update_yaxes(showgrid=False,
                                  **self.subplot_row_col)


    def _extract_font_properties(self, **kwargs):
        font = {}
        font['color'] = kwargs.get('color', self.rcParams_text['color'])
        font['size'] = kwargs.get('fontsize', self.font['size'])
        if 'size' in kwargs:
            font['size'] = kwargs.get('size', self.font['size'])
            if 'fontsize' in kwargs:
                warnings.warn("Both 'size' and 'fontsize' given, defaulting to 'size'.")

        font['family'] = kwargs.get('family', self.font['family'])

        font['size'] = self._convert_relative_text_size(font['size'])

        return font

    def _convert_text_using_rcParams(self, string):
        if self.font['weight']:
            return f"<b>{string}</b>"

    def _convert_relative_text_size(self, size):
        default_size = self.font['size']

        try:
            size = float(size)
        except:
            if size == 'xx-small':
                size = max(default_size - 6, 2)
            elif size == 'x-small':
                size = max(default_size - 4, 2)
            elif size == 'small':
                size = max(default_size - 2, 2)
            elif size == 'medium':
                size = default_size
            elif size == 'large':
                size = default_size + 2
            elif size == 'x-large':
                size = default_size + 4
            elif size == 'xx-large':
                size = default_size + 6
            else:
                raise ValueError(f"""font size {size} not recognised: must be an int, float, or one of the following:
                'xx-small'
                'x-small'
                'small'
                'medium'
                'large'
                'x-large'
                'xx-large'
                """)

        return size

    def matplotlibify_the_color(self, color):
        alpha = 1
        if color in mcolors.BASE_COLORS:
            color = self.base_color_dict[color]
        elif color in mcolors.TABLEAU_COLORS:
            None
        elif color in mcolors.CSS4_COLORS:
            None
        elif type(color) == str:
            if color[:3] == 'rgb':
                color, alpha = self._get_rgb_color_tuple(color)
        color_rgb = matplotlib.colors.to_rgb(color)

        if max(color_rgb) <= 1:
            color_rgb = [c * 256 for c in color_rgb]

        if alpha != 1:
            color_rgb = tuple(list(color_rgb) + [alpha])

        return color_rgb


    def _get_rgb_color_list(self, rgb_str):
        return [float(c) for c in rgb_str.split('(')[1].split(')')[0].split(', ')]

    def _get_rgb_color_tuple(self, rgb_str):
        rgb_str = rgb_str.replace('a', '')
        rgb_list = [float(c) for c in rgb_str.split('(')[1].split(')')[0].split(', ')]
        if max(rgb_list) > 1:
            rgb_list = [c / 256 for c in rgb_list]
        if len(rgb_list) == 3:
            return tuple(rgb_list), 1
        else:
            return tuple(rgb_list[:3]), rgb_list[-1]

    def _rgb_to_rgba_tuple(self, rgb_tuple_or_list, alpha):
        return (rgb_tuple_or_list[0], rgb_tuple_or_list[1], rgb_tuple_or_list[2], alpha)

    def _named_color_to_rgb_tuple(self, named_color_str):
        return matplotlib.colors.to_rgb(matplotlib.colors.get_named_colors_mapping()[named_color_str])

    def _named_color_to_rgba_tuple(self, named_color_str, alpha):
        rgb_tuple = self._named_color_to_rgb_tuple(named_color_str)
        return self._rgb_to_rgba_tuple(rgb_tuple, alpha)

    def _rgb_tuple_to_str(self, rgb_tuple):
        rgb_tuple = tuple(rgb_tuple)
        return f"rgba{rgb_tuple}"

    def _update_alpha_in_rgb_str(self, rgb_str, alpha):
        rgb_list = self._get_rgb_color_list(rgb_str)
        rgba_tuple = self._rgb_to_rgba_tuple(rgb_list, alpha)
        return self._rgb_tuple_to_str(rgba_tuple)

    def _add_alpha_value(self, color, alpha):
        if color[:3] == 'rgb':
            rbga_color_str = self._update_alpha_in_rgb_str(color, alpha)
        else:
            try:
                rbga_color_str = self._named_color_to_rgba_tuple(color)
            except:
                raise ValueError(f"unrecognised color {color}")

        return rgba_color_str


    def _convert_color_to_rgba_str(self, color, alpha):

        if type(color) == str:
            if color[:3] != 'rgb':
                # string defined color
                if alpha is not None:
                    #alpha specified
                    color_rgba_tuple = self._named_color_to_rgba_tuple(color, alpha)
                    color_rgba = self._rgb_tuple_to_str(color_rgba_tuple)
                else:
                    # alpha not specified default to 1
                    color_rgba_tuple = self._named_color_to_rgba_tuple(color, 1)
                    color_rgba = self._rgb_tuple_to_str(color_rgba_tuple)
            elif color[:4] != 'rgba':
                # given rgb or rgba without alpha given as keyword argument
                color_rgba = color
                # given rgb or rgba with alpha given as keyword argument
                if alpha is not None:
                    color_rgba = self._update_alpha_in_rgb_str(color, alpha)
            else:
                if alpha is not None:
                    color_rgba = self._update_alpha_in_rgb_str(color, alpha)
                else:
                    color_rgba = self._update_alpha_in_rgb_str(color, 1)
        elif (type(color) == tuple) | (type(color) == list):
            color = tuple(color)
            # tuple provided
            if alpha is not None:
                # given tuple with alpha given as keyword argument
                color_rgba = self._rgb_tuple_to_str(self._rgb_to_rgba_tuple(color, alpha))
            elif len(color) == 4:
                # rgba tuple given
                color_rgba = self._rgb_tuple_to_str(color)
            if len(color) == 3:
                # rgb tuple given default alpha to 1
                color_rgba = self._rgb_tuple_to_str(self._rgb_to_rgba_tuple(color, 1))
        else:
            raise ValueError('Unsupported color type. Specify named string, rgb, or rgba colours')

        return color_rgba

    def _set_marker_defaults(self):
        marker_defaults = {'marker': {'color': self.lines['markerfacecolor'],
                                   'size': self.lines['markersize'],
                                   'line': {'color': self.lines['markeredgecolor'],
                                            'width': self.lines['markeredgewidth']}},
                        'marker_symbol': self.lines['marker']}
        return marker_defaults

    def _set_legend_defaults(self):
        legend_defaults = {}

        title_font = self._extract_font_properties({'size': self.rcParams_legend['title_fontsize']})
        legend_defaults['legend_title_font'] = title_font
        font = self._extract_font_properties({'size': self.rcParams_legend['fontsize']})
        legend_defaults['font'] = font

        loc = self.rcParams_legend['loc']
        legend_defaults.update(self._get_legend_loc_params(loc))

        if self.rcParams_legend['frameon']:
            legend_defaults['borderwidth'] = self.lines['linewidth']
            legend_defaults['bordercolor'] = self.rcParams_legend['edgecolor']
            legend_defaults['bgcolor'] = self.rcParams_legend['facecolor']



    def _get_legend_loc_params(self, loc):

        loc_dict = {}
        if (loc == 'best') | (loc == 0):
            None
        elif (loc == 'upper right') | (loc == 1):
            loc_dict['xanchor'] = 'right'
            loc_dict['yanchor'] = 'top'
            loc_dict['x'] = 0.95
            loc_dict['y'] = 0.95
        elif (loc == 'upper left') | (loc == 2):
            loc_dict['xanchor'] = 'left'
            loc_dict['yanchor'] = 'top'
            loc_dict['x'] = 0.05
            loc_dict['y'] = 0.95
        elif (loc == 'lower left') | (loc == 3):
            loc_dict['xanchor'] = 'left'
            loc_dict['yanchor'] = 'bottom'
            loc_dict['x'] = 0.05
            loc_dict['y'] = 0.05
        elif (loc == 'lower right') | (loc == 4):
            loc_dict['xanchor'] = 'right'
            loc_dict['yanchor'] = 'bottom'
            loc_dict['x'] = 0.95
            loc_dict['y'] = 0.05
        elif (loc == 'right') | (loc == 5):
            loc_dict['xanchor'] = 'right'
            loc_dict['yanchor'] = 'middle'
            loc_dict['x'] = 0.95
            loc_dict['y'] = 0.5
        elif (loc == 'center left') | (loc == 6):
            loc_dict['xanchor'] = 'left'
            loc_dict['yanchor'] = 'middle'
            loc_dict['x'] = 0.05
            loc_dict['y'] = 0.5
        elif (loc == 'center right') | (loc == 7):
            loc_dict['xanchor'] = 'right'
            loc_dict['yanchor'] = 'middle'
            loc_dict['x'] = 0.95
            loc_dict['y'] = 0.5
        elif (loc == 'lower center') | (loc == 8):
            loc_dict['xanchor'] = 'center'
            loc_dict['yanchor'] = 'bottom'
            loc_dict['x'] = 0.5
            loc_dict['y'] = 0.05
        elif (loc == 'upper center') | (loc == 9):
            loc_dict['xanchor'] = 'center'
            loc_dict['yanchor'] = 'top'
            loc_dict['x'] = 0.5
            loc_dict['y'] = 0.95
        elif (loc == 'center') | (loc == 10):
            loc_dict['xanchor'] = 'center'
            loc_dict['yanchor'] = 'middle'
            loc_dict['x'] = 0.5
            loc_dict['y'] = 0.5
        return loc_dict

    def _read_in_rcParams(self, stylesheet_filename):

        rcp = {}
        with open(stylesheet_filename, "r") as f:
            for line in f:
                line = line.strip()
                if len(line) > 0:
                    if (':' in line) & ('.' in line) & (line.strip()[0] != '#'):
                        try:
                            rcpline = line.strip()
                            rcpline = rcpline.split('#')[0]
                            rcpline = rcpline.split(':')[: 2]
                            rcp[rcpline[0].strip()] = rcpline[1].strip()

                        except:
                            raise ValueError(f"unpassable rcParam line {line}")

        return rcp

    def style_use(self, stylesheet_filename):

        rcParams = self._read_in_rcParams(stylesheet_filename)

        self.lines = {}
        self.markers = {}
        self.lines['width'] = float(rcParams.get('lines.linewidth', 1.5))
        self.lines['dash'] = rcParams.get('lines.linestyle')
        self.lines['color'] = rcParams.get('lines.color', 'steelblue')
        # lines.dash_joinstyle : round        ## miter|round|bevel
        # lines.dash_capstyle : butt          ## butt|round|projecting
        # lines.solid_joinstyle : round       ## miter|round|bevel
        # lines.solid_capstyle : projecting   ## butt|round|projecting
        # lines.antialiased : True         ## render lines in antialiased (no jaggies)
        # # The three standard dash patterns.  These are scaled by the linewidth.
        # lines.dashed_pattern : 3.7, 1.6
        # lines.dashdot_pattern : 6.4, 1.6, 1, 1.6
        # lines.dotted_pattern : 1, 1.65
        # lines.scale_dashes : True
        self.markers = {'line': {}}
        self.markers['symbol'] = rcParams.get('lines.marker', self.marker_dict['.'])
        self.markers['color'] = rcParams.get('lines.markerfacecolor', 'steelblue')
        self.markers['size'] = float(rcParams.get('lines.markersize', 5))
        self.markers['line']['color'] = rcParams.get('lines.markeredgecolor', 'steelblue')
        self.markers['line']['width'] = float(rcParams.get('lines.markeredgewidth', 1.5))

        self.rcParams_legend = {}
        # 'legend.borderaxespad': 0.5,
        # 'legend.borderpad': 0.4,
        # 'legend.columnspacing': 2.0,
        self.rcParams_legend['edgecolor'] = rcParams.get('legend.edgecolor')
        self.rcParams_legend['facecolor'] = rcParams.get('legend.facecolor')
        # 'legend.fancybox': True,
        self.rcParams_legend['fontsize'] = rcParams.get('legend.fontsize')
        # 'legend.framealpha': 0.8,
        self.rcParams_legend['frameon'] = rcParams.get('legend.frameon', False)
        # 'legend.handleheight': 0.7,
        # 'legend.handlelength': 2.0,
        # 'legend.handletextpad': 0.8,
        # 'legend.labelspacing': 0.5,
        self.rcParams_legend['loc'] = rcParams.get('legend.loc', 'upper right')
        # 'legend.markerscale': 1.0,
        # 'legend.numpoints': 1,
        # 'legend.scatterpoints': 1,
        # 'legend.shadow': False,
        self.rcParams_legend['title_fontsize'] = rcParams.get('legend.title_fontsize')

        self.patch = {}
        self.patch['linewidth'] = float(rcParams.get('patchlinewidth', 0))
        self.patch['facecolor'] = rcParams.get('patch.facecolor', 'steelblue')
        self.patch['edgecolor'] = rcParams.get('patch.edgecolor')
        # patch.force_edgecolor  : False   ## True to always use edgecolor
        # patch.antialiased      : True    ## render patches in antialiased (no jaggies)

        self.font = {}
        self.font['family'] = rcParams.get('font.family', 'serif')
        # font.style          : normal
        # font.variant        : normal
        self.font['weight'] = rcParams.get('font.weight')
        # font.stretch        : normal
        self.font['size'] = float(rcParams.get('font.size', 16))
        # font.serif          : DejaVu Serif, Bitstream Vera Serif, Computer Modern Roman, New Century Schoolbook, Century Schoolbook L, Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L, Times New Roman, Times, Palatino, Charter, serif
        # font.sans-serif     : DejaVu Sans, Bitstream Vera Sans, Computer Modern Sans Serif, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
        # font.cursive        : Apple Chancery, Textile, Zapf Chancery, Sand, Script MT, Felipa, cursive
        # font.fantasy        : Comic Sans MS, Chicago, Charcoal, ImpactWestern, Humor Sans, xkcd, fantasy
        # font.monospace      : DejaVu Sans Mono, Bitstream Vera Sans Mono, Computer Modern Typewriter, Andale Mono, Nimbus Mono L, Courier New, Courier, Fixed, Terminal, monospace

        self.rcParams_text = {}
        self.rcParams_text['color'] = rcParams.get('text.color', 'grey')
        self.rcParams_text['usetex'] = rcParams.get('text.usetex', True)
        # text.latex.preamble :      ## IMPROPER USE OF THIS FEATURE WILL LEAD TO LATEX FAILURES
        # text.latex.preview : False
        # text.hinting : auto   ## May be one of the following:
        # text.hinting_factor : 8 ## Specifies the amount of softness for hinting in the
        # text.antialiased : True ## If True (default), the text will be antialiased.

        self.rcParams_layout = {'xaxis': {'tickfont': {}, 'title': {}},
                                'yaxis': {'tickfont': {}, 'title': {}},
                                # 'zaxis': {'tickfont': {}, 'title': {}},
                                'title': {}}
        self.rcParams_layout['plot_bgcolor'] = rcParams.get('axes.facecolor', 'rgba(0, 0, 0, 0)')
        self.rcParams_layout['paper_bgcolor'] = 'rgba(0, 0, 0, 0)'
        self.rcParams_layout['xaxis']['linecolor'] = rcParams.get('axes.edgecolor', 'grey')
        self.rcParams_layout['xaxis']['linewidth'] = float(rcParams.get('axes.linewidth', 2))
        self.rcParams_layout['yaxis']['linecolor'] = rcParams.get('axes.edgecolor', 'grey')
        self.rcParams_layout['yaxis']['linewidth'] = float(rcParams.get('axes.linewidth', 2))
        # self.rcParams_layout['zaxis']['linecolor'] = rcParams.get('axes.edgecolor', 'grey')
        # self.rcParams_layout['zaxis']['linewidth'] = float(rcParams.get('axes.linewidth', 2))
        if rcParams.get('axes.grid', False):
            if rcParams.get('axes.grid.axis') == 'x':
                self.rcParams_layout['xaxis']['showgrid'] = True
                self.rcParams_layout['yaxis']['showgrid'] = False
                # self.rcParams_layout['zaxis']['showgrid'] = False
            elif rcParams.get('axes.grid.axis') == 'y':
                self.rcParams_layout['xaxis']['showgrid'] = False
                self.rcParams_layout['yaxis']['showgrid'] = True
                # self.rcParams_layout['zaxis']['showgrid'] = False
            elif rcParams.get('axes.grid.axis') == 'z':
                self.rcParams_layout['xaxis']['showgrid'] = False
                self.rcParams_layout['yaxis']['showgrid'] = False
                # self.rcParams_layout['zaxis']['showgrid'] = True
            elif rcParams.get('axes.grid.axis') == 'both':
                self.rcParams_layout['xaxis']['showgrid'] = True
                self.rcParams_layout['yaxis']['showgrid'] = True
                # self.rcParams_layout['zaxis']['showgrid'] = True
        self.rcParams_layout['xaxis']['zeroline'] = False
        self.rcParams_layout['yaxis']['zeroline'] = False
        # self.rcParams_layout['zaxis']['zeroline'] = False
        # axes.grid.which     : major   ## gridlines at major, minor or both ticks
        self.rcParams_layout['title']['font'] = {
            'size': self._convert_relative_text_size(rcParams.get('axes.labelsize', 'x-large'))}
        # axes.titleweight    : normal  ## font weight of title
        # axes.titlepad       : 6.0     ## pad between axes and title in points
        self.rcParams_layout['xaxis']['title']['font'] = {
            'size': self._convert_relative_text_size(rcParams.get('axes.labelsize', 'medium')),
            'color': rcParams.get('axes.labelcolor', 'grey')}
        self.rcParams_layout['yaxis']['title']['font'] = {
            'size': self._convert_relative_text_size(rcParams.get('axes.labelsize', 'medium')),
            'color': rcParams.get('axes.labelcolor', 'grey')}
        # self.rcParams_layout['zaxis']['title']['font'] = {
        #     'size': self._convert_relative_text_size(rcParams.get('axes.labelsize', 'medium')),
        #     'color': rcParams.get('axes.labelcolor', 'grey')}
        # axes.labelpad       : 4.0     ## space between label and axis
        # axes.labelweight    : normal  ## weight of the x and y labels
        # axes.axisbelow      : line    ## draw axis gridlines and ticks below
        # axes.formatter.limits : -7, 7 ## use scientific notation if log10
        # axes.formatter.use_locale : False ## When True, format tick labels
        # axes.formatter.use_mathtext : False ## When True, use mathtext for scientific
        # axes.formatter.min_exponent: 0 ## minimum exponent to format in scientific notation
        # axes.formatter.useoffset      : True    ## If True, the tick label formatter
        # axes.formatter.offset_threshold : 4     ## When useoffset is True, the offset

        self.spines['top'].set_visible(eval(rcParams.get('axes.spines.top', False)), setting_default=True)
        self.spines['left'].set_visible(eval(rcParams.get('axes.spines.left', True)), setting_default=True)
        self.spines['bottom'].set_visible(eval(rcParams.get('axes.spines.bottom', True)), setting_default=True)
        self.spines['right'].set_visible(eval(rcParams.get('axes.spines.right', False)), setting_default=True)

        self.rcParams_layout['yaxis']['showline'] = eval(rcParams.get('axes.spines.left', True))
        self.rcParams_layout['xaxis']['showline'] = eval(rcParams.get('axes.spines.bottom', True))
        self.rcParams_layout['xaxis']['mirror'] = eval(rcParams.get('axes.spines.top', False))
        self.rcParams_layout['yaxis']['mirror'] = eval(rcParams.get('axes.spines.right', False))

        if (not self.rcParams_layout['yaxis']['showline']) & self.rcParams_layout['yaxis']['mirror']:
            warnings.warn('Cannot display right spine without left spine in plotly')
        if (not self.rcParams_layout['xaxis']['showline']) & self.rcParams_layout['xaxis']['mirror']:
            warnings.warn('Cannot display top spine without bottom spine in plotly')

        # axes.unicode_minus  : True    ## use unicode for the minus symbol
        # axes.autolimit_mode : data ## How to scale axes limits to the data.
        # axes.xmargin        : .05  ## x margin.  See `axes.Axes.margins`
        # axes.ymargin        : .05  ## y margin See `axes.Axes.margins`
        # polaraxes.grid      : True    ## display grid on polar axes
        # axes3d.grid         : True    ## display grid on 3d axes

## xtick properties
        self.rcParams_layout['xaxis']['ticks'] = None

        if bool(rcParams.get('xtick.top', False)):
            self.rcParams_layout['xaxis']['ticks'] = 'inside'
        if bool(rcParams.get('xtick.bottom', False)):
            self.rcParams_layout['xaxis']['ticks'] = 'outside'
        # xtick.labeltop       : False  ## draw label on the top
        # xtick.labelbottom    : True   ## draw label on the bottom
        self.rcParams_layout['xaxis']['ticklen'] = float(rcParams.get('xtick.major.size', 3.5))
        # xtick.minor.size     : 2      ## minor tick size in points
        self.rcParams_layout['xaxis']['tickwidth'] = float(rcParams.get('xtick.major.width', 3.5))
        # xtick.minor.width    : 0.6    ## minor tick width in points
        # xtick.major.pad      : 3.5    ## distance to major tick label in points
        # xtick.minor.pad      : 3.4    ## distance to the minor tick label in points
        self.rcParams_layout['xaxis']['tickfont']['family'] = self.font['family']
        self.rcParams_layout['xaxis']['color'] = rcParams.get('xtick.color', 'grey')
        self.rcParams_layout['xaxis']['tickfont']['size'] = self._convert_relative_text_size(
            rcParams.get('xtick.labelsize', 'medium'))

        if rcParams.get('xtick.direction', 'out') == 'out':
            self.rcParams_layout['xaxis']['ticks'] = 'outside'
        else:
            self.rcParams_layout['xaxis']['ticks'] = 'inside'

        if rcParams.get('xtick.major.top') is not None:
            if rcParams.get('xtick.major.top'):
                self.rcParams_layout['xaxis']['ticks'] = 'inside'
            else:
                self.rcParams_layout['xaxis']['ticks'] = 'outside'
        if rcParams.get('xtick.major.bottom') is not None:
            if rcParams.get('xtick.major.bottom'):
                self.rcParams_layout['xaxis']['ticks'] = 'outside'
            else:
                self.rcParams_layout['xaxis']['ticks'] = 'inside'
        # xtick.minor.visible  : False  ## visibility of minor ticks on x-axis
        # xtick.major.top      : True   ## draw x axis top major ticks
        # xtick.major.bottom   : True   ## draw x axis bottom major ticks
        # xtick.minor.top      : True   ## draw x axis top minor ticks
        # xtick.minor.bottom   : True   ## draw x axis bottom minor ticks
        # xtick.alignment      : center ## alignment of xticks

## ytick properties
        self.rcParams_layout['yaxis']['ticks'] = None
        if bool(rcParams.get('ytick.top', False)):
            self.rcParams_layout['yaxis']['ticks'] = 'inside'
        if bool(rcParams.get('ytick.bottom', False)):
            self.rcParams_layout['yaxis']['ticks'] = 'outside'
        # ytick.labeltop       : False  ## draw label on the top
        # ytick.labelbottom    : True   ## draw label on the bottom
        self.rcParams_layout['yaxis']['ticklen'] = float(rcParams.get('ytick.major.size', 3.5))
        # ytick.minor.size     : 2      ## minor tick size in points
        self.rcParams_layout['yaxis']['tickwidth'] = float(rcParams.get('ytick.major.width', 3.5))
        # ytick.minor.width    : 0.6    ## minor tick width in points
        # ytick.major.pad      : 3.5    ## distance to major tick label in points
        # ytick.minor.pad      : 3.4    ## distance to the minor tick label in points
        self.rcParams_layout['yaxis']['color'] = rcParams.get('ytick.color', 'grey')
        self.rcParams_layout['yaxis']['tickfont']['family'] = self.font['family']

        self.rcParams_layout['yaxis']['tickfont']['size'] = self._convert_relative_text_size(
            rcParams.get('ytick.labelsize', 'medium'))

        if rcParams.get('ytick.direction', 'out') == 'out':
            self.rcParams_layout['yaxis']['ticks'] = 'outside'
        else:
            self.rcParams_layout['yaxis']['ticks'] = 'inside'

        if rcParams.get('ytick.major.top') is not None:
            if rcParams.get('ytick.major.top'):
                self.rcParams_layout['yaxis']['ticks'] = 'inside'
            else:
                self.rcParams_layout['yaxis']['ticks'] = 'outside'
        if rcParams.get('ytick.major.bottom') is not None:
            if rcParams.get('ytick.major.bottom'):
                self.rcParams_layout['yaxis']['ticks'] = 'outside'
            else:
                self.rcParams_layout['yaxis']['ticks'] = 'inside'

#### GRIDS
        self.rcParams_layout['xaxis']['gridcolor'] = rcParams.get('grid.color', 'silver')
        self.rcParams_layout['yaxis']['gridcolor'] = rcParams.get('grid.color', 'silver')
        # self.rcParams_layout['xaxis']['gridcolor'] = rcParams.get('grid.color', 'silver')
        #grid.linestyle   :   -         ## solid
        self.rcParams_layout['xaxis']['gridwidth'] = float(rcParams.get('grid.linewidth', 0))
        self.rcParams_layout['yaxis']['gridwidth'] = float(rcParams.get('grid.linewidth', 0.8))
        # self.rcParams_layout['xaxis']['gridwidth'] = float(rcParams.get('grid.linewidth', 0.8))
        if float(rcParams.get('grid.alpha', 1)) < 0:
            self.rcParams_layout['xaxis']['gridcolor'] = self._add_alpha_value(
                self.rcParams_layout['xaxis']['gridcolor'], rcParams.get('grid.alpha'))

#### FIGURE
        # self.figure = {}
#figure.titlesize : large      ## size of the figure title (Figure.suptitle())
#figure.titleweight : normal   ## weight of the figure title
        if 'figure.figsize' in rcParams:
            self.figsize = tuple(float(x) for x in rcParams.get('figure.figsize').replace(' ', '').split(','))
        else:
            self.figsize = (7, 5)
#figure.dpi       : 100        ## figure dots per inch
#figure.facecolor : white      ## figure facecolor
#figure.edgecolor : white      ## figure edgecolor
#figure.frameon : True         ## enable figure frame
#figure.max_open_warning : 20  ## The maximum number of figures to open through
                               ## the pyplot interface before emitting a warning.
                               ## If less than one this feature is disabled.
## The figure subplot parameters.  All dimensions are a fraction of the
#figure.subplot.left    : 0.125  ## the left side of the subplots of the figure
#figure.subplot.right   : 0.9    ## the right side of the subplots of the figure
#figure.subplot.bottom  : 0.11   ## the bottom of the subplots of the figure
#figure.subplot.top     : 0.88   ## the top of the subplots of the figure
#figure.subplot.wspace  : 0.2    ## the amount of width reserved for space between subplots,
                                 ## expressed as a fraction of the average axis width
#figure.subplot.hspace  : 0.2    ## the amount of height reserved for space between subplots,
                                 ## expressed as a fraction of the average axis height

## Figure layout
#figure.autolayout : False     ## When True, automatically adjust subplot
                               ## parameters to make the plot fit the figure
                               ## using `tight_layout`
#figure.constrained_layout.use: False ## When True, automatically make plot
                                      ## elements fit on the figure. (Not compatible
                                      ## with `autolayout`, above).
#figure.constrained_layout.h_pad : 0.04167 ## Padding around axes objects. Float representing
#figure.constrained_layout.w_pad : 0.04167 ##  inches. Default is 3./72. inches (3 pts)
#figure.constrained_layout.hspace : 0.02   ## Space between subplot groups. Float representing
#figure.constrained_layout.wspace : 0.02   ##  a fraction of the subplot widths being separated.

        ## savefig
        self.rcParams_savefig = {}
        self.rcParams_savefig['transparent'] = eval(rcParams.get('savefig.transparent', True))
        if rcParams.get('savefig.dpi') == 'figure':
            self.rcParams_savefig['dpi'] = 200
        else:
            self.rcParams_savefig['dpi'] = rcParams.get('savefig.dpi', 300)

    def _get_plot_defaults(self):
        return go.Scatter(marker=self.markers, line=self.lines)

    def _get_scatter_defaults(self):
        return go.Scatter(marker=self.markers)

    def _get_bar_defaults(self):
        return go.Bar()


class figure_handle(go.Figure):
    def __init__(self, **kwargs):
        if 'figure' in kwargs:
            self.figure
        data = kwargs.get('data', ())
        layout = kwargs.get('layout', None)
        go.Figure.__init__(self, data=data, layout=layout)
        self._rcParams_savefig = {'transparent': True,
                                 'dpi': 200}

    def savefig(self, filename, **kwargs):

        if 'transparent' in kwargs:
            self._rcParams_savefig['transparent'] = kwargs.get('transparent')
        if 'dpi' in kwargs:
            self._rcParams_savefig['dpi'] = kwargs.get('dpi')

        if self._rcParams_savefig['transparent']:
            self.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
                               paper_bgcolor='rgba(0, 0, 0, 0)')

        if filename[-4:] in ['.pdf', '.jpg']:
            self.write_image(filename)
        elif filename[-4:] == '.png':
            with tempfile.TemporaryDirectory() as path:
                #     images_from_path = convert_from_path('figures/bubble_plot_example.pdf', output_folder=path)
                image = convert_from_bytes(open(f"filename[:-4].pdf", 'rb').read(),
                                           single_file=True,
                                           dpi=self._rcParams_savefig['dpi'],
                                           transparent=True,
                                           use_cropbox=True)
                image[0].save(filename)

    def _set_rcParams(self, rcParams_savefig):
        self._rcParams_savefig = rcParams_savefig

# class subplots_handle(make_subplots):
#     def __init__(self, rows, cols, subplot_titles, **kwargs):
#         make_subplots(rows, cols, subplot_titles, **kwargs).__init__(self)
#
#     def savefig(self, filename):
#         if self.rcParams_savefig['transparent']:
#             self.f.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',
#                                  paper_bgcolor='rgba(0, 0, 0, 0)')
#
#         if filename[-4:] in ['.pdf', '.jpg']:
#             self.write_image(filename)
#         elif filename[-4:] == '.png':
#             self.rcParams_savefig['dpi']
#             self.write_image(filename.replace('.png', '_temp.pdf'))


class spine_class():
    def __init__(self, label):
        self.spine = {'visible': False,
                      'color': 'grey'}
        self.label = label

    def set_visible(self, set_visible_bool, setting_default=False):

        self.spine['visible'] = set_visible_bool

        if not setting_default:
            if 'fig' not in dir(self):
                raise ValueError("spines haven't been associated with a set of axes")
            else:
                if self.label == 'bottom':
                    self.fig.update_xaxes(showline=True, **self.subplot_row_col)
                elif self.label == 'left':
                    self.fig.update_yaxes(showline=True, **self.subplot_row_col)
                elif (self.label == 'right'):
                    self.fig.update_yaxes(showline=True, mirror=True, **self.subplot_row_col)
                    warnings.warn(
                        "Warning: you cannot display the right axis without the left; turning on both. This is a plotly issue, not a mattplotlib issue.")
                elif (self.label == 'top'):
                    self.fig.update_xaxes(showline=True, mirror=True, **self.subplot_row_col)
                    warnings.warn(
                        "Warning: you cannot display the top axis without the bottom; turning on both. This is a plotly issue, not a mattplotlib issue.")

    def set_color(self, set_color_value, setting_default=False):

        self.spine['color'] = set_color_value

        if not setting_default:
            if 'fig' not in dir(self):
                raise ValueError("spines haven't been associated with a set of axes")
            else:
                if self.label == 'bottom':
                    self.fig.update_xaxes(linecolor=set_color_value, **self.subplot_row_col)
                elif self.label == 'left':
                    self.fig.update_yaxes(linecolor=set_color_value, **self.subplot_row_col)
                elif (self.label == 'right'):
                    self.fig.update_yaxes(linecolor=set_color_value, mirror=True, **self.subplot_row_col)
                    warnings.warn(
                        "Warning: you cannot display the right axis without the left; turning on both. This is a plotly issue, not a mattplotlib issue.")
                elif (self.label == 'top'):
                    self.fig.update_xaxes(linecolor=set_color_value, mirror=True, **self.subplot_row_col)
                    warnings.warn(
                        "Warning: you cannot display the top axis without the bottom; turning on both. This is a plotly issue, not a mattplotlib issue.")


    def _attach_spines_to_ax(self, fig, **subplot_row_col):
        self.subplot_row_col = {'row': subplot_row_col.get('row', 1),
                                'col': subplot_row_col.get('col', 1)}
        self.fig = fig
