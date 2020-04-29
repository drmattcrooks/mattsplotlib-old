import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
import warnings

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

    def figure(self, figsize=(10, 7)):
        self.figsize = figsize
        self.fig = go.Figure(data=(), layout={})

    def bar(self, x, y,
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

        if s is None:
            s = 10
        if c is None:
            c = 'steelblue',
        if cmap is None:
            cmap = 'Blues'
        if alpha is None:
            if max(s) <= 10:
                alpha = 1
            else:
                alpha = 0.5
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


    def _format_axes(self):
        font = self._get_font(color=None, size=None, family=None)
        self.fig.update_xaxes(tickfont=font)
        self.fig.update_yaxes(tickfont=font)
        self.fig.update_xaxes(titlefont=font)
        self.fig.update_yaxes(titlefont=font)

        self.fig.layout.yaxis['gridcolor'] = 'grey'
        self.fig.layout.yaxis['zeroline'] = False
        self.fig.layout.xaxis['gridcolor'] = 'grey'
        self.fig.layout.xaxis['showgrid'] = False
        self.fig.layout.xaxis['zeroline'] = False


    def _get_font(self,
                  color=None,
                  size=None,
                  family=None):
        font = {'color': 'grey',
                'size': 16,
                'family': 'serif'}
        if color is not None:
            font['color'] = color
        if size is not None:
            font['size'] = size
        if family is not None:
            font['family'] = family
        return font

    def set_xlabel(self,
               text,
               color=None,
               size=None,
               family=None,
               **kwargs):
        """Update x-axis title"""
        font = self._get_font(color=color, size=size, family=family)
        self.fig.update_layout(xaxis_title=text)
        self.fig.layout.xaxis.title['font'] = font

    def set_xticks(self,
               xtick_locs,
               xticklabels,
               rotation=0,
               color=None,
               size=None,
               family=None,
               **kwargs):

        """Update x-axis ticks and labels"""
        font = self._get_font(color=color, size=size, family=family)
        self.fig.update_xaxes(tickvals=list(xtick_locs),
                              ticktext=list(xticklabels),
                              tickangle=-rotation,
                              tickfont=font)

    def set_xticklabels(self,
                        xticklabels,
                        rotation=0,
                        color=None,
                        size=None,
                        family=None,
                        **kwargs):

        font = self._get_font(color=color, size=size, family=family)
        self.fig.update_xaxes(ticktext=list(xticklabels),
                              tickangle=-rotation,
                              tickfont=font)


    def set_ylabel(self,
               text,
               color=None,
               size=None,
               family=None,
               **kwargs):
        """Update y-axis title"""
        font = self._get_font(color=color, size=size, family=family)
        self.fig.update_layout(yaxis_title=text)
        self.fig.layout.yaxis.title['font'] = font

    def set_yticks(self,
               ytick_locs,
               yticklabels,
               rotation=0,
               color=None,
               size=None,
               family=None,
               **kwargs):

        "Update y-axis ticks and labels"
        font = self._get_font(color=color, size=size, family=family)
        self.fig.update_xaxes(tickvals=list(ytick_locs),
                              ticktext=list(yticklabels),
                              tickangle=-rotation,
                              tickfont=font)

    def set_yticklabels(self,
                        yticklabels,
                        rotation=0,
                        color=None,
                        size=None,
                        family=None,
                        **kwargs):

        font = self._get_font(color=color, size=size, family=family)
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
              color=None,
              size=None,
              family=None,
              **kwargs):
        "Set a title on the plot"
        font = self._get_font(color=color, size=size, family=family)
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
               handles,
               title=None,
               **kwargs):
        self.fig.update_layout(showlegend=True)
        for i, handle in enumerate(handles):
            if i < len(self.fig.data):
                if handle == '_nolabel_':
                    self.fig.data[i].showlegend = False
                else:
                    self.fig.data[i]['name'] = handle

        if title is not None:
            self.fig.update_layout(legend_title_text=title)


class figure_handle(object):
    def __init__(self, ax):
        self.ax = ax

    def show(self):
        self.ax.show()