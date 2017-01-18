define({ "api": [
  {
    "type": "post",
    "url": "/upload/",
    "title": "Upload Video",
    "name": "UploadVideo",
    "group": "Upload",
    "description": "<p>This route will analyze the provided video, and return the project identifier.</p>",
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
    "version": "0.0.0",
    "filename": "app/handlers/upload.py",
    "groupTitle": "Upload"
  }
] });
