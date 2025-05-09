
<body>
  <h1>Sarracenia ECCC Feed Listener</h1>

  <p>Receive <em>instant</em> notifications when new Canadian GRIB‑2 forecast files land on the Meteorological Service of Canada (MSC) data mart. This tiny script uses the open‑source <a href="https://github.com/MetPX/sarracenia">Sarracenia</a> toolkit to subscribe to AMQP messages from Environment and Climate Change Canada’s public broker.</p>

  <hr />

  <h2>✨ Features</h2>
  <table>
    <thead>
      <tr><th>What it does</th><th>Why it matters</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Subscribes in real‑time</strong> to HPFX (<code>hpfx.collab.science.gc.ca</code>)</td><td>No more polling or cron jobs; get alerts the second data arrive.</td></tr>
      <tr><td><strong>Multiple model feeds out‑of‑the‑box</strong></td><td>HRDPA 2.5 km, HRDPS continental 2.5 km, GEM‑Regional 10 km, GEM‑Global 15 km, GEPS, REPS.</td></tr>
      <tr><td><strong>Runs anywhere Python 3 runs</strong></td><td>Windows, macOS, Linux; no Docker required.</td></tr>
      <tr><td><strong>Fully configurable</strong></td><td>Change broker, routing keys, log level, heartbeat … with one dictionary.</td></tr>
    </tbody>
  </table>

  <hr />

  <h2>📦 Requirements</h2>
  <ul>
    <li>Python ≥ 3.8</li>
    <li><code>pip install sarracenia</code></li>
  </ul>
  <blockquote>
    <p>The script uses anonymous TLS (AMQPS) access; no credentials beyond the default guest account are needed.</p>
  </blockquote>

  <hr />

  <h2>🚀 Quick start</h2>
  <pre><code># 1 – clone or copy this repo
git clone https://github.com/&lt;your‑user&gt;/sarracenia-eccc-feed-listener.git
cd sarracenia-eccc-feed-listener

# 2 – install dependencies (preferably in a venv)
pip install -r requirements.txt   # optional helper file

# 3 – run the listener
python sarracenia_eccc_feed_listener.py
Connected to subscriber and listening for messages!
Got a new message!
Message content:
 {
   "url": "https://hpfx.collab.science.gc.ca/.../HRDPA/20250509/...grib2",
   "size": 15432109,
   "md5": "...",
   ...
 }</code></pre>
  <p>Press <strong>Ctrl +C</strong> to stop the listener gracefully.</p>

  <hr />

  <h2>🔧 Configuration</h2>
  <p>Open <code>sarracenia_eccc_feed_listener.py</code> and tweak the <code>options</code> dictionary:</p>
  <table>
    <thead>
      <tr><th>Key</th><th>Default</th><th>Description</th></tr>
    </thead>
    <tbody>
      <tr><td><code>broker</code></td><td><code>amqps://anonymous:anonymous@hpfx.collab.science.gc.ca</code></td><td>AMQP broker URL.</td></tr>
      <tr><td><code>bindings</code></td><td>six patterns (see script)</td><td>Routing keys that decide <em>which</em> files trigger messages.</td></tr>
      <tr><td><code>queueName</code></td><td><code>q_anonymous&lt;hostname&gt;_...</code></td><td>Unique queue so you don’t collide with other anonymous users.</td></tr>
      <tr><td><code>logLevel</code></td><td><code>debug</code></td><td><code>info</code>, <code>warning</code>, <code>error</code> also supported.</td></tr>
    </tbody>
  </table>
  <p>Need a different model? Add another tuple to <code>bindings</code>, e.g.</p>
  <pre><code>('xpublic', ['v02','post'], ['*.WXO-DD.model_hrdps.arctic.*.grib2'])</code></pre>

  <hr />

  <h2>🛠 How it works (under the hood)</h2>
  <ol>
    <li><strong>Connect</strong> – Sarracenia’s <code>Moth</code> client opens an AMQPS session to HPFX.</li>
    <li><strong>Bind</strong> – A private queue is bound to the <code>xpublic</code> topic exchange using the routing keys above.</li>
    <li><strong>Listen</strong> – The script blocks on <code>getNewMessage()</code>; when the broker publishes a matching message, it pops off the queue.</li>
    <li><strong>Ack</strong> – After printing, the message is acknowledged so RabbitMQ can drop it.</li>
  </ol>
  <p>No files are downloaded—only notifications. Attach your own downloader in the <code>if message:</code> block if you need the data.</p>

  <hr />

  <h2>🐞 Troubleshooting</h2>
  <table>
    <thead>
      <tr><th>Symptom</th><th>Possible cause &amp; fix</th></tr>
    </thead>
    <tbody>
      <tr><td><em>"SSL: CERTIFICATE_VERIFY_FAILED"</em></td><td>Set <code>options['tlsRigour'] = "lax"</code> (already the default) or install the SSCAC root CA bundle.</td></tr>
      <tr><td>No messages after several hours</td><td>Check that the model actually ran; try a less specific routing key to verify connectivity.</td></tr>
      <tr><td><code>AMQPConnectionError</code> on startup</td><td>Broker may be down or blocked by a firewall; test with <code>telnet hpfx.collab.science.gc.ca 5671</code>.</td></tr>
    </tbody>
  </table>


  <h2>🙌 Acknowledgements</h2>
  <ul>
    <li><strong>Environment and Climate Change Canada</strong> for the free public data feeds.</li>
    <li><strong>MetPX / Sarracenia</strong> project for the elegant pub‑sub toolkit.</li>
    <li>Inspired by MSC’s <a href="https://github.com/MetPX/sarracenia/tree/master/examples">Sarracenia examples</a>.</li>
  </ul>

  <hr />

</body>
</html>
