from Crawler import DownloadReport
from Setting import work_info

if __name__ == '__main__':
    for reportType in work_info['reportType']:
        beginTime =work_info['beginTime']
        endTime =work_info['endTime']
        file_path = work_info['file_path']
        substract_option=work_info['substract_option']

        DownloadReport(reportType, beginTime, endTime, file_path,substract_option)