from os import path
from os import curdir
import re
from sphinx.directives.other import TocTree
from sphinx import addnodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from sphinx_tagtoctree import _version
import boolean
from sphinx.util import logging

logger = logging.getLogger(__name__)

log_prefix = '[TagTocTree]'


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
        tag_filter_str = toctree_info['tag_expr']
        has_filter_expr=False
        algebra:boolean.BooleanAlgebra = None
        
        if(tag_filter_str): #has precedence over single tag_filter    
            try: 
                allowed_in_token = list(toctree_info['allowed_in_token'])
                logger.verbose(f"{log_prefix}  Allowed: {allowed_in_token}")
                algebra = boolean.BooleanAlgebra(allowed_in_token=allowed_in_token)
                algebra.parse(tag_filter_str)
                has_filter_expr=True
            except Exception:
                #TODO which exception
                raise Exception("The filter expression is not valid: " + tag_filter_str)

        for includefile in toctree_info['includefiles']:
            fs = toctree.attributes['includefiles']
            es = toctree.attributes['entries'] 
            meta_value = app.env.metadata[includefile][fieldname]   
            meta_values_case_sensitive = [v.strip() for v in meta_value.split(",")]
            meta_values_upper = [v.upper() for v in meta_values_case_sensitive]
            
            logger.verbose(f"{log_prefix} Processing page '{includefile}' Meta values: {meta_value}")
            
            tag_filter_expr_local = None
            if(has_filter_expr):
                logger.verbose(f"{log_prefix}  Filter expression: {tag_filter_str}")
                tag_filter_expr_local = algebra.parse(tag_filter_str)
                
                tag_vals_as_expr = [ algebra.parse(tag) for tag in meta_values_case_sensitive] 
                
                for tag_val_expr in tag_vals_as_expr:
                    tag_filter_expr_local = tag_filter_expr_local.subs( { tag_val_expr: algebra.TRUE}).simplify()
                    if(tag_filter_expr_local == algebra.TRUE):
                        break;
                
                
                logger.verbose(f"{log_prefix}  Expression after substituting includefile tags (0=page excluded from ToC): '{tag_filter_expr_local}'")
              
                
                if(tag_filter_expr_local == algebra.TRUE): #the expression evaluates to true for the tags in the current page
                    pass;
                else:
                    #now exhaust other Symbols, setting to FALSE (a tag was NOT present in the includefile)
                    remaining_symbols =  tag_filter_expr_local.get_symbols()
                    logger.verbose(f"{log_prefix}  Remaining symbols in include page '{remaining_symbols}'")
                    for symb in remaining_symbols:
                        tag_filter_expr_local = tag_filter_expr_local.subs( { symb : algebra.FALSE}).simplify()
                    
                    logger.verbose(f"{log_prefix}  Expression after substituting remaining symbols (0=page excluded from ToC): '{tag_filter_expr_local}'")
                    
                    #check again
                    if(tag_filter_expr_local == algebra.TRUE): #the expression evaluates to true for the tags in the current page
                        pass;
                    else:
                        # the tags in the current includefile did NOT pass the filter expression, 
                        # so we remove file from tree
                        toctree.attributes['includefiles'] = [ f for f in fs if f.casefold()!=includefile.casefold()] 
                        toctree.attributes['entries'] = [e for e in es if e[1].casefold()!=includefile.casefold()]

            else: # has simple tags, use intersect to see if includefile stays in the toctree
                intersects = any( [ (i in meta_values_upper) for i in filter_values])   
                #this inverted logic REMOVES current `includefile` if NOT intersect
                #very confusing 
                if not intersects:
                    toctree.attributes['includefiles'] = [ f for f in fs if f.casefold()!=includefile.casefold()] 
                    toctree.attributes['entries'] = [e for e in es if e[1].casefold()!=includefile.casefold()]

def setup(app):    
    app.add_directive('tagtoctree', TagTocTree)    
    # adds a new configuration value, default 'tagtoctree'
    # this is the tag users will add to the page headers
    app.add_config_value('tagtoctree_tag','tagtoctree', 'env')
    app.add_config_value('tagtoctree_allowed_in_token', '', 'env')
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
    option_spec['tag_expr'] = directives.unchanged
   

    def collect_metadata(self, toctree):
        if not hasattr(self.env, 'tagtoctree_all'):
            self.env.tagtoctree_all = []

        
        self.env.tagtoctree_all.append({
            'docname': self.env.docname,
            'lineno': self.lineno,
            'tag_filter' : self.options.get('tag',""),
            'tag_expr' : self.options.get('tag_expr',""),
            'allowed_in_token' : self.config['tagtoctree_allowed_in_token'],
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
