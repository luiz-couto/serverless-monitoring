import datetime
import json
import redis
import os
import importlib
import time

user_module = importlib.util.find_spec('usermodule')

if not user_module:
    print("usermodule.py not found")
    exit(1)

import usermodule

REDIS_HOST = os.getenv('REDIS_HOST', "localhost")
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_INPUT_KEY = os.getenv('REDIS_INPUT_KEY', None)
REDIS_OUTPUT_KEY = os.getenv('REDIS_OUTPUT_KEY', None)

SLEEP_TIME = 5

class Context(object):
    def __init__(self, host, port, input_key, output_key):
        self.host = host
        self.port = port
        self.input_key = input_key
        self.output_key = output_key
        self.last_execution = None
        self.env = {}

        tmp = os.path.getmtime("/app/usermodule.py")
        self.function_getmtime = datetime.datetime.fromtimestamp(tmp).strftime('%Y-%m-%d %H:%M:%S')
        
    def set_env(self, env):
        self.env = env

    def set_last_execution(self):
        self.last_execution = datetime.datetime.now()



def main():
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, charset="utf-8", decode_responses=True)

    if not REDIS_OUTPUT_KEY:
        print("Cannot find REDIS OUTPUT KEY")
        exit(1)

    context = Context(host=REDIS_HOST, port=REDIS_PORT, input_key=REDIS_INPUT_KEY, output_key=REDIS_OUTPUT_KEY)

    while True:
        input = None
        output = None
        
        try:
            input = redis_client.get(REDIS_INPUT_KEY)
        
        except:
            print("Cannot get input from Redis")

    
        if input:
            try:
                input = json.loads(input)
                output = usermodule.handler(input, context)
                if REDIS_OUTPUT_KEY and output:
                    redis_client.set(REDIS_OUTPUT_KEY, json.dumps(output))

                context.set_last_execution()

            except:
                print("Cannot send the output of handler to Redis")
            
        
        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()