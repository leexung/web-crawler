import sys
import launchpad,bugzilla,mantis,pythonbug,debian


def argumentError():
    print "You must input <bts> <crawl> <fromBugnumber> <toBugnumber> or <bts> <update> <date last updated> "

if (sys.argv[2] == "crawl"):
    if len(sys.argv) < 5:
        argumentError()
        exit()
    else:
        if sys.argv[1] == "launchpad":
            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])
                launchpad.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                timeEnd = int(sys.argv[3])
                launchpad.update(timeEnd)
        elif sys.argv[1] == "bugzilla":

            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])

                bugzilla.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                print ("Function update bug will be update in next version")
        elif sys.argv[1] == "mantis":
            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])
                mantis.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                timeEnd = int(sys.argv[3])
                mantis.update(timeEnd)
        elif sys.argv[1] == "debian":
            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])
                debian.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                print ("Function update bug will be update in next version")
        elif sys.argv[1] == "pythonbug":
            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])
                pythonbug.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                timeEnd = int(sys.argv[3])
                pythonbug.update(timeEnd)
else:
    if len(sys.argv) < 4:
        argumentError()
        exit()
    else:
        if sys.argv[1] == "launchpad":
            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])
                launchpad.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                timeEnd = int(sys.argv[3])
                launchpad.update(timeEnd)
        elif sys.argv[1] == "bugzilla":

            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])

                bugzilla.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                print ("Function update bug will be update in next version")
        elif sys.argv[1] == "mantis":
            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])
                mantis.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                timeEnd = int(sys.argv[3])
                mantis.update(timeEnd)
        elif sys.argv[1] == "debian":
            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])
                debian.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                print ("Function update bug will be update in next version")
        elif sys.argv[1] == "pythonbug":
            if sys.argv[2] == "crawl":
                bugIdStart = int(sys.argv[3])
                bugIdEnd = int(sys.argv[4])
                pythonbug.run(bugIdStart,bugIdEnd)
            elif sys.argv[2] == "update":
                timeEnd = int(sys.argv[3])
                pythonbug.update(timeEnd)