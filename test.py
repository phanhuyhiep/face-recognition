# -*- coding: utf-8 -*-
"""
@author: https://hiepph.com
"""
from __future__ import print_function
import os
import cv2
from models.resnet import *
import torch
import numpy as np
import time
import requests
from configs.config import Config
from torch.nn import DataParallel

def get_lfw_list(pair_list):
    with open(pair_list, 'r') as fd:
        pairs = fd.readlines()
    data_list = []
    for pair in pairs:
        splits = pair.split()

        if splits[0] not in data_list:
            data_list.append(splits[0])

        if splits[1] not in data_list:
            data_list.append(splits[1])
    return data_list


def load_image(url: str):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        img_array = np.frombuffer(resp.content, np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return None
        # resize về 128x128
        image = cv2.resize(image, (128, 128))
        image = np.dstack((image, np.fliplr(image)))
        image = image.transpose((2, 0, 1))
        image = image[:, np.newaxis, :, :]
        image = image.astype(np.float32, copy=False)
        image -= 127.5
        image /= 127.5
        return image
    except Exception as e:
        print(f"Error loading image from {url}: {e}")
        return None

def get_featurs(model, test_list, batch_size=10):
    images = None
    features = None
    cnt = 0
    for i, img_path in enumerate(test_list):
        image = load_image(img_path)
        if image is None:
            print('read {} error'.format(img_path))

        if images is None:
            images = image
        else:
            images = np.concatenate((images, image), axis=0)

        if images.shape[0] % batch_size == 0 or i == len(test_list) - 1:
            cnt += 1

            data = torch.from_numpy(images)
            data = data.to(torch.device("cpu"))
            output = model(data)
            output = output.data.cpu().numpy()

            fe_1 = output[::2]
            fe_2 = output[1::2]
            feature = np.hstack((fe_1, fe_2))

            if features is None:
                features = feature
            else:
                features = np.vstack((features, feature))

            images = None

    return features, cnt


def load_model(model, model_path):
    model_dict = model.state_dict()
    pretrained_dict = torch.load(model_path)
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)


def get_feature_dict(test_list, features):
    fe_dict = {}
    for i, each in enumerate(test_list):
        # key = each.split('/')[1]
        fe_dict[each] = features[i]
    return fe_dict


def cosin_metric(x1, x2):
    # Flatten arrays to 1D if they are 2D
    x1 = x1.flatten()
    x2 = x2.flatten()
    return np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))


def cal_accuracy(y_score, y_true):
    y_score = np.asarray(y_score)
    y_true = np.asarray(y_true)
    best_acc = 0
    best_th = 0
    for i in range(len(y_score)):
        th = y_score[i]
        y_test = (y_score >= th)
        acc = np.mean((y_test == y_true).astype(int))
        if acc > best_acc:
            best_acc = acc
            best_th = th

    return (best_acc, best_th)


def test_performance(fe_dict, pair_list):
    with open(pair_list, 'r') as fd:
        pairs = fd.readlines()

    sims = []
    labels = []
    for pair in pairs:
        splits = pair.split()
        fe_1 = fe_dict[splits[0]]
        fe_2 = fe_dict[splits[1]]
        label = int(splits[2])
        sim = cosin_metric(fe_1, fe_2)

        sims.append(sim)
        labels.append(label)

    acc, th = cal_accuracy(sims, labels)
    return acc, th


def lfw_test(model, img_paths, identity_list, compair_list, batch_size):
    s = time.time()
    features, cnt = get_featurs(model, img_paths, batch_size=batch_size)
    print(features.shape)
    t = time.time() - s
    print('total time is {}, average time is {}'.format(t, t / cnt))
    fe_dict = get_feature_dict(identity_list, features)
    acc, th = test_performance(fe_dict, compair_list)
    print('lfw face verification accuracy: ', acc, 'threshold: ', th)
    return acc

def convert_img_to_embedding(img_path, model):
    image = load_image(img_path)
    print()
    if image is None:
        print('read {} error'.format(img_path))
        return None

    data = torch.from_numpy(image)
    data = data.to(torch.device("cpu"))
    output = model(data)
    output = output.data.cpu().numpy()

    fe_1 = output[::2]
    fe_2 = output[1::2]
    feature = np.hstack((fe_1, fe_2))
    # print(feature.shape)
    return feature


def load_face_model():
    opt = Config()
    if opt.backbone == 'resnet18':
        model = resnet_face18(opt.use_se)
    elif opt.backbone == 'resnet34':
        model = resnet34()
    elif opt.backbone == 'resnet50':
        model = resnet50()
    else:
        raise ValueError(f"Unsupported backbone: {opt.backbone}")

    model = DataParallel(model)
    state_dict = torch.load(opt.test_model_path, map_location='cpu', weights_only=True)
    model.load_state_dict(state_dict)
    model.to(torch.device("cpu"))
    model.eval()
    return model


def get_face_similarity(img_path1: str, img_path2: str, model) -> float:
    if not img_path1.lower().startswith(("http://", "https://")) and ":" in img_path1:
        img_path1 = "http://" + img_path1
    if not img_path2.lower().startswith(("http://", "https://")) and ":" in img_path2:
        img_path2 = "http://" + img_path2
    feature1 = convert_img_to_embedding(img_path1, model)
    feature2 = convert_img_to_embedding(img_path2, model)
    sim = cosin_metric(feature1, feature2)
    print(f"Similarity between {img_path1} and {img_path2}: {sim}")
    return sim


# if __name__ == '__main__':
#     model = load_face_model()
#     img1 = '192.168.100.20:9000/face-search/b4a53e9082b44c05b704afdbae960e2a.jpg'
#     img2 = '192.168.100.20:9000/face-search/ce7395acb3cb42eb92df7ee6efa9e904.jpg'
#     similarity = get_face_similarity(img1, img2, model)
#     print("similarity:", similarity)