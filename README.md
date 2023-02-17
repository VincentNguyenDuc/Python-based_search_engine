# A search engine implemented in Python

## Table of Contents

- [A search engine implemented in Python](#a-search-engine-implemented-in-python)
  - [Table of Contents](#table-of-contents)
  - [General Information](#general-information)
  - [Technologies](#technologies)
  - [Set Up](#set-up)
  - [Usage](#usage)

## General Information

- In this project, I will try to implement a simple search engine using python
- The idea of this project followed this [video](https://www.youtube.com/watch?v=cY7pE7vX6MU)

## Technologies

- Python
- Search engine

## Set Up

- Install Pip following this [instruction](https://pip.pypa.io/en/stable/installation/)
- Set up virtual environment following this [instruction](https://docs.python.org/3/library/venv.html)
- Clone [this repository](https://github.com/VincentNguyenDuc/Python-based_search_engine.git) to your working directory
- Install dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

- To install 'pysearch' into your virtual environment run:

```bash
pip install .
```

## Usage

```Python
from pysearch import PySearch
import os

# Create an instance, pointing it to where the data should be stored.
# In this example I will put the data int the current working env
engine = PySearch.PySearch(os.path.join(os.getcwd(), "SearchData"))

# Index some data.
engine.index('email_1', {'text': "Peter,\n\nI'm going to need those TPS reports on my desk first thing tomorrow! And clean up your desk!\n\nLumbergh"})
engine.index('email_2', {'text': 'Everyone,\n\nM-m-m-m-my red stapler has gone missing. H-h-has a-an-anyone seen it?\n\nMilton'})
engine.index('email_3', {'text': "Peter,\n\nYeah, I'm going to need you to come in on Saturday. Don't forget those reports.\n\nLumbergh"})
engine.index('email_4', {'text': 'How do you feel about becoming Management?\n\nThe Bobs'})

# Search on it.
engine.search('Peter')
engine.search('tps report')
```
