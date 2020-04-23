import asyncio
import pprint
import config.credentials as config
from td.client import TDClient


# Create a new session
TDSession = TDClient(
    client_id=config.CLIENT_ID,
    redirect_uri=config.REDIRECT_URI,
    credentials_path=config.JSON_PATH
)

# Login to the session
TDSession.login()

# Create a streaming sesion
TDStreamingClient = TDSession.create_streaming_session()

# Level One Quote
TDStreamingClient.level_one_quotes(symbols=["SPY", "IVV", "SDS", "SH", "SPXL", "SPXS", "SPXU", "SSO", "UPRO", "VOO"],  fields=list(range(0,50)))

# Level One Option
TDStreamingClient.level_one_options(symbols=['AAPL_040920C115'], fields=list(range(0,42)))

# Data Pipeline function
async def data_pipeline():

    # Build the Pipeline.
    await TDStreamingClient.build_pipeline()

    # Keep going as long as we can recieve data.
    while True:
        
        # Start the Pipeline.
        data = await TDStreamingClient.start_pipeline()
        
        # Grab the Data.
        if 'data' in data:
            data_content = data['data'][0]['content']

            pprint.pprint(data_content)

            # Here I can grab data as it comes in and do something with it.
            if 'key' in data_content[0]:
                print('Here is my key: {}'.format(data_content[0]['key']))

            print('='*80)

# Run the pipeline.
asyncio.run(data_pipeline())
