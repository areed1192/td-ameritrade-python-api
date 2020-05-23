import asyncio
import pprint
from td.client import TDClient

# Create a new session
TDSession = TDClient(
    client_id='<YOUR_CLIENT_ID>',
    redirect_uri='<YOUR_REDIRECT_URI>',
    credentials_path='<YOUR_CREDENTIALS_PATH>'
)

# Login to the session
TDSession.login()

# Create a streaming sesion
TDStreamingClient = TDSession.create_streaming_session()

# Level One Quote
TDStreamingClient.level_one_quotes(
    symbols=["SPY", "IVV", "SDS", "SH"],
    fields=list(range(0,50))
)

# Level One Option
TDStreamingClient.level_one_futures(
    symbols=['/ES'],
    fields=list(range(0,42))
)

# Data Pipeline function
async def data_pipeline():
    """
    This is an example of how to build a data pipeline,
    using the library. A common scenario that would warrant
    using a pipeline is taking data that is sent back to the stream
    and processing it so it can be used in other programs or functions.

    Generally speaking, you will need to wrap the operations that process
    and handle the data inside an async function. The reason being is so
    that you can await the return of data.

    However, operations like creating the client, and subscribing to services
    can be performed outside the async function. In the example below, we demonstrate
    building the pipline, which is connecting to the websocket and logging in.

    We then start the pipeline, which is where the services are subscribed to and data
    begins streaming. The `start_pipeline()` will return the data as it comes in. From
    there, we process the data however we choose.

    Additionally, we can also see how to unsubscribe from a stream using logic and how
    to close the socket mid-stream.
    """

    data_response_count = 0
    heartbeat_response_count = 0

    # Build the Pipeline.
    await TDStreamingClient.build_pipeline()

    # Keep going as long as we can recieve data.
    while True:
        
        # Start the Pipeline.
        data = await TDStreamingClient.start_pipeline()
       
        # Grab the Data, if there was any. Remember not every message will have `data.`
        if 'data' in data:

            print('='*80)

            data_content = data['data'][0]['content']
            pprint.pprint(data_content, indent=4)

            # Here I can grab data as it comes in and do something with it.
            if 'key' in data_content[0]:
                print('Here is my key: {}'.format(data_content[0]['key']))

            print('-'*80)
            data_response_count += 1
        
        # If we get a heartbeat notice, let's increment our counter.
        elif 'notify' in data:
            print(data['notify'][0])
            heartbeat_response_count += 1

        # Once we have 1 data responses, we can unsubscribe from a service.
        if data_response_count == 1:
            unsub = await TDStreamingClient.unsubscribe(service='LEVELONE_FUTURES')
            data_response_count += 1
            print('='*80)
            print(unsub)
            print('-'*80)

        # Once we have 5 heartbeats, let's close the stream. Make sure to break the while loop.
        # or else you will encounter an exception.
        if heartbeat_response_count == 3:
           await TDStreamingClient.close_stream()
           break

# Run the pipeline.
asyncio.run(data_pipeline())
