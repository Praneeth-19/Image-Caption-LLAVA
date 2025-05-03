from fastapi import FastAPI, UploadFile, File, HTTPException
import requests
import base64

app = FastAPI()

@app.post("/caption/")
async def caption_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        try:
            # In your backend code
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "tinyllama",  # Try a tiny model
                    "prompt": "Describe this image in one sentence.",
                    "images": [image_base64],
                    "stream": False
                },
                timeout=120
            )
            
            if response.status_code != 200:
                return {"error": f"Ollama API returned status code {response.status_code}: {response.text}"}
                
            result = response.json()
            return {"caption": result["response"].strip()}
            
        except requests.exceptions.ConnectionError:
            return {"error": "Could not connect to Ollama. Make sure Ollama is running on localhost:11434."}
        except requests.exceptions.Timeout:
            return {"error": "Request to Ollama timed out. The image might be too complex or Ollama is overloaded."}
        except Exception as e:
            return {"error": f"Error communicating with Ollama: {str(e)}"}
            
    except Exception as e:
        return {"error": f"Error processing image: {str(e)}"}
