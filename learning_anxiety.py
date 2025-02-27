# -*- coding: utf-8 -*-
"""Learning_anxiety.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vgCrambQ-xg2N_aPmArt4Bh1RcmozHYg
"""

#colab without interruption : ctrl_shft+i
function ClickConnect()
{
console.log("Working");
document.querySelector("colab-toolbar-button").click()
}
setInterval(ClickConnect,60000)

import torch
torch.cuda.empty_cache()
a = []
while(1):
  a.append('1')

#package
!pip3 install Torch
!pip3 install detecto
!pip install utils
#libraries
from detecto import core, utils, visualize
from detecto.utils import read_image
from detecto.core import Dataset
from detecto.utils import xml_to_csv
from detecto.visualize import show_labeled_image
from detecto.core import DataLoader, Model
from detecto.visualize import show_labeled_image, plot_prediction_grid
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np
import os
# Import the 'utils' module
import utils as utils
import sys
import torch
print(torch.cuda.is_available())

#dataset path
from google.colab import drive
drive.mount('/content/gdrive')
os.chdir(r'/content/gdrive/My Drive/PHD_ResearchWork/Obj_1/Obj1_R_DS')
!ls 'Test/'

#Show Image
image = read_image('Test/Test (17).jpg')
plt.imshow(image)
plt.show()

#!unzip Obj1_Validation.zip -d Obj1_R_DS

#import utils as utils
import sys
# Add the directory containing the 'utils' module to the system path
sys.path.append('/path/to/utils/module/directory')
# Import the 'utils' module
#import utils as utils
import torchvision.transforms as transforms
import torch
from detecto import core, utils, visualize
#from transforms as det_transforms

#After Data Augmentation
custom_transforms = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize(500),
    transforms.RandomRotation(360),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(saturation=1),
    transforms.ToTensor(),
    utils.normalize_transform(),])

dataset = Dataset('Train', transform=custom_transforms)
image, targets = dataset[177]
show_labeled_image(image, targets['boxes'])

Train_dataset=core.Dataset('Train',transform=custom_transforms)#L1
Test_dataset = core.Dataset('Validation')#L2
loader=core.DataLoader(Train_dataset, batch_size=4, shuffle=True)#L3
#model = core.Model(['Anger', 'Contempt', 'Disgust','Fear', 'Happy','Sad','Surprise'])#L4
#losses = model.fit(loader, Test_dataset, epochs=20, lr_step_size=5, learning_rate=0.001, verbose=True)#L5
#plt.plot(losses)#4.03timing
#plt.show()
#model.save('model_weights.pth')
model = core.Model.load('model_weights.pth', ['Anger','Contempt','Disgust','Fear','Happy','Sad','Surprise'])



#image Prediction
image  = utils.read_image('Test/baby_cry.png')
predictions = model.predict(image)
labels, boxes, scores = predictions
show_labeled_image(image, boxes, labels)
for label, score in zip(labels, scores):
  print(f"{label}: {score:.2f}")

#print(labels,scores)

#Pruning
thresh=0.49
filtered_indices=np.where(scores>=thresh)
filtered_scores=scores[filtered_indices]
filtered_boxes=boxes[filtered_indices]
num_list = filtered_indices[0].tolist()
filtered_labels = [labels[i] for i in num_list]
show_labeled_image(image, filtered_boxes, filtered_labels)
s1 = np.round(np.array(filtered_scores),2)
print("Emotions Labels & Score" )
for label, score in zip(filtered_labels, s1):
  print(f"{label}: {score:.2f}")
#print(filtered_labels,s1)
#filtered_labels,s1)

labels, boxes, scores = predictions

labels,scores = np.array(labels),np.array(scores)
labels = [labels[i] for i in range(len(labels)) if scores[i]>0.4]
labels = np.array(labels)

labels,scores = np.array(labels),np.array(scores)
scores = [scores[i] for i in range(len(labels)) if scores[i]>0.4]
scores = np.round(np.array(scores),2)
print("Labels:",labels,"IoU:", scores)


emot_high_score= {}
emot_values = {}

for i in range(len(labels)):
    if labels[i] in emot_values:
      # Replace with the higher value between the current highest mark and the new mark
      emot_values[labels[i]] = max(emot_values[labels[i]], scores[i])
    else:
      # Keep the current highest mark if the new mark is lower
      emot_values[labels[i]] = scores[i]


# Print the resulting dictionary with the highest marks
print("Highest marks after replacement:", emot_values)
emot_values

for label, value in emot_values.items():
  print(f"P_{label}, Value: {value:.2f}")

total_value = np.round(sum(emot_values.values()),2)

Learning_Anxiety_Score = 0

for label, value in emot_values.items():
  # Compute weight for the label
  w_label = value / total_value
  print(f"w_{label}, Value: {w_label:.2f}")
  weighted_contribution = value * w_label
  Learning_Anxiety_Score += weighted_contribution

# Print the final weighted sum
print(f"Learning Anxiety: {Learning_Anxiety_Score:.2f}")

label = list(emot_values.keys())
values = list(emot_values.values())

# Path to the image
image_path = 'Test/Age6_1.png'

# Load and display the image
image = plt.imread(image_path)
plt.imshow(image)
plt.axis('off')

# Overlay scatter plot for Learning Anxiety Score
plt.scatter([200], [100], c=[Learning_Anxiety_Score], cmap='cool', s=200, alpha=0.75)

Learning_Anxiety_Score = 0.9
# Categorize Learning Anxiety
if 0.0 <= Learning_Anxiety_Score < 0.25:
    LAnxiety_Label = 'Low Anxiety'
elif 0.25 <= Learning_Anxiety_Score < 0.50:
    LAnxiety_Label = 'Mild Anxiety'
elif 0.50 <= Learning_Anxiety_Score < 0.75:
    LAnxiety_Label = 'Moderate Anxiety'
elif 0.75 <= Learning_Anxiety_Score < 1.0:
    LAnxiety_Label = 'High Anxiety'
else:
    LAnxiety_Label = 'Debilitating Anxiety'

# Annotate with emotion labels
for i, (emotion, value) in enumerate(emot_values.items()):
  x = 200 + i * 150  # X position
  y = 200 + i * 150  # Y position
plt.annotate(f'{label}:{LAnxiety_Label}: {Learning_Anxiety_Score:.2f}', (x, y), fontsize=10, color='red', ha='center', va='center')

# Add color bar legend
scatter = plt.scatter([100], [100], c=[Learning_Anxiety_Score], cmap='cool', s=200)
plt.colorbar(scatter, label='Learning Anxiety Value')

# Print Learning Anxiety details
#print("Highest marks after replacement:", emot_values)



plt.title(
    'Visualization: Understanding Emotional Impact \n Level of Learning Anxiety',
    fontsize=16,
    fontweight='bold',
    color='#0D47B1',  # Greenish color for the title
    loc='center',  # Center alignment
    pad=20,  # Extra padding above the title
)

# Show plot
plt.show()
#print("Learning Anxiety" , f"{LAnxiety_Label} : {round(Learning_Anxiety_Score * 100)}%")
# Aesthetic bold output with emojis
print("\033[1m✨ Learning Anxiety ✨\033[0m")
print(f"🌀 Status: \033[1;95m{LAnxiety_Label}\033[0m , 📊 Score: \033[1;35m{round(Learning_Anxiety_Score * 100)}%\033[0m")
#print(f"Learning Anxiety: {Learning_Anxiety_Score*100:.2f}%")

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Define a function for processing frames and calculating learning anxiety
def process_frame(frame, model, thresh=0.3):
    predictions = model.predict(frame)
    labels, boxes, scores = predictions

    # Prune based on the threshold
    filtered_indices = np.where(scores >= thresh)
    filtered_scores = scores[filtered_indices]
    filtered_boxes = boxes[filtered_indices]
    filtered_labels = [labels[i] for i in filtered_indices[0].tolist()]

    # Calculate the emotional values
    emot_values = {}
    for i in range(len(filtered_labels)):
        label = filtered_labels[i]
        score = filtered_scores[i]
        emot_values[label] = max(emot_values.get(label, 0), score)

    # Calculate total emotional weight and learning anxiety score
    total_value = sum(emot_values.values())
    if total_value > 0:
        Learning_Anxiety_Score = sum(
            (value / total_value) * value for value in emot_values.values()
        )
    else:
        Learning_Anxiety_Score = 0

    return frame, emot_values, Learning_Anxiety_Score

# Categorize Learning Anxiety
def categorize_anxiety(score):
  if 0.0 <= score < 0.25:
    return 'Low Anxiety'
  elif 0.25 <= score < 0.50:
    return 'Mild Anxiety'
  elif 0.50 <= score < 0.75:
    return 'Moderate Anxiety'
  elif 0.75 <= score < 1.0:
    return 'High Anxiety'
  else:
    return 'Debilitating Anxiety'

# Video Input and Output Setup
video_input = 'Test/age16-17.mp4'  # Path to input video
video_output = 'Test/LA16.1.mp4'
cap = cv2.VideoCapture(video_input)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_output, fourcc, fps, (frame_width, frame_height))

# Load the emotion model (replace with your model loading code)
# model = load_your_model()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Process frame to find emotions and calculate anxiety
    processed_frame, emot_values, Learning_Anxiety_Score = process_frame(frame, model)

    # Categorize anxiety
    LAnxiety_Label = categorize_anxiety(Learning_Anxiety_Score)

    # Add annotations to the frame
    y_start = 50
    cv2.putText(processed_frame, f"Learning Anxiety: {Learning_Anxiety_Score:.2f}",
                (50, y_start), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(processed_frame, f"Category: {LAnxiety_Label}",
                (50, y_start + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Annotate emotions
    for i, (emotion, value) in enumerate(emot_values.items()):
        cv2.putText(processed_frame, f"{emotion}: {value:.2f}",
                    (50, y_start + 80 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Overlay dynamic marker
    x, y = frame_width // 2, frame_height // 2  # Center position
    cv2.circle(processed_frame, (x, y), 30, (255, 0, 255), -1)  # Marker
    cv2.putText(processed_frame, f"{Learning_Anxiety_Score:.2f}",
                (x - 20, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Write processed frame to output
    out.write(processed_frame)

# Release resources
cap.release()
out.release()
print(f"Processed video saved as {video_output}")







