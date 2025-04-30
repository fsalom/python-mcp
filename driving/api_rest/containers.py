from fastapi import FastAPI

from driving.api_rest.v1.bitbucket.adapter import BitbucketContainer


def add_containers(app: FastAPI):
    bitbucket_container = BitbucketContainer()
    app.bitbucket_container = bitbucket_container
