import os

from openn.models import *

def save_document(attrs={}):
    doc = Document(**attrs)
    doc.full_clean()
    doc.save()
    return doc

def save_image(doc,attrs={}):
    return doc.image_set.create(**attrs)

def save_images(doc,attr_array=[{}]):
    return [ save_image(doc,attrs) for  attrs in attr_array ]

def save_deriv(image,attrs={}):
    return image.derivative_set(**attrs)

def save_derivs(image,attr_array=[{}]):
    return [ save_deriv(image,attrs) for attrs in attr_array ]

def save_image_data(doc,file_list_dict):
    """
    Save image data for a file list dict like this:

    {
      "document": [
        {
          "filename": "data/mscodex1589_wk1_front0001.tif",
          "image_type": "document",
          "derivs": {
            "web": {
              "path": "data/web/0001_0000_web.jpg",
              "bytes": 2218,
              "width": 78,
              "height": 100
            },
            "master": {
              "path": "data/master/0001_0000.tif",
              "bytes": 24912,
              "width": 78,
              "height": 100
            },
            "thumb": {
              "path": "data/thumb/0001_0000_thumb.jpg",
              "bytes": 2218,
              "width": 78,
              "height": 100
            }
          },
          "label": "Front cover"
        },
        {
          "filename": "data/mscodex1589_wk1_front0002.tif",
          "image_type": "document",
          "derivs": {
            "web": {
              "deriv_type": "web",
              "path": "data/web/0001_0001_web.jpg",
              "bytes": 1823,
              "width": 78,
              "height": 100
            },
            "master": {
              "deriv_type": "master",
              "path": "data/master/0001_0001.tif",
              "bytes": 24912,
              "width": 78,
              "height": 100
            },
            "thumb": {
              "deriv_type": "master",
              "path": "data/thumb/0001_0001_thumb.jpg",
              "bytes": 1823,
              "width": 78,
              "height": 100
            }
          },
          "label": "Inside front cover"
        },
        // ...
       ],
      "extra": [
        {
          "image_type": "extra",
          "filename": "data/mscodex1589_test ref1_1.tif"
          "label": "None"
        }
      ]
    }
    """
    for image_type in file_list_dict:
        for image_attrs in file_list_dict.get(image_type):
            attr_copy = dict(image_attrs)
            if 'derivs' in attr_copy:
                del(attr_copy['derivs'])
            image = save_image(doc, attr_copy)
            if 'deriv' in image_attrs:
                save_derivs(image, image_attrs['deriv'].values())
