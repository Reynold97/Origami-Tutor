import base64
import os
import pandas as pd
import requests

# OpenAI API Key
api_key = ""

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def classify_step(instruction_image_path, step_image_path, frame_image_path):
    # Encode the images to base64
    instruction_image = encode_image(instruction_image_path)
    step_image = encode_image(step_image_path)
    frame_image = encode_image(frame_image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert origami crafter. Your job is to evaluate when I complete a step of the following instructions:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{instruction_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "This is the current step I am trying to make:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{step_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "This is an image of my progress:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{frame_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Classify my progress with JUST one of 2 stages: 'In progress' or 'Done'."
                    }
                ]
            }
        ],
        "max_tokens": 10
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Debugging: print the full response
    print(response.json())

    # Extract and return the result
    try:
        return response.json()["choices"][0]["message"]["content"]
    except KeyError as e:
        print(f"KeyError: {e}. Full response: {response.json()}")
        return "Error"

def main():
    instruction_image_path = r"data\instructions\crane\instructions-1024.jpg"
    step_images_folder = r"data\instructions\crane\steps"
    frames_folder = r"data\video\crane\frames"

    step_images = sorted(os.listdir(step_images_folder))
    frames = sorted(os.listdir(frames_folder))

    results = []

    current_step = 1
    for frame in frames:
        frame_path = os.path.join(frames_folder, frame)
        step_image_path = os.path.join(step_images_folder, step_images[current_step])

        result = classify_step(instruction_image_path, step_image_path, frame_path)
        print(f"Frame {frame}: Step {step_images[current_step]}, {result}")

        # Store the result in the table
        results.append({
            "Frame": frame,
            "Step": current_step,
            "Result": result,
            "Instruction Image Path": instruction_image_path,
            "Step Image Path": step_image_path,
            "Frame Image Path": frame_path
        })

        if "done" in result.lower():
            current_step += 1
            if current_step >= len(step_images) + 1:
                print("Origami completed successfully!")
                break

    # Convert the results to a DataFrame and save to CSV
    df = pd.DataFrame(results)
    df.to_csv("origami_evaluation_results.csv", index=False)
    print("Results saved to origami_evaluation_results.csv")

if __name__ == "__main__":
    main()
