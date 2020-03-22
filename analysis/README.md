## Memonavirus Analysis Scripts

In this directory you'll find all the analysis scripts (both python and js) for ripping through the `/data` folder. Python scripts may require the library `matplotlib`.

## Please document scripts below

* sunburst_vis/
  * memonavirus_infection_graphs.ipynb
    * jupyter notebook containing code that writes out a sunburst visualization image representing the hierarchy of infected users (patient 0 at the center)
  * plot.png
    * example output image
  * memonavirus_infection_graphs.html
    * notebook export for displaying code without jupyter
* trends/
  * infections_per_hour.py
    * Shows the by-hour infection rate
  * cumulative_infections_by_hour.py
    * Shows the total number of infections increased by hour
  * output/
    * Contains all output from the `trends/` folder
* cleanse_ancestry/
  * cleanse_data.py
    * script to cleanse data
  * cleanse_data.ipynb
    * notebook with same code

