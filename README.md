## what does this code do?

The code performs three actions sequentially.

First, the program scrapes the content of each presidential address. Then the content of each address is fed to ChatGPT in order to discover the topics of the article. Lastly, the information is output in JSON format.

## ok, but what happens exactly?

The file ``index.py`` is the main driver of the program.
It takes the urls of each presidential address from ``urls.json`` and scrapes it for its content using two python packages called ``cloudscraper`` and ``BeautifulSoup``.
When extrating the information, the program ignores all figures and acknowledgements as they are supplementary, not essential.

Then, the data is fed to an LLM in order to find the main topics of each article.
LLMs have been trained on vast amounts of text, so it can pick up on nuances and implied themes that are missed by other topic modeling methods.
LLMs also integrate information from the entire article, so a stray section won't skew the topic list.
Additionally, the topics generated are human-friendly, not just a list of words.

In this case, I use OpenAI's ChatGPT 4o model to generate the topics for each article. The program takes the recently extracted content of each article, feeds it to ChatGPT and gets back the major themes of said article alongside a description of what that topic means.

Finally, the program outputs a JSON file with all of the information gathered, sectioned by the year of the address.

## how can i run the code?

In order to make the code run, you're going to need two things:

(1) An API key from OpenAI. You can get one by going to [this link](https://platform.openai.com/api-keys) and generating one. You may need to deposit some balance into your account first.

(2) A laptop with an internet connection and Python (ideally version 3.12.5) installed.

Once you've cloned this repository, you're navigate to the project's root directory and create a file called ``.env``.

Then, add your API key into the file like so:

```.env
OPENAI_API_KEY={your_api_key}
```

Then, simply run the code by putting these commands into the terminal at the root directory of the project.

```shell
pip install -r requirements.txt
python index.py
```