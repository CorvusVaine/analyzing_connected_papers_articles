This tiny project allows to analyze a repository containing bib files generated through Connected Papers software (https://www.connectedpapers.com/). 

It is linked to the methodology of the article "Deep learning methods in metagenomics: a systematic review" by Gaspar ROY et al.

Connected Papers is a software computing a graph of Papers from one query article. The list of articles in the graph can be downloaded as a bib file. This project, in compare_connected_papers.py, contains a small number of functions made to analyze a repository of these bib files. It allows to retrieve the list of articles, articles in common and computes a list of directed links between graphs when a graph is pointing to another one. 

These functions can be used in graph.ipynb to compute graphs of articles representing articles and their links, eventually filtered by degree. Note that this book is still a prototype and should soon be updated.

Finally, an additional file, zotero_access.py, offers some tools in Zotero allowing to process a dataset of articles and sort them through tags or filtering them by keywords in abstract.
