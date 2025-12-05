

## **5️⃣ data_loader.py**

import kagglehub
from pathlib import Path
import zipfile
import os

def download_call_center_dataset():
    """
    Automatically download the latest call center speech dataset from KaggleHub.
    Returns the path to the extracted dataset folder.
    """
    dataset_name = "axondata/call-center-speech-dataset"
    dataset_path = Path("datasets") / "call_center_speech"

    if not dataset_path.exists():
        dataset_path.mkdir(parents=True, exist_ok=True)
        zip_path = Path("datasets") / "call_center_speech.zip"

        # Download dataset
        kagglehub.dataset_download(dataset_name, path=str(zip_path), unzip=False)

        # Unzip dataset
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dataset_path)
        os.remove(zip_path)
    
    return dataset_path

if __name__ == "__main__":
    path = download_call_center_dataset()
    print("Dataset ready at:", path)
