sudo rm -rf /etc/supervisor/conf.d/bot.conf &&\
sudo supervisorctl reread &&\
sudo supervisorctl update

cp bot.conf /etc/supervisor/conf.d/bot.conf &&\
supervisorctl reread &&\
supervisorctl update


tail -f bot stderr


cp bot.conf /etc/supervisor/conf.d/web.conf
sudo rm -rf /etc/supervisor/conf.d/web.conf

curl http://0.0.0.0:8443
ufw status
ufw enable
ufw allow ssh
ufw allow 8443
