import aiocoap.resource as resource
import aiocoap
import asyncio
import requests
import json
import datetime

class CoAPResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.csv_filename = 'training_data.csv'
        self.last_hour = datetime.datetime.now().hour

    async def render_put(self, request):
        payload_str = request.payload.decode('utf-8')
        print('data received!')
        print(f"Received payload: {payload_str}")
        payload = json.loads(payload_str)
        payload = {
            "temperature": payload['Tp'],
            "humidity": payload['Hm'],
            "co2": payload['CO'],
            "pm1_0": payload['1p0'],
            "pm2_5": payload['2p5'],
            "pm4": payload['4p0'],
            "pm10": payload['10p0'],
            "eco2": payload['eCO'],
            "partical_size": payload['ps'],
            "tvoc": payload['tv'],
        }

        SERVER_URL = 'https://airquality.faizan.me/api/air-quality-readings'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(SERVER_URL, data=json.dumps(payload), headers=headers)

        return aiocoap.Message(code=aiocoap.CHANGED, payload="")


def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['storedata'], CoAPResource())
    print('Binding asyncio task on 5683 port.')
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('::', 5683)))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
