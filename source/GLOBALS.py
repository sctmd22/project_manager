from enum import Enum


class TIME_FORMATS(Enum):
    ISO_TIME_FORMAT = "%H:%M:%S"
    SIMPLE_TIME_FORMAT = "%H:%M"
    DECIMAL_TIME_FORMAT = "%H:%M:%S.%f"

class DATE_FORMATS(Enum):
    ISO_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"          #SQL uses this (but supports many time formats)
    ISO_DATE_FORMAT_U = "%Y-%m-%d %H:%M:%S.%f"
    SIMPLE_DATE_FORMAT = "%Y-%m-%d"                #Returned by HTML date input
    SIMPLE_DATE_FORMAT_T = "%Y-%m-%d %H:%M"
    HTML_DATE_FORMAT_T = "%Y-%m-%dT%H:%M"          #Returned by HTML date and time input



#Dict used to parse the url into readable values for the breadcrumb links
breadCrumbsData = {
    'home':'Home',
    'cylinders':'Cylinders',
    'cubes':'Cubes',
    'prisms':'Prisms',
    'new':'New',
    'delete':'Delete',
}

reportsMenuItem = 'reports_menu'
cylindersMenuLink = 'cylinders_bp'

cylindersPages = [
    {'pageTitle':'Cylinder Reports',        'path':'cylinders',         'nav-item':reportsMenuItem,      'nav-link':cylindersMenuLink},
    {'pageTitle':'New Cylinder Report',     'path':'cylinders/new',     'nav-item':reportsMenuItem,      'nav-link':cylindersMenuLink}

]

reportsMenu = [
    {'menuName':'Cylinders',                'pageTitle':'Cylinder Reports',                 'id':'',    'path':'',    'submenus':None, 'pages':cylindersPages},
    {'menuName':'Grout and Epoxy Cubes',    'pageTitle':'Grout and Epoxy Cube Reports',     'id':'',    'path':'',    'submenus':None, 'pages':None},
    {'menuName':'Shrinkage Prisms',         'pageTitle':'Shrinkage Prism Reports',          'id':'',    'path':'',    'submenus':None, 'pages':None},
]


rootMenu = [
    {'menuName':'Dashboard', 'pageTitle':'Dashboard',       'id':'',    'path':'root',          'submenus':None},
    {'menuName':'Projects',  'pageTitle':'Projects',        'id':'',    'path':'/projects',     'submenus':None},
    {'menuName':'Reports',   'pageTitle':'Reports',         'id':'',    'path':None,            'submenus':reportsMenu},

]
