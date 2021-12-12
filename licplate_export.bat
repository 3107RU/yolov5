rem python detect.py --weights runs/train/exp/weights/best.pt --source ../../../datasets/numbers/test --img-size 320 --exist-ok
python export.py --weights runs/train/exp/weights/best.pt --img-size 320 --include onnx --opset 14 --dynamic --simplify
