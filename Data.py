from torch.utils.data import Dataset
import torch
import numpy as np

# class that creates a dataset which pytorch can use to train and evaluate a convolutional neural network
class Data(Dataset):
    def __init__(self, inputs, labels):
        super().__init__()

        self.inputs = torch.from_numpy(inputs)
        self.index2label = [label for label in np.unique(labels)]
        self.label2index = {label: i for i, label in enumerate(self.index2label)}
        self.labels = []
        for i in labels:
            self.labels.append(torch.tensor(self.label2index.get(i)))
        self.labels = torch.stack(self.labels)

    def __getitem__(self, index):
        return self.inputs[index], self.labels[index]

    def __len__(self):
        return len(self.inputs)