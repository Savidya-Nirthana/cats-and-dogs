from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from PIL import Image
import numpy as np
from pathlib import Path
import os
import tensorflow as tf


# load model
BASE_DIR = Path(__file__).resolve().parent.parent
model_dir = os.path.join(BASE_DIR, 'dataset/models/cat_dog.h5')
model = tf.keras.models.load_model(model_dir)


# prediction
def image_prediction(img_path):
    global model
    with Image.open(img_path) as img:
        img = img.resize((224,224))
        pixel_array = np.array(img)
    
    pixel_array = pixel_array/255
    pixel_array = pixel_array.reshape(1,224,224,3)

    y_pred = model.predict(pixel_array)
    y_pred = np.argmax(y_pred[0])
    if y_pred == 0:
        pred = 'Cat'
    else:
        pred = 'Dog'
    return pred


# actual view
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            img_path = image_instance.image.path
            prediction = image_prediction(img_path)
            return render(request, 'upload.html', {'form': form, 
                                                  'prediction':prediction, 
                                                  'img_path': image_instance.image.url})
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})



def index(request):
    if request.method == 'POST':
        return redirect('image_upload')
    return render(request, 'index.html')