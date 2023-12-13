from typing import Optional, TypedDict


class Neo4j(TypedDict):
    url: str
    username: str
    password: str
    encrypted: bool


class Config(TypedDict):
    neo4j: Neo4j
    match_resource: Optional[str]


config: Config = {
    "neo4j": {
        "url": "bolt://localhost:7687",
        "username": "neo4j",
        "password": "neo4j",
        "encrypted": False,
    },
    "match_resource": None
}
