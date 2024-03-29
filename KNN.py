# KNN structure used from https://gist.github.com/wzjoriv/7e89afc7f30761022d7747a501260fe3
import torch

class KNN():
    def __init__(self, X=None, Y=None, k=3, p=2):
        self.k = k
        self.p = p
        self.train(X, Y)
    def train(self, X, Y):
        self.train_pts = X
        self.train_label = Y
        if type(Y) != type(None):
            self.unique_labels = self.train_label.unique()

    def predict(self, x):
        if type(self.train_pts) == type(None) or type(self.train_label) == type(None):
            name = self.__class__.__name__
            raise RuntimeError(f"{name} wasn't trained. Need to execute {name}.train() first")

        dist = distance_matrix(x, self.train_pts, self.p)

        knn = dist.topk(self.k, largest=False)
        votes = self.train_label[knn.indices]

        winner = torch.zeros(votes.size(0), dtype=votes.dtype, device=votes.device)
        count = torch.zeros(votes.size(0), dtype=votes.dtype, device=votes.device) - 1

        for lab in self.unique_labels:
            vote_count = (votes == lab).sum(1)
            who = vote_count >= count
            winner[who] = lab
            count[who] = vote_count[who]

        return winner

    def __call__(self, x):
        return self.predict(x)


def random_sample(tensor, k):
    return tensor[torch.randperm(len(tensor))[:k]]


def distance_matrix(x, y=None, p=2):  # pairwise distance of vectors

    y = x if type(y) == type(None) else y

    n = x.size(0)
    m = y.size(0)
    d = x.size(1)

    x = x.unsqueeze(1).expand(n, m, d)
    y = y.unsqueeze(0).expand(n, m, d)

    dist = torch.linalg.vector_norm(x - y, p, 2) if torch.__version__ >= '1.7.0' else torch.pow(x - y, p).sum(2) ** (1 / p)

    return dist