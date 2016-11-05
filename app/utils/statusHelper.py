
import Enum
class Status(Enum):
	Uploading = "Uploading video"
	TrackingFeatures = "Tracking features"
	TrackingObjects = "Tracking objects"
	GeneratingVideos = "Generating short videos"
	CombiningVideos = "Combining videos"
	SafetyAnalysis = "Running safety analysis"

class StatusHelper(object):
	def __init__(self):
		self.status_dict = {}

	def set_status(identifier, status):
		self.status_dict[identifier] = status

	def get_status(identifier):
		return self.status_dict[identifier]

sharedStatusHelper = StatusHelper()