deploy:
	@echo "Deploying the bot..."
	sudo cp -r ./anketa_bot.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl start anketa_bot.service
	sudo systemctl enable anketa_bot.service
	@echo "Bot deployed successfully."

restart:
	@echo "Restarting the bot..."
	sudo systemctl restart anketa_bot.service

status:
	@echo "Checking the bot status..."
	sudo systemctl status anketa_bot.service
