import json
from pathlib import Path

def main():
    dataToWrite = {
        "name": "Carlos",
        "role": "Developer",
        "skills": [
            "Unity",
            "C#",
            "HLSL"
        ]
    }
    currentFolder = Path(__file__).parent
    folder = Path(currentFolder / "__pycache__")
    folder.mkdir(parents=True, exist_ok=True)

    # NOTE: This writes JSON to a file:
    with open(folder / "output.json", "w", encoding="utf-8", newline="\n") as file:
        json.dump(dataToWrite, file, indent=4)
        file.write('\n')

    # NOTE: This reads JSON from a file:
    with open(folder / "output.json", "r", encoding="utf-8", newline="\n") as file:
        dataToRead = json.load(file)
    print(type(dataToRead))
    print(dataToRead)

main()
