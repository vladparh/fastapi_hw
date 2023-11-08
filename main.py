from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind='bulldog'),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return "Hello!"

@app.post('/post')
def simple_post(timestamp: Timestamp):
    post_db.append(timestamp)
    return post_db[-1]

@app.get('/dog')
def get_dogs(kind: str):
    dogs=[]
    for key, item in dogs_db.items():
        if item.kind == kind:
            dogs.append(item)
    if len(dogs) == 0:
        raise HTTPException(status_code=409, detail='The specified kind does not found')
    return dogs

@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    if dog.pk in dogs_db.keys():
        raise HTTPException(status_code=409,detail='The specified Pk already exists.')
    if dog.pk not in dogs_db.keys():
        dogs_db[dog.pk] = dog
    return dog

@app.get('/dog/{pk}')
def get_dog(pk: int):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=409, detail='The specified dog does not found')
    return dogs_db[pk]

@app.patch('/dog/{pk}')
def patch_dog(pk: int, dog: Dog):
    if pk not in dogs_db.keys():
        raise HTTPException(status_code=409, detail='The specified dog does not found')
    if pk in dogs_db.keys():
        dogs_db[pk] = dog
    return dog

