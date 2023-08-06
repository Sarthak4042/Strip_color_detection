import os
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
import json
import cv2
import numpy as np
from django.views import View


class AnalyzeEndpoint(View):
    def get(self, request):
        raise NotImplementedError()


def homepage(request):
    return render(request, "trial.html")




def analyze_endpoint(request):
    if request.method == 'POST':
        try:
            # Get the uploaded image from the POST request
            uploaded_image = request.FILES['user_group_logo']

            # Save the uploaded image to a temporary location
            # with open(uploaded_image, 'wb') as f:
            #    for chunk in uploaded_image.chunks():
            #        f.write(chunk)

            # Perform color identification using OpenCV
            colors = identify_colors(uploaded_image)

            # Delete the temporary image file
            os.remove(uploaded_image)

            # Convert colors to a JSON object
            color_json = json.dumps(colors, default=lambda x: x.tolist())

            return JsonResponse({'colors': color_json})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def identify_colors(uploaded_image, num_colors=10):
    # Load the image
    image = cv2.imread(uploaded_image)

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for the urine strip colors (example ranges)
    color_ranges = [
        ((0, 0, 100), (20, 255, 255)),   # Red
        ((25, 0, 100), (35, 255, 255)),  # Orange
        ((40, 0, 100), (80, 255, 255)),  # Yellow
        # Add more color ranges here
    ]

    identified_colors = []

    for lower, upper in color_ranges:
        lower_np = np.array(lower, dtype=np.uint8)
        upper_np = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(hsv_image, lower_np, upper_np)
        count = cv2.countNonZero(mask)

        if count > 0:
            average_color = cv2.mean(image, mask=mask)[:3]
            identified_colors.append(average_color)

    return identified_colors[:num_colors]
