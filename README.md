# mattsplotlib
matplotlib syntax for plotly

Despite what people think, matplotlib is great! If you think Seaborn is the doggy's doo-das; you do realise that's matplotlib, right?? 
You can plot using Pandas? Yeah that's matplotlib! The defaults in neither of these are good, just like standard matplotlib, 
so if you want to create a nice plot using either of these you stil need to know matplotlib. 

But Matplotlib isn't interactive like Plotly. True. So let's use Plotly? It's not that easy. It's a steep learning curve, despite what they 
claim you can't really save static images, which means it's useless. It's also json based, which is much more difficult to read than setting 
attributes on a class instance. Also, Plotly scans your input dictionaries for parameters/keys that it recognises and overwrites the defaults. 
Problem with that is you don't get errors if you try set the wrong parameter. You can write reams of code in Plotly and it will simply ignore it 
without telling you you're doing anything wrong - very frustrating! Also the documentation - it's next to useless. I would guess that about 20% of 
Plotly is documented. The examples in the documentation are often hundreds of lines of code to demonstrate how to change the colour of a bar chart
and you're expected to find the right line in all that code. That's what stack overflow is for? The problme with python packages that aren't very 
good is that no one uses them which means there isn't a huge community. Plus you get people from Plotly asking for "simple explicit examples of your
problem" which I find too antagonising given the examples they provide in the documentation!

One of the common complaints of matplotlib is you have to write lots of code. I disagree, especially compared to Plotly. If you create a style sheet
in matplotlib then the line `plt.style.use(stylesheet.mplstyle)` will set the majority of your defaults. Plotly doesn't do style sheets so every 
single plot you create has to be built from scratch and the defaults are...not to my taste. Plotly often has multiple commands per feature. If you 
want to remove the yaxis you have to turn off the x gridlines, the y axis, and the x zero line. That's 3 lines for a single command! 

Rant over, enter Mattsplotlib...

# Mattsplotlib

A plotly interface with matplotlib syntax. The aim is to allow you to replace the line `import matplotlib.pyplot as plt` with `import mattsplotlib 
as plt` and get interactive plots. You can add hover text by simple passing in the keyword argument hovertext into each plottling element AND
you can import your favourite matplotlib style sheet to automatically replace all the hideous Plotly defaults.

# Limitations

Ok so I can't do everything. If you want a really niche plot the you're going to have to do that yourself. But the aim is be able to create 
Plotly images using the following matplotlib formula\\
```
import mattsplotlib as mplt
f, ax = mplt.subplots()
ax.plot(x, y)
f.show()
```
