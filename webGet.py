#!/usr/bin/env python
import urllib.request
from urllib import error
import sys
import threading
from time import time
from os import path
import ssl


def html_downloader(url, file_name, all_downloaded_files_info):
    try:
        opener = urllib.request.FancyURLopener({})
        time_start = time()
        connection = opener.open(url)
        content = str(connection.read())
        time_end = time()
        connection.close()
    except (urllib.error.URLError, urllib.error.HTTPError, ssl.CertificateError, OSError, ValueError) as msg:
        print(msg, "for", url)
    else:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
            file.close()
        all_downloaded_files_info[file_name] = {"URL": connection.geturl(),
                                                "HTTP status code": connection.getcode(),
                                                "File": file_name,
                                                "Elapsed time in ms": round((time_end - time_start) * 1000),
                                                "Size in KB": round((path.getsize(file_name) + sys.getsizeof(connection.headers))/1000),
                                                "ThreadId": threading.get_ident()}


def main(argv):
    all_downloaded_files_info = {}
    threads = []
    for i in range(0, len(argv)-1):
        threads.append(threading.Thread(target=html_downloader, args=(argv[i], str(i)+'.html', all_downloaded_files_info,)))
        threads[i].start()
    html_downloader(argv[-1], str((len(argv))-1) + '.html', all_downloaded_files_info)
    for thread in threads:
        thread.join()
    if not len(all_downloaded_files_info):
        print("None of provided URL has been downloaded")
        sys.exit()
    print(all_downloaded_files_info)
    list_of_times_and_sizes = []
    for value in all_downloaded_files_info.values():
        list_of_times_and_sizes.append([value["Elapsed time in ms"], value["Size in KB"]])
    list_of_sum_of_times_and_sizes = [sum(i) for i in zip(*list_of_times_and_sizes)]
    print("Total: ", len(all_downloaded_files_info.keys()), " file(s) ", list_of_sum_of_times_and_sizes[0], "ms ",
          list_of_sum_of_times_and_sizes[1], "KB")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide at least one URL")
    else:
        main(sys.argv[1:])
