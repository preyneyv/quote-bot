# Quote Bot

Here's the code for a quote bot.

Just add :arrow_forward: as the reaction to a message you want to quote.

Then, the next message you send will have a link to the first one.

Easy peasy.

Quote Bot will automatically create webhooks for each channel as it needs them.
You don't need to worry about it.

[Click here](https://discordapp.com/oauth2/authorize?client_id=584448384308609034&permissions=536879104&scope=bot) to add the bot to your server!

## RUNNING LOCALLY

Copy `config.sample.json` to `config.json`.

Then, in `config.json`, insert your token in place of `"your token here"`.

If you want to use a different emoji than :arrow_forward:, just paste it in
`config.json` as well.

When you're ready to go, just run `main.py` as a Python 3 script.

## LICENSE

Copyright (c) 2019 Pranav Nutalapati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
