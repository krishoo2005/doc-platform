from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import os

from database import engine, Base, SessionLocal
from models import User, Document
from auth.jwt_handler import create_access_token, get_current_user

from schemas import (
    UserCreate,
    UserResponse,
    LoginRequest
)

from auth.hashing import (
    hash_password,
    verify_password
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "FastAPI is running .."}


@app.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_pw = hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_correct = verify_password(
        user.password,
        existing_user.password
    )

    if not password_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return {"logged_in_as": current_user}


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    MAX_SIZE = 10 * 1024 * 1024

    contents = file.file.read()

    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 10MB"
        )

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    user = db.query(User).filter(
        User.email == current_user
    ).first()

    new_doc = Document(
        filename=file.filename,
        file_path=file_path,
        user_id=user.id
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        "message": "File uploaded successfully",
        "filename": new_doc.filename,
        "uploaded_at": new_doc.uploaded_at
    }