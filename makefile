deploy:
	@echo "Deploying the bot..."
	sudo cp -r ./weather_andijan_bot.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl start weather_andijan_bot.service
	sudo systemctl enable weather_andijan_bot.service
	@echo "Bot deployed successfully."

restart:
	@echo "Restarting the bot..."
	sudo systemctl restart weather_andijan_bot.service

status:
	@echo "Checking the bot status..."
	sudo systemctl status weather_andijan_bot.service
