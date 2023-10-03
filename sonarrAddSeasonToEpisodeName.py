import logging

from re import search
from glob import glob
from argparse import ArgumentParser
from sharedData import sharedDataInstance

class hlRenamer:
    def __init__(self):
        self.sharedData = sharedDataInstance
        
    def doAllWork(self):
        # Step 0
        self.findSeasonFolders()
        
        # Step 1
        self.constructLinksAndConsiderReleaseGroup()
        
        # Step 3
        if not self.sharedData.args.dontRemoveReleaseGroup:
            self.createFolderLinks()
        
        # Step 4
        self.searchForEpisodesInSeasonFoldersAndCreateTheLinks()
        
    def findSeasonFolders(self):
        self.seasonFolders = []

        filesGrabbed = glob(self.sharedData.args.glob, root_dir=self.sharedData.args.directory)
        for self.fileName in filesGrabbed:
            if regexResults := search(self.sharedData.args.regex, self.fileName):
                self.seasonNumber = regexResults.group()
                self.sharedData.logger.info(f"Found: {self.fileName} - Season Number: {self.seasonNumber}")
                self.seasonDict = {
                    'seasonNumber': self.seasonNumber,
                    'fileName': self.fileName
                }
                self.seasonFolders.append(self.seasonDict)
            else:
                self.sharedData.logger.info(f"Skipping: {self.fileName}")
            
    def constructLinksAndConsiderReleaseGroup(self):
        self.directoryList = []

        for self.seasonFolderItem in self.seasonFolders:
            self.seasonFolder = self.seasonFolderItem['fileName']
            self.seasonNumber = self.seasonFolderItem['seasonNumber']
            self.sharedData.logger.info(f'Working on: {self.seasonFolder}')

            # Remove release group if true
            if self.sharedData.args.dontRemoveReleaseGroup:
                self.fullLinkDir = f'{self.sharedData.args.directory}/{self.seasonFolder}'
                self.sharedData.logger.info('Not removing release group from folder name')
            else:
                self.newSeasonFolder = self.seasonFolder.split(self.sharedData.args.releaseGroupBeginningBracket)[1].split(self.sharedData.args.releaseGroupEndingBracket)[1].rstrip().strip()
                self.fullLinkDir = f'{self.sharedData.args.directory}/{self.newSeasonFolder}'
                self.sharedData.logger.info(f'Removed release group from folder name & now going to create {self.sharedData.linkType}: {self.fullLinkDir}')

            self.fullLinkDict = {
                'seasonNumber': self.seasonNumber,
                'fullLinkDir': self.fullLinkDir
            }
            self.directoryList.append(self.fullLinkDict)
            
    def createFolderLinks(self):
        for self.linkDirItem in self.directoryList:
            self.linkDir = self.linkDirItem['fullLinkDir']
            self.seasonNumber = self.linkDirItem['seasonNumber']
            
            self.sharedData.logger.info(f'Creating {self.sharedData.linkType}: {self.linkDir}')
            self.sharedData.createLink(self.seasonFolder, self.linkDir)
            self.sharedData.logger.info(f'Created {self.sharedData.linkType}: {self.linkDir}')

    def searchForEpisodesInSeasonFoldersAndCreateTheLinks(self):
        for self.linkDirItem in self.directoryList:
            self.linkDir = self.linkDirItem['fullLinkDir']
            self.seasonFolder = self.linkDirItem['seasonNumber']
            
            self.sharedData.logger.info(f'Searching for episodes in: {self.linkDir}')
            self.episodes = glob(f'*{self.sharedData.args.fileExtension}', root_dir=self.linkDir)
            
            for self.episode in self.episodes:
                self.sharedData.logger.info(f'Found episode: {self.episode}')
                
                try:
                    self.episodeNumber = search(r'[0-9][0-9]', self.episode).group()
                    self.episodeName = self.episode.split(' - ')[0]
                    self.newEpisodeName = f'{self.episodeName} - {self.seasonFolder}E{self.episodeNumber}{self.sharedData.args.fileExtension}'
                    self.fullNewEpisodeDir = f'{self.linkDir}/{self.newEpisodeName}'
                    self.sharedData.logger.info(f'New episode name: {self.newEpisodeName}')
                except (IndexError, AttributeError):
                    self.sharedData.logger.info(f'Episode name is in a different format? Skipping: {self.episode}')
                    continue
                
                self.sharedData.logger.info(f'Official creating {self.sharedData.linkType}: {self.fullNewEpisodeDir}')
                self.fullOriginalEpisodeDir = f'{self.linkDir}/{self.episode}'
                try:
                    if self.sharedData.args.createLink:
                        self.sharedData.createLink(self.fullOriginalEpisodeDir, self.fullNewEpisodeDir)
                except FileExistsError:
                    self.sharedData.logger.info(f'Episode already exists, skipping: {self.episode}')
                    continue
                self.sharedData.logger.info(f'Successfully created {self.sharedData.linkType}: {self.fullNewEpisodeDir}')            
                
if __name__ == "__main__":
    instance = hlRenamer()
    instance.doAllWork()