import plotly.graph_objects as go
from mattsplotlib_class import mattsplotlib, figure_handle

global _figure, _new_fig
_new_fig = True


def figure():
    global _figure, _new_fig
    _figure = mattsplotlib()
    _figure.figure()


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
    ax = mattsplotlib()
    ax.figure(*args, **kwargs)
    f = figure_handle(ax)
    return f, ax

def legend(*args, **kwargs):
    global _figure, _new_fig
    _figure.legend(*args, **kwargs)