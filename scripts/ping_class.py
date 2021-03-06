from threading import Thread
import subprocess
import datetime
from pydispatch import dispatcher


class PingJob(Thread):

    def __init__(self, obj):
        self.obj = obj
        self.keeprunning = True
        Thread.__init__(self)

    def run(self):
        """Ping devices constantly for troubleshooting"""
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        ping = subprocess.Popen(['ping', self.obj.ip_address, '-t'], shell=False,
                                stdout=subprocess.PIPE, startupinfo=startupinfo)
        while self.keeprunning:
            for line in iter(ping.stdout.readline, ''):
                result = line.rstrip()
                if len(result) < 10:
                    continue
                if result == '':
                    continue
                elif result == '\n':
                    continue
                elif result[:7] == 'Pinging':
                    continue

                elif result.split()[-1] == 'unreachable.' or result == 'Request timed out.':
                    success = 'No'
                    ms_delay = "N/A"
                    data = (self.obj, [datetime.datetime.now(), ms_delay, success])

                elif result.split()[-1][:3] == 'TTL':
                    temp = result.split()[-2]
                    ms_delay = ''.join([str(s) for s in temp if s.isdigit()])
                    success = 'Yes'
                    data = (self.obj, [datetime.datetime.now(), ms_delay, success])

                else:
                    success = 'No'
                    ms_delay = "N/A"
                    data = (self.obj, [datetime.datetime.now(), ms_delay, success])
                if self.keeprunning:
                    dispatcher.send(signal="Incoming Ping", sender=data)
                else:
                    break
            # print 'keeprunnning: ', self.keeprunning
        # print 'attempting kill'
        ping.kill()


def main():
    test = PingJob(None)


if __name__ == "__main__":
    main()
