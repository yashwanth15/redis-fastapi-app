#create environment
python3 -m venv venv

#activate environment
source venv/bin/activate

#install dependencies
pip install -r requirements.txt

#run the app
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
