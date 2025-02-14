# ai-cmdline-client
A command line client to hosted LLMs such as Anthropic/Google/OpenAI

## To install
- Clone this repo onto the computer where one wants to install this tool
- Change directory to the root dir of this repo
- If one wants to install into a virtual environment, they should first activate it
- Run `pip install .`
- If one hasn't installed within a virtual environment, they need to add the dir that contains the installed python packages executables to the PATH environment variable. For e.g., on Mac OS X, one might run: `export PATH="$PATH":/Users/username/Library/Python/3.9/bin`. One could add this command to their `.bashrc`.

## To run
- One must have followed all the instructions in the 'To install' section.
- Put a JSON file at `~/.har/keys.json`. One can copy from below and insert the API keys for the API providers that they have keys from. All providers currently supported by the tool are listed below. One needs to use the same mixed case for the provider names as below.
```json
{
    "Anthropic": "<anthropic-api-key>",
    "Google": "<google-api-key>",
    "OpenAI": "<openai-api-key>",
    "XAI": "<xai-api-key>"
}
```
- This tool is invoked via the executable `har`. Run `har` on the shell prompt. ([Demo video](https://www.dropbox.com/scl/fi/1wv5ivvpb5ngpp80ujk4f/2024-02-13-demo-video.m4v?rlkey=mscl33ormf6zmzu6f4kc07xn4&st=wb3r66ee&dl=0))
