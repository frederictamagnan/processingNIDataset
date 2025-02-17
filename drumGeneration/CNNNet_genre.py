import torch.nn as nn
import torch.nn.functional as F
import torch
class CNNNet(nn.Module):
    def __init__(self,batch_size=256,nb_genre=15):
        super(CNNNet, self).__init__()
        self.conv1 = nn.Conv2d(2, 6, 3,padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 2,padding=1)
        self.fc1 = nn.Linear(768+nb_genre, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, 864)
        self.batch_size=batch_size

    def forward(self, x,genre):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(self.batch_size, -1)
        genre=genre.float()
        # print(genre.size(),"genre")
        x=torch.cat([x,genre ], 1)
        # print(x.size())
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))

        return x


