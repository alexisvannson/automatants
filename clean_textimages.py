# -*- coding: utf-8 -*-
"""baseline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jeVzLas1s11o1SnYiDs-umFZKpmmlxQ2

## Import des libraries
"""

!pip install torchinfo
import numpy as np
import torch
import torch.nn as nn
import gdown
import os
from torchinfo import summary

"""## Téléchargement du dataset"""

#Téléchargement du dataset
url = 'https://drive.google.com/uc?id=1KIX6QASxnWGPJcQ_Q-W8O1UPSbPA4uat'
output = 'dataset.zip'
if not os.path.exists(output):
	gdown.download(url, output, quiet=False)

#Dézippage du dataset

def unzip(zip_file, dest_dir):
	import zipfile
	with zipfile.ZipFile(zip_file, 'r') as zip_ref:
		zip_ref.extractall(dest_dir)

unzip('dataset.zip', './')

"""## Load le dataset"""

X_train = np.load('X_train.npy')
X_clean_train = np.load('X_clean_train.npy')
X_test = np.load('X_test.npy')

print(X_train.shape)
print(X_clean_train.shape)
print(X_test.shape)

"""## Affichage des données"""

import matplotlib.pyplot as plt

# first row show 5 noised images, second row show 5 clean images
for i in range(5):
	plt.subplot(2, 5, i + 1)
	plt.imshow(X_train[i])
	plt.title("Noised")
	plt.axis('off')

	plt.subplot(2, 5, i + 6)
	plt.imshow(X_clean_train[i])
	plt.title("Clean")
	plt.axis('off')

plt.show()

"""## Batch les données"""

batch_size = 20
width = X_train.shape[1]
height = X_train.shape[2]
X_train_reshaped = X_train.reshape(-1, batch_size, width, height)
X_clean_train_reshaped = X_clean_train.reshape(-1, batch_size, width, height)

print(X_train_reshaped.shape)
print(X_clean_train_reshaped.shape)

"""## Ajouter la dimension de couleur
Pour l'instant, nos images sont de shape (width, height). Les couches de convolution veulent des images de shape (color, width, height). On va donc ajouter une dimension de couleur à nos images.
"""

X_train_expanded = np.expand_dims(X_train_reshaped, axis=2)
X_clean_train_expanded = np.expand_dims(X_clean_train_reshaped, axis=2)

print(X_train_expanded.shape)
print(X_clean_train_expanded.shape)

"""## Convertir les données en torch.tensor"""

X_train_torch = torch.from_numpy(X_train_expanded).float()
X_clean_train_torch = torch.from_numpy(X_clean_train_expanded).float()

"""## Faire la même chose pour les données test"""

batch_size_test = 14
X_test = X_test.reshape(-1, batch_size_test, width, height)
X_test_expanded = np.expand_dims(X_test, axis=2)
X_test_torch = torch.from_numpy(X_test_expanded).float()

"""## Créer le modèle"""

class Model(nn.Module) :

  def __init__(self):

    super().__init__()

    self.convolution = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=0)





    self.seq = nn.Sequential(

            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1),

            nn.BatchNorm2d(16),

            nn.ReLU(),

            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1),

            nn.BatchNorm2d(32),

            nn.ReLU(),

            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1),

            nn.BatchNorm2d(64),

            nn.ReLU(),

            nn.Conv2d(in_channels=64, out_channels=1, kernel_size=3, stride=1, padding=1),

        )

  def forward(self, x):

    x = self.seq(x)

    return x

"""### Modèle 1

class Model(nn.Module):
	def __init__(self):
		super().__init__()
		self.layer1 = nn.Conv2d(1, 8, kernel_size=3, padding=1, stride =2) #argument 1:input, argument 2:
		self.layer2 = nn.Conv2d(8,16, kernel_size=3, padding=1, stride =2)
		self.layer3 = nn.Conv2d(16, 32, kernel_size=3, padding=0,stride =2)
		self.layer4 = nn.ConvTranspose2d(32,16, kernel_size=4, padding=1, stride =2)
		self.layer5 = nn.ConvTranspose2d(in_channels=16, out_channels=8, kernel_size=4, stride=2, padding=1)
		self.layer6 = nn.ConvTranspose2d(8, 1, kernel_size=4, padding=1,stride=2)
		self.relu = nn.ReLU()
		#self.max_pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
		#self.convolution_transpose = nn.ConvTranspose2d(in_channels=16, out_channels=1, kernel_size=3, stride=1, padding=0)

	def forward(self, x):
		y = self.layer1(x)
		y1 = self.relu(y)

		y2 = self.layer2(y1)
		y3 = self.relu(y2)

		y4 = self.layer3(y3)
		y5 = self.relu(y4)

		y6 = self.layer4(y5)
		y7 = self.relu(y6)

		y8 = self.layer5(y7)
		y9 = self.relu(y8)

		y10 = self.layer6(y9)
		return self.relu(y10)

		""
"""

batch_size = 5
input_shape = (batch_size, 1, 128, 200)
model = Model()
summary(model, input_size=input_shape)

"""# Boucle d'entrainement"""

model = Model()
loss_function = nn.MSELoss()

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
num_epochs = 20
for epoch in range(num_epochs):
  for j in range(len(X_train_torch)):
    input_tensor = X_train_torch[j]
    optimizer.zero_grad()
    output_tensor = model(input_tensor)
    loss = loss_function(output_tensor, X_clean_train_torch[j])
    loss.backward()
    optimizer.step()
    print(f'Epoch [{epoch}/{num_epochs}], Loss: {loss.item()}')

"""# Prédiction"""

batch_size_test = 14
X_test = X_test.reshape(-1, batch_size_test, width, height)
X_test_expanded = np.expand_dims(X_test, axis=2)
X_test_torch = torch.from_numpy(X_test_expanded).float()

predictions = []
for i in range(len(X_test_torch)):
    X = X_test_torch[i]
    X_pred = model(X)
    predictions.append(X_pred.detach().numpy())

predictions = np.array(predictions)
predictions = predictions.reshape(-1, width, height)

np.save('predictions.npy', predictions)

for i in range(5):
	plt.subplot(2, 5, i + 6)
	plt.imshow(predictions[i])
	plt.title("Clean")
	plt.axis('off')