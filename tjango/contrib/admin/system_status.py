# -*- coding: UTF-8 -*-
'''
    Brief monitoring module for VPS
'''

import psutil
import platform


class PsutilStats(object):

    def loadPlatform(self):
        x = platform.uname()
        return x

    def loadSummaryData(self):
        summary_data = {}
        summary_data['cpu'] = psutil.cpu_percent(interval=None, percpu=False)
        summary_data['memory'] = psutil.virtual_memory().percent
        summary_data['disk'] = psutil.disk_usage('/').percent
        summary_data['virtual'] = psutil.virtual_memory()
        summary_data['net_sent'] = psutil.net_io_counters(
            pernic=False).bytes_sent
        summary_data['net_recv'] = psutil.net_io_counters(
            pernic=False).bytes_recv
        return summary_data

    def getTopProcesses(self, limit=None):
        m = {}
        for x in psutil.get_process_list():
            cpu_time = x.get_cpu_times()[1]
            if not cpu_time:
                continue
            k = x.pid; v = {"pid": x.pid, "name": x.name, "cpu_time": cpu_time}
            m[k] = v
        p = m.items()
        p.sort(key=lambda x: x[1]["cpu_time"], reverse=True)
        return p[0:limit]

    def getProcessDetails(self, pid):
        x = psutil.Process(pid)
        xcuse = """Information about this process is either
        or you lack the proper permissions to view it"""

        try:
            process_details = {}
            process_details['Status'] = str(x.status)
            process_details['Username'] = x.username
            process_details['Terminal'] = x.terminal
            process_details['IO Count'] = x.get_io_counters()
            process_details['CPU Times'] = x.get_cpu_times()
            process_details['Threads'] = x.get_threads()
            process_details['Memory'] = x.get_memory_info()
            process_details['Connections'] = x.get_connections()
        except BaseException:
            process_details = xcuse
        # return x
        return process_details
