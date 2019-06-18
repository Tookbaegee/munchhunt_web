# API Documentation

There are multiple sections of this API, divided into files for each specific task. All API endpoints will be documented in their respective sub-modules, so travel to those to locate the ones that are desired.

## Algorithms

The algorithms module will contain endpoints with algorithms, for example the recommendation algorithm and others.

## Auth

This contains functions for authentication such as verifying a token, password verification, and token handlers. __These are not meant to be used in API calls.__

## Errors

This contains functions for returning API HTML errors such as 404, 400, 200, etc. __These are not mean to be used in API calls.__

## Restaurants

The restaurants module contains endpoints that relate to restaurant searching. For instance, getting all restaurants, getting the information of a specific restaurant, etc.

## Tokens

This module contains methods that deal with returning a token of a current user. Certain HTTP headers will need to be used.

## Users

This module contains all routes related to registration, and other methods for dealing with user validation. 

# How To Document

## Quick Guide

All documentation is in Markdown (MD) format, and is stored in the folder `docs`.  

Consider the following snippet of Python code, created in the python file `mycode.py`:

```python
def func():
    print("Hello World!")
```

To document, create a file in the directory `docs/mycode/` called `func.md` (yes, create the directory if it does not exist). Note this must be the `docs` folder that is in the `api` module folder.  

Change the python code from above to the following (WITHOUT the square braces around the ::) :

```python
def func():
    """
    ..include[::] docs/mycode/func.md
    """
    print("Hello World!")
```

Now when the docs are auto-generated, that Markdown file will be used for the documentation. 

I made this convention to standardize the way our documentation is created, and it is much easier to edit Markdown files rather than editing Markdown in Python files.

To generalize, documentation should be created in the location: `docs/{module}/{function-name.md}` using a markdown file.

## How to Markdown?

Look in the docs folder to see examples of documentation I have made already. It should be very easy to pick up Markdown, and you might just be able to copy paste then edit previous docs to make new documentation.

## Background

This is the documenting convention:

Python uses the following notation to demonstrate a documentation-related string:

```python
def sample_function()
    """my documentation string"""
    print("Hello World!")
```

