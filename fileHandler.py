import glob
import os

from sketch_generator import DIR

DIR = "_recentImgcache_"

# recent generated images
def getRecentGPImages():
    files = glob.glob("%s/*" % (DIR))
    i = 0
    # logic to maintain image file amount to 6
    if len(files) > 6:
        for i in range(len(files) - 6):
            os.remove(files[i])
            i += 1
    updated_files = glob.glob("%s/*" % (DIR))
    if len(updated_files) != 0:
        updated_files.reverse()

    return updated_files
