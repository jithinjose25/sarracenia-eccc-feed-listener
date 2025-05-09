Sarracenia ECCC Feed Listener

Receive instant notifications when new Canadian GRIB‑2 forecast files land on the Meteorological Service of Canada (MSC) data mart. This tiny script uses the open‑source Sarracenia toolkit to subscribe to AMQP messages from Environment and Climate Change Canada’s public broker.

✨ Features

What it does

Why it matters

Subscribes in real‑time to HPFX (hpfx.collab.science.gc.ca)

No more polling or cron jobs; get alerts the second data arrive.

Multiple model feeds out‑of‑the‑box

HRDPA 2.5 km, HRDPS continental 2.5 km, GEM‑Regional 10 km, GEM‑Global 15 km, GEPS, REPS.

Runs anywhere Python 3 runs

Windows, macOS, Linux; no Docker required.

Fully configurable

Change broker, routing keys, log level, heartbeat … with one dictionary.

📦 Requirements

Python ≥ 3.8

pip install sarracenia

The script uses anonymous TLS (AMQPS) access; no credentials beyond the default guest account are needed.

🚀 Quick start

# 1 – clone or copy this repo
$ git clone https://github.com/<your‑user>/sarracenia-eccc-feed-listener.git
$ cd sarracenia-eccc-feed-listener

# 2 – install dependencies (preferably in a venv)
$ pip install -r requirements.txt   # optional helper file

# 3 – run the listener
$ python sarracenia_eccc_feed_listener.py
Connected to subscriber and listening for messages!
Got a new message!
Message content:
 {
   "url": "https://hpfx.collab.science.gc.ca/.../HRDPA/20250509/...grib2",
   "size": 15432109,
   "md5": "...",
   ...
 }

Press Ctrl +C to stop the listener gracefully.

🔧 Configuration

Open sarracenia_eccc_feed_listener.py and tweak the options dictionary:

Key

Default

Description

broker

amqps://anonymous:anonymous@hpfx.collab.science.gc.ca

AMQP broker URL.

bindings

six patterns (see script)

Routing keys that decide which files trigger messages.

queueName

q_anonymous<hostname>_...

Unique queue so you don’t collide with other anonymous users.

logLevel

debug

info, warning, error also supported.

Need a different model? Add another tuple to bindings, e.g. 

('xpublic', ['v02','post'], ['*.WXO-DD.model_hrdps.arctic.*.grib2'])

🛠 How it works (under the hood)

Connect – Sarracenia’s Moth client opens an AMQPS session to HPFX.

Bind – A private queue is bound to the xpublic topic exchange using the routing keys above.

Listen – The script blocks on getNewMessage(); when the broker publishes a matching message, it pops off the queue.

Ack – After printing, the message is acknowledged so RabbitMQ can drop it.

No files are downloaded—only notifications. Attach your own downloader in the if message: block if you need the data.