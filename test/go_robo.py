import json
from robotjes.sim import Engine, Map, Success
# from robotjes.remote import Handler


def go_robo(map_file, script_file, success_file):
    host = "localhost"
    port = 6000
    secret = b"secret"
    engine = Engine(Map.fromfile(map_file))
    with open(script_file, 'r') as f:
        scriptstr = "\n".join(line.strip() for line in f)
    with open(success_file, 'r') as f:
        successjson = json.load(f)
    success = Success.from_json(successjson, engine)
    handler = Handler(host, port, secret)

    # run (like bin/simulation_runner)
    engine.world.inc("scriptTotalCharacters", len(scriptstr))
    engine.world.inc("scriptCharacters", len(scriptstr))
    success.beforeRun()
    with open(script_file) as script:
        handler.run_client(script)
    handler.run(engine)
    success.afterRun()
    engine.world.inc("robotHasBeacon", len(engine.world.bot.beacons)>0)
    engine.world.inc("robotOrientation", engine.world.bot.dir)
    engine.world.inc("robotX", engine.world.bot.pos[0])
    engine.world.inc("robotY", engine.world.bot.pos[1])

    # done
    recording = engine.get_recording()
    return [engine, recording, success]
