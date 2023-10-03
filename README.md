# sonarrEpisodeRenamer.py

# Usage

    PS C:\Users\a\Documents\Git\sonarrEpisodeRenamer.py> python .\sonarrAddSeasonToEpisodeName.py -h
    usage: hardLinkRenamer [-h] [--fileExtension FILEEXTENSION] [--symLink] [--directory DIRECTORY]
                        [--glob GLOB] [--regex REGEX] [--log LOG] [--dontRemoveReleaseGroup]
                        [--releaseGroupBeginningBracket RELEASEGROUPBEGINNINGBRACKET]
                        [--releaseGroupEndingBracket RELEASEGROUPENDINGBRACKET]

    Supply an anime directory, fill search season folders for episodes and make it have SXXEXX in name.
    Most applicable for Sonarr.

    options:
    -h, --help            show this help message and exit
    --fileExtension FILEEXTENSION
                            The file extension of the files you want to search for.
    --symLink             Use this flag to make the script use symlinks instead of hardlinks.
    --directory DIRECTORY
                            Directory to search in
    --glob GLOB           The string being used in glob, can be used to narrow your search.
    --regex REGEX         The regex to be used when searching for season number in the season folder
                            filenames.
    --log LOG             File name for python logging.
    --dontRemoveReleaseGroup
                            Disable removing release group from folder names.
    --releaseGroupBeginningBracket RELEASEGROUPBEGINNINGBRACKET
                            The beginning bracket of the release group. Default=[
    --releaseGroupEndingBracket RELEASEGROUPENDINGBRACKET
                            The ending bracket of the release group. Default=]

    Thanks for checking out my script!