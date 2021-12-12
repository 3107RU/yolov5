rem python licplate_datasets_converter.py --clear --test --via ../../../datasets/numbers/autoriaNumberplateDataset-2021-05-12 ../../../datasets/numbers/plates
python train.py --data licplate.yaml --cfg yolov5n.yaml --weights yolov5n.pt --img-size 320 --batch-size 64 --epochs 300 --multi-scale --single-cls --exist-ok
