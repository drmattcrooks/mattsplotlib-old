import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
import numpy as np
import warnings
import matplotlib

class mattsplotlib():
    def __init__(self):
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

        self.color_iterable = ['steelblue', 'sandybrown', 'forestgreen', 'firebrick']


    def figure(self, figsize=(10, 7)):
        self.figsize = figsize
        self.fig = go.Figure(data=(), layout={})

    def nxdraw(self, *args, **kwargs):
        self._nxdraw(*args, **kwargs)

    def _nxdraw(self, *args, **kwargs):
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

        edge_trace = go_scatter(
            x=xcoords,
            y=ycoords,
            mode='lines',
            line_color = line_color_rgba,
            line_width = linewidth,
            hoverinfo='text',
            hovertext=None,
            showlegend=False)
        if is_3d:
            edge_trace['z'] = zcoords


        cmap = 'Blues'
        if 'cmap' in kwargs:
            cmap = kwargs['cmap']

            if type(cmap) == matplotlib.colors.ListedColormap:
                color_map = cmap.colors
                color_map = [f"rgb{tuple([ci * 256 for ci in c])}" for c in color_map]
                if type(node_colours[0]) == int:
                    node_colours = [color_map[nc] for nc in node_colours]

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
            for color in set(node_colours):
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
                               width = self.figsize[0] * 500 / 7,
                               height = self.figsize[1] * 500 / 7,
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
                    visible=False)))


    def bar(self,
            x,
            y,
            color='steelblue',
            alpha=1,
            edgecolor=None,
            linewidth=0,
            tick_label=None,
            log=False,
            hoverinfo='text',
            hovertext=None,
            **kwargs):
        self._bar(x, y,
                  color=color,
                  alpha=alpha,
                  edgecolor=edgecolor,
                  linewidth=linewidth,
                  tick_label=tick_label,
                  log=log,
                  hoverinfo=hoverinfo,
                  hovertext=hovertext,
                  **kwargs)

    def _bar(self, x, y,
            color='steelblue',
            alpha=1,
            edgecolor=None,
            linewidth=0,
            tick_label=None,
            log=False,
            hoverinfo='text',
            hovertext=None,
            **kwargs):
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

bar_width : float, optional
    The width of the bars. This is automatically converted in
    to a bargap for plotly by subtracting the bar width from
    the distance between x[1] and x[0]

bar_mode : stacked
        """

        if log:
            yaxis_type = 'log'
        else:
            yaxis_type = 'linear'

        if 'figsize' not in dir(self):
            self.figsize = (10, 7)

        if 'xerr' in kwargs:
            warnings.warn('xerr specified - this feature is not support yet and the argument will be ignored')
        if 'yerr' in kwargs:
            warnings.warn('yerr specified - this feature is not support yet and the argument will be ignored')

        x = list(x)
        y = list(y)

        bar_data = {'x': x,
                    'y': y,
                    'type': 'bar',
                    'marker': {'color': color,
                               'opacity': alpha,
                               'line': {'color': edgecolor, 'width': linewidth}},
                    'hoverinfo': hoverinfo,
                    'hovertext': hovertext}

        if 'bar_width' in kwargs:
            if len(x) > 1:
                bargap = x[1] - x[0] - kwargs['bar_width']
            else:
                bargap = 0.1
        else:
            bargap = 0.1

        if 'name' in kwargs:
            bar_data['name'] = kwargs['name']
            self.fig.update_layout(showlegend=True)
        else:
            if not self.fig.layout.showlegend:
                self.fig.update_layout(showlegend=False)

        layout = {'plot_bgcolor': 'rgba(0,0,0,0)',
                  'paper_bgcolor': 'rgba(0,0,0,0)',
                  'width': self.figsize[0] * 500 / 7,
                  'height': self.figsize[1] * 500 / 7,
                  'font': {'color': 'silver'},
                  'xaxis': {'title': 'x',
                            'color': 'grey'},
                  'yaxis': {'title': 'y',
                            'type': yaxis_type,
                            'color': 'grey'},
                  'bargap': bargap,
                  'margin': {'l': 20,
                             'r': 20,
                             'b': 20,
                             't': 50}}

        if 'fig' not in dir(self):
            self.figure()

        data = go.Bar(bar_data)

        self.fig.add_trace(data)
        self.fig.update_layout(layout)

        if tick_label is not None:
            self.fig.layout.xaxis['tickvals'] = list(x)
            self.fig.layout.xaxis['ticktext'] = tick_label

        self._format_axes()
        self.fig.layout.xaxis['showline'] = True

    def scatter(self,
                x,
                y,
                s=None,
                c='steelblue',
                marker=None,
                cmap=None,
                norm=None,
                vmin=None,
                vmax=None,
                alpha=None,
                linewidths=None,
                edgecolors=None,
                hoverinfo='text',
                hovertext=None,
                **kwargs):

        self._scatter(x,
                      y,
                      s=s,
                      c=c,
                      marker=marker,
                      cmap=cmap,
                      norm=norm,
                      vmin=vmin,
                      vmax=vmax,
                      alpha=alpha,
                      linewidths=linewidths,
                      edgecolors=edgecolors,
                      hoverinfo=hoverinfo,
                      hovertext=hovertext,
                      **kwargs)

    def _scatter(self,
                x,
                y,
                s=None,
                c=None,
                marker=None,
                cmap=None,
                norm=None,
                vmin=None,
                vmax=None,
                alpha=None,
                linewidths=0,
                edgecolors=None,
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


        if marker is not None:
            if marker not in self.marker_dict:
                if marker not in SymbolValidator().values:
                    raise warnings.warn(f"marker style {marker} not available, defaulting to 'o'")
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

        if 'name' in kwargs:
            scatter_data['name'] = kwargs['name']
            self.fig.update_layout(showlegend=True)
        else:
            if not self.fig.layout.showlegend:
                self.fig.update_layout(showlegend=False)

        layout = {'plot_bgcolor': 'rgba(0,0,0,0)',
                  'paper_bgcolor': 'rgba(0,0,0,0)',
                  'width': self.figsize[0] * 500 / 7,
                  'height': self.figsize[1] * 500 / 7,
                  'font': {'color': 'silver'},
                  'xaxis': {'title': 'x',
                            'color': 'grey'},
                  'yaxis': {'title': 'y',
                            'color': 'grey'},
                  'margin': {'l': 20,
                             'r': 20,
                             'b': 20,
                             't': 50}}

        if 'fig' not in dir(self):
            self.figure()

        data = go.Scatter(scatter_data)

        self.fig.add_trace(data)
        self.fig.update_layout(layout)
        self._format_axes()
        self.fig.layout.yaxis['showgrid'] = False
        self.fig.layout.yaxis['showline'] = True
        self.fig.layout.xaxis['showline'] = True

        self.fig.update_layout(legend={'itemsizing': 'constant'})

    def _plot(self,
              *args,
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

            x = args[0]
            y = args[1]
            if len(args) > 2:
                linestyle = args[2]
            else:
                linestyle = '-'

            if 'hoverinfo' in kwargs:
                hoverinfo = kwargs['hoverinfo']
            else:
                hoverinfo = 'text'
            hovertext = kwargs.get('hovertext')


            if 'color' in kwargs:
                color = kwargs['color']
            else:
                color = 'steelblue'
            if 'linewidth' in kwargs:
                linewidth = kwargs['linewidth']
            else:
                linewidth = 3

            color_rgba = self._convert_color_to_rgba_str(color, kwargs.get('alpha'))

            mode = 'lines'
            if linestyle == '-':
                dash = None
            elif linestyle == '.':
                dash = 'dot'
            elif linestyle == '--':
                dash = 'dash'
            elif linestyle == '-.':
                dash = 'dashdot'
            elif linestyle == '.-':
                dash = None
                mode = 'markers+lines'

            plot_data = {'x': x,
                         'y': y,
                         'mode': mode,
                         'hoverinfo': hoverinfo,
                         'hovertext': hovertext,
                         'line': {'color': color_rgba,
                                  'width': linewidth,
                                  'dash': dash}
                         }

            if 'name' in kwargs:
                plot_data['name'] = kwargs['name']
                self.fig.update_layout(showlegend=True)
            else:
                if not self.fig.layout.showlegend:
                    self.fig.update_layout(showlegend=False)

            layout = {'plot_bgcolor': 'rgba(0,0,0,0)',
                      'paper_bgcolor': 'rgba(0,0,0,0)',
                      'width': self.figsize[0] * 500 / 7,
                      'height': self.figsize[1] * 500 / 7,
                      'font': {'color': 'silver'},
                      'xaxis': {'title': 'x',
                                'color': 'grey'},
                      'yaxis': {'title': 'y',
                                'color': 'grey'},
                      'margin': {'l': 20,
                                 'r': 20,
                                 'b': 20,
                                 't': 50}}

            if 'fig' not in dir(self):
                self.figure()

            data = go.Scatter(plot_data)
            self.fig.add_trace(data)
            self.fig.update_layout(layout)

            self._format_axes()
            self.fig.layout.yaxis['showgrid'] = False
            self.fig.layout.yaxis['showline'] = True
            self.fig.layout.xaxis['showline'] = True

            self.fig.update_layout(legend={'itemsizing': 'constant'})

    def plot(self,
             *args,
             **kwargs):

        if (len(args) < 2):
            if ('x' not in kwargs) & ('y' not in kwargs):
                raise ValueError(f"2 positional arguments required for plot: x and y. Only {len(args)} given.")
            else:
                if 'df' not in kwargs:
                    raise ValueError("No dataframe given")

                df = kwargs['df']
                if 'color' in kwargs:
                    if kwargs['color'] not in list(df):
                        raise ValueError(f"Column {kwargs['color']} not in dataframe")
                    else:
                        color_col = kwargs['color']
                        list_of_colors = list(df[color_col].drop_duplicates())
                        for iter, cat in enumerate(list_of_colors):
                            df = kwargs['df']
                            x = df.loc[df[color_col] == cat, kwargs['x']].values
                            y = df.loc[df[color_col] == cat, kwargs['y']].values
                            args = (x, y)

                            kwargs['color'] = self.color_iterable[iter]
                            kwargs['name'] = cat

                            self._plot(*args,
                                       **kwargs)
                else:
                    df = kwargs['df']
                    x = df[kwargs['x']].values
                    y = df[kwargs['y']].values
                    args = (x, y)

                    self._plot(*args,
                               **kwargs)


        else:
            self._plot(*args,
                       **kwargs)

    def text(self, *args, **kwargs):
        self._text(*args, **kwargs)

    def _text(self, *args, **kwargs):
        if len(args) == 0:
            raise TypeError("text() missing 3 required positional arguments: 'x', 'y', and 's'")
        elif len(args) == 1:
            raise TypeError("text() missing 2 required positional arguments: 'y', and 's'")
        elif len(args) == 2:
            raise TypeError("text() missing 1 required positional arguments: 's'")
        else:
            x = args[0]
            y = args[1]
            s = args[2]

        horizontalalignment = kwargs.get('horizontalalignment', 'left')
        vertalalignment = kwargs.get('verticalalignment', 'bottom')

        if 'fontweight' in kwargs:
            if kwargs['fontweight'] == 'bold':

                s = f"<b>{s}</b>"

        font = self._extract_font_properties(**kwargs)

        self.fig.add_annotation(
            x=x,
            y=y,
            xref='x',
            yref='y',
            text=s,
            showarrow=False,
            xanchor=horizontalalignment,
            yanchor=vertalalignment,
            font=font
        )

    def _format_axes(self, **kwargs):
        font = self._extract_font_properties(**kwargs)
        self.fig.update_xaxes(tickfont=font)
        self.fig.update_yaxes(tickfont=font)
        self.fig.update_xaxes(titlefont=font)
        self.fig.update_yaxes(titlefont=font)

        self.fig.layout.yaxis['gridcolor'] = 'grey'
        self.fig.layout.yaxis['zeroline'] = False
        self.fig.layout.xaxis['gridcolor'] = 'grey'
        self.fig.layout.xaxis['showgrid'] = False
        self.fig.layout.xaxis['zeroline'] = False



    def set_xlabel(self,
               text,
               **kwargs):
        """Update x-axis title"""
        font = self._extract_font_properties(**kwargs)
        self.fig.update_layout(xaxis_title=text)
        self.fig.layout.xaxis.title['font'] = font

    def set_xticks(self,
               **kwargs):

        """Update x-axis ticks and labels"""
        font = self._extract_font_properties(**kwargs)
        self.fig.update_xaxes(tickvals=list(xtick_locs),
                              tickangle=-rotation,
                              tickfont=font)

    def set_xticklabels(self,
                        xticklabels,
                        rotation=0,
                        **kwargs):

        font = self._extract_font_properties(**kwargs)
        self.fig.update_xaxes(ticktext=list(xticklabels),
                              tickangle=-rotation,
                              tickfont=font)


    def set_ylabel(self,
               text,
               **kwargs):
        """Update y-axis title"""
        font = self._extract_font_properties(**kwargs)
        self.fig.update_layout(yaxis_title=text)
        self.fig.layout.yaxis.title['font'] = font

    def set_yticks(self,
               ytick_locs,
               rotation=0,
               **kwargs):

        "Update y-axis ticks and labels"
        font = self._extract_font_properties(**kwargs)
        self.fig.update_xaxes(tickvals=list(ytick_locs),
                              tickangle=-rotation,
                              tickfont=font)

    def set_yticklabels(self,
                        yticklabels,
                        rotation=0,
                        **kwargs):

        font = self._extract_font_properties(**kwargs)
        self.fig.update_yaxes(ticktext=list(yticklabels),
                              tickangle=-rotation,
                              tickfont=font)

    def set_xlim(self, xlim_lower, xlim_upper, **kwargs):
        "Set lower and upper limits on x axis"
        self.fig.update_layout(xaxis_range=[xlim_lower, xlim_upper])

    def set_ylim(self, ylim_lower, ylim_upper, *args, **kwargs):
        "Set lower and upper limits on y axis"
        if ylim_lower == 0:
            ylim_lower = - 0.01 * ylim_upper
        self.fig.update_layout(yaxis_range=[ylim_lower, ylim_upper * 1.01])

    def show(self):
        if self.fig is not None:
            self.fig.show()
            self.fig = None

    def set_title(self,
              title_text,
              y=0.9,
              **kwargs):
        "Set a title on the plot"
        font = self._extract_font_properties(**kwargs)
        if y > 1:
            y = 0.9
        self.fig.update_layout(title={
            'text': title_text,
            'y': y,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': font})
        self.fig.layout.margin['t'] += 50

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

        if ('loc' not in kwargs):
            None
        else:
            loc = kwargs['loc']
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

    def _extract_font_properties(self, **kwargs):
        self.default_fontsize = 16

        font = {}
        font['color'] = kwargs.get('color', 'grey')
        font['size'] = kwargs.get('fontsize', self.default_fontsize)
        if 'size' in kwargs:
            font['size'] = kwargs['size']
            if 'fontsize' in kwargs:
                warnings.warn("Both 'size' and 'fontsize' given, defaulting to 'size'.")

        font['family'] = kwargs.get('family', 'serif')

        font['size'] = self._convert_relative_text_size(font)

        return font

    def _convert_relative_text_size(self, font):
        default_size = self.default_fontsize
        print(f"size: {font['size']}")
        try:
            font['size'] = float(font['size'])
        except:
            if font['size'] == 'xx-small':
                font['size'] = max(default_size - 6, 2)
            elif font['size'] == 'x-small':
                font['size'] = max(default_size - 4, 2)
            elif font['size'] == 'small':
                font['size'] = max(default_size - 2, 2)
            elif font['size'] == 'large':
                font['size'] = default_size + 2
            elif font['size'] == 'x-large':
                font['size'] = default_size + 4
            elif font['size'] == 'xx-large':
                font['size'] = default_size + 6
            else:
                raise ValueError(f"""font size {font['size']} not recognised: must be an int, float, or one of the following:
                'xx-small'
                'x-small'
                'small'
                'medium'
                'large'
                'x-large'
                'xx-large'
                """)

        return font['size']


    def _get_rgb_color_list(self, rgb_str):
        return [float(c) for c in rgb_str.split('(')[1].split(')')[0].split(', ')]

    def _rgb_to_rgba_tuple(self, rgb_tuple_or_list, alpha):
        return (rgb_tuple_or_list[0], rgb_tuple_or_list[1], rgb_tuple_or_list[2], alpha)

    def _named_color_to_rgb_tuple(self, named_color_str):
        return matplotlib.colors.to_rgb(matplotlib.colors.get_named_colors_mapping()[named_color_str])

    def _named_color_to_rgba_tuple(self, named_color_str, alpha):
        rgb_tuple = self._named_color_to_rgb_tuple(named_color_str)
        return self._rgb_to_rgba_tuple(rgb_tuple, alpha)

    def _rgb_tuple_to_str(self, rgb_tuple):
        return f"rgba{rgb_tuple}"

    def _update_alpha_in_rgb_str(self, rgb_str, alpha):
        rgb_list = self._get_rgb_color_list(rgb_str)
        rgba_tuple = self._rgb_to_rgba_tuple(rgb_list, alpha)
        return self._rgb_tuple_to_str(rgba_tuple)

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
        elif type(color) == tuple:
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



class figure_handle(object):
    def __init__(self, ax):
        self.ax = ax

    def show(self):
        self.ax.show()