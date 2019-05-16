git pull
docker build . -t 8binance
docker rm -f 8binance
docker run --name 8binance -d 8binance