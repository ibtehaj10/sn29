import bittensor as bt
import asyncio
import torchvision.transforms as transforms
import time
from PIL import Image
# from bittensor_utils import send_request_to_bittensor
from fractal.fractal.protocol import PromptRequest, PromptRequestSamplingParams
from flask import Flask, request, jsonify
from bittensor import Keypair, metagraph, Keypair
from bittensor import bittensor, wallet
import pydantic

import torch
import numpy as np

app = Flask(__name__)



hotkey = Keypair.create_from_mnemonic("fever unlock seven sphere robot royal feature post tennis ivory black when")
dendrite = bt.dendrite(wallet=hotkey)
bt.trace()

metagraph = bt.metagraph(29, network="finney")
metagraph.sync()
neuron = metagraph.neurons[29]



axons = metagraph.axons
wallet = bittensor.wallet()



def generate(prompt):
    
    custom_sampling_params = PromptRequestSamplingParams(seed=4000)
    synapse = PromptRequest(
        query=prompt,
        sampling_params=custom_sampling_params,
        completion=None,  # Assuming this will be filled after processing
        required_hash_fields=["query", "sampling_params"],
        timeout=300,  # Timeout in seconds
        response_format="json",  # Expected response format
        language="en",  # Language of the query
        context=None,  # Additional context if necessary
        # metadata={"version": "1.0", "experiment": "geo-query"}  # Additional metadata
    )
    async def call_single(uid, synapse):
        neuron = metagraph.neurons[uid]

        # Extracting IP and port from the AxonInfo object
        ip_address = neuron.axon_info.ip  # Assuming the IP address is correctly stored here
        port = neuron.axon_info.port      # Assuming the port is correctly stored here

        # Now use ip_address and port in your dendrite.forward call
    def call_single():
        call_single_uid = dendrite(
            axons[:9],
            # synapse=synapse,
            timeout=300.0,

            # bt.axon(),
            synapse=synapse

            # hotkey='ni'
        )
        # print("UID -------  ",uid)
        return call_single_uid

    async def query_async(call_single_uid):
        corutines = [call_single_uid]
        return await asyncio.gather(*corutines)

    x = asyncio.run(query_async(call_single()))
    li = []
    for i,j in enumerate(x[0]):
        if j.completion != None:
            print(i)
            li.append(i)

    data = x[0][li[0]].completion
    return data


@app.route('/video', methods=['POST'])
def video():
    prompt = request.json['prompt']
    v = generate(prompt)
    return v


if __name__ == '__main__':
    app.run(port=8060,host="0.0.0.0")
