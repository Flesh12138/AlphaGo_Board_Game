import numpy as np
import torch as t
import torch.nn as nn
from gobang_board import GoBangBoard
from time import time


class ConvBlk(nn.Module):
    def __init__(self):
        super(ConvBlk, self).__init__()
        self.conv = nn.Conv2d(3, 256, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(256)
        self.relu = nn.LeakyReLU(inplace=True)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x


class ResBlk(nn.Module):
    def __init__(self):
        super(ResBlk, self).__init__()
        self.conv1 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(256)
        self.relu1 = nn.LeakyReLU(inplace=True)
        self.conv2 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(256)
        self.relu2 = nn.LeakyReLU(inplace=True)

    def forward(self, x):
        backup = x
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x += backup
        x = self.relu2(x)
        return x


class PolicyHead(nn.Module):
    def __init__(self):
        super(PolicyHead, self).__init__()
        self.conv = nn.Conv2d(256, 2, kernel_size=1)
        self.bn = nn.BatchNorm2d(2)
        self.relu = nn.LeakyReLU(inplace=True)
        self.fc = nn.Linear(2 * 15 * 15, 15 * 15)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        x = t.flatten(x, start_dim=1)
        x = self.fc(x)
        return t.softmax(x, dim=1)


class ValueHead(nn.Module):
    def __init__(self):
        super(ValueHead, self).__init__()
        self.conv = nn.Conv2d(256, 1, kernel_size=1)
        self.bn = nn.BatchNorm2d(1)
        self.relu1 = nn.LeakyReLU(inplace=True)
        self.fc1 = nn.Linear(15*15, 256)
        self.relu2 = nn.LeakyReLU(inplace=True)
        self.fc2 = nn.Linear(256, 1)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu1(x)
        x = t.flatten(x, start_dim=1)
        x = self.fc1(x)
        x = self.relu2(x)
        x = self.fc2(x)
        return t.tanh(x)


class GoBangNet(nn.Module):
    def __init__(self):
        super(GoBangNet, self).__init__()
        self.conv_block = ConvBlk()

        self.res_block1 = ResBlk()
        self.res_block2 = ResBlk()
        self.res_block3 = ResBlk()

        self.policy_head = PolicyHead()
        self.value_head = ValueHead()

    def forward(self, x):
        x = self.conv_block(x)

        x = self.res_block1(x)
        x = self.res_block2(x)
        x = self.res_block3(x)

        policy = self.policy_head(x)
        value = self.value_head(x)

        return policy, value

    def load_param(self, path):
        self.load_state_dict(t.load(path)['weight'])

    def predict(self, x):
        with t.no_grad():
            flag_single_board = False
            if isinstance(x, GoBangBoard):
                flag_single_board = True
                x = x.get_network_input().cuda()
            policy, value = self.forward(x)
            if flag_single_board:
                policy = policy[0]
                value = value[0]
            return policy.cpu(), value.cpu().item()

if __name__ == '__main__':
    import os
    model = GoBangNet().cuda()
    state = {"weight": model.state_dict()}
    t.save(state, os.path.join('./data/nets', f'gen_0.net'))

    a = t.rand(512, 3, 15, 15).to('cuda')

    board = GoBangBoard()
    t1 = time()
    for i in range(100):
        x = board.get_network_input().cuda()
        model.predict(x)
    print(time() - t1)

    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(1024, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(1024, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(1024, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(32, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(16, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(8, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(4, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(2, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)

    a = t.rand(1, 3, 15, 15).to('cuda')
    t1 = time()
    for i in range(1):
        model(a)
    print(time() - t1)