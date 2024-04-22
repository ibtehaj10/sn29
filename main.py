from flask import Flask, request, jsonify
from bittensor import Keypair
import bittensor as bt
import asyncio
from flask_executor import Executor

app = Flask(__name__)
executor = Executor(app)  # Helps manage thread pools for non-async functions

def create_dendrite():
    hotkey = Keypair.create_from_mnemonic("fever unlock seven sphere robot royal feature post tennis ivory black when")
    return bt.Dendrite(wallet=hotkey), hotkey

async def run_dendrite(dendrite, synapse):
    """ Run the dendrite call asynchronously and handle exceptions safely. """
    try:
        response = await dendrite(axons[:9], synapse=synapse, timeout=300.0)
        return response
    except Exception as e:
        print(f"Error during dendrite run: {e}")
        return None

def generate(prompt, dendrite):
    from fractal.fractal.protocol import PromptRequest, PromptRequestSamplingParams

    custom_sampling_params = PromptRequestSamplingParams(seed=4000)
    synapse = PromptRequest(
        query=prompt,
        sampling_params=custom_sampling_params,
        completion=None,
        required_hash_fields=["query", "sampling_params"],
        timeout=300,
        response_format="json",
        language="en"
    )
    
    response = asyncio.run(run_dendrite(dendrite, synapse))
    if response and response[0].completion is not None:
        return response[0].completion
    return "No completion found or error occurred."

@app.route('/video', methods=['POST'])
async def video():
    dendrite, _ = create_dendrite()
    prompt = request.json.get('prompt', '')
    result = generate(prompt, dendrite)
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8060, host="0.0.0.0")
