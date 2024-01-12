import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
import numpy as np
import pandas as pd
import pickle
from ActionUnitDetector import ActionUnitDetector
from Data import Data
from kmeans_pytorch import kmeans, kmeans_predict
import torch.nn.functional as F
from KNN import KNN

# class to detect emotions
class EmotionDetector():
    def __init__(self, csvPaths):
        self.auDetector = ActionUnitDetector()
        data = pd.read_csv(csvPaths)
        try:
            with open('imageAUs.npy', 'rb') as f:
                inputs = np.load(f)
        except (OSError, IOError) as e:
            inputs = self.auDetector.detectAUImagesPath(data['subDirectory_filePath'])
            with open('imageAUs.npy', 'wb') as f:
                np.save(f, inputs)
        try:
            with open('imageLabels.npy', 'rb') as f:
                labels = np.load(f)
        except (OSError, IOError) as e:
            labels = []
            for i in data["subDirectory_filePath"]:
                labels.append(i.split("/")[-2])
            with open('imageLabels.npy', 'wb') as f:
                np.save(f, labels)
        labelsVal = data["valence"]
        self.dataset = Data(inputs, labels)
        self.datasetVal = Data(inputs, labelsVal)

        try:
            self.model = NN(20,len(np.unique(self.dataset.labels)), 256)
            self.model.load_state_dict(torch.load('best_emotion_model.pth'))
        except (OSError, IOError) as e:
            self.train(self.dataset, 'emotion')
        try:
            self.modelVal = NN(20,len(np.unique(self.datasetVal.labels)), 256)
            self.modelVal.load_state_dict(torch.load('best_valence_model.pth'))
        except (OSError, IOError) as e:
            self.train(self.datasetVal, 'valence')
        try:
            with open('knn.pkl', 'rb') as f:
                self.knn = pickle.load(f)
        except (OSError, IOError) as e:
            self.knn = self.trainKMeans(self.dataset.labels, self.datasetVal.labels)
            with open('knn.pkl', 'wb') as f:
                pickle.dump(self.knn, f)

    def train(self, data, typeNN):
        torch.set_grad_enabled(True)
        generator = torch.Generator().manual_seed(2023)
        train, val, test = random_split(data, [0.8, 0.1, 0.1], generator=generator)

        train_loader = DataLoader(train, batch_size=4, shuffle=True)
        val_loader = DataLoader(dataset=val, shuffle=False, batch_size=4)
        test_loader = DataLoader(dataset=test, shuffle=False, batch_size=4)

        #in order to run on all machines after training only cpu is used
        #self.device = "cuda" if torch.cuda.is_available() else "cpu"
        #self.device = "mps" if torch.backends.mps.is_available() else self.device
        self.device = "cpu"

        loss_fn = nn.CrossEntropyLoss()

        best_lr = 0
        best_nodes = 0
        max_acc = 0
        for learningrate in [0.001, 0.005, 0.01]:
            for nodes in [128, 256, 512]:
                model, epoch, min_val_loss, accuracy = trainNN(train_loader, val_loader, test_loader,
                        train[0][0].shape[0], len(np.unique(data.labels)), nodes, learningrate, 200, loss_fn, self.device)
                if accuracy > max_acc:
                    max_acc = accuracy
                    best_lr = learningrate
                    best_nodes = nodes
                    torch.save(model.state_dict(), f'best_{typeNN}_model.pth')
                    self.model = model
                print("Accuracy for lr:", learningrate, " and nodes:", nodes,
                      f" is: {accuracy * 100}% and the best epoch was ", epoch,
                      " with a val loss of ", min_val_loss)
        print("The best network had a learning rate of ", best_lr, " and ", best_nodes, " nodes in the middle")

    def trainKMeans(self, data1, data2):
        data1OneHot = F.one_hot(data1)
        data2OneHot = F.one_hot(data2)
        data = torch.cat((data1OneHot, data2OneHot), 1)
        data = np.asarray(data)
        data = data.astype('float64')
        data = torch.Tensor(data)

        self.knn = KNN(data, data1)
        return self.knn
    
    def predict(self, aus):
        #self.device = "cuda" if torch.cuda.is_available() else "cpu"
        #self.device = "mps" if torch.backends.mps.is_available() else self.device
        self.device = "cpu"
        with torch.no_grad():
            predictionVal = self.modelVal(torch.from_numpy(aus))
            predictionVal = predictionVal.softmax(dim=1)
        with torch.no_grad():
            prediction = self.model(torch.from_numpy(aus))
            prediction = prediction.softmax(dim=1)
        data = torch.cat((prediction, predictionVal), 1)
        data = np.asarray(data)
        data = data.astype('float64')
        data = torch.Tensor(data)
        pred = self.knn(data)
        return self.dataset.index2label[pred[0]]

class NN(nn.Module):
    def __init__(self, features_in, features_out, middle_layer=32):
        super().__init__()
        kernel_size = 5
        channels = 32
        padding = 1
        self.nn = nn.Sequential(
            nn.Conv1d(1, channels, kernel_size=5, stride=1, padding=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear((features_in-kernel_size+2*padding+1)*32, 120),
            nn.ReLU(),
            nn.Linear(120, middle_layer),
            nn.ReLU(),
            nn.Linear(middle_layer, features_out)
        )

    def forward(self, x):
        if np.ndim(x)<3:
            x = x.unsqueeze(1)
        return self.nn(x)


def trainNN(train_loader, val_loader, test_loader, inputShape, outputShape, nodes, learningrate, epochs, loss_fn, device):
    model = NN(inputShape, outputShape, middle_layer=nodes)
    model = model.to(device)
    optim = torch.optim.SGD(model.parameters(), lr=learningrate)
    count = 0
    min_val_loss = 1000
    min_val_loss_epoch = 0
    for epoch in range(epochs):
        train_loss = 0.0
        for inputs, labels in train_loader:
            optim.zero_grad()

            inputs = inputs.unsqueeze(1)
            inputs = inputs.to(device)
            labels = labels.to(device)

            out = model(inputs)
            loss = loss_fn(out, labels)

            loss.backward()
            optim.step()
            optim.zero_grad()
            train_loss += loss.item()

        valid_loss = 0.0
        for inputs, labels in val_loader:
            inputs = inputs.unsqueeze(1)
            inputs = inputs.to(device)
            labels = labels.to(device)

            target = model(inputs)
            loss = loss_fn(target, labels)
            valid_loss = loss.item() * inputs.size(0)

        count += 1
        if valid_loss / len(val_loader) < min_val_loss:
            min_val_loss = valid_loss / len(val_loader)
            min_val_loss_epoch = epoch
    with torch.no_grad():
        correct = 0
        totalTestSize = 0
        test = 0
        for inputs, labels in test_loader:
            inputs = inputs.unsqueeze(1)
            inputs = inputs.to(device)
            labels = labels.to(device)
            predictions = model(inputs)
            correct += (predictions.softmax(dim=1).argmax(dim=1) == labels).sum()
            test +=4
            totalTestSize += len(predictions)
    return model,min_val_loss_epoch, min_val_loss, correct/totalTestSize



