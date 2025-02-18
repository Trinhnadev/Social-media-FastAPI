<!--  install python version -->

pip python 3.9



<!-- create virual enviroment -->
python3 -m venv venv  
source venv/bin/activate # active on macOS
venv\Scripts\activate  # active on Windows



<!-- install application -->

git clone https://github.com/yourusername/fastapi-social-media.git
cd fastapi-social-media

<!--  install fastapi and libary -->
pip install fastapi[all] pymongo motor uvicorn python-dotenv

<!-- import to create token and use Jwt -->
install "pip install fastapi[all] pymongo[srv] motor PyJWT passlib python-dotenv

<!-- create file .env -->

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


MONGO_URI=mongodb://trinhna:anhtrinh05102003@mongo:27017/



<!-- run the project -->
fastapi dev main.py



<!-- access to API to test API -->
http://localhost:8000/docs
