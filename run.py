import sys
from server import app, cfg

app.run(host=cfg.get('web', 'host'), port=cfg.getint('web', 'port'), debug=True)
