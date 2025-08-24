from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from fastapi.middleware.cors import CORSMiddleware
import model
import schemas
import database



model.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
origins = [
    "http://localhost:5173",   
    "http://192.168.235.218:5173",   
      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],          
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get('/')
def read_root():
    return {"message": "Welcome to the Agro API"}
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(model.User).filter(
        (model.User.username == user.username) | (model.User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = model.User( Lastname=user.Lastname , Othername=user.Othername, Phonenumber= user.Phonenumber, username=user.username, email=user.email, password=hashed_password, role =user.role )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "role": new_user.role.value}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.email== user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    token = jwt.encode({"sub": db_user.email}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "role": db_user.role.value }



