from subprocess import check_output, Popen, CalledProcessError
import os
import sys
import time

__author__ = 'BluABK'

if sys.platform == "win32":
    ffmpeg = "ffmpeg.exe"
else:
    ffmpeg = "ffmpeg"
path = "X:\\Twitch\\dump\\"
#path = "X:/Twitch/dump/"
# TODO: Replace with pyinotify


def file_in_use(filename):
    # TODO: Look for process etc
    f = str(path + filename)

    # file modified method (quick and dirty)
    initial_stat = os.stat(f).st_mtime
    time.sleep(3)
    if os.stat(f).st_mtime == initial_stat:
        print "%s: not in use" % f
        return False
    return True


def remux(filename, container_in='.ts', container_out='.mkv'):
    outname = filename.split(container_in) + container_out
    try:
        print "REMUX:\t%s --> %s" % (filename, outname)
        check_output(ffmpeg + " -i \"%s\" -vcodec copy -acodec copy \"%s\"" % (filename, outname), shell=True)
    except CalledProcessError:
        return False
    return True


def traverse(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.ts'):
                print f
                file_list.append(os.path.join(root, f))
    return file_list

"""
                state = None
                if os.path.isfile()
                    state =file_in_use(f)
                except Exception:
                    for d in dirs:
                        try:
                            f = d + os.sep + f
                            state = file_in_use(f)
                        except Exception:
                            continue
                if state is not None and state is False:
                    print f
"""

if __name__ == "__main__":
    while 1:
        files = traverse(path)
        print files
        for f in files:
            if file_in_use(f) is False:
                ret = remux(f)
                if ret:
                    print "rm -rf %s" % f
        #time.sleep(5)
        exit(0)
