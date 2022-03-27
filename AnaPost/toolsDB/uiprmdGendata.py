#------------------------------------------------------------------
# Code written by Idris DULAU, Rodin DUHAYON and Guillaume DUBRASQUET-DUVAL.
# Adapted from https://github.com/Chiaraplizz/ST-TR.
# For the use of Dr. Marie Beurton-Aimar and Phd. student Kévin Réby.
#------------------------------------------------------------------

import argparse
import os
import numpy as np
import json
from torch.utils.data import Dataset
import pickle
from tqdm import tqdm

num_joint = 22
max_frame = 10000
num_person_out = 1
num_person_in = 1

class Feeder_kinetics(Dataset):

    def __init__(self,
                 data_path,
                 label_path,
                 ignore_empty_sample=True,
                 window_size=-1,
                 num_person_in=num_person_in,
                 num_person_out=num_person_out):
        self.data_path = data_path
        self.label_path = label_path
        self.window_size = window_size
        self.num_person_in = num_person_in
        self.num_person_out = num_person_out
        self.ignore_empty_sample = ignore_empty_sample

        self.load_data()

    def load_data(self):
        self.sample_name = os.listdir(self.data_path)

        label_path = self.label_path
        with open(label_path) as f:
            label_info = json.load(f)

        sample_id = [name.split('.')[0] for name in self.sample_name]
        self.label = np.array([label_info[id]['label_index'] for id in sample_id])

        self.N = len(self.sample_name) 
        self.C = 3 #Number of channels
        self.T = max_frame  
        self.V = num_joint 
        self.M = self.num_person_out 

    def __len__(self):
        return len(self.sample_name)

    def __iter__(self):
        return self

    def __getitem__(self, index):

        sample_name = self.sample_name[index]
        sample_path = os.path.join(self.data_path, sample_name)
        with open(sample_path, 'r') as f:
            video_info = json.load(f)

        data_numpy = np.zeros((self.C, self.T, self.V, self.num_person_in))
        for frame_info in video_info['data']:
            frame_index = frame_info['frame_index']
            for m, skeleton_info in enumerate(frame_info["skeleton"]):
                if m >= self.num_person_in:
                    break
                pose = skeleton_info['pose']
                data_numpy[0, frame_index, :, m] = pose[0::3]
                data_numpy[1, frame_index, :, m] = pose[1::3]
                data_numpy[2, frame_index, :, m] = pose[2::3]

        label = video_info['label_index']
        assert (self.label[index] == label)
        
        return data_numpy, label


def gendata(data_path, label_path,
            data_out_path, label_out_path,
            num_person_in=num_person_in, 
            num_person_out=num_person_out,  
            max_frame=max_frame):
    feeder = Feeder_kinetics(
        data_path=data_path,
        label_path=label_path,
        num_person_in=num_person_in,
        num_person_out=num_person_out,
        window_size=max_frame)

    sample_name = feeder.sample_name
    sample_label = []

    fp = np.zeros((len(sample_name), 3, max_frame, num_joint, num_person_out), dtype=np.float32)

    for i, s in enumerate(tqdm(sample_name)):
        data, label = feeder[i]
        fp[i, :, 0:data.shape[1], :, :] = data
        sample_label.append(label)

    with open(label_out_path, 'wb') as f:
        pickle.dump((sample_name, list(sample_label)), f)

    np.save(data_out_path, fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Kinetics-skeleton Data Converter.')
    parser.add_argument(
        '--data_path', default='./uiprmd/')
    parser.add_argument(
        '--out_folder', default='./uiprmd_data/')
    arg = parser.parse_args()

    part = ['val', 'train']
    for p in part:
        print('uiprmd ', p)
        if not os.path.exists(arg.out_folder):
            os.makedirs(arg.out_folder)
        data_path = '{}/uiprmd_{}'.format(arg.data_path, p)
        label_path = '{}/uiprmd_{}_label.json'.format(arg.data_path, p)
        data_out_path = '{}/{}_data_joint.npy'.format(arg.out_folder, p)
        label_out_path = '{}/{}_label.pkl'.format(arg.out_folder, p)

        gendata(data_path, label_path, data_out_path, label_out_path)
