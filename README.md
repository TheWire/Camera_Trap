## Install
- `apt install python3-picamera2`
- `python3 -m venv --system-site-packages venv`
- `source ./venv/bin/activate`

## Pi node install
- `curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - &&\
sudo apt-get install -y nodejs`

## Build Frontend
- `cd frontend`
- `npm install`
- `cd ../`
- `./build-frontend.sh`
