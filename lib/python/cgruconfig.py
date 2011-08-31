import os
import sys
import time
import xml.parsers.expat

VARS = dict()

class Config:
   def __init__( self, variables = VARS, configfiles = None, Verbose = False):
      self.verbose = Verbose
      self.Vars = variables

      cgrulocation =  os.getenv('CGRU_LOCATION')
      if cgrulocation is None or cgrulocation == '': return

      self.Vars['CGRU_LOCATION'] = cgrulocation

      self.Vars['CONFIGFILE'] = os.path.join( cgrulocation, 'config.xml')
      home = os.getenv('HOME', os.getenv('HOMEPATH'))
      self.Vars['HOME'] = home
      self.Vars['HOME_CGRU'] = os.path.join( home, '.cgru')
      if not os.path.isdir( self.Vars['HOME_CGRU']):
         os.mkdir( self.Vars['HOME_CGRU'])
      self.Vars['HOME_CONFIGFILE'] = os.path.join( self.Vars['HOME_CGRU'], 'config.xml')
      # Create home config file if not preset
      if not os.path.isfile( self.Vars['HOME_CONFIGFILE']):
         cfile = open( self.Vars['HOME_CONFIGFILE'], 'w')
         cfile.write('<!-- Created at ' + time.ctime() + ' -->\n')
         cfile.write('<cgru>\n')
         cfile.write('</cgru>\n')
         cfile.close()

      if configfiles is None:
         configfiles = []
         configfiles.append( os.path.join( cgrulocation, 'config_default.xml'))
         configfiles.append( self.Vars['CONFIGFILE'])
         configfiles.append( self.Vars['HOME_CONFIGFILE'])

      for filename in configfiles:
#         if self.verbose: print 'Trying to open %s' % filename
#         print('Trying to open %s' % filename)
         if os.path.isfile( filename):
            file = open( filename, 'r')
            filedata = file.read()
            file.close()
            parser = xml.parsers.expat.ParserCreate()
            parser.StartElementHandler    = self.parser_start_element
            parser.EndElementHandler      = self.parser_end_element
            parser.CharacterDataHandler   = self.parser_char_data
#            if self.verbose: print 'Parsing %s' % filename
            parser.Parse( filedata)
#            try:
#               parser.Parse( filedata)
#            except xml.parsers.expat.ExpatError as err:
#               print("Error:", xml.parsers.expat.errors.messages[err.code], ': line', err.lineno, ', column', err.offset)

   def parser_start_element( self, name, attrs ):
      self.element_hasdata = False
      if name != 'cgru': self.element = name
      else: self.element = ''

   def parser_end_element( self, name ):
      if self.element == '': return
      if self.element_hasdata == False: self.Vars[self.element] = ''
#      if self.verbose: print '\t' + self.element + ' = "%s"' % self.Vars[self.element]
      self.element = ''

   def parser_char_data( self, data ):
      if self.element == '': return
      self.Vars[self.element] = str(data)
      self.element_hasdata = True

Config()
