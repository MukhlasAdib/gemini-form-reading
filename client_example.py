import requests

# Path to the image file
IMAGE_PATH = "test-form.png"

with open(IMAGE_PATH, "rb") as img_file:
    image_bytes = img_file.read()

# Send POST request with raw image data
response = requests.post(
    url="http://localhost:5000/read-image",
    headers={"Content-Type": "application/octet-stream"},
    data=image_bytes,
)

# Print the server response
print("Status Code:", response.status_code)
print("Response:", response.json())
