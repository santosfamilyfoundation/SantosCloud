
from traffic_cloud_utils.statusHelper import StatusHelper

def cleanup_func():
    print('Cleaning up...')
    StatusHelper.mark_all_failed()
    print('Cleaned up.')

