import logging
from flask import Flask, request, jsonify
import asyncio
import bittensor as bt
from bittensor import Keypair

# Create a logger object
logger = logging.getLogger('BittensorApp')
logger.setLevel(logging.DEBUG)  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add formatter to ch
ch.setFormatter(formatter)

# Add ch to logger
logger.addHandler(ch)

app = Flask(__name__)


metagraph = bt.metagraph(29, network="finney")
metagraph.sync()
# Function to create a dendrite and hotkey pair
# Function to create a dendrite and hotkey pair
def create_dendrite():
    logger.debug("Creating dendrite and hotkey pair")
    hotkey = Keypair.create_from_mnemonic("fever unlock seven sphere robot royal feature post tennis ivory black when")
    return bt.Dendrite(wallet=hotkey), hotkey

# Function to handle asynchronous calls to multiple neurons
async def run_dendrite(dendrite, axons, synapse):
    logger.debug("Running dendrite call asynchronously")
    tasks = []
    for axon in axons:
        task = asyncio.create_task(dendrite(axon, synapse=synapse, timeout=300.0))
        tasks.append(task)
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    logger.debug(f"Received responses: {responses}")
    return responses

# Function to generate response based on a prompt
def generate(prompt, dendrite, axons):
    logger.info(f"Generating output for prompt: {prompt}")
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
        logger.info("Valid completions found")
        return completions
    logger.warning("No valid completions found or errors occurred")
    return "No valid completions found or errors occurred."

# Route to handle video generation
@app.route('/video', methods=['POST'])
async def video():
    logger.debug("Received video generation request")
    dendrite, _ = create_dendrite()
    prompt = request.json.get('prompt', '')
    axons = select_axons()
    result = generate(prompt, dendrite, axons)
    return jsonify(result)

# Function to select axons
def select_axons():
    logger.debug("Selecting axons")
    axons = metagraph.axons[:10]
    logger.debug(f"Selected axons: {axons}")
    return axons

if __name__ == '__main__':
    app.run(port=8060, host="0.0.0.0")

