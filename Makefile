# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t twitbot -f Dockerfile .

run: ## Run the container
	docker run --rm -v $(shell pwd):$(shell pwd) -it twitbot:latest

run-jupyter: ## Run a Jupyter notebook at port 8989
	docker run --rm -v $(shell pwd):$(shell pwd) --env-file .env -it -p 8989:8989 twitbot:latest /bin/sh -c 'cd $(shell pwd); jupyter notebook --allow-root --no-browser --port=8989 --ip=0.0.0.0;'

tweet:  ## Post a tweet
	docker run --rm -v $(shell pwd):$(shell pwd) --env-file .env -it twitbot:latest  /bin/sh -c 'cd $(shell pwd); python3 twitbot.py post-tweet'

wait:  ## Start a daemon that waits and tweets when the trainer tweets
	docker run -d --rm -v $(shell pwd):$(shell pwd) --env-file .env -it twitbot:latest  /bin/sh -c 'cd $(shell pwd); python3 twitbot.py wait-and-tweet'


