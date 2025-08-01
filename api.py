from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
import subprocess
import os
from fastapi.middleware.cors import CORSMiddleware
import base64
from synthapi import synthesize_tamil  # Import the synthesizer
import shutil

# Dynamically determine the base directory of the app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update allowed origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to make files executable
def ensure_executable(file_path):
    current_permissions = os.stat(file_path).st_mode
    executable_mode = current_permissions | 0o111  # Add execute permissions
    os.chmod(file_path, executable_mode)

# Helper function to run shell commands
def runs(command: str, cwd: str = None):
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return {"message" : f'executed runs: {result.stdout}'}
    except subprocess.CalledProcessError as e:
        return {"error": f"Error: {e.stderr}"}

# Define the directory where files will be saved
UPLOAD_DIRECTORY = os.path.join(BASE_DIR, "uploads")

# Ensure that the directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Main API to handle file uploads, processing, and running shell scripts
@app.post("/run_model/")
async def run_model(file: UploadFile = File(...), severity: str = Form(...)):
    try:
        # Define the path where the uploaded file will be saved
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

        # Save the uploaded file to the specified directory
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Dynamically resolve script and config paths
        espnet_tools_dir = os.path.join(BASE_DIR, "opt", "espnet", "tools")
        kaldi_egs_dir = os.path.join(BASE_DIR)
        # If your kaldi/egs directory is not the app root, adjust accordingly

        # Activate virtual environment and run Kaldi commands
        activate_venv = runs("source activate_python.sh", cwd=espnet_tools_dir)
        pyversion = runs('python3 --version')
        cmd_source = runs("source cmd.sh", cwd=kaldi_egs_dir)
        path_try = runs("source path_try.sh", cwd=kaldi_egs_dir)

        # Ensure the main Kaldi script is executable
        if severity == 'moderate':
            main_script_path = os.path.join(kaldi_egs_dir, 'main_run.sh')
            ensure_executable(main_script_path)
        else: # In case of mild
            main_script_path = os.path.join(kaldi_egs_dir, 'main_run_mild.sh')
            ensure_executable(main_script_path)

        # Run the Kaldi script, passing the uploaded file as an argument
        run_main = subprocess.run(
            ["/bin/bash", main_script_path, file.filename],
            cwd=kaldi_egs_dir,
            capture_output=True, text=True
        )

        # Check if output.txt exists before proceeding
        output_txt_path = os.path.join(kaldi_egs_dir, "output.txt")
        if not os.path.exists(output_txt_path):
            raise HTTPException(status_code=404, detail="Output file not found.")
        
        # Read and process output.txt
        with open(output_txt_path, "r") as file:
            content = file.read()
        cnt = content.split(" ")
        speaker = cnt[0][:3]  # Extract the speaker part
        text = cnt[1:]
        texts = " ".join(text)

        # Call the Tamil synthesizer API
        synth = synthesize_tamil(texts)

        # Build the new translated text
        pron_dict_path = os.path.join(kaldi_egs_dir, 'pronuncing_dictionary')
        with open(pron_dict_path) as f:
            lines = f.readlines()

        d = {}
        for line in lines:
            tam, eng, lex = line.strip().split('\t')
            d[eng] = tam

        # Generate translated text
        new_text = ""
        for word in text:
            if word != '\n':
                new_text += d.get(word, word) + ' '

        # Check if the output WAV file exists
        output_file_path = os.path.join(kaldi_egs_dir, "test.wav")
        if not os.path.exists(output_file_path):
            raise HTTPException(status_code=404, detail="Output WAV file not found.")

        # Read and encode the WAV file to base64 for frontend
        with open(output_file_path, "rb") as wav_file:
            wav_blob = base64.b64encode(wav_file.read()).decode("utf-8")

        return JSONResponse(content={
            "run_main_stdout": run_main.stdout,
            "run_main_stderr": run_main.stderr,
            "py_version": pyversion,
            "speaker": speaker,
            "content": new_text,
            "wav_blob": wav_blob,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
