# Base image
FROM python:latest

RUN pip3 install transformers==2.9.1 pytorch-lightning==0.7.6 aitextgen tweepy numpy jupyter click

# Enter the Shell
CMD /bin/bash
