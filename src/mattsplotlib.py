#
#    __   ___
#   /  |_/  / _   /_  /_ __  __ /  __ /_  /  * /__
#  / /|_// / __| /   /  /_  / //  / //   /  / /  /
# /_/   /_/ /_///__ /__ __//_//_ /_//__ /_ / /__/
#                         /
#

import plotly.graph_objects as go
from mattsplotlib_class import mattsplotlib, figure_handle
from plotly.subplots import make_subplots
import numpy as np
import style

global _figure, _new_fig, _stylesheet


_new_fig = True
_stylesheet = 'empty_stylesheet.py'


def figure(*args, **kwargs):
    global _figure, _new_fig
    _figure = mattsplotlib()
    _figure.figure(*args, **kwargs)


def bar(x, y,
        color='steelblue',
        alpha=1,
        edgecolor=None,
        linewidth=0,
        tick_label=None,
        log=False,
        hoverinfo='text',
        hovertext=None,
        **kwargs):
    global _figure, _new_fig

    if _new_fig:
        figure()
        _new_fig = False

    _figure.bar(x, y,
                color=color,
                alpha=alpha,
                edgecolor=edgecolor,
                linewidth=linewidth,
                tick_label=tick_label,
                log=log,
                hoverinfo=hoverinfo,
                hovertext=hovertext,
                **kwargs)

def scatter(x,
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
    global _figure, _new_fig

    if _new_fig:
        figure()
        _new_fig = False

    _figure.scatter(x,
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

def plot(*args, **kwargs):
    global _figure, _new_fig

    if _new_fig:
        figure()
        _new_fig = False

    _figure.plot(*args, **kwargs)

def nxdraw(*args, **kwargs):
    global _figure, _new_fig

    if _new_fig:
        figure()
        _new_fig = False

    _figure.nxdraw(*args, **kwargs)

def text(*args, **kwargs):
    global _figure, _new_fig
    if _new_fig:
        figure()
        _new_fig = False

    _figure.text(*args, **kwargs)

def fill(*args, **kwargs):
    global _figure, _new_fig
    if _new_fig:
        figure()
        _new_fig = False

    _figure.fill(*args, **kwargs)


def xlim(xlower, xupper):
    global _figure, _new_fig
    _figure.set_xlim(xlower, xupper)

def ylim(ylower, yupper):
    global _figure, _new_fig
    _figure.set_ylim(ylower, yupper)

def ylabel(text, color=None, size=None, family=None, **kwargs):
    global _figure, _new_fig
    _figure.set_ylabel(text, color=None, size=None, family=None, **kwargs)

def xlabel(text, color=None, size=None, family=None, **kwargs):
    global _figure, _new_fig
    _figure.set_xlabel(text, color=None, size=None, family=None, **kwargs)

def title(title_text,
          y=0.9,
          color=None,
          size=None,
          family=None,
          **kwargs):
    global _figure, _new_fig
    _figure.set_title(title_text, y=y, color=color, size=size, family=family, **kwargs)

def show():
    global _figure, _new_fig
    _figure.show()
    _new_fig = True

def subplots(*args, **kwargs):
    if len(args) == 0:
        rows = 1
        cols = 1
    elif len(args) == 1:
        rows = args[0]
        cols = 1
    elif len(args) == 2:
        rows = args[0]
        cols = args[1]

    subplot_row_col = {'row': rows, 'col': cols}

    ax = mattsplotlib()
    ax.make_subplots(rows, cols, *args, subplot_row_col=subplot_row_col, **kwargs)
    f = ax.fig
    return f, ax

def subplots(*args, **kwargs):
    if len(args) == 0:
        rows = 1
        cols = 1
    elif len(args) == 1:
        rows = args[0]
        cols = 1
    elif len(args) == 2:
        rows = args[0]
        cols = args[1]

    _kwargs = {}
    _kwargs['shared_yaxes'] = kwargs.get('sharey', False)
    _kwargs['shared_xaxes'] = kwargs.get('sharex', False)

    subplot_figure = make_subplots(rows, cols, subplot_titles=tuple([' '] * (rows * cols)), **_kwargs)
    figure = figure_handle(layout=subplot_figure.layout)
    figure._grid_ref = subplot_figure._grid_ref

    figsize = kwargs.get('figsize', (10, 7))
    subplot_layout = {'rows': rows,
                      'cols': cols,
                      'sharedy': kwargs.get('sharey', False),
                      'sharedx': kwargs.get('sharex', False)}

    return _generate_axes(rows=rows, cols=cols, figure=figure, figsize=figsize, subplot_layout=subplot_layout)


def _generate_axes(rows=None, cols=None, figure=None, figsize=None, subplot_layout=None):
    if rows * cols == 1:
        axes = mattsplotlib(figure=figure,
                            row=1,
                            col=1,
                            figsize=figsize,
                            subplot_layout=subplot_layout,
                            )
    elif rows == 1:
        axes = []
        for c in range(1, cols + 1):
            axes.append(mattsplotlib(figure=figure, row=1, col=c, figsize=figsize, subplot_layout=subplot_layout))
    elif cols == 1:
        axes = []
        for r in range(1, rows + 1):
            axes.append(mattsplotlib(figure=figure, row=r, col=1, figsize=figsize, subplot_layout=subplot_layout))
    else:
        axes = np.zeros((rows, cols))
        for r in range(1, rows + 1):
            for c in range(1, cols + 1):
                axes[rows, cols] = mattsplotlib(figure=figure, row=r, col=c, figsize=figsize, subplot_layout=subplot_layout)

    return figure, axes

def legend(*args, **kwargs):
    global _figure, _new_fig
    _figure.legend(*args, **kwargs)

