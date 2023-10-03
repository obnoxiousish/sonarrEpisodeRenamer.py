import logging

from re import search
from glob import glob
from argparse import ArgumentParser

class hlRenamer:
    def __init__(self):
        self.setupArgParse()
        self.setupLogging()
        
        if self.args.symLink:
            self.logger.info('Using symlinks instead of hardlinks.')
            self.linkType = 'symlink'
            from os import symlink as createLink
            self.createLink = createLink
        else:
            self.logger.info('Using hardlinks.')
            self.linkType = 'hardlink'
            from os import link as createLink
            self.createLink = createLink
        
    def doAllWork(self):
        # Step 0
        self.findSeasonFolders()
        
        # Step 1
        self.constructLinksAndConsiderReleaseGroup()
        
        # Step 3
        if not self.args.dontRemoveReleaseGroup:
            self.createFolderLinks()
        
        # Step 4
        self.searchForEpisodesInSeasonFolders()
        
        
    def findSeasonFolders(self):
        self.seasonFolders = []
        
        filesGrabbed = glob(self.args.glob, root_dir=self.args.directory)
        for self.fileName in filesGrabbed:
            regexResults = search(self.args.regex, self.fileName)
            
            if regexResults:
                self.seasonNumber = regexResults.group()
                self.logger.info(f"Found: {self.fileName} - Season Number: {self.seasonNumber}")
                self.seasonDict = {
                    'seasonNumber': self.seasonNumber,
                    'fileName': self.fileName
                }
                self.seasonFolders.append(self.seasonDict)
            else:
                self.logger.info(f"Skipping: {self.fileName}")
            
    def constructLinksAndConsiderReleaseGroup(self):
        self.directoryList = []
        
        for self.seasonFolderItem in self.seasonFolders:
            self.seasonFolder = self.seasonFolderItem['fileName']
            self.seasonNumber = self.seasonFolderItem['seasonNumber']
            self.logger.info(f'Working on: {self.seasonFolder}')
            
            # Remove release group if true
            if self.args.dontRemoveReleaseGroup:
                self.fullLinkDir = f'{self.args.directory}/{self.seasonFolder}'
                self.logger.info(f'Not removing release group from folder name')
                self.fullLinkDict = {
                    'seasonNumber': self.seasonNumber,
                    'fullLinkDir': self.fullLinkDir
                }
                self.directoryList.append(self.fullLinkDict)
            else:
                self.newSeasonFolder = self.seasonFolder.split(self.args.releaseGroupBeginningBracket)[1].split(self.args.releaseGroupEndingBracket)[1].rstrip().strip()
                self.fullLinkDir = f'{self.args.directory}/{self.newSeasonFolder}'
                self.logger.info(f'Removed release group from folder name & now going to create {self.linkType}: {self.fullLinkDir}')
                self.fullLinkDict = {
                    'seasonNumber': self.seasonNumber,
                    'fullLinkDir': self.fullLinkDir
                }
                self.directoryList.append(self.fullLinkDict)
            
    def createFolderLinks(self):
        for self.linkDirItem in self.directoryList:
            self.linkDir = self.linkDirItem['fullLinkDir']
            self.seasonNumber = self.linkDirItem['seasonNumber']
            
            self.logger.info(f'Creating {self.linkType}: {self.linkDir}')
            self.createLink(self.seasonFolder, self.linkDir)
            self.logger.info(f'Created {self.linkType}: {self.linkDir}')
            
    def searchForEpisodesInSeasonFolders(self):
        for self.linkDirItem in self.directoryList:
            self.linkDir = self.linkDirItem['fullLinkDir']
            self.seasonFolder = self.linkDirItem['seasonNumber']
            
            self.logger.info(f'Searching for episodes in: {self.linkDir}')
            self.episodes = glob(f'*{self.args.fileExtension}', root_dir=self.linkDir)
            
            for self.episode in self.episodes:
                self.logger.info(f'Found episode: {self.episode}')
                
                try:
                    self.episodeNumber = search(r'[0-9][0-9]', self.episode).group()
                    self.episodeName = self.episode.split(' - ')[0]
                    self.newEpisodeName = f'{self.episodeName} - {self.seasonFolder}E{self.episodeNumber}{self.args.fileExtension}'
                    self.fullNewEpisodeDir = f'{self.linkDir}/{self.newEpisodeName}'
                    self.logger.info(f'New episode name: {self.newEpisodeName}')
                except (IndexError, AttributeError):
                    self.logger.info(f'Episode name is in a different format? Skipping: {self.episode}')
                    continue
                
                self.logger.info(f'Official creating {self.linkType}: {self.fullNewEpisodeDir}')
                self.fullOriginalEpisodeDir = f'{self.linkDir}/{self.episode}'
                try:
                    self.createLink(self.fullOriginalEpisodeDir, self.fullNewEpisodeDir)
                except FileExistsError:
                    self.logger.info(f'Episode already exists, skipping: {self.episode}')
                    continue
                self.logger.info(f'Successfully created {self.linkType}: {self.fullNewEpisodeDir}')            
    
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
        
if __name__ == "__main__":
    instance = hlRenamer()
    instance.doAllWork()