# backend

Backend for animatrix website

# Dependencies

Python version used: 3.6.7

- [flask](http://flask.pocoo.org)
- flask-cors
- opencv-python
- ffmpeg
- pymongo

# Bash scripts
### react.sh
(`bash react.sh`)
Copies latest build from [frontend](https://github.com/seth-gil/frontend) repo into the `/root` directory.

### restart.sh
(`bash restart.sh`)
Restarts all background processes so that file updates become visible.