import cv2
import numpy as np


INPUT_SIZE = 257


def run_model(interpreter, frame):
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Test model on random input data.
    input_data = frame_to_input(frame)
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    output_tensor = []
    for i in range(len(output_details)):
        output_tensor.append(interpreter.get_tensor(output_details[i]['index']))
    if len(output_details) == 1:
        output_tensor = output_tensor[0]
    return output_tensor


def frame_to_input(frame):
    # Default values
    width = 257
    height = 257
    num_channels = 3
    image = cv2.resize(frame, (width, height), num_channels)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image = image * (2.0 / 255.0) - 1.0
    image = image.reshape((1, width, height, num_channels)).astype(np.float32)
    return image


def output_to_classes(output):
    ret = np.argmax(output, axis=-1)
    # Flatten to 2D
    return ret[0, :, :]



