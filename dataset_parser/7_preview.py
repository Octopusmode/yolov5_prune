import fiftyone as fo
dataset = fo.load_dataset('coco_pv_base')
session = fo.launch_app(view=dataset.view())