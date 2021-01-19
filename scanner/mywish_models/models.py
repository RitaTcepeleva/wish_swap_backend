from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from wish_swap.settings_local import mywish_pg_engine

Base = automap_base()
engine = create_engine(mywish_pg_engine)
Base.prepare(engine, reflect=True)

#CORRECT PATH TO MODELS
Dex = Base.classes.tokens_dex
Token = Base.classes.tokens_token

session = Session(engine)