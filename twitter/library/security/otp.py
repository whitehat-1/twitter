import random
import string
import redis


class OTPManager:
    ##manages user OTP
    redis = redis.Redis(host="redis", port=6379, db=1)

    @staticmethod
    def generate_token(num: int =9) -> str:
        #generate random token.that contains upper,lower cases and numbers
        return "".join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            
        )
        for _ in range(num) #start from 0 till 8
        )
    @classmethod
    def create_otp(cls, user_id:str, expires:int =900):
        #create an OTP
        otp = cls.generate_token()
        while cls.redis.exists(otp): #check the redis db(while the conditionis true continue to generate)
            otp= cls.generate_token()
        cls.redis.set(otp, user_id, ex=expires)
        return otp

    @classmethod
    def get_otp_user(cls, otp: str):
        #return the owner f the OTP
        if cls.redis.exists(otp):
            return cls.redis.get(otp).decode("utf-8")


otp_manager = OTPManager()
