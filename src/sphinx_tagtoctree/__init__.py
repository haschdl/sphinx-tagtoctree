from os import path
from os import curdir
import re
from sphinx.directives.other import TocTree
from sphinx import addnodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from sphinx_tagtoctree import _version
import boolean

log_prefix = '[TagTocTree]'

def log(message, prefix=log_prefix):
    print('{} {}'.format(prefix, message))

def doctreeresolved_handler(app, doctree, fromdocname):
    # return if the directive has not been used
    # in any document
    if not hasattr(app.env, 'tagtoctree_all'):
         return
    
    # traverse all toctree in the current document
    for toctree in doctree.traverse(addnodes.toctree):        
        #check if `toctree` is a `tagtoctree`
        toctree_info = next(
            (i for i in app.env.tagtoctree_all 
            if i['docname'] == fromdocname 
            and i['lineno'] == toctree.line), None)
        
        # if it's built-in toctree then continue to 
        # the rest of the document
        if not toctree_info:
            continue
        
        fieldname = "".join(app.config.tagtoctree_tag)
        
        filter_values = [v.strip().upper() for v in toctree_info['tag_filter']]
        

        for includefile in toctree_info['includefiles']:
            meta_value = app.env.metadata[includefile][fieldname]                      
            meta_values = [v.strip().upper() for v in meta_value.split(",")]
            
            tag_filter_str = toctree_info['tag_expr']
            if(tag_filter_str != ""): #has precedence over single tag_filter
                algebra = boolean.BooleanAlgebra()
                tag_filter_expr = algebra.parse(tag_filter_str)

                tag_vals_as_expr = [ algebra.parse(tag) for tag in meta_values] 
                for tag_val_expr in tag_vals_as_expr:
                    tag_filter_expr = tag_filter_expr.subs( { tag_val_expr: algebra.TRUE}).simplify()
                if(tag_filter_expr == algebra.TRUE):
                    break;

                if(tag_filter_expr == algebra.TRUE): #the expression evaluates to true for the tags in the current page
                    pass;

            intersects = any( [ (i in meta_values) for i in filter_values])    
            if not intersects:
                fs = toctree.attributes['includefiles']
                es = toctree.attributes['entries'] 
                toctree.attributes['includefiles'] = [ f for f in fs if f.casefold()!=includefile.casefold()] 
                toctree.attributes['entries'] = [e for e in es if e[1].casefold()!=includefile.casefold()]

def setup(app):    
    app.add_directive('tagtoctree', TagTocTree)    
    # adds a new configuration value, default 'tagtoctree'
    # this is the tag users will add to the page headers
    app.add_config_value('tagtoctree_tag','tagtoctree', 'env')
    app.connect('doctree-resolved', doctreeresolved_handler)
    return {'version': _version.__version__}

class TagTocTree(TocTree):
    """
    Directive to notify Sphinx about the hierarchical structure of the docs,
    and to include a table-of-contents like tree in the current document. This
    version filters the entries based a tag ("banana"), or an boolean expression of tags
    ("banana AND orange").
    """    

    option_spec = TocTree.option_spec
    option_spec['tag'] = directives.class_option
    option_spec['tag_expr'] = directives.class_option

    def collect_metadata(self, toctree):
        if not hasattr(self.env, 'tagtoctree_all'):
            self.env.tagtoctree_all = []

        self.env.tagtoctree_all.append({
            'docname': self.env.docname,
            'lineno': self.lineno,
            'tag_filter' : self.options['tag'],
            'tag_expr' : self.options['tag_expr'],
            'includefiles' : toctree[0].children[0].attributes['includefiles'],
        })
        return

    def run(self):
        """
        Sphinx function, called for each instance of
        TagTocTree found across documents.
        """
        toctree =  super().run()
        self.collect_metadata(toctree)        
        return toctree
