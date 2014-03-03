import json
import xml.etree.ElementTree as ET
import codecs
import sys
import re

"""
TODOs: 
 * Preserve xrefs within notebooks
 * Remove contiguous whitespaces within elements like <code> that preserve them.
   (Currently requires manual tweaking in ipynb to fixup.)
 * Add in regex to remove anchor links of the form <a id="..." /> that are xref targets
 * Swap out code tags for pre tags or nbconvert won't render properly. (Should be a 1-1 conversion for block level tags)

 * The biggest TODO is just to rewrite the element_to_string function to use the DOM
   versus resorting to regex hacks
"""

sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

NB = {
 "metadata": {
  "name": ""
 },
 "nbformat": 3,
 "nbformat_minor": 0,
 "worksheets": [
  {
   "cells": [],  
   "metadata": {}
  }
 ]
}

# collect the notebook cells here and dump them into the template
nb_cells = []

def emit_markdown_cell(markdown_lines):
    if type(markdown_lines) == str:
        markdown_lines = [markdown_lines]
    return {   
     "cell_type": "markdown",
     "metadata": {}, 
     "source": markdown_lines
    }

def emit_code_cell(code_lines):
    return {   
     "cell_type": "code",
     "collapsed": False,
     "input": code_lines, 
     "language": "python",
     "metadata": {}, 
     "outputs": []
    }   

def emit_heading_cell(heading, level):
    return {   
     "cell_type": "heading",
     "level": level,
     "metadata": {}, 
     "source": [
      heading
     ]   
    }

# XXX: Need to rewrite this to be recursive so that it definitively handles arbitrarily
# nested trees and allows for more precision in handling various types of elements. For now it uses
# all sorts of hacks to do what it does to get something working.

def element_to_string(element, formatting=None):

    s = element.text or ""
    for sub_element in element:
        s += ET.tostring(sub_element)
    s += (element.tail or "")

    # All sorts of ugly string hacks follow...

    # Remove indexterm anchor tags entirely (attributes from the .tostring
    # call above are serialized out in lexographic order, it appears, so use
    # that to simplify things since this code needs to be rewritten anyway)
    def repl(m): return ""
    pattern = re.compile(r'<a class="indexterm".*?".*?/>', re.DOTALL)
    s = re.sub(pattern, repl, s)

    # Remove xref anchor tags for the time being
    # XXX: replace with ipynb intra-notebook refs
    def repl(m):
        # Capture the final grouping
        full_a, a_txt = m.groups()
        return a_txt
    pattern = re.compile(r'(<a class="xref".*?>(.*?)</a>)', re.DOTALL)
    s = re.sub(pattern, repl, s)

    # And strip out footnote xrefs as well for the time being
    # XXX: replace with ipynb intra-notebook refs
    def repl(m):
        full_a, a_txt, optional_trailing_space = m.groups()
        return "<sup>[{}]{}</sup>".format(a_txt,optional_trailing_space)
    pattern = re.compile(r'(<sup>\[<a.*?class="(?:footnote|para)".*?>(.*?)</a>\]( ?)</sup>)', re.DOTALL)
    s = re.sub(pattern, repl, s)



    # Prepend to images path in img elements
    s = s.replace('src="images', 'src="files/resources/sampler-images/images')

    # Escape # but not in html entities, 
    result = s.strip().replace("#", "\#").replace("&\#", "&#")
    
    # Escape * 
    result = result.replace("*", "\*")
    
    # Also escape _ and *, but not _ in image filenames
    result = result.replace("_", "\_").replace("mswb\_", "mswb_").replace("math\_", "math_")

    if formatting == "programlisting":
        return u"<code>{0}</code>".format(result)
    elif formatting == "note":
        return u"<blockquote><div><strong>Note:</strong></div><p>{0}</blockquote>".format(result[len("<p>"):])

    elif formatting == "sidebar":
        prefix = '<div class="titlepage">'
        return u"<blockquote><div><strong>Sidebar Discussion:</strong></div>{0}{1}</blockquote>".format(prefix, result[len(prefix):])
    else:
        return result

def append_cell(el, content_type, heading_level=None, heading_title=None):

    if content_type == "markdown":
        if el.get("class") in ("note", "sidebar", "programlisting"):
            nb_cells.append(emit_markdown_cell(element_to_string(el, formatting=el.get("class"))))
        else:
            nb_cells.append(emit_markdown_cell(element_to_string(el)))
    elif content_type == "heading":
        if el and not heading_title:
            heading_title = el.get("title")
        if el and not heading_level:
            heading_level = int(el.get("class")[-1])
        nb_cells.append(emit_heading_cell(heading_title, heading_level))
    elif content_type == "code":
        example_code = el.findall("div[@class='example-contents']/div[@class='programlisting']")[0].text
        nb_cells.append(emit_code_cell(example_code.split("\n")))
    else:
        raise Exception("Unknown content_type: " + content_type)

def handleElement(el):

    if el.tag == 'section' and el.get("class") == 'chapter':
        # To be safe, let's assume that only div and p appear at the top and 
        # explicitly handle anything else that might show up

        append_cell(el, "heading", heading_level=1)

        for e in el.findall("*"):
            if e.tag in ("div", "p"):
                handleElement(e)
            else:
                raise Exception("UnhandledTopLevelElement")
        return

    if el.tag == 'p':
        append_cell(el, "markdown")
        return
    
    # Assume it is a div...
    if el.tag != 'div':
        raise Exception("Unexpected element type: " + el.tag)

    elif el.get("class") == "titlepage": 
        pass

    elif el.get("class") in ("footnotes", "itemizedlist", "blockquote"):
        append_cell(el, "markdown")

    elif el.get("class") in ("note", "sidebar", "programlisting"):
        append_cell(el, "markdown")

    elif el.get("class") in ("figure"):
        append_cell(el, "markdown")

    elif el.get("class") in ("example"):

        example_title = el.findall("div[@class='example-title']")[0].text
        example_title = ' '.join(example_title.split())
        append_cell(None, "heading", heading_level=4, heading_title=example_title)

        append_cell(el, "code")

    elif el.get("class") and el.get("class").startswith("sect"):

        append_cell(el, "heading")

        # Again, be explicit about what is handled here by raising for unexpected types...
        for e in el.findall("*"):
            if e.tag in ("div", "p"):
                handleElement(e)
            elif e.tag == "br":
                pass
            else:
                raise Exception("UnhandledTopLevelElement: " + e.tag)


if __name__ == '__main__':

    F = sys.argv[1]

    with codecs.open(F, encoding='utf-8', errors='ignore') as f:

        # Rip out the namespace of the string before processing. Adds too much clutter to the code
        # in exchange for no value at all.
        xml_str = f.read().encode('utf-8').replace('<!DOCTYPE html>', '').replace('<html xmlns="http://www.w3.org/1999/xhtml"', '<html')
        root = ET.fromstring(xml_str)

    ch = root.findall("body/section[@data-type='chapter']")[0]

    handleElement(ch)

    NB['worksheets'][0]['cells'] = nb_cells

    # Can capture stdout. Could just as easily write directly to a file.
    print json.dumps(NB, indent=1)
    print 
