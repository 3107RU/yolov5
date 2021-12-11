import argparse
import os, os.path
import shutil
import PIL.Image
import json
import tqdm
import random

TEST_COUNT = 100
TRAIN_SPLIT = .9

class Item:
    def __init__(self, path):
        self.image = path
        self.objects = []
    class Object:
        def __init__(self, cls):
            self.cls = cls

def via_dataset(path, test):
    list = []
    for dataset in ['train', 'val']:
        with open(os.path.join(path, dataset, 'via_region_data.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
        for key in tqdm.tqdm(data['_via_img_metadata'], desc=f'Reading {dataset} via dataset...'):
            if test and len(list) > TEST_COUNT:
                break
            metadata = data['_via_img_metadata'][key]
            item = Item(os.path.join(path, dataset, metadata['filename']))
            image = PIL.Image.open(item.image)
            for region in metadata['regions']:
                shape = region['shape_attributes']
                if shape['name'] != 'polygon':
                    continue
                corners = [(x, y) for x, y in zip(shape['all_points_x'], shape['all_points_y'])]
                obj = Item.Object(0)
                obj.x = min([c[0] for c in corners]) / image.size[0]
                obj.y = min([c[1] for c in corners]) / image.size[1]
                obj.w = max([c[0] for c in corners]) / image.size[0] - obj.x
                obj.h = max([c[1] for c in corners]) / image.size[1] - obj.y
                obj.x += obj.w / 2
                obj.y += obj.h / 2
                item.objects.append(obj)
            list.append(item)

    return list


def write(path, list):
    for p in 'images', 'labels':
        os.makedirs(os.path.join(path, p), exist_ok=True)
        for q in 'train', 'val':
            os.makedirs(os.path.join(path, p, q), exist_ok=True)

    random.shuffle(list)
    count = len(list)
    with tqdm.tqdm(total=count, desc='Writing dataset...') as pbar:
        for i in range(count):
            split = 'train' if i / count < TRAIN_SPLIT else 'val'
            images, labels = os.path.join(path, 'images', split), os.path.join(path, 'labels', split)
            item = list[i]
            img_name = os.path.basename(item.image)
            label_name = os.path.splitext(img_name)[0] + '.txt'
            shutil.copyfile(item.image, os.path.join(images, img_name))
            with open(os.path.join(labels, label_name), 'a') as file:
                for obj in item.objects:
                    file.write(f'{obj.cls} {obj.x:.5f} {obj.y:.5f} {obj.w:.5f} {obj.h:.5f}\n')
            pbar.update(1)

def main(opt):
    if opt.clear and os.path.exists(opt.dest):
        shutil.rmtree(opt.dest)
    if opt.via:
        write(opt.dest, via_dataset(opt.via, opt.test))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dest', type=str, help='path to output dataset for yolov5')
    parser.add_argument('--clear', action='store_true', help='remove output dataset directory')
    parser.add_argument('--test', action='store_true', help='test run (convert no more than 100 images)')
    parser.add_argument('--via', type=str, default='', help='path to via dataset')
    opt = parser.parse_args()
    main(opt)
