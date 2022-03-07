apt-get update &&\
apt-get install supervisor -y &&\
mkdir -p /home/eco-fruit &&\
mv  ./* /home/eco-fruit &&\
mv ./.env /home/eco-fruit/.env &&\
cd /home/eco-fruit &&\
cp bot.conf /etc/supervisor/conf.d/bot.conf &&\
apt install python3-pip &&\
python3 -m pip install -r requirements.txt &&\
supervisorctl reread &&\
supervisorctl update


cp bot.conf /etc/supervisor/conf.d/bot.conf &&\
supervisorctl reread &&\
supervisorctl update