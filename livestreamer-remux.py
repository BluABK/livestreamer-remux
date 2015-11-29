from subprocess import check_output, CalledProcessError
import os
import sys
import time
import argparse

__author__ = 'BluABK'

if sys.platform == "win32":
    ffmpeg = "ffmpeg.exe"
    ffmpeg_opts = "-n -vcodec copy -acodec copy"
else:
    ffmpeg = "ffmpeg"
    ffmpeg_opts = "-n -vcodec copy -acodec copy"
# TODO: Replace with pyinotify

parser = argparse.ArgumentParser(description='Twitch Local VOD Remux')
#parser.add_argument('-v', '--verbose', action='count', help='enable verbose mode')
parser.add_argument('-p', '--path', type=str, help='Path to vod directory')

args = vars(parser.parse_args())

if args['path']:
    path = str(args['path'])
else:
    path = "."

def file_in_use(filename):
    # TODO: Look for process etc
    f = str(filename)

    # file modified method (quick and dirty)
    initial_stat = os.stat(f).st_mtime
    time.sleep(3)
    if os.stat(f).st_mtime == initial_stat:
        print "%s: not in use" % f
        return False
    return True


def remux(filename, container_in='.ts', container_out='.mkv'):
    outname = str(filename.split(container_in)[0] + container_out)
    try:
        print "REMUX:\t%s --> %s" % (filename, outname)
        check_output(ffmpeg + " -i \"%s\" %s \"%s\"" % (filename, ffmpeg_opts, outname), shell=True)
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
                    #print "rm -rf %s" % f
                    os.rename(f, str(f + '.old'))
        time.sleep(3600)
        exit(0)
