from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    name: str
    email: str

# Endpoint para agregar un usuario, le agrego validación para no repetir del mismo correo en ningun usuario. 
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):

    for existing_user in users:
        #validacion para no hacer duplicados del mismo correo. 
        if existing_user.id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El ID del usuario ya existe"
            )
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo del usuario ya existe"
            )
    #crea un nuevo usuario
    users.append(user)
    return {"message": "Usuario agregado con éxito", "user": user}

#feature-get-user
# Endpoint para obtener a todos los usuarios
@app.get("/users/", status_code=status.HTTP_200_OK)
async def get_users():
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay usuarios registrados"
        )
    
    
    return {"users": users}

