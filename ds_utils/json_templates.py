import json, copy
import numpy as np
true=True


via_filename_template =  {
                            "filename": "_.jpg",
                            "size": 0,
                            "regions": [],
                            "file_attributes": {
                                "caption": "",
                                "public_domain": "no",
                                "image_url": ""
                            }
                        }
region_template = {
            "shape_attributes": {
                "name": "polygon",
                "all_points_x": [],
                "all_points_y": []
            },
            "region_attributes": {
                "call": "",
                "call_type": "",
                "counter_type":"unknown"
            }
}


via_project_TEMPLATE = {"_via_settings": {
                        "ui": {
                            "annotation_editor_height": 25,
                            "annotation_editor_fontsize": 0.8,
                            "leftsidebar_width": 18,
                            "image_grid": {
                                "img_height": 80,
                                "rshape_fill": "none",
                                "rshape_fill_opacity": 0.3,
                                "rshape_stroke": "yellow",
                                "rshape_stroke_width": 2,
                                "show_region_shape": true,
                                "show_image_policy": "all"
                            },
                            "image": {
                                "region_label": "call",
                                "region_label_font": "10px Sans",
                                "on_image_annotation_editor_placement": "NEAR_REGION"
                            }
                        },
                        "core": {
                            "buffer_size": "18",
                            "filepath": {
                                "C:\\Users\\Public\\Segmentation\\seg-countertops\\annotationsWithImages/": 1
                            },
                            "default_filepath": "C:\\Users\\Public\\Segmentation\\seg-countertops\\annotationsWithImages/"
                        },
                        "project": {
                            "name": "kitchencounter_labeler_via_iteration1"
                        }
                    },
                    "_via_img_metadata": {}
}

def Make_via_attributes_template():
    return {
    "region": {
        "call_type": {
            "type": "radio",
            "description": "Type of call",
            "options": {
                "train":"",
                "eval":"",
                "eval_correct":"",
                "unknown": ""
            },
            "default_options": {
                "train": true
            }
        },
        "call": {
            "type": "radio",
            "description": "Category of object",
            "options": {
                "counter_top": "",
                "sink": "",
                "floor": "",
                "stove": "",
                "fridge": "",
                "unknown": ""
            },
            "default_options": {"unknown": true}
        },
        "counter_type": {
            "type": "radio",
            "description": "only for counter calls",
            "options": {
                "quartz": "",
                "butcherblock": "",
                "formica": "",
                "granite": "",
                "unknown":""
            },
            "default_options": {"unknown": true}
    }
    },
    "file": {
        "caption": {
            "type": "text",
            "description": "",
            "default_value": ""
        },
        "image_url": {
            "type": "text",
            "description": "",
            "default_value": ""
        }
    }
}


def Make_via_filename_template(img_file_name, pLstLst, scoreLst=[], callLst=[], file_sz = 0):
    d = copy.deepcopy(via_filename_template)
    d["filename"] = img_file_name
    d["size"] = file_sz
    
    for i in range(len(pLstLst)):
        num_points = len(pLstLst[i])
        if num_points <4:continue
        region = copy.deepcopy(region_template)
        region["region_attributes"]["call_type"]="eval"
        if scoreLst: region["region_attributes"]["model_score"]=float(scoreLst[i])
        if callLst: region["region_attributes"]["model_call"]=callLst[i]
        for p in pLstLst[i]:
            region["shape_attributes"]["all_points_x"].append(int(p[0]))
            region["shape_attributes"]["all_points_y"].append(int(p[1]))
        d["regions"].append(region)
    return d



""" Training set used for training image network"""

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def makesegmentLst(X,Y):
    assert len(X)==len(Y)
    sLst = []
    for i in range(len(X)):
        sLst.append(X[i])
        sLst.append(Y[i])
    return sLst,  PolyArea(np.array(X),np.array(Y))


def Make_tsImagerec(fn, id):
    return {
        "url": "http:\\/\\/x.com\\/8227\\/y.jpg",
        "height": 768,
        "license": 0,
        "file_name": fn,
        "width": 1024,
        "id": id,
        "date_captured": ""
    }
def Make_tsCategory(name, id, supercategory=""):
    return {"supercategory": supercategory,
        "id": id,
        "name": name
    }
    
def Make_tsAnnotation(annot_id, image_id, sLst, category_id, bbox=[0,0,0,0]):
    x,y = sLst
    segmentlst, s_area = makesegmentLst(x,y)
    return {
        "segmentation": [segmentlst],
        "bbbox": bbox,
        "iscrowd": 0,
        "category_id": category_id,
        "image_id": image_id,
        "area": s_area,
        "id": annot_id
    }
    
def Make_TrainingSet_Template():
    return {
        "images": [],
    "info": {
        "url": "url",
        "contributor": "mls",
        "description": "kitchen",
        "date_created": "",
        "year": 0,
        "version": "1.0"
    },
    "type": "instances",
    "categories": [],
    "annotations": [],
    "licenses": [{
                "url": "http:\\/\\/creativecommons.org\\/licenses\\/by-nc-sa\\/2.0\\/",
                "id": 1,
                "name": "Attribution-NonCommercial-ShareAlike License"
            }]
        }