from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import subprocess
import os
from fastapi.middleware.cors import CORSMiddleware
import base64
from synthapi import synthesize_tamil
import shutil

app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def ensure_executable(file_path):
    current_permissions = os.stat(file_path).st_mode
    executable_mode = current_permissions | 0o111  # This adds execute permission for user, group, and others
    os.chmod(file_path, executable_mode)

def runs(command: str, cwd: str = None):
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

@app.post("/run_model/")
async def run_model(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to a temporary location
        input_file_path = f"/home/sltlab/kaldi/egs/SISOCADEMO/{file.filename}"
        with open(input_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        activate_venv = runs("source activate_python.sh", cwd="/home/sltlab/espnet/tools")
        pyversion = runs('python3 --version')
        cmd_source = runs("source cmd.sh", cwd="/home/sltlab/kaldi/egs/SISOCADEMO/")
        path_try = runs("source path_try.sh", cwd="/home/sltlab/kaldi/egs/SISOCADEMO")
        print(activate_venv, cmd_source, path_try)
        
        # Ensure the main script is executable
        main_script_path = '/home/sltlab/kaldi/egs/SISOCADEMO/main_run.sh'
        ensure_executable(main_script_path)

        # Run the main script with the uploaded file name as an argument
        run_main = subprocess.run(["/bin/bash", main_script_path, file.filename], 
                                  cwd='/home/sltlab/kaldi/egs/SISOCADEMO/', 
                                  capture_output=True, text=True)


        with open('pronuncing_dictionary') as f:
             lines = f.readlines()

        d = {}
        for line in lines:
              tam, eng, lex = line.strip().split('\t')
              d[eng] = tam


        # Read output.txt and synthesize audio

        with open("output.txt", "r") as file:
            content = file.read()
        cnt = content.split(" ")
        speaker = cnt[0]
        speaker = speaker[0:3]
        text = cnt[1::]
        texts = ""
        for i in text:
            if i == '\n' or i == '\\n':
                break
            texts += i + " "

        synth = synthesize_tamil(texts)


        new_text=''

        for word in text:
            if word !='\n':
               print(word)
               new_text+=d[word]+' ' 

        output_file_path = "/home/sltlab/kaldi/egs/SISOCADEMO/test.wav"

        # Check if output file exists
        if not os.path.exists(output_file_path):
            raise HTTPException(status_code=404, detail="Output file not found.")

        # Read WAV file as binary and encode it to base64
        with open(output_file_path, "rb") as wav_file:
            wav_blob = base64.b64encode(wav_file.read()).decode("utf-8")


        # Return the output of the process and the WAV blob
        return JSONResponse(content={
            "run_main_stdout": run_main.stdout,
            "run_main_stderr": run_main.stderr,
            "py version": pyversion,
            "speaker": speaker,
            "content": new_text,
            "wav_blob": wav_blob,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
