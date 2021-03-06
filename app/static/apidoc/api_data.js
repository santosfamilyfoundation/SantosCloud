define({ "api": [
  {
    "type": "post",
    "url": "/analysis/",
    "title": "Analysis",
    "name": "Analysis",
    "version": "0.1.0",
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
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>The email address that should be notified when the analysis is complete.</p>"
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
    "filename": "app/handlers/analysis.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/objectTracking/",
    "title": "Object Tracking",
    "name": "ObjectTracking",
    "version": "0.1.0",
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
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>The email address that should be notified when the object tracking is complete.</p>"
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
    "filename": "app/handlers/objectTracking.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/safetyAnalysis/",
    "title": "Safety Analysis",
    "name": "SafetyAnalysis",
    "version": "0.1.0",
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
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>The email address that should be notified when the safety analysis is complete</p>"
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
    "filename": "app/handlers/safetyAnalysis.py",
    "groupTitle": "Analysis"
  },
  {
    "type": "post",
    "url": "/config/",
    "title": "Configure Project",
    "name": "Configure_Project",
    "version": "0.1.0",
    "group": "Configuration",
    "description": "<p>Calling this route will modify a specified configuration file using values of the provided arguments.</p>",
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
            "type": "Integer",
            "optional": true,
            "field": "max_features_per_frame",
            "description": "<p>This is the maximum number of features to track per frame. If not provided, a value of 1000 will be used. The recommended value for this is 1000 or greater.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "num_displacement_frames",
            "description": "<p>This parameter determines how long features will be tracked. If not provided, a value of 10 will be used. The recommended value for this is 2-15.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "min_feature_displacement",
            "description": "<p>This is the displacement needed to track a feature. If not provided, a value of 0.0001 will be used. The recommended value for this is 0.0001-0.1.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "max_iterations_to_persist",
            "description": "<p>This is the maximum number of iterations that an unmoving feature should persist. If not provided, a value of 200 will be used. The recommended value for this is 10-1000.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "min_feature_frames",
            "description": "<p>This is the minimum number of frames that a feature must persist in order to be considered a feature. If not provided, a value of 15 will be used. The recommended value for this is 10-25.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "max_connection_distance",
            "description": "<p>This is the maximum distance that two features can be apart and still be considered part of the same object. If not provided, a value of 1 will be used.</p>"
          },
          {
            "group": "Parameter",
            "type": "Number",
            "optional": true,
            "field": "max_segmentation_distance",
            "description": "<p>This is the maximum distance that two features that are moving relative to each other can be apart and still be considered part of the same object. If not provided, a value of .7 will be used.</p>"
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
    "filename": "app/handlers/config.py",
    "groupTitle": "Configuration"
  },
  {
    "type": "get",
    "url": "/defaultConfig/",
    "title": "Default Configuration",
    "name": "Default_Configuration",
    "version": "0.1.0",
    "group": "Configuration",
    "description": "<p>Calling this route will return the default values for the configuration files used by the server. This is useful if you want to display the values of the configuration parameters to the user, without hardcoding the values and potentially being incorrect if default values on the server change.</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "max_features_per_frame",
            "description": "<p>This is the maximum number of features to track per frame.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "num_displacement_frames",
            "description": "<p>This parameter determines how long features will be tracked.</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "min_feature_displacement",
            "description": "<p>This is the displacement needed to track a feature.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "max_iterations_to_persist",
            "description": "<p>This is the maximum number of iterations that an unmoving feature should persist.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "min_feature_frames",
            "description": "<p>This is the minimum number of frames that a feature must persist in order to be considered a feature.</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "max_connection_distance",
            "description": "<p>This is the maximum distance that two features can be apart and still be considered part of the same object.</p>"
          },
          {
            "group": "Success 200",
            "type": "Number",
            "optional": false,
            "field": "max_segmentation_distance",
            "description": "<p>This is the maximum distance that two features that are moving relative to each other can be apart and still be considered part of the same object.</p>"
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
    "filename": "app/handlers/defaultConfig.py",
    "groupTitle": "Configuration"
  },
  {
    "type": "get",
    "url": "/homography/",
    "title": "Get Homography",
    "name": "GetHomography",
    "version": "0.1.0",
    "group": "Configuration",
    "description": "<p>Use this route to get the homography calculated during configuration.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project for which to configure the homography.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer[]",
            "optional": false,
            "field": "homography",
            "description": "<p>The API will return an array containing the 3x3 matrix of homography points.</p>"
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
    "filename": "app/handlers/homography.py",
    "groupTitle": "Configuration"
  },
  {
    "type": "get",
    "url": "/testConfig/",
    "title": "Get Test Configuration",
    "name": "GetTestConfig",
    "version": "0.1.0",
    "group": "Configuration",
    "description": "<p>Calling this route will return the video created by testing the video's configuration.</p>",
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
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "File",
            "optional": false,
            "field": "video_mp4",
            "description": "<p>The API will return this generated test video as a video file upon sucess.</p>"
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
    "filename": "app/handlers/testConfig.py",
    "groupTitle": "Configuration"
  },
  {
    "type": "post",
    "url": "/homography/",
    "title": "Post Homography",
    "name": "PostHomography",
    "version": "0.2.0",
    "group": "Configuration",
    "description": "<p>Use this route to upload homography data for a project.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project for which to configure the homography.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "unit_pixel_ratio",
            "description": "<p>The unit_pixel_ratio of the images (ie. 0.05 meters per pixel).</p>"
          },
          {
            "group": "Parameter",
            "type": "JSON",
            "optional": false,
            "field": "aerial_pts",
            "description": "<p>A JSON array containing the coordinates of point clicks on the aerial image as arrays in the form [x_coord, y_coord], where x_coord and y_coord are floats</p>"
          },
          {
            "group": "Parameter",
            "type": "JSON",
            "optional": false,
            "field": "camera_pts",
            "description": "<p>A JSON array containing the coordinates of point clicks on the camera image as arrays in the form [x_coord, y_coord], where x_coord and y_coord are floats</p>"
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
    "filename": "app/handlers/homography.py",
    "groupTitle": "Configuration"
  },
  {
    "type": "post",
    "url": "/testConfig/",
    "title": "Post Test Configuration",
    "name": "PostTestConfig",
    "version": "0.1.0",
    "group": "Configuration",
    "description": "<p>Calling this route will test the video's configuration. This test consists of running object tracking on a small subset of the video, and producing a video showing the results of the tracking. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
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
    "filename": "app/handlers/testConfig.py",
    "groupTitle": "Configuration"
  },
  {
    "type": "get",
    "url": "/highlightVideo/",
    "title": "Get Highlight Video",
    "name": "GetHighlightVideo",
    "version": "0.1.0",
    "group": "Results",
    "description": "<p>Calling this route will get the highlight video created by the hightlightVideo route and returns it in the response body. This route requires the video to be created beforehand.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to create a highlight video for.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "File",
            "optional": false,
            "field": "video_mp4",
            "description": "<p>The API will return the highlight video upon success.</p>"
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
    "filename": "app/handlers/createHighlightVideo.py",
    "groupTitle": "Results"
  },
  {
    "type": "get",
    "url": "/makeReport/",
    "title": "Make Report",
    "name": "MakeReport",
    "version": "0.1.0",
    "group": "Results",
    "description": "<p>Calling this route will create a safety report for a specified project. The report is returned in the response body. This route requires running roadUserCounts and createSpeedDistribution to generate the report images.</p>",
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
            "type": "File",
            "optional": false,
            "field": "report_pdf",
            "description": "<p>The API will return the created report upon success.</p>"
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
    "filename": "app/handlers/makeReport.py",
    "groupTitle": "Results"
  },
  {
    "type": "post",
    "url": "/highlightVideo/",
    "title": "Post Highlight Video",
    "name": "PostHighlightVideo",
    "version": "0.1.0",
    "group": "Results",
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
            "type": "Float",
            "optional": true,
            "field": "ttc_threshold",
            "description": "<p>Threshold for determining whether an interaction is dangerous. Default 1.5 seconds.</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "num_near_misses_to_use",
            "description": "<p>Number of near misses to use in creating the highlight video. If provided a value greater than 10, it will default to 10.</p>"
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
    "filename": "app/handlers/createHighlightVideo.py",
    "groupTitle": "Results"
  },
  {
    "type": "get",
    "url": "/retrieveResults/",
    "title": "Retrieve Results",
    "name": "RetrieveResults",
    "version": "0.1.0",
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
            "type": "File",
            "optional": false,
            "field": "results_zip",
            "description": "<p>The API will return all metadata (Images, Report, etc.) as a compressed archive.</p>"
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
    "filename": "app/handlers/retrieveResults.py",
    "groupTitle": "Results"
  },
  {
    "type": "get",
    "url": "/roadUserCounts/",
    "title": "Road User Counts",
    "name": "RoadUserCounts",
    "version": "0.1.0",
    "group": "Results",
    "description": "<p>Calling this route will create a road user counts image from a specified project. The image will then be sent back in the response body. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand.</p>",
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
            "type": "File",
            "optional": false,
            "field": "image_jpg",
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
    "filename": "app/handlers/roadUserCounts.py",
    "groupTitle": "Results"
  },
  {
    "type": "get",
    "url": "/speedDistribution/",
    "title": "Speed Distribution",
    "name": "SpeedDistribution",
    "version": "0.1.0",
    "group": "Results",
    "description": "<p>Calling this route will create a graph of the speed distribution from a specified project. The image will then be sent back in the response body. This route requires running object tracking on the video beforehand.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to create a speed distribution for.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "File",
            "optional": false,
            "field": "image_jpg",
            "description": "<p>The API will return the created graph upon success.</p>"
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
    "filename": "app/handlers/createSpeedDistribution.py",
    "groupTitle": "Results"
  },
  {
    "type": "get",
    "url": "/turningCounts/",
    "title": "Turning Counts",
    "name": "TurningCounts",
    "version": "0.1.0",
    "group": "Results",
    "description": "<p>Calling this route will create an image detailing the counts of turning motions for a specified project. The image will then be sent back in the response body. This route requires running object tracking on the video, and then running safety analysis on the results of the object tracking beforehand.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>The identifier of the project to create a speed distribution for.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "File",
            "optional": false,
            "field": "image_jpg",
            "description": "<p>The API will return the created graph upon success.</p>"
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
    "filename": "app/handlers/turningCounts.py",
    "groupTitle": "Results"
  },
  {
    "type": "get",
    "url": "/compareSpeeds/",
    "title": "Visualize how speed distributions compare across projects",
    "name": "compareSpeeds",
    "version": "0.1.0",
    "group": "Results",
    "description": "<p>Calling this route will create a graph of comparing the speed distributions of different project video data. The image will then be sent back in the response body. This route requires running object tracking on the video.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "identifier",
            "description": "<p>identifier of the parent project. This is used to decide in which project directory to save the compare speeds graph.</p>"
          },
          {
            "group": "Parameter",
            "type": "JSON",
            "optional": false,
            "field": "identifiers_to_cmp",
            "description": "<p>A json array of the identifiers of the projects of which to compare speeds.</p>"
          },
          {
            "group": "Parameter",
            "type": "JSON",
            "optional": false,
            "field": "labels_to_cmp",
            "description": "<p>A json array of the human readable string text for each of the projects in project_identifiers. These will be used in the legends and axes labels of the graph.</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": true,
            "field": "only_show_85th",
            "description": "<p>Control whether the graph will only compare the 85th percentile speeds. If you are comparing more than 4 projects, it is recommended to set this to True, for visual purposes. Defaults to False.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "File",
            "optional": false,
            "field": "image_jpg",
            "description": "<p>The API will return the created graph upon success.</p>"
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
    "filename": "app/handlers/compareSpeeds.py",
    "groupTitle": "Results"
  },
  {
    "type": "get",
    "url": "/status/",
    "title": "Processing Status",
    "name": "ProcessingStatus",
    "version": "0.1.0",
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
            "type": "Integer",
            "optional": false,
            "field": "upload_homography",
            "description": "<p>The status of homography file uploading.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "configuration_test",
            "description": "<p>The status of the configuration test.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "object_tracking",
            "description": "<p>The status of object tracking.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "safety_analysis",
            "description": "<p>The status of performing safety analysis.</p>"
          },
          {
            "group": "Success 200",
            "type": "Integer",
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
    "filename": "app/handlers/status.py",
    "groupTitle": "Status"
  },
  {
    "type": "post",
    "url": "/uploadVideo/",
    "title": "Upload Video",
    "name": "UploadVideo",
    "version": "0.2.0",
    "group": "Upload",
    "description": "<p>This route will create a new project and upload a video to it.</p>",
    "parameter": {
      "fields": {
        "Parameter": [
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
            "field": "identifier",
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
    "filename": "app/handlers/uploadVideo.py",
    "groupTitle": "Upload"
  }
] });
