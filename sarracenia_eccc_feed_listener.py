import sarracenia.credentials
import sarracenia.moth
import sarracenia.moth.amqp
import socket
import time

def main():

    options = sarracenia.moth.default_options.copy()
    options.update(sarracenia.moth.amqp.default_options)

    # Configurations
    options['broker'] = sarracenia.credentials.Credential("amqps://anonymous:anonymous@hpfx.collab.science.gc.ca")
    options['topicPrefix'] = ['v02','post']
    options['bindings'] = [('xpublic', ['v02', 'post'], ['*.WXO-DD.model_hrdpa.2.5km.#.grib2']),
        ('xpublic', ['v02', 'post'], ['*.WXO-DD.model_hrdps.continental.2.5km.#.grib2']),
        ('xpublic', ['v02', 'post'], ['*.WXO-DD.model_gem_regional.10km.grib2.#.grib2']),
        ('xpublic', ['v02', 'post'], ['*.WXO-DD.model_gem_global.15km.grib2.lat_lon.#.grib2']),
        ('xpublic', ['v02', 'post'], ['*.WXO-DD.ensemble.geps.grib2.raw.#.grib2']),
        ('xpublic', ['v02', 'post'], ['*.WXO-DD.ensemble.reps.10km.grib2.#.grib2'])]

    
    options['queueName'] = "q_anonymous" + socket.getfqdn() + "_453456354_kkk"
    options['heartbeat'] = 30
    options['tlsRigour'] = "lax"
    options['logLevel'] = "debug"

    subscriber = sarracenia.moth.Moth.subFactory(options)
    print("Connected to subscriber and listening for messages!")

    try:
        while True:
            message = subscriber.getNewMessage()
            if message:
                print("Got a new message!")
                print(f"Message content: \n {message}")
                subscriber.ack(message)
            else: 
                time.sleep(2)
    except KeyboardInterrupt:
        print("The user has interrupted the program. Exiting now...")
    finally:
        subscriber.close()
        print("Subscriber closed!")

if __name__ == "__main__":
            main()