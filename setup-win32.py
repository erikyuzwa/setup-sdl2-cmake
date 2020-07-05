# download any necessary SDL libraries and put them
# into an "extern" folder that we've included in
# our FindlSDL2 modules
# only necessesary for win32
import os
import urllib.request
import zipfile

def downloadZip(url, extractedFolderName = None):
    zipFileName = url.rsplit('/', 1)[-1]
    assert zipFileName.endswith('.zip')
    if not extractedFolderName:
        extractedFolderName = zipFileName[:-4]
    if not os.path.exists(extractedFolderName):
        print('Downloading %s' % zipFileName)
        urllib.request.urlretrieve(url, zipFileName)
        zipfile.ZipFile(zipFileName).extractall()
        os.remove(zipFileName)
        assert os.path.exists(extractedFolderName)

externFolder = os.path.normpath(os.path.join(__file__, '../extern'))
os.makedirs(externFolder, exist_ok=True)
os.chdir(externFolder)

# SDL2
downloadZip('https://www.libsdl.org/release/SDL2-devel-2.0.12-VC.zip', 'SDL2-2.0.12')

# SDL2_image
downloadZip('https://www.libsdl.org/projects/SDL_image/release/SDL2_image-devel-2.0.5-VC.zip', 'SDL2_image-2.0.5')

# SDL2_mixer
downloadZip('https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-devel-2.0.4-VC.zip', 'SDL2_mixer-2.0.4')

# SDL2_ttf
downloadZip('https://www.libsdl.org/projects/SDL_ttf/release/SDL2_ttf-devel-2.0.15-VC.zip', 'SDL2_ttf-2.0.15')
