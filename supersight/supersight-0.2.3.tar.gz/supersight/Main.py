# coding: utf-8



import io
import os
import shutil
import collections

from itertools import accumulate

from jinja2 import Environment, FileSystemLoader

try :
    import pandas as pd
except :
    pass

class Plots_gatherer(object):
    def __init__(self):
        self.__plot_dict = {}
        
    def add_plot(self, name, plot):
        #perform some checks
        self.__plot_dict[name] = plot.getvalue()
        
    def get_plot(self, name):
        return self.__plot_dict[name]


class PlotObjectType(Exception):
    """A plot object has to be a io.BytesIO object. Super Sight will gather plots/images and save them
    in dedicated folders when the dashboard is rendered."""

class BootstrapLayout(Exception):
    """Each tuple in the layout of a page should have a sum equal to 12. It is a requirement to comply with
    Bootstrap's grid system"""

class Dashboard(object):
    """The Dashboard is the main object. It represents the website at the highest level.
    the add_section method will add a section to the navbar of this dashboard."""
    
    def __init__(self, name = "New Dashboard", directory = ".", noHome = False, HomeName = "Home"):
        
        self.name = name
        self.directory = directory
        self.HomeName = HomeName
        
        self.sections = collections.OrderedDict()
        self.title = "Super Sight is self hostable dashboard to properly report your work"
        self.display = "Welcome to <b>Super Sight !</b>"
        self.display_message = """Super Sight generates a multipage dashboard from a Matplotlib 
        plots collection. It helps data scientists and business analysts reporting their work in a 
        methodical and structured manner. It is lightweight, hackable, written in Python and you can host 
        its static output anywhere (local network, AWS S3 ...)."""
        self.nav_bar_right_side = "Custom information here"
        self.footer = "&copy; SuperSight 2017"
        
        if noHome == False:
            # Add Home Section and Page by default. Add it to the sections dict.
            self.home = Section(name = self.HomeName, isHome = True)
            self.sections[self.HomeName] = self.home
        
    def add_section(self, name):
        self.sections[name] = Section(name)
        
    def __make_skeleton(self, path):
        """This method creates the folder tree which will contain the website."""
        
        self.path = path
        if os.path.exists(os.path.join(self.path, "output", self.name)):
            shutil.rmtree(os.path.join(self.path, "output", self.name))
        
        self.path_folders = os.path.join(self.path, "output", self.name, "site", "static")
        os.makedirs(self.path_folders)
        
        self.path_folders = os.path.join(self.path, "output", self.name, "site", "static", "css")
        os.makedirs(self.path_folders)
        
        self.path_folders = os.path.join(self.path, "output", self.name, "site", "static", "js")
        os.makedirs(self.path_folders)
        
        for key in self.sections:
            self.path_folders = os.path.join(self.path, "output", self.name, "site", key)
            os.makedirs(self.path_folders)
            
    def __copy_static(self, template, output_path):
        """This method takes the files in css and js folders of the template and copy to final folders"""
        
        self.path_static = os.path.join(template, "static", "css")
        for file in os.listdir(self.path_static):
            print(file)
            shutil.copyfile(os.path.join(template, "static", "css", file), 
                            os.path.join(output_path, "output", self.name, "site", "static", "css", file))
            
        self.path_static = os.path.join(template, "static", "js")
        for file in os.listdir(self.path_static):
            print(file)
            shutil.copyfile(os.path.join(template, "static", "js", file), 
                            os.path.join(output_path, "output", self.name, "site", "static", "js", file))
            
    def __create_lists_for_nav_bar(self):
        """This method is called by __create_template_vars_index.
        Once the index is created, self.nav_bar_section_page is available for each page."""
        
        nav_bar_section = []
        nav_bar_section_page = []
        for key in self.sections:
            nav_bar_section.append(key)
            nav_bar_page = []
            for page in self.sections[key].pages:
                nav_bar_page.append(page)
            nav_bar_section_page.append(nav_bar_page)
        
        nav_bar_section_page_len = [len(x) for x in nav_bar_section_page]
        
        self.nav_bar_section_page = nav_bar_section_page # create a variable for later
        
        # nav_bar_page is a list of lists
        return nav_bar_section, nav_bar_section_page, nav_bar_section_page_len 
    
    def __get_layout_of_the_current_page(self, section, page):
        
        layout = self.sections[section].pages[page].layout
        
        return layout
    
    def __get_headings_of_the_current_page(self, section, page):
        
        headings = []
        structure = [len(x) for x in self.sections[section].pages[page].layout]
        for key in self.sections[section].pages[page].elements.keys():
            headings.append(self.sections[section].pages[page].elements[key].heading)
        
        
        headings_sub = []
        for idx, i in enumerate(list(accumulate(structure))):
            if idx == 0:
                headings_sub.append(headings[0:i])
            else :
                headings_sub.append(headings[list(accumulate(structure))[idx - 1]:i])
        
        return headings_sub
    
    def __save_plots_of_the_current_page(self, section, page, output_path):
        """This method saves plots in the appropriate section folder.
        As a consequence two plots cannot have the same name within the same section."""
        
        for key in self.sections[section].pages[page].elements.keys():
            print(section, page, key) # debug print
            
            buf_temp = self.sections[section].pages[page].elements[key].plot_object
            if buf_temp is not None :

                plot_path = os.path.join(output_path, "output", self.name, "site", section, key + ".svg")
                
                
                try :
                    my_file = open(plot_path, "wb")
                    my_file.write(buf_temp)
                    my_file.close()
                except Exception as e:
                    print (e)
                    print ("In {section} and {page}, an element exists without a valid plot object.".format(section = section, page = page))

            
            
        
    def __get_plots_of_the_current_page(self, section, page):
        """This method is similar to __get_headings_of_the_current_page.
        It will organise plots to match the stucture of a page.
        The output will be passed to render to link elements to its path."""
        
        plots = []
        structure = [len(x) for x in self.sections[section].pages[page].layout]
        for key in self.sections[section].pages[page].elements.keys():
            if self.sections[section].pages[page].elements[key].plot_object is None:
                plots.append(None)
            else:
                plots.append(self.sections[section].pages[page].elements[key].name)


        plots_sub = []
        for idx, i in enumerate(list(accumulate(structure))):
            if idx == 0:
                plots_sub.append(plots[0:i])
            else :
                plots_sub.append(plots[list(accumulate(structure))[idx - 1]:i])

        return plots_sub
    
    def __get_above_comment_of_the_current_page(self, section, page):
        comments = []
        structure = [len(x) for x in self.sections[section].pages[page].layout]
        for key in self.sections[section].pages[page].elements.keys():
            comments.append(self.sections[section].pages[page].elements[key].comment_above)
        
        
        comments_sub = []
        for idx, i in enumerate(list(accumulate(structure))):
            if idx == 0:
                comments_sub.append(comments[0:i])
            else :
                comments_sub.append(comments[list(accumulate(structure))[idx - 1]:i])
        
        return comments_sub
    
    def __get_below_comment_of_the_current_page(self, section, page):
        
        comments = []
        structure = [len(x) for x in self.sections[section].pages[page].layout]
        for key in self.sections[section].pages[page].elements.keys():
            comments.append(self.sections[section].pages[page].elements[key].comment_below)
        
        
        comments_sub = []
        for idx, i in enumerate(list(accumulate(structure))):
            if idx == 0:
                comments_sub.append(comments[0:i])
            else :
                comments_sub.append(comments[list(accumulate(structure))[idx - 1]:i])
        
        return comments_sub

    def __get_table_of_the_current_page(self, section, page):
        
        table = []
        structure = [len(x) for x in self.sections[section].pages[page].layout]
        for key in self.sections[section].pages[page].elements.keys():
            table.append(self.sections[section].pages[page].elements[key].table)
        
        
        tables_sub = []
        for idx, i in enumerate(list(accumulate(structure))):
            if idx == 0:
                tables_sub.append(table[0:i])
            else :
                tables_sub.append(table[list(accumulate(structure))[idx - 1]:i])
        
        return tables_sub
            
    def __create_template_vars_index(self):
        """This method will create the dictionnary to be passed
        in the template in order to generate index.html"""
        template_vars = {}
        template_vars["index"] = True
        template_vars["name"] = self.name
        template_vars["title"] = self.title
        template_vars["main_display"] = self.display
        template_vars["display_message"] = self.display_message
        
        template_vars["home_page_name"] = self.HomeName
        template_vars["current_section"] = "Home"
        
        template_vars["index_address"] = "index.html"
        template_vars["address_prefix"] = "./site"
        template_vars["nav_bar_right_side"] = self.nav_bar_right_side
        # Get the number of rows and how elements are organised
        template_vars["layout"] = self.__get_layout_of_the_current_page(self.HomeName, "Home")
        template_vars["headings"] = self.__get_headings_of_the_current_page(self.HomeName, "Home")
        
        
        # Plots, comments and table :
        template_vars["plots"] = self.__get_plots_of_the_current_page(self.HomeName, "Home")
        template_vars["comments_below"] = self.__get_below_comment_of_the_current_page(self.HomeName, "Home")
        template_vars["comments_above"] = self.__get_above_comment_of_the_current_page(self.HomeName, "Home")
        template_vars["tables"] = self.__get_table_of_the_current_page(self.HomeName, "Home")

        # Sections
        template_vars["sections"], template_vars["pages"], template_vars["pages_len"] = self.__create_lists_for_nav_bar()

        # footer
        template_vars["footer"] = self.footer

        #Css and JS
        template_vars["bootstrap_min_css"] = "./site/static/css/bootstrap.min.css"
        template_vars["jumbotron_css"] = "./site/static/css/jumbotron.css"
        template_vars["bootstrap_js"] = "./site/static/js/bootstrap.min.js"
        
        return template_vars
    
    def __create_template_vars(self, section, page):
        """This method will create the dictionnary to be passed
        in the template in order to generate each page"""
        
        template_vars = {}
        template_vars["index"] = False
        
        template_vars["name"] = self.name
        template_vars["title"] = self.title
        template_vars["main_display"] = self.display
        template_vars["display_message"] = self.display_message
        
        template_vars["home_page_name"] = self.HomeName
        template_vars["current_section"] = section
        
        template_vars["index_address"] = "../../index.html"
        template_vars["address_prefix"] = ".."
        template_vars["nav_bar_right_side"] = self.nav_bar_right_side
        # Get the number of rows and how elements are organised
        template_vars["layout"] = self.__get_layout_of_the_current_page(section, page)
        template_vars["headings"] = self.__get_headings_of_the_current_page(section, page)
        
        # Plots, comments and table :
        template_vars["plots"] = self.__get_plots_of_the_current_page(section, page)
        template_vars["comments_below"] = self.__get_below_comment_of_the_current_page(section, page)
        template_vars["comments_above"] = self.__get_above_comment_of_the_current_page(section, page)
        template_vars["tables"] = self.__get_table_of_the_current_page(section, page)

        # Sections
        template_vars["sections"], template_vars["pages"], template_vars["pages_len"] = self.__create_lists_for_nav_bar()

        # footer
        template_vars["footer"] = self.footer

        #Css and JS
        template_vars["bootstrap_min_css"] = "../static/css/bootstrap.min.css"
        template_vars["jumbotron_css"] = "../static/css/jumbotron.css"
        template_vars["bootstrap_js"] = "../static/js/bootstrap.min.js"
        
        return template_vars
    
    def __render_page(self, section, page, template_vars, output_path):
        
        # Plots :
        self.__save_plots_of_the_current_page(section, page, output_path)
        
        # create and save the html file
        
        html_out = self.template_file.render(template_vars)
        self.output = os.path.join(output_path, "output", self.name, "site", section)
        mon_fichier2 = open(os.path.join(self.output, page + '.html'), "w")
        mon_fichier2.write(html_out)
        mon_fichier2.close()
            
    def __render_index(self, template_vars, output_path):
        
        # Plots :
        self.__save_plots_of_the_current_page(self.HomeName, "Home", output_path)
        
        # create and save the html file
        
        html_out = self.template_file.render(template_vars)
        self.output_index = os.path.join(self.output_path, 'output', self.name)
        mon_fichier2 = open(os.path.join(self.output_index,'index.html'), "w")
        mon_fichier2.write(html_out)
        mon_fichier2.close()
        
    
    def render(self, template = 'default_template', output_path = "."):
        
        #Where to find the template. By default the folder is next to the script.
        # Otherwise try a relative path.
        
        ####################################
        self.file_path = os.path.dirname(os.path.realpath(__file__)) # ok dans un script
        # self.file_path = get_ipython().getoutput('pwd')
        # self.file_path = self.file_path[0] # Solution alternative pour jupyter
        ####################################
        self.template = template
        if self.template == 'default_template':
            self.template = os.path.join(self.file_path, self.template)
        
        self.output_path = output_path
        
        self.__make_skeleton(path = self.output_path)
        self.__copy_static(self.template, self.output_path)
        
        self.env = Environment(loader=FileSystemLoader(self.template))
        self.template_file = self.env.get_template("index.html")
        
        
        self.template_vars_index = self.__create_template_vars_index()
        self.__render_index(self.template_vars_index, output_path)
        
        for idx, section in enumerate(self.nav_bar_section_page[1:]):
            for page in section:
                section_name = list(self.sections.keys())
                print("Starting individual page :", section_name[idx+1], page)

                # Check the layout comply to Bootstrap == 12 :
                lay = self.sections[section_name[idx+1]].pages[page].layout
                for i in lay:
                    if sum(i) != 12: raise BootstrapLayout ("Each tuple in the layout of a page should have a sum equal to 12.")

                self.template_vars = self.__create_template_vars(section_name[idx+1], page)
                self.__render_page(section_name[idx+1], page, self.template_vars, output_path)
                
    
    
class Section (object):
    """Sections compose the dashboard. Several sections can be added to the dashboard in order
    to organize your plots logically."""
    
    def __init__(self, name = "New Section", isHome = False):
        self.name = name
        self.isHome = isHome
        self.pages = collections.OrderedDict()
        
        if isHome :
            self.add_page(name = "Home", isHome = True)
          
        
    def add_page(self, name, isHome = False):
        self.pages[name] = Page(name, isHome)

        
class Page (object):
    """Pages compose a section. Several pages can be added to a section in order to
    divide the section in smaller subjects. A simple section can have only one page."""
    
    def __init__(self, name = "New Page", isHome = False):
        self.name = name
        self.isHome = isHome
        
        self.layout = [(6, 6), (6, 6), (6, 6)]
        self.elements = collections.OrderedDict()
    
    def add_element(self, name, plot_object = None, heading = None, comment_below = None, comment_above = None):
        self.elements[name] = Element(name, plot_object, heading, comment_below, comment_above)

class Element (object):
    """Elements are displayed on a page. Theoretically, the number of elements on a page
    should be equal to the number of Bootstrap containers on a page.
    Example : if Page.layout = [(6, 6), (6, 6), (6, 6)], you can have up to six elements.
    if Page.layout = [(12,), (6, 6), (6, 6)] you can have up to five elements.
    Elements are inserted left to right, up to bottom."""
    
    def __init__(self, name = "New Element", plot_object = None, heading = None, comment_below = None, comment_above = None):
        """The ___init___ method offers a way to directly create a plot element.
        To add comments seperate methods will have to be called."""
        #self.element_detail = collections.OrderedDict()
        self.name = name
        #self.element_detail["name"] = self.name
        self.heading = heading

        self.comment_below = comment_below
        self.comment_above = comment_above
        
        self.plot_object = plot_object
        self.table = None

    def add_plot(self, plot_object):
        self.plot = plot_object

    def add_comment_above(self, comment):
        self.comment_above = comment
    
    def add_heading(self, heading):
        self.heading = heading

    def add_comment_below(self, comment):

        self.comment_below = comment
    
    def add_table(self, dataframe):
        """This method stores plain html string."""

        table_string = dataframe.to_html(classes="table table-sm table-hover")
        table_string = table_string.replace("\n", "").replace("<thead>", """<thead class="thead-inverse">""")
        self.table = table_string


