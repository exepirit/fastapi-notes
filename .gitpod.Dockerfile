FROM gitpod/workspace-full

USER gitpod

RUN python3 -m pip install -r requirements.txt
