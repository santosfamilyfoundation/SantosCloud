define({ "api": [
  {
    "type": "post",
    "url": "/analyze/",
    "title": "Analysis",
    "name": "Analysis",
    "group": "Analysis",
    "description": "<p>Calling this route will perform analysis on the video. When the analysis is done, an email will be sent to the project's user. This test consists of running object tracking on the video, and then running safety analysis on the results of the object tracking. When the analysis is complete, the system will produce a safety report for the intersection. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to test configuration of.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/analysis.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/hightlightVideo/",
    "title": "Hightlight Video",
    "name": "HighlightVideo",
    "group": "Analysis",
    "description": "<p>Calling this route will create a highlight video of dangerous interactions from a specified project. When the video is created, an email will be sent to the project's user. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand. (Due to the potentially long duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to create a highlight video for.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "ttc_threshold",
            "description": "<p>Threshold for determining whether an interaction is dangerous.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "vehicle_only",
            "description": "<p>Flag for specifying only vehicle-vehicle interactions</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/createHightlightVideo.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/makeReport/",
    "title": "Make Report",
    "name": "MakeReport",
    "group": "Analysis",
    "description": "<p>Calling this route will create a safety report for a specified project. When the report is created, an email will be sent to the project's user. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand. (Due to the potentially long duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project for which to create the report.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/makeReport.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/objectTracking/",
    "title": "Object Tracking",
    "name": "ObjectTracking",
    "group": "Analysis",
    "description": "<p>Calling this route will perform object tracking on the video. When the analysis is done, an email will be sent to the project's user. (Due to the potentially long run duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project on which to run object tracking.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/objectTracking.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/roadUserCounts/",
    "title": "Road User Counts",
    "name": "RoadUserCounts",
    "group": "Analysis",
    "description": "<p>Calling this route will create a road user counts image from a specified project. When the image is created, an email will be sent to the project's user. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand. (Due to the potentially long duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to create road user counts for.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/roadUserCounts.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/safetyAnalysis/",
    "title": "Safety Analysis",
    "name": "SafetyAnalysis",
    "group": "Analysis",
    "description": "<p>Calling this route will perform safety analysis on a project that object tracking has already been run on. When the analysis is done, an email will be sent to the project's user. (Due to the potentially long run duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project on which to run safety analysis.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display. (Will return unique error message if object tracking has NOT been run on specified project)</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/safetyAnalysis.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/speedCDF/",
    "title": "Speed CDF",
    "name": "SpeedCDF",
    "group": "Analysis",
    "description": "<p>Calling this route will create a graph of the speed CDF's from a specified project. When the output is created, an email will be sent to the project's user. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand. (Due to the potentially long duration, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to create a speed CDF for.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "ttc_threshold",
            "description": "<p>Threshold for determining whether an interaction is dangerous.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "vehicle_only",
            "description": "<p>Flag for specifying only vehicle-vehicle interactions</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/createSpeedCDF.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/config/",
    "title": "Configure Files",
    "name": "Configure_Files",
    "group": "Configuration",
    "description": "<p>Calling this route will modify a specified configuration file using specified key:value pairs. Provides a way to modify configuration files by changing variables rather than uploading complete files.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project whose configuration files are to be modified.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "filename",
            "description": "<p>The name of the configuration file to be modified</p>"
          },
          {
            "group": "Parameter",
            "type": "Dictionary",
            "optional": false,
            "field": "config_data",
            "description": "<p>A dictionary of key:value pairs containing the configuration variables to be modified.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/config.py",
    "groupTitle": "Configuration"
  },
  {
    "type": "post",
    "url": "/testConfig/",
    "title": "Test Configuration",
    "name": "TestConfig",
    "group": "Configuration",
    "description": "<p>Calling this route will test the video's configuration. When testing is done, an email will be sent to the project's user. This test consists of running object tracking on a small subset of the video, and producing a video showing the results of the tracking. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "test_flag",
            "description": "<p>Flag to determine whether feature tracking or object tracking will be tested.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to test configuration of.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "frame_start",
            "description": "<p>The frame number to start the configuration test at. If no frame_start is provided, the configuration test will start at the beginning of the video.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "num_frames",
            "description": "<p>The number of frames to analyze. To keep configuration testing short, this parameter must be less than 200. If no num_frames is provided, a default value of 100 will be used.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/testConfig.py",
    "groupTitle": "Configuration"
  },
  {
    "type": "get",
    "url": "/retrieveResults/",
    "title": "Retrieve Results",
    "name": "RetrieveResults",
    "group": "Results",
    "description": "<p>This route will retrieve any metadata associated with the project. This includes test video files and safety analysis results.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to retrieve results from.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "files",
            "description": "<p>The API will return all metadata since last retrieval as a compressed archive.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/retrieveResults.py",
    "groupTitle": "Results"
  },
  {
    "type": "post",
    "url": "/status/",
    "title": "Processing Status",
    "name": "ProcessingStatus",
    "group": "Status",
    "description": "<p>Calling this route will return the current status of any long-running processing that your project can perform, is performing or has performed. It returns a field for each possible long-running process whose value can be 0, 1 or 2. A status of 0 for a given field means that that type of processing has not been run on this project. A status of 1 means that that type of processing is currently running for this process. A status of 2 means that the type of processing has been completed for this project. You can poll this endpoint in order to know the status of processing so that you may call the next API call, such as returning results or performing subsequent analysis.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project on which to return status information.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "upload_video",
            "description": "<p>The status of the video uploading.</p>"
          },
          {
            "group": "Success 200",
            "optional": false,
            "field": "upload_homography",
            "description": "<p>The status of homography file uploading.</p>"
          },
          {
            "group": "Success 200",
            "optional": false,
            "field": "configuration_test",
            "description": "<p>The status of the configuration test.</p>"
          },
          {
            "group": "Success 200",
            "optional": false,
            "field": "feature_tracking",
            "description": "<p>The status of feature tracking.</p>"
          },
          {
            "group": "Success 200",
            "optional": false,
            "field": "object_tracking",
            "description": "<p>The status of object tracking.</p>"
          },
          {
            "group": "Success 200",
            "optional": false,
            "field": "safety_analysis",
            "description": "<p>The status of performing safety analysis.</p>"
          },
          {
            "group": "Success 200",
            "optional": false,
            "field": "highlight_video",
            "description": "<p>The status of creating the highlight video.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display. (Will return unique error message if object tracking has NOT been run on specified project)</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/status.py",
    "groupTitle": "Status"
  },
  {
    "type": "post",
    "url": "/uploadHomography/",
    "title": "Upload Homography",
    "name": "UploadHomography",
    "group": "Upload",
    "description": "<p>Use this route to upload homography files for a project.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to upload files to.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "homography/aerialpng",
            "description": "<p>An aerial photo of the intersection.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "homography/camerapng",
            "description": "<p>A screenshot of the intersection from the video.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "homography/homographytxt",
            "description": "<p>The homography text file to use.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "status_code",
            "description": "<p>The API will return a status code of 200 upon success.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/uploadHomography.py",
    "groupTitle": "Upload"
  },
  {
    "type": "post",
    "url": "/upload/",
    "title": "Upload Video",
    "name": "UploadVideo",
    "group": "Upload",
    "description": "<p>This route will upload files to a project (and create a new project if an old one is not specified). You may provide a project identifier if you would like to update the files from an old project. If you provide a project identifier for an old project, all of the parameters are optional. If you are creating a new project, all parameters are required. This route will always return a dictionary containing the project identifier.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>The email to notify when analysis is done.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "identifier",
            "description": "<p>The identifier of the project to update the file of. If no identifier is provided, a new project will be created, and the identifier will be returned in the response.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "homography/aerialpng",
            "description": "<p>An aerial photo of the intersection.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "homography/camerapng",
            "description": "<p>A screenshot of the intersection from the video.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "homography/homographytxt",
            "description": "<p>The homography text file to use.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "project_namecfg",
            "description": "<p>The project name configuration file.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "trackingcfg",
            "description": "<p>The tracking configuration file.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "temp/test/test_object/object_trackingcfg",
            "description": "<p>The object tracking configuration file.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "temp/test/test_feature/feature_trackingcfg",
            "description": "<p>The feature tracking configuration file.</p>"
          },
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "video",
            "description": "<p>The video file to analyze. This can have any file extension.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "project_identifier",
            "description": "<p>The project identifier. This will be used to reference the project in all other requests.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/upload.py",
    "groupTitle": "Upload"
  },
  {
    "type": "post",
    "url": "/uploadVideo/",
    "title": "Upload Video",
    "name": "UploadVideo",
    "group": "Upload",
    "description": "<p>This route will upload a video to a project (and create a new project if an old one is not specified)</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "video",
            "description": "<p>The video file to analyze. This can have any file extension.</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "identifier",
            "description": "<p>The identifier of the project to update the video of. If no identifier is provided, a new project will be created, and the identifier will be returned in the response.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "project_identifier",
            "description": "<p>The project identifier. This will be used to reference the project in all other requests.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "error_message",
            "description": "<p>The error message to display.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "app/handlers/uploadVideo.py",
    "groupTitle": "Upload"
  }
] });