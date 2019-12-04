# Python script : generate facet visuals from data to html file
With this script you'll be able to generate a html file containing facet visualization.

You can find the source of facets here :
* [Facets website](https://github.com/PAIR-code/facets)
* [Github repo](https://pair-code.github.io/facets/)


## Install

1. Clone the repo

    `git clone https://github.com/Nathanlauga/script-generate-facet-visual-html.git`


2. Install packages

    `pip install -r requirements.txt`


3. Use the script ! :) 

    `python generate_html_facets.py data/adult.csv --type dive --output output/example-facets-dive.html`
    or
    `python generate_html_facets.py  data/adult.csv --type overview --output output/example-facets-overview.html --target income`


## How it works

```
usage: generate_html_facets.py [-h] [--type TYPE] [--output OUTPUT]
                               [--target TARGET]
                               data

positional arguments:
  data             path to csv data

optional arguments:
  -h, --help       show this help message and exit
  --type TYPE      type of facets generation : dive or overview
  --output OUTPUT  path and file name where the html will be stored
  --target TARGET  target column to split your data for overview
```