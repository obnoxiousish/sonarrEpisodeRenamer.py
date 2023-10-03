import logging

from re import search
from glob import glob
from argparse import ArgumentParser

class sharedData:
    def __init__(self):
        self.setupArgParse()
        self.setupLogging()
        
        if self.args.symLink:
            self.logger.info('Using symlinks instead of hardlinks.')
            self.linkType = 'symlink'
            from os import symlink as createLink
        else:
            self.logger.info('Using hardlinks.')
            self.linkType = 'hardlink'
            from os import link as createLink

        self.createLink = createLink
    
    def setupLogging(self):
        logFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Logger to file
        fileHandler = logging.FileHandler(self.args.log)
        fileHandler.setLevel(logging.DEBUG)  # Set log level to DEBUG for file logging
        fileHandler.setFormatter(logFormatter)

        # Logger to console
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)  # Set log level to DEBUG for console output
        consoleHandler.setFormatter(logFormatter)

        # Configure the root logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)  # Set overall log level to DEBUG
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
            
    def setupArgParse(self):
        self.parser = ArgumentParser(
            prog='hardLinkRenamer',
            description='Supply an anime directory, fill search season folders for episodes and make it have SXXEXX in name. Most applicable for Sonarr.',
            epilog='Thanks for checking out my script!'
        )
        
        self.parser.add_argument(
            '--fileExtension',
            default='.mkv',
            help='The file extension of the files you want to search for.'
        )
        
        self.parser.add_argument(
            '--symLink',
            default=False,
            action='store_true',
            help="Use this flag to make the script use symlinks instead of hardlinks."
        )
        
        self.parser.add_argument(
            '--createLink',
            default=False,
            action='store_true',
            help="Use this flag to make the script actually run, by default it just shows you what it would do if this flag were on."
        )
        
        self.parser.add_argument(
            '--directory', 
            default='/tenTBHDD/tvShows/Shakugan No Shana',
            help='Directory to search in'
        )
        
        self.parser.add_argument(
            '--glob',
            default='*',
            help='The string being used in glob, can be used to narrow your search.'
        )
        
        self.parser.add_argument(
            '--regex', 
            default=r'S[0-9][0-9]',
            help='The regex to be used when searching for season number in the season folder filenames.'
        )
        
        self.parser.add_argument(
            '--log',
            default='hlRenamer.log',
            help='File name for python logging.'
        )
        
        self.parser.add_argument(
            '--dontRemoveReleaseGroup',
            default=True,
            action='store_false',
            help='Disable removing release group from folder names.'
        )
        
        self.parser.add_argument(
            '--releaseGroupBeginningBracket',
            default='[',
            help='The beginning bracket of the release group. Default=['
        )
        
        self.parser.add_argument(
            '--releaseGroupEndingBracket',
            default=']',
            help='The ending bracket of the release group. Default=]'
        )
        
        
        self.args = self.parser.parse_args()

if __name__ != '__main__':
    sharedDataInstance = sharedData()