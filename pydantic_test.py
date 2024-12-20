from pydantic import BaseModel, ValidationError, Field, field_validator, model_validator
from pprint import pprint


class Tag(BaseModel):
    id: int
    name: str


class City(BaseModel):
    city_id: int
    name: str = Field(alias='cityFullName')
    population: int
    tags: list[Tag]

    @field_validator('name')
    def name_should_be_spb(cls, v: str) -> str:
        if 'spb' not in v.lower():
            raise ValueError("Work with SPB!")
        return v

    @model_validator(mode='after')
    def object_validator(self):
        return self


class UserWithoutPassword(BaseModel):
    name: str
    email: str


class User(UserWithoutPassword):
    password: str


input_json = """
{
    "city_id": 1,
    "cityFullName": "Spb",
    "population": "10000", 
    "tags": [{"id": 1, "name": "capital"},
             {"id": 0, "name": "garbige"}
    ]
}
"""


try:
    # city = City.parse_raw(input_json)
    city = City.model_validate_json(input_json)
except ValidationError as e:
    pprint(e.json())
else:
    print(city.name)
    print(city)

    # tag_1 = city.tags[0]
    # print(tag_1.model_dump_json())

    print(city.model_dump_json(by_alias=True, exclude={"city_id"}))
