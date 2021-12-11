rem python detect.py --weights runs/train/%1/weights/best.pt --source ../../../datasets/numbers/test
python licplate_export.py --weights runs/train/%1/weights/best.pt --include onnx --opset 11 --dynamic --simplify
