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
    "url": "/testConfig/",
    "title": "Test Configuration",
    "name": "TestConfig",
    "group": "Test_Configuration",
    "description": "<p>Calling this route will test the video's configuration. When testing is done, an email will be sent to the project's user. This test consists of running object tracking on a small subset of the video, and producing a video showing the results of the tracking. (Due to the potentially long duration of testing, it is infeasible to return the results as a response to the HTTP request. In order to check the status of the testing and view results, see the Status group of messages.)</p>",
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
    "groupTitle": "Test_Configuration"
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
  }
] });
