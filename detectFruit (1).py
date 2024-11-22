import requests
import base64

# Đặt API_KEY của bạn vào đây
API_KEY = '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'  # Thay thế bằng API key thực của bạn

API_URL = 'https://api.openai.com/v1/chat/completions'

def detect_fruit(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}",
                        }
                    },
                ],
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            return "No fruits detected or no response from the model."
    else:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

# Example usage
image_path = r'C:\Users\dungvnzx1\Downloads\screenshot_20241016_003455.png'
try:
    fruits = detect_fruit(image_path)
    print(f"Detected fruits: {fruits}")
except Exception as e:
    print(f"An error occurred: {e}")