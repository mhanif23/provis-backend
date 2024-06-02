import bcrypt
from datetime import datetime, timedelta

from schemas import *
from jose import jwt # Json web tokens

SALT = b'$2b$12$UFwvJrU2gFC/QSAIGT1lWu.'

# Token for auth
class Token(BaseModel):
    access_token: str
    token_type: str

def encrypt(passwd: str):
    bytePwd = passwd.encode('utf-8')
    pwd_hash = bcrypt.hashpw(bytePwd, SALT)
    return pwd_hash

    
def create_access_token(username):
    expiration_time = datetime.utcnow() + timedelta(hours=24)    # .now(datetime.UTC)
    access_token = jwt.encode({"username":username,"exp":expiration_time},"krakukra",algorithm="HS256")
    return access_token

def verify_token(token: str):
    try:
        payload = jwt.decode(token,"krakukra",algorithms=["HS256"])
        username = payload["username"]  
     
    # exception jika token invalid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Unauthorize token, expired signature, harap login")
    except jwt.JWSError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWS Error")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWT Claim Error")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWT Error")   
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorize token, unknown error"+str(e))
    
    return {"user_name": username}
