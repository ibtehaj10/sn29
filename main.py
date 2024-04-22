from flask import Flask, request, jsonify
import asyncio
import bittensor as bt
from bittensor import Keypair

app = Flask(__name__)



metagraph = bt.metagraph(29, network="finney")
metagraph.sync()
# Function to create a dendrite and hotkey pair
def create_dendrite():
    hotkey = Keypair.create_from_mnemonic("fever unlock seven sphere robot royal feature post tennis ivory black when")
    return bt.Dendrite(wallet=hotkey), hotkey

# Function to handle asynchronous calls to multiple neurons
async def run_dendrite(dendrite, axons, synapse):
    """ Run the dendrite call asynchronously across multiple axons and handle exceptions safely. """
    tasks = []
    for axon in axons:
        task = asyncio.create_task(dendrite(axon, synapse=synapse, timeout=300.0))
        tasks.append(task)
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return responses

# Function to generate response based on a prompt
def generate(prompt, dendrite, axons):
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
    
    response = asyncio.run(run_dendrite(dendrite, axons, synapse))
    completions = [resp.completion for resp in response if resp and resp.completion is not None]
    if completions:
        return completions
    return "No valid completions found or errors occurred."

# Route to handle video generation
@app.route('/video', methods=['POST'])
async def video():
    dendrite, _ = create_dendrite()
    prompt = request.json.get('prompt', '')
    axons = select_axons()  # This function needs to be defined to choose the right axons
    result = generate(prompt, dendrite, axons)
    return jsonify(result)

# Function to select axons
def select_axons():
    # Assuming metagraph is globally available or refreshed inside this function
    # Choose 10 random or top axons based on some criteria
    axons = metagraph.axons[:10]  # Adjust this selection mechanism as needed
    return axons

if __name__ == '__main__':
    app.run(port=8060, host="0.0.0.0")
