rem python licplate_datasets_converter.py --clear --test --via ../../../datasets/numbers/autoriaNumberplateDataset-2021-05-12 ../../../datasets/numbers/plates
python licplate_datasets_converter.py --clear --via ../../../datasets/numbers/autoriaNumberplateDataset-2021-05-12 ../../../datasets/numbers/plates
python train.py --data licplate.yaml --cfg yolov5n.yaml --weights yolov5n.pt --batch-size 32 --epochs 50
rem python train.py --data licplate.yaml --cfg yolov5n.yaml --hyp hyp.finetune.yaml --weights yolov5n.pt --batch-size 32 --epochs 50
