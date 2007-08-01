# Copyright(c) 2005-2007 Angelantonio Valente (y3sman@gmail.com)
# See LICENSE file for details.

""" 
Base classes.

This module defines the classes to use to build a report.

Millimeters is the default measurement.
"""

import copy
import datetime
import decimal

import dataproviders

def mm(*values):
    """
    Returns the given values in millimeters (does nothing, since mm is the default)
    """
    if len(values) == 1:
        return values[0]
    return values

def cm(*values):
    """
    Returns the given values converted in millimeters from centimeters
    """
    if len(values) == 1:
        return values[0] * 10
    return tuple([x * 10 for x in values])

# Supported units
units={
    'mm':mm,
    'cm':cm,
    '':mm,
}

class ReportError(StandardError):
    """
    Exception
    """

class Color(object):
    """
    Object's color
    """

    class ColorMetaClass(type):
        """
        Used to add constants to the class
        """
        
        defaults = {
                  'BLACK': (0, 0, 0),
                  'WHITE': (255, 255, 255),
                  'RED': (255, 0, 0),
                  'GREEN': (0, 255, 0),
                  'BLUE': (0, 0, 255)
                  }
        
        def __new__(cls,classname,bases,classdict):
            c = type.__new__(cls, classname, bases, classdict)
            
            for k, v in cls.defaults.items():
                setattr(c, k, c(*v))
            
            return c
    
    __metaclass__ = ColorMetaClass
    
    def __init__(self, red, green, blue):
        """
        Constructor
        @param red: Red component in decimal 0-255 range
        @param green: Green component in decimal 0-255 range
        @param blue: Blue component in decimal 0-255 range
        """
        
        for x in ("red", "green", "blue"):
            v = locals()[x]
            if v<0 or v>255:
                raise ReportError("Invalid value for %s component: %s (must be in range 0 - 255)"%(x,v))
        
        self.red = red
        self.green = green
        self.blue = blue
        
    def to_hex(self):
        """
        Converts the color values to hex (web) format
        """
        return "#%X%X%X"%(self.red, self.green, self.blue)
    
    @classmethod
    def from_hex(cls, hexvalue):
        """
        Create a color object from an hex-encoded string (eg. #AABBCC)
        """
        #TODO: Implement
        raise NotImplementedError()

    def __str__(self):
        """
        If this is a default colour, returns its name, else the tuple (red, green, blue)
        """
        for k, c in self.__metaclass__.defaults.items():
            if self == Color(*c):
                return "Color.%s"%k
            
        return "(%s, %s, %s)"%(self.red, self.green, self.blue)
    
    def __eq__(self, color):
        return self.red == color.red and self.green == color.green and self.blue == color.blue
    
class Font(object):
    """
    Font object
    @ivar id: Font's identificator (string)
    @ivar face: Font face name. Valid faces are defined by the implementation.
    @ivar size: Font size in points
    @ivar style: A combination of styles flags (ITALIC,BOLD,UNDERLINED)
    """
    ITALIC = 1
    BOLD = 2
    UNDERLINED = 4
    
    fonts = dict()
    font_faces = list()
    
    def __init__(self,id,face,size,style=[]):
        """
        Constructor
        @param id: Font's identificator (string)
        @param face: Font face name. Valid faces are defined by implementation.
        @param size: Font size in points
        @param style: A combination of styles flags (ITALIC, BOLD, UNDERLINED)
        """
        
        if id is None:
            id = "font_%s"%len(self.__class__.fonts)
            
        self.id = id
        
        self.faces = face.split(",")
        self.face = self.faces[0]
                
        self.size = size
        
        self.style = style
        
        self.__class__.fonts[id] = self
        
    def __str__(self):
        return  "Font %s face: %s size %s style %s"%(self.id, self.face, self.size, self.style)
    
class DrawableObject(object):
    """
    Base class for drawable objects. A drawable object knows its size and how to draw itself.
    """
    
    def __init__(self, size, **kwargs):
        """
        Constructor
        @param parent: The parent section
        @param size: Object's size (as a sequence of width, height)
        @param position: Object's position (as a sequence of x, y)
        @param color: Object's foreground color
        @param backcolor: Object's background color
        """
        
        self._size = (0, 0)
        self._position = (0, 0)
        
        self.parent = kwargs.get('parent', None)

        self.size = size
        self.position = kwargs.get('position', (0, 0))
        
        self.color = kwargs.get('color', Color.BLACK)
        self.backcolor = kwargs.get('backcolor', Color.WHITE)
            
    def check_tuple(self, t):
        """
        Returns the two-items iterable t as a touple
        @param t: An object that supports unpacking
        @returns: A Tuple with the two elements of t
        """
        
        w, h = t
        return (w, h)
    
    def set_size(self, size):
        """
        Sets the object's size
        @param size: A two items iterable
        @raise ReportError: Exception raised if the size isn't correct
        """
        
        size = list(self.check_tuple(size))

        if self.parent is not None:
            if self.size[0] + self.x > self.parent.size[0]:
                raise ReportError("Child %s exceed parent's width (parent: %s, child: %s + %s)!"%(self, self.parent.size[0], self.x, self.size[0]))
    
            if self.size[1] + self.y > self.parent.size[1]:
                raise ReportError("Child %s exceed parent's height (parent: %s, child: %s + %s)!"%(self, self.parent.size[1], self.y, self.size[1]))

        self._size = tuple(size)
        
    def get_size(self):
        """
        Returns the object's size
        @returns: A (width, height) tuple
        """
        
        size = list(self._size)
        for i in (0, 1):
            if size[i] == -1 and self.parent is not None:
                size[i] = self.parent.size[i]
        return tuple(size)
    
    def set_position(self, position):
        """
        Sets the object's position
        @param position: The position to set
        """
        
        self._position = self.check_tuple(position)

    def draw(self, renderer, environment = None):
        """
        Ask the renderer to draw ourself
        @param renderer: A renderer object
        @param environment: The environment data
        """
        
        raise NotImplementedError("Please use a subclass!")

    def set_x(self, x):
        self.position = (x, self.position[1])
    
    def set_y(self, y):
        self.position = (self.position[0], y)

    def set_width(self, w):
        self.size = (w, self.height)
        
    def set_height(self, h):
        self.size = (self.width, h)
    
    def __str__(self):
        return "<%s> size (%s, %s), pos (%s, %s)"%(self.__class__.__name__, self.width, self.height, self.x, self.y)
        
    size = property(get_size, set_size, None, """ Object's size """)
    position = property(lambda self: self._position, set_position, None, """ Object's position """)
    width = property(lambda self: self.size[0], set_width, None, """ Object's width """ )
    height = property(lambda self: self.size[1], set_height, None, """ Object's height """ )
    x = property(lambda self: self.position[0], set_x, None, """ Object's x position """)
    y = property(lambda self: self.position[1], set_y, None, """ Object's y position """)
    
class Container(DrawableObject):
    """
    An object that contains one or more children
    """
    
    def __init__(self, size, **kwargs):
        """
        Constructor
        @param size: Object's size
        @keyword default_font: The object's default font.
        """
        
        super(Container, self).__init__(size, **kwargs)
        
        self.children = list()
        
        self.default_font = kwargs.get("default_font", Font("default", "Helvetica", 10))
        
    def add_child(self, position, child):
        """
        Adds a child to this container
        @param position: The child's position
        @param child: The child object. It must expose the "draw" method
        """
        
        if not hasattr(child, 'draw') or not callable(getattr(child, 'draw')): 
            raise ReportError("Child object is not drawable: %s"%child)
        
        x, y = child.check_tuple(position)

        child.parent = self

        if child.size[0] + x > self.size[0]:
            raise ReportError("Child %s exceed parent's width (parent: %s, child: %s + %s)!"%(child, self.size[0], x, child.size[0]))

        if child.size[1] + y > self.size[1]:
            raise ReportError("Child %s exceed parent's height (parent: %s, child: %s + %s)!"%(child, self.size[1], y, child.size[1]))
        
        child.position = position
        self.children.append(child)
            
    def draw(self, renderer, environment = None):
        for child in self.children:
            child.draw(renderer, environment)
            
class Page(DrawableObject):
    """
    Page definition
    """
    
    standard_pages={
                    'A4': (210,297),
                    'Letter': (210, 279),
                    }
    
    user_defined_pages={}
    
    def __init__(self, size = 'A4'):
        """
        Constructor
        @param size: Page size (as a tuple or as a standard page name: eg. A4, Letter)
        """
        self.set_size(size)
        
        self.margins=[0,0,0,0]
        
    def set_size(self, size):
        """
        Sets the page's size
        @param size: A ISO page size name (like A4, Letter, etc.) or a (width, height) tuple
        """
        
        s = None
        try:
            s = self.__class__.standard_pages[size]
        except KeyError:
            try:
                s = self.__class__.user_defined_pages[size]
            except KeyError:
                pass
        
        if s is None:
            try:
                width = s[0]+0
                height = s[1]+0
            except:
                raise
        else:
            width, height = s
            
        self._size = (width, height)
    
    size = property(lambda self: self._size, None, None)
    
    @classmethod
    def add_userdefined_pagesize(cls, name, size):
        """
        Adds an user-defined page size to the pages registry
        @param name: Page size's name
        @param size: (width, height) tuple
        """
        cls.user_defined_pages[name] = size
        
class Picture(DrawableObject):
    """
    An image - TO DEFINE
    """
    
class Text(DrawableObject):
    """
    A Text value, used to display any kind of textual value
    """
    
    ALIGN_LEFT = 0
    ALIGN_CENTER = 1
    ALIGN_RIGHT = 2
    
    def __init__(self, size, **kwargs):
        """
        Constructor
        @param size: The field's size as a tuple of (width, height)
        @keyword font: Object's font
        @keyword value: Object's value (a valid python expression to be evaulated)
        @keyword alignment: one of ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT: Aligns the text in the field
        """
        
        super(Text,self).__init__(size, **kwargs)
        
        self.font = kwargs.get('font', None)
        
        self.value = kwargs.get('value', "")
        
        self.alignment = kwargs.get('alignment', self.__class__.ALIGN_LEFT)
    
    def draw(self, renderer, environment = None):
        if self.font is None:
            self.font = self.parent.default_font
            
        renderer.draw_text(self, environment)
    
    def __str__(self):
        return "Text object: %s"%self.value
    
class Shape(DrawableObject):
    """ Base class for shapes. TO DOCUMENT """
    SOLID = 1

    def __init__(self, size, linewidth = 0.5, linetype = SOLID):
        super(Shape, self).__init__(size)
        
        self.linewidth = linewidth
        self.linetype = linetype
        
class HLine(Shape):
    """ Horizontal line """

    def __init__(self, width = -1, linewidth = 0.2, linetype = Shape.SOLID):
        """
        Constructor
        @param width: Line's width on the page, expressed in millimeters. If -1, the container's width will be used
        @param linewidth: The line's width (defaults to 0.2 millimeters)
        @param linetype: The line's type. By now, only solid lines are supported
        """
        
        super(HLine, self).__init__( (width,linewidth), linewidth, linetype )

    def draw(self, renderer, environment = None):
        renderer.draw_hline(self, environment)
        
class VLine(Shape):
    """ Vertical line """

    def __init__(self, height = -1, linewidth = 0.2, linetype = Shape.SOLID):
        """
        Constructor
        @param height: Line's height on the page, expressed in millimeters. If -1, the container's height will be used
        @param linewidth: The line's width (defaults to 0.2 millimeters)
        @param linetype: The line's type. By now, only solid lines are supported
        """
        super(VLine, self).__init__( (linewidth, height), linewidth, linetype )

    def draw(self, renderer, environment = None):
        renderer.draw_vline(self, environment)
    
class Rect(Shape):
    """ Rectangle """

class Section(Container):
    """ A Report's section """
    
    def __init__(self, parent, size, **kwargs):
        kwargs['parent'] = parent
        super(Section, self).__init__(size, **kwargs)

class Group(object):
    """
    Data groups - NOT IMPLEMENTED
    """
    
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression
        
        self.header = Section(self, (0,0))
        self.footer = Section(self, (0,0))

class Data(object):
    class _Object(object):
        pass
    
    def __init__(self, report):
        self.report = report
        
    def get_data(self):
        """
        Returns valid data
        """
        
        import __builtin__

        # System variables
        system = self.__class__._Object()
        system.page = self.report.pagenum     # Current page number
        system.date = datetime.date.today()

        # User-defined variables
        vars = self.__class__._Object()
        for name, val in self.report.variables.items():
            setattr(vars, name, val.value)

        # Report parameters
        parameters = self.__class__._Object()
        for name, val in self.report.parameters.items():
            setattr(parameters, name, val.value)
            
        # System functions
        funcs = self.__class__._Object()
        # Builds a "safe" functions dict
        valid_names = ('abs', 'bool', 'chr', 'cmp', 'divmod', 'float', 'hash', 
                       'hex', 'int', 'len', 'max', 'min', 'oct', 'ord', 'pow',
                       'range', 'round', 'str', 'sum', 'unichr', 'unicode', 
                       )
        for name in valid_names:
            setattr(funcs, name, getattr(__builtin__, name))

        # Current datasource row
        row = self.report.currentrow
                
        d = dict()
        for n in ('system', 'vars', 'row', 'funcs'):
            d[n] = locals()[n]
            
        return d
        
class Report(object):
    """
    The Report class
    """
    
    def __init__(self, page = Page('A4')):
        
        self.page = page
        
        # Preferred renderer
        self.preferred_renderer = None
        
        # Title band (printed only once per report)
        self.title = Section(self, (-1,0))
        
        # Page header (printed once per page)
        self.header = Section(self, (-1,0))
        
        # Report detail (body)
        self.body = Section(self, (-1,0))
        
        # Page footer (once per page)
        self.footer = Section(self, (-1,0))
        
        # Report summary (printed after report ending)
        self.summary = Section(self, (-1,0))
        
        # Groups of data
        self.groups = list()
        
        # Subreports
        self.subreports = list()
        
        # Variables
        self.variables = dict()
        
        # Parameters
        self.parameters = dict()
        
        # Calculations
        self.calculations = list()
        
        # Report-defined data sources
        self.datasources = dict()
        
        # Fonts
        self.fonts = dict()
    
    def add_variable(self, var):
        self.variables[var.name] = var
    
    def add_parameter(self, par):
        self.parameters[par.name] = par
    
    def add_calculation(self, calc):
        calc.report = self
        self.calculations.append(calc)
    
    def register_font(self, font):
        self.fonts[font.id] = font
        
    def get_font(self, name):
        try:
            return self.fonts[name]
        except KeyError:
            raise ReportError("Unregistered font name: %s"%name)
    
    def get_size(self):
        return self.page.size
    
    size = property(get_size, None, None, """ Report's size is page's size! """)
        
    def process(self, renderer):
        self.pagenum = 0
        newpage = True
        reset_calcs = False
        self.currentrow = None
        footer_drawn = False
        rec_count = 0
        
        environment = Data(self)
        
        y = self.title.y
        
        # Print this only once per page
        self.title.draw(renderer, environment)
        y += self.title.height
        self.header.y = y
        
        # Cycle trough the datasource
        datasource = renderer.maindatasource

        for self.currentrow in datasource:
            rec_count += 1

            if newpage:
                # For each page, print an header
                renderer.start_page()
                self.pagenum += 1

                self.header.draw(renderer, environment)
                y += self.header.height
                self.body.y = y
                newpage = False
                
            footer_drawn = False
                
            # If y position exceeds body's reserved space, draws the footer
            # and starts a new page
            if (y + self.body.height) > self.page.height - self.footer.height:
                # Draws footer
                newpage = True
                self.footer.y = self.page.height - self.footer.height
                
                self.footer.draw(renderer, environment)
                renderer.finalize_page()
                footer_drawn = True
                
                y = 0
                self.header.y = y
                
                # Draws page header
                renderer.start_page()
                self.pagenum += 1

                self.header.draw(renderer, environment)
                y += self.header.height
                self.body.y = y
                newpage = False
                
                reset_calcs = True
                
            # Draws body band
            self.body.draw(renderer, environment)
            y += self.body.height
            self.body.y = y

            if reset_calcs:
                reset_calcs = False
                # Reset page-resetted calcs
                for calc in self.calculations:
                    if calc.reset_at == "page":
                        calc.reset()

            # Execute report's calculations
            for calc in self.calculations:
                calc.execute(renderer, environment)
        
        if not rec_count:
            raise ReportError("No data available!")
        
        if not footer_drawn:
            self.footer.y = self.page.height - self.footer.height
            self.footer.draw(renderer, environment)

        # Draws summary band
        if self.summary.height < self.page.height - self.footer.height - y:
            self.summary.y = y
            self.summary.draw(renderer, environment)
            renderer.finalize_page()
        else:
            # New page
            renderer.finalize_page()
            renderer.start_page()
            self.summary.draw(renderer, environment)
            renderer.finalize_page()
            
            
class Renderer(object):
    """
    Base renderer class
    """

    def render(self, *args, **kwargs):

        # Data sources
        self.datasources = kwargs.get('datasources', None)
        if self.datasources is None:
            if self.report.datasources:
                self.datasources = []
                if "main" in self.report.datasources:
                    self.datasources.append(self.report.datasources['main'])
                    
                for name, ds in self.report.datasources.items():
                    if name != 'main':
                        self.datasources.append(ds)

            
        if not self.datasources:
            self.datasources = [dataproviders.DataProvider([1])]

        # Main datasource
        self.maindatasource = kwargs.get('maindatasource', self.datasources[0])
        
        for ds in self.datasources:
            dargs = {}
            for arg in kwargs:
                if arg in ("conn", "module", "conn_pars"):
                    dargs[arg] = kwargs[arg]
            ds.run(**dargs)
        
    def start_page(self):
        pass
    
    def finalize_page(self):
        pass
    
    def draw_text(self, text, environment = None):
        raise NotImplementedError("Please use a subclass!")

    def draw_text(self, shape, environment = None):
        raise NotImplementedError("Please use a subclass!")

    def draw_text(self, shape, environment = None):
        raise NotImplementedError("Please use a subclass!")
    
    def safe_eval(self, expr, environment):
        """
        Safely evaluates the expression "expr"
        @param expr: The expression to be evaluated
        @param environment: The environment object to use
        @returns: the evaluated value
        @raises: ReportError if the expression cannot be evaluated
        """

        loc = dict()
        if hasattr(environment, "get_data"):
            loc.update(environment.get_data())
        
        glo = dict()
        builtins = dict()
            
        glo['__builtins__'] = builtins

        try:
            val = eval(expr, glo, loc)
        except AttributeError, err:
            e = err.args[0]
            i = e.find(" attribute ")
            i += len(" attribute ")
            msg = "Invalid variable/function name: %s"%e[i:]
            raise ReportError(msg)
        
        return val

class Variable(object):
    """
    This is a report-defined variable.
    """
    
    vartypes={
              'integer': int,
              'string': unicode,
              'decimal': decimal.Decimal,
              'float': float,
              'date': datetime.date
    }
    
    def __init__(self,name,type,value=None):
        """
        Constructor
        @param name: Variable's name
        @param type: Variable's type (one of vartypes strings)
        @param value: Current value, or None
        """
        
        if not type in self.__class__.vartypes:
            raise ReportError("Invalid variable type %s for variable %s"%type,name)
            
        self.name=name
        self.type=type
        try:
            self.value=self.__class__.vartypes[type](value)
        except TypeError:
            self.value=None

class Parameter(Variable):
    """
    A Parameter is a special type of Variable, its initial value is given by the caller.
    """
    pass

class Calculation(object):
    """
    An automatic calculation made on the datasource
    """
    
    def __init__(self, type, variable, value, reset = "end", startvalue = None):
        if not type in ("sum", "avg", "min", "max"):
            raise ReportError("Invalid calculation type: %s"%type)
        
        if not reset in ("end", "page"):
            raise ReportError("Invalid reset value: %s"%reset)
        
        self.type = type
        
        self.variable = variable
        self.value = value
        self.reset_at = reset
        
        self.startvalue = None
        
        if self.startvalue is not None:
            self.value = self.startvalue
    
        self.partial = 0
        self.count = 0
        
        self.report = None
        
    def reset(self):
        if self.startvalue is not None:
            self.partial = self.startvalue
        else:
            self.partial = None
            
        self.count = 0
        
    def execute(self, renderer, environment):
        self.count += 1
        
        if not self.variable in self.report.variables.values():
            raise ReportError("Variable not found:"%self.variable)
        
        val = renderer.safe_eval(self.value, environment)
        if self.partial is None:
            self.partial = val
            
        if self.type == "sum":
            self.partial += val
            self.variable.value = self.partial
        elif self.type == "avg":
            self.partial += val
            self.variable.value = self.partial/self.count
        elif self.type == "min":
            if val < self.partial:
                self.partial = val
            self.variable.value = self.partial
        elif self.type == "max":
            if val > self.partial:
                self.partial = val
            self.variable.value = self.partial
            
            